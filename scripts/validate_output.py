#!/usr/bin/env python3
"""Validate CV and CL YAML data against style-specific rules.

Checks:
  - JSON Schema validation (via validate_schema.py)
  - CV summary word count (min/max)
  - CV bullet word count per bullet
  - CV bullet count per role (recent vs old)
  - CL total word count (min/max)
  - CL paragraph count (min/max)
  - Header consistency: name match between CV and CL
  - JD keyword coverage (warnings only)

Usage:
    python3 scripts/validate_output.py --type both \
        --data-dir job-applications/output/folder \
        --cv-config .claude/skills/cv-style-europe/cv-format.yaml \
        --cl-config .claude/skills/cl-style-europe/cl-format.yaml \
        [--cv-schema .claude/skills/cv-style-europe/cv-data-schema.yaml] \
        [--cl-schema .claude/skills/cl-style-europe/cl-data-schema.yaml] \
        [--jd-text "job description text for keyword matching"]

Output: JSON to stdout with {valid, errors[], warnings[]}
"""

import argparse
import json
import sys
from pathlib import Path

import yaml

from validate_schema import validate


def _word_count(text: str) -> int:
    """Count words in a text string."""
    return len(text.split())


def _load_yaml(path: Path) -> dict:
    """Load a YAML file, return empty dict if missing."""
    if not path.exists():
        return {}
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _get_validation_config(config: dict) -> dict:
    """Extract validation block from format config with defaults."""
    return config.get("validation", {})


def _validate_cv(cv_data: dict, cv_config: dict, cv_schema_path: str = None) -> tuple:
    """Validate CV data. Returns (errors, warnings)."""
    errors = []
    warnings = []
    val = _get_validation_config(cv_config)

    # Schema validation
    if cv_schema_path and Path(cv_schema_path).exists():
        schema_errors = validate(cv_data, cv_schema_path)
        errors.extend(f"[schema] {e}" for e in schema_errors)

    # Summary word count
    summary = cv_data.get("summary", "")
    if summary:
        wc = _word_count(summary)
        min_w = val.get("summary_min_words", 40)
        max_w = val.get("summary_max_words", 100)
        if wc < min_w:
            errors.append(f"[cv] Summary too short: {wc} words (min {min_w})")
        if wc > max_w:
            errors.append(f"[cv] Summary too long: {wc} words (max {max_w})")

    # Experience bullets
    max_bullet_words = val.get("max_bullet_words", 18)
    max_bullets_recent = val.get("max_bullets_recent", 6)
    max_bullets_old = val.get("max_bullets_old", 3)

    experience = cv_data.get("experience", [])
    for i, role in enumerate(experience):
        company = role.get("company", "?")
        title = role.get("title", "?")
        bullets = role.get("bullets", [])
        is_recent = (i == 0)

        max_b = max_bullets_recent if is_recent else max_bullets_old
        if len(bullets) > max_b:
            label = "most recent" if is_recent else "older"
            errors.append(
                f"[cv] {title} @ {company}: {len(bullets)} bullets "
                f"(max {max_b} for {label} role)"
            )

        for j, bullet in enumerate(bullets):
            bwc = _word_count(bullet)
            if bwc > max_bullet_words:
                warnings.append(
                    f"[cv] {title} @ {company}, bullet {j+1}: "
                    f"{bwc} words (max {max_bullet_words})"
                )

    return errors, warnings


def _validate_cl(cl_data: dict, cl_config: dict, cl_schema_path: str = None) -> tuple:
    """Validate CL data. Returns (errors, warnings)."""
    errors = []
    warnings = []
    val = _get_validation_config(cl_config)

    # Schema validation
    if cl_schema_path and Path(cl_schema_path).exists():
        schema_errors = validate(cl_data, cl_schema_path)
        errors.extend(f"[schema] {e}" for e in schema_errors)

    # Paragraph count
    paragraphs = cl_data.get("paragraphs", [])
    num_p = len(paragraphs)
    min_p = val.get("min_paragraphs", 2)
    max_p = val.get("max_paragraphs", 6)
    if num_p < min_p:
        errors.append(f"[cl] Too few paragraphs: {num_p} (min {min_p})")
    if num_p > max_p:
        errors.append(f"[cl] Too many paragraphs: {num_p} (max {max_p})")

    # Total word count
    total_words = sum(_word_count(p) for p in paragraphs)
    min_w = val.get("min_total_words", 250)
    max_w = val.get("max_total_words", 400)
    if total_words < min_w:
        errors.append(f"[cl] Too few words: {total_words} (min {min_w})")
    if total_words > max_w:
        errors.append(f"[cl] Too many words: {total_words} (max {max_w})")

    return errors, warnings


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
        if term in jd_lower and term not in prose
    )

    if not_surfaced:
        return [
            "[keywords] Skills you list that the JD asks for but aren't "
            f"surfaced in your summary/bullets: {', '.join(not_surfaced)}"
        ]
    return []


def validate_output(
    doc_type: str,
    data_dir: str,
    cv_config_path: str = "",
    cl_config_path: str = "",
    cv_schema_path: str = "",
    cl_schema_path: str = "",
    jd_text: str = "",
) -> dict:
    """Validate CV and/or CL data files.

    Args:
        doc_type: "cv", "cl", or "both"
        data_dir: Path to the output folder containing cv-data.yaml / cl-data.yaml
        cv_config_path: Path to cv-format.yaml
        cl_config_path: Path to cl-format.yaml
        cv_schema_path: Path to cv-data-schema.yaml (optional)
        cl_schema_path: Path to cl-data-schema.yaml (optional)
        jd_text: Job description text for keyword coverage (optional)

    Returns:
        Dictionary with valid (bool), errors (list), warnings (list)
    """
    data_path = Path(data_dir)
    all_errors = []
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
            cv_config = _load_yaml(Path(cv_config_path)) if cv_config_path else {}
            schema = cv_schema_path or None
            errs, warns = _validate_cv(cv_data, cv_config, schema)
            all_errors.extend(errs)
            all_warnings.extend(warns)

    if do_cl:
        cl_file = data_path / "cl-data.yaml"
        if not cl_file.exists():
            all_errors.append(f"[cl] File not found: {cl_file}")
        else:
            cl_data = _load_yaml(cl_file)
            cl_config = _load_yaml(Path(cl_config_path)) if cl_config_path else {}
            schema = cl_schema_path or None
            errs, warns = _validate_cl(cl_data, cl_config, schema)
            all_errors.extend(errs)
            all_warnings.extend(warns)

    # Cross-document checks
    if do_cv and do_cl and cv_data and cl_data:
        all_errors.extend(_check_header_consistency(cv_data, cl_data))

    # JD keyword coverage
    if do_cv and cv_data and jd_text:
        all_warnings.extend(_check_jd_keywords(cv_data, jd_text))

    return {
        "valid": len(all_errors) == 0,
        "errors": all_errors,
        "warnings": all_warnings,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate CV/CL YAML data against style-specific rules"
    )
    parser.add_argument(
        "--type", required=True, choices=["cv", "cl", "both"],
        help="What to validate: cv, cl, or both"
    )
    parser.add_argument(
        "--data-dir", required=True,
        help="Path to output folder containing data YAML files"
    )
    parser.add_argument(
        "--cv-config", default="",
        help="Path to cv-format.yaml"
    )
    parser.add_argument(
        "--cl-config", default="",
        help="Path to cl-format.yaml"
    )
    parser.add_argument(
        "--cv-schema", default="",
        help="Path to cv-data-schema.yaml"
    )
    parser.add_argument(
        "--cl-schema", default="",
        help="Path to cl-data-schema.yaml"
    )
    parser.add_argument(
        "--jd-text", default="",
        help="Job description text for keyword coverage check"
    )
    args = parser.parse_args()

    result = validate_output(
        doc_type=args.type,
        data_dir=args.data_dir,
        cv_config_path=args.cv_config,
        cl_config_path=args.cl_config,
        cv_schema_path=args.cv_schema,
        cl_schema_path=args.cl_schema,
        jd_text=args.jd_text,
    )

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
