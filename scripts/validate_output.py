#!/usr/bin/env python3
"""Validate an application folder's CV and CL data against the Netherlands rules.

errors (structure — the documents cannot be rendered until fixed):
  - JSON Schema validation (via validate_schema.py)
  - Header consistency: name match between CV and CL
  - CV skill category listed twice
limits (CV_LIMITS / CL_LIMITS below):
  - CV summary word count (min/max)
  - CV bullet word count per bullet
  - CV bullet count per role (most recent / previous / older)
  - CL total word count (min/max)
  - CL paragraph count (min/max)
warnings:
  - JD keyword coverage (JD read from the folder's input.md)

Usage:
    python scripts/run.py scripts/validate_output.py <folder> [--type cv|cl|both]

Output: JSON to stdout with {valid, errors[], limits[], warnings[]}; exit 1 if errors.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

import contracts
from parse_input import parse_input
from validate_schema import validate


def _word_count(text: str) -> int:
    """Count words in a text string."""
    return len(text.split())


def _mentions(term: str, text: str) -> bool:
    """True if *term* appears in *text* as a standalone token rather than inside
    a larger alphanumeric word — so "sql" does NOT match inside "mysql", and
    "go" does NOT match inside "category". Both args should already be lowercased.
    Handles terms with regex-special characters (c++, c#, node.js, ci/cd)."""
    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None


def _load_yaml(path: Path) -> dict:
    """Load a YAML file, return empty dict if missing."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


# Netherlands content limits. They keep the CV to two A4 pages and the letter
# to one; render.py checks the real page counts on the PDF.
CV_LIMITS = {
    "summary_min_words": 40,
    "summary_max_words": 80,
    "max_bullet_words": 18,
    "max_bullets_recent": 5,     # most recent role
    "max_bullets_previous": 4,   # second role
    "max_bullets_old": 3,        # every older role
}
CL_LIMITS = {
    "min_paragraphs": 4,
    "max_paragraphs": 5,
    "min_total_words": 200,
    "max_total_words": 350,
}


def _validate_cv(cv_data: dict, cv_schema_path: str) -> tuple:
    """Validate CV data. Returns (errors, limits)."""
    errors = []
    limits = []
    val = CV_LIMITS

    schema_errors = validate(cv_data, cv_schema_path)
    errors.extend(f"[schema] {e}" for e in schema_errors)

    categories = [g.get("category") for g in cv_data.get("skills", []) if isinstance(g, dict)]
    for dup in sorted({c for c in categories if categories.count(c) > 1}):
        errors.append(f"[cv] Skill category listed twice: {dup} (merge the items into one entry)")

    # Summary word count
    summary = cv_data.get("summary", "")
    if summary:
        wc = _word_count(summary)
        min_w = val.get("summary_min_words", 40)
        max_w = val.get("summary_max_words", 100)
        if wc < min_w:
            limits.append(f"[cv] Summary too short: {wc} words (min {min_w})")
        if wc > max_w:
            limits.append(f"[cv] Summary too long: {wc} words (max {max_w})")

    # Experience bullets — the limit depends on the role's position:
    # most recent, previous, then every older role.
    max_bullet_words = val.get("max_bullet_words", 18)
    by_position = [
        ("most recent", val.get("max_bullets_recent", 5)),
        ("previous", val.get("max_bullets_previous", 4)),
    ]
    older = ("older", val.get("max_bullets_old", 3))

    experience = cv_data.get("experience", [])
    for i, role in enumerate(experience):
        company = role.get("company", "?")
        title = role.get("title", "?")
        bullets = role.get("bullets", [])

        label, max_b = by_position[i] if i < len(by_position) else older
        if len(bullets) > max_b:
            limits.append(
                f"[cv] {title} @ {company}: {len(bullets)} bullets "
                f"(max {max_b} for {label} role)"
            )

        for j, bullet in enumerate(bullets):
            bwc = _word_count(bullet)
            if bwc > max_bullet_words:
                limits.append(
                    f"[cv] {title} @ {company}, bullet {j+1}: "
                    f"{bwc} words (max {max_bullet_words})"
                )

    return errors, limits


def _validate_cl(cl_data: dict, cl_schema_path: str) -> tuple:
    """Validate CL data. Returns (errors, limits)."""
    errors = []
    limits = []
    val = CL_LIMITS

    schema_errors = validate(cl_data, cl_schema_path)
    errors.extend(f"[schema] {e}" for e in schema_errors)

    # Paragraph count
    paragraphs = cl_data.get("paragraphs", [])
    num_p = len(paragraphs)
    min_p = val.get("min_paragraphs", 2)
    max_p = val.get("max_paragraphs", 6)
    if num_p < min_p:
        limits.append(f"[cl] Too few paragraphs: {num_p} (min {min_p})")
    if num_p > max_p:
        limits.append(f"[cl] Too many paragraphs: {num_p} (max {max_p})")

    # Total word count
    total_words = sum(_word_count(p) for p in paragraphs)
    min_w = val.get("min_total_words", 250)
    max_w = val.get("max_total_words", 400)
    if total_words < min_w:
        limits.append(f"[cl] Too few words: {total_words} (min {min_w})")
    if total_words > max_w:
        limits.append(f"[cl] Too many words: {total_words} (max {max_w})")

    return errors, limits


def _check_header_consistency(cv_data: dict, cl_data: dict) -> list:
    """Check that CV and CL headers have matching name."""
    errors = []
    cv_name = cv_data.get("header", {}).get("name", "")
    cl_name = cl_data.get("header", {}).get("name", "")
    if cv_name and cl_name and cv_name != cl_name:
        errors.append(
            f"[consistency] Name mismatch: CV '{cv_name}' vs CL '{cl_name}'"
        )
    return errors


def _check_jd_keywords(cv_data: dict, jd_text: str) -> list:
    """Warn about candidate skills the JD asks for that aren't surfaced in the
    CV prose (summary + experience bullets). Warnings only.

    The vocabulary is derived from the candidate's OWN documented skills
    (cv-data, sourced from candidate.md) rather than a hardcoded keyword list,
    so this check is profession-agnostic — it works the same for a data
    engineer, a nurse, or a lawyer.
    """
    if not jd_text:
        return []

    jd_lower = jd_text.lower()

    # Vocabulary = the candidate's documented skill terms.
    skill_terms = set()
    for skill_cat in cv_data.get("skills", []):
        for item in skill_cat.get("items", []):
            term = str(item).strip().lower()
            if len(term) >= 2:
                skill_terms.add(term)

    if not skill_terms:
        return []

    # CV prose a recruiter reads first: summary + experience bullets
    # (the skills list itself is excluded on purpose — we want these surfaced
    # in the narrative, not just enumerated).
    prose_parts = [cv_data.get("summary", "")]
    for role in cv_data.get("experience", []):
        prose_parts.extend(role.get("bullets", []))
    prose = " ".join(prose_parts).lower()

    not_surfaced = sorted(
        term for term in skill_terms
        if _mentions(term, jd_lower) and not _mentions(term, prose)
    )

    if not_surfaced:
        return [
            "[keywords] Skills you list that the JD asks for but aren't "
            f"surfaced in your summary/bullets: {', '.join(not_surfaced)}"
        ]
    return []


def validate_output(doc_type: str, data_dir: str) -> dict:
    """Validate CV and/or CL data files in an application folder.

    Args:
        doc_type: "cv", "cl", or "both"
        data_dir: Path to the application folder (cv-data.yaml, cl-data.yaml, input.md)

    Returns:
        Dictionary with valid (bool), errors, limits and warnings (lists)
    """
    data_path = Path(data_dir)
    all_errors = []
    all_limits = []
    all_warnings = []

    do_cv = doc_type in ("cv", "both")
    do_cl = doc_type in ("cl", "both")

    cv_data = {}
    cl_data = {}

    if do_cv:
        cv_file = data_path / "cv-data.yaml"
        if not cv_file.exists():
            all_errors.append(f"[cv] File not found: {cv_file}")
        else:
            cv_data = _load_yaml(cv_file)
            errs, lims = _validate_cv(cv_data, str(contracts.CV_SCHEMA))
            all_errors.extend(errs)
            all_limits.extend(lims)

    if do_cl:
        cl_file = data_path / "cl-data.yaml"
        if not cl_file.exists():
            all_errors.append(f"[cl] File not found: {cl_file}")
        else:
            cl_data = _load_yaml(cl_file)
            errs, lims = _validate_cl(cl_data, str(contracts.CL_SCHEMA))
            all_errors.extend(errs)
            all_limits.extend(lims)

    # Cross-document check: when only one document was asked for, the other is
    # read from disk, so revising one cannot drift from the other.
    if not cl_data:
        cl_data = _load_yaml(data_path / "cl-data.yaml")
    if not cv_data:
        cv_data = _load_yaml(data_path / "cv-data.yaml")
    if cv_data and cl_data:
        all_errors.extend(_check_header_consistency(cv_data, cl_data))

    # JD keyword coverage
    input_md = data_path / "input.md"
    if do_cv and cv_data and input_md.exists():
        jd_text = parse_input(str(input_md))["job_description"]
        all_warnings.extend(_check_jd_keywords(cv_data, jd_text))

    return {
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "limits": all_limits,
        "warnings": all_warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate an application folder's CV/CL data against the Netherlands rules"
    )
    parser.add_argument("folder", help="Application folder containing the data YAML files")
    parser.add_argument(
        "--type", default="both", choices=["cv", "cl", "both"],
        help="What to validate: cv, cl, or both (default)"
    )
    args = parser.parse_args()

    result = validate_output(doc_type=args.type, data_dir=args.folder)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
