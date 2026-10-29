#!/usr/bin/env python3
"""Validate an application folder's CV and CL data against the Netherlands rules.

errors (structure — the documents cannot be rendered until fixed):
  - JSON Schema validation (via validate_schema.py)
  - Header consistency: name match between CV and CL
  - CV skill category listed twice
  - jd-keywords.yaml and the three mapping files: schema
  - jd-to-profile.yaml: exactly one entry per jd-keywords.yaml term
  - every evidence quote found word for word in candidate.md (research
    quotes in research.md)
  - a CV skill the candidate lacks (match: no) or knows too weakly to list
    (strength tooling / certified / learning / planned)
  - fit-verdict.yaml: schema, a verdict above fit_check.py's ceiling, or
    blockers that differ from fit_check.py's
limits (CV_LIMITS / CL_LIMITS below):
  - CV summary word count (min/max)
  - CV bullet word count per bullet
  - CV bullet count per role (most recent / previous / older)
  - CL total word count (min/max)
  - CL paragraph count (min/max)
warnings:
  - JD keyword coverage: with jd-keywords.yaml + jd-to-profile.yaml, every
    must-have tool/skill the candidate has must reach the skills section and
    the summary/bullets; without them, falls back to the JD text in input.md

Usage:
    python scripts/run.py scripts/validate_output.py <folder> [--type TYPE]

    TYPE: cv | cl | both (default) | keywords | jd-to-profile | profile-to-jd |
          company-to-profile | mappings (all three mapping files) | fit

Output: JSON to stdout with {valid, errors[], limits[], warnings[]}; exit 1 if errors.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

import contracts
import fit_check
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


# Keyword types the coverage check matches literally. Responsibilities, domains
# and soft skills are phrased freely in bullets, so a literal check would be noise.
_LITERAL_TYPES = ("tool", "skill")

# Evidence strengths strong enough for the CV skills list (profile-mapping skill).
_SKILL_LIST_STRENGTHS = ("shipped", "built")


def _keyword_names(kw: dict) -> list:
    """The words the CV should carry for a keyword, lowercased: the candidate's
    own term for an analogue; otherwise the posting's term, its aliases and
    the candidate's wording."""
    if kw.get("match") == "analogue":
        names = [kw.get("use_as", "")]
    else:
        names = [kw.get("term", ""), kw.get("use_as", ""), *kw.get("aliases", [])]
    return [n.strip().lower() for n in names if n and n.strip()]


def _merge_keywords(kw_data: dict, map_data: dict) -> list:
    """Join jd-keywords.yaml (what the posting asks) with jd-to-profile.yaml
    (what the candidate has) on the keyword term."""
    by_term = {m.get("keyword"): m for m in map_data.get("mappings", [])}
    merged = []
    for kw in kw_data.get("keywords", []):
        m = by_term.get(kw.get("term"), {})
        merged.append({**kw, **{k: v for k, v in m.items() if k != "keyword"}})
    return merged


def _check_keyword_coverage(cv_data: dict, keywords: list) -> tuple:
    """Check the CV against the merged keyword list. Returns (errors, warnings).

    errors:   a gap (match: no), or a keyword whose evidence is too weak for
              the skills list (tooling / certified / learning / planned),
              listed in the skills section.
    warnings: a must-have tool/skill the candidate has (yes or analogue) that is
              missing from the summary/bullets/projects, or from the summary
              when placed there; a must-have *tool* placed in skills that is
              missing from the skills section. Techniques and practices are not
              required in the skills list — it stays a crisp list of tools.
    """
    errors, warnings = [], []

    skill_text = " | ".join(
        str(item) for g in cv_data.get("skills", []) for item in g.get("items", [])
    ).lower()
    summary = str(cv_data.get("summary", "")).lower()
    prose_parts = [summary]
    for role in cv_data.get("experience", []):
        prose_parts.extend(role.get("bullets", []))
    for project in cv_data.get("projects", []):
        prose_parts.append(project.get("description", ""))
        prose_parts.extend(project.get("bullets", []))
    # A certification is proof too: a must-have known from a certificate is
    # shown in the certifications section, not claimed in a bullet.
    for cert in cv_data.get("certifications", []):
        prose_parts.append(cert.get("name", ""))
    prose = " ".join(str(p) for p in prose_parts).lower()

    def found(names, text):
        return any(_mentions(n, text) for n in names)

    missing_skills, missing_prose, missing_summary = [], [], []
    for kw in keywords:
        if kw.get("type") not in _LITERAL_TYPES:
            continue
        match = kw.get("match")
        if match == "no":
            gap = kw.get("term", "").strip().lower()
            if gap and _mentions(gap, skill_text):
                errors.append(
                    f"[keywords] '{kw['term']}' is a gap in jd-to-profile.yaml (match: no) "
                    "but is listed as a skill — remove it or list the candidate's analogue"
                )
            continue
        if match not in ("yes", "analogue"):
            continue
        names = _keyword_names(kw)
        strength = kw.get("strength")
        if strength and strength not in _SKILL_LIST_STRENGTHS and found(names, skill_text):
            errors.append(
                f"[keywords] '{names[0]}' is listed as a skill but its evidence is "
                f"'{strength}' in jd-to-profile.yaml — only shipped or built work goes in "
                "the skills list; show it in a bullet worded as the mapping says"
            )
        if kw.get("priority") != "must":
            continue
        label = names[0] if names else kw.get("term", "?")
        place = kw.get("place") or []
        if kw.get("type") == "tool" and "skills" in place and not found(names, skill_text):
            missing_skills.append(label)
        if not found(names, prose):
            missing_prose.append(label)
        if "summary" in place and not found(names, summary):
            missing_summary.append(label)

    if missing_skills:
        warnings.append(
            "[keywords] Must-have keywords the candidate has, missing from the "
            f"skills section: {', '.join(missing_skills)}"
        )
    if missing_prose:
        warnings.append(
            "[keywords] Must-have keywords the candidate has, not shown in the "
            f"summary, bullets, projects or certifications: {', '.join(missing_prose)}"
        )
    if missing_summary:
        warnings.append(
            "[keywords] Keywords jd-to-profile.yaml places in the summary but the "
            f"summary lacks: {', '.join(missing_summary)}"
        )
    return errors, warnings


# ── Evidence quotes ──────────────────────────────────────────────────────────

_QUOTE_CHARS = str.maketrans({
    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
    "\u2013": "-", "\u2014": "-", "\u2212": "-", "\u00a0": " ",
})


def _normalise(text: str) -> str:
    """Lowercase, straighten quotes and dashes, drop markdown emphasis and
    collapse whitespace, so a quote matches its source despite formatting."""
    text = str(text).translate(_QUOTE_CHARS).lower()
    text = re.sub(r"[*`]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _quote_found(quote: str, source: str) -> bool:
    """True if every fragment of *quote* (fragments joined by ... or …) appears
    word for word in *source*. *source* must already be normalised."""
    fragments = re.split(r"\s*(?:\.\.\.|\u2026)\s*", str(quote))
    fragments = [_normalise(f) for f in fragments if f.strip()]
    return bool(fragments) and all(f in source for f in fragments)


def _evidence_quotes(name: str, data: dict) -> list:
    """(location, quote, source) for every quote in a mapping file; source is
    'candidate' or 'research'."""
    out = []
    if name == "jd-to-profile":
        for m in data.get("mappings", []):
            for e in m.get("evidence", []):
                out.append((f"keyword '{m.get('keyword')}'", e.get("quote", ""), "candidate"))
    elif name == "profile-to-jd":
        for h in data.get("highlights", []):
            for e in h.get("evidence", []):
                out.append((f"highlight '{h.get('title')}'", e.get("quote", ""), "candidate"))
    elif name == "company-to-profile":
        for link in data.get("links", []):
            where = f"link '{link.get('company_fact')}'"
            out.append((where, link.get("research_quote", ""), "research"))
            for e in link.get("candidate_evidence", []):
                out.append((where, e.get("quote", ""), "candidate"))
    return out


def _check_quotes(name: str, data: dict, sources: dict) -> list:
    """Errors for every quote not found in its source file."""
    errors = []
    file_name = contracts.MAPPINGS[name][0]
    for where, quote, source in _evidence_quotes(name, data):
        text = sources.get(source)
        if text is None:
            errors.append(f"[{name}] Cannot check quotes: {source} file not found")
            break
        if not _quote_found(quote, text):
            short = quote if len(quote) <= 80 else quote[:77] + "..."
            errors.append(
                f"[{name}] {where}: quote not found in {source} file "
                f"(copy it exactly from the source, or drop the claim): \"{short}\""
            )
    return errors


def _check_mapping_terms(kw_data: dict, map_data: dict) -> list:
    """jd-to-profile.yaml must hold exactly one entry per jd-keywords.yaml term."""
    terms = [k.get("term") for k in kw_data.get("keywords", [])]
    mapped = [m.get("keyword") for m in map_data.get("mappings", [])]
    errors = []
    missing = [t for t in terms if t not in mapped]
    unknown = [m for m in mapped if m not in terms]
    dupes = sorted({m for m in mapped if mapped.count(m) > 1})
    if missing:
        errors.append(f"[jd-to-profile] Keywords with no mapping: {', '.join(missing)}")
    if unknown:
        errors.append(
            "[jd-to-profile] Mappings for terms not in jd-keywords.yaml "
            f"(use the exact term): {', '.join(unknown)}"
        )
    if dupes:
        errors.append(f"[jd-to-profile] Keywords mapped more than once: {', '.join(dupes)}")
    return errors


def _read_text(path: Path):
    return _normalise(path.read_text(encoding="utf-8")) if path.exists() else None


_MAPPING_TYPES = tuple(contracts.MAPPINGS)


def _check_fit(data_path: Path, candidate_path=None) -> list:
    """fit-verdict.yaml: schema, verdict within fit_check.py's ceiling, same blockers."""
    path = data_path / contracts.FIT_FILE
    if not path.exists():
        return [f"[fit] File not found: {path}"]
    data = _load_yaml(path)
    errors = [f"[schema:fit] {e}" for e in validate(data, str(contracts.FIT_SCHEMA))]
    if errors:
        return errors
    try:
        facts = fit_check.check_fit(data_path, candidate_path)
    except FileNotFoundError as e:
        return [f"[fit] {e}"]
    verdict, ceiling = data["verdict"], facts["ceiling"]
    if fit_check.VERDICTS.index(verdict) > fit_check.VERDICTS.index(ceiling):
        errors.append(
            f"[fit] Verdict '{verdict}' is above what fit_check.py allows ('{ceiling}'): "
            f"must coverage {facts['must_coverage']}, top-5 gaps {facts['top_must_gaps']}, "
            f"top-5 weak {facts['top_must_weak']}, blockers {[b['code'] for b in facts['blockers']]}"
        )
    expected = sorted(b["code"] for b in facts["blockers"])
    given = sorted(b.get("code") for b in data.get("blockers", []))
    if given != expected:
        errors.append(f"[fit] Blockers must be exactly fit_check.py's: expected {expected}, got {given}")
    return errors


def validate_output(doc_type: str, data_dir: str, candidate_path=None) -> dict:
    """Validate the data files in an application folder.

    Args:
        doc_type: "cv", "cl", "both", "keywords", one mapping name
            ("jd-to-profile", "profile-to-jd", "company-to-profile"),
            "mappings" for all three, or "fit" (fit-verdict.yaml)
        data_dir: Path to the application folder
        candidate_path: candidate.md to check quotes against (default: the
            project's candidate.md)

    Returns:
        Dictionary with valid (bool), errors, limits and warnings (lists)
    """
    data_path = Path(data_dir)
    all_errors = []
    all_limits = []
    all_warnings = []

    do_cv = doc_type in ("cv", "both")
    do_cl = doc_type in ("cl", "both")
    required_mappings = (
        _MAPPING_TYPES if doc_type == "mappings"
        else (doc_type,) if doc_type in _MAPPING_TYPES else ()
    )

    cv_data = {}
    cl_data = {}

    # jd-keywords.yaml: required for --type keywords, checked whenever present.
    kw_file = data_path / contracts.KEYWORDS_FILE
    kw_data = {}
    if kw_file.exists():
        kw_data = _load_yaml(kw_file)
        kw_errors = [f"[schema:keywords] {e}" for e in validate(kw_data, str(contracts.KEYWORDS_SCHEMA))]
        terms = [k.get("term") for k in kw_data.get("keywords", []) if isinstance(k, dict)]
        dupes = sorted({t for t in terms if terms.count(t) > 1})
        if dupes:
            kw_errors.append(f"[keywords] Terms listed more than once: {', '.join(dupes)}")
        all_errors.extend(kw_errors)
        if kw_errors:
            kw_data = {}
    elif doc_type == "keywords":
        all_errors.append(f"[keywords] File not found: {kw_file}")

    # Mapping files: required for their own --type, checked whenever present.
    sources = None
    mapping_data = {}
    for name, (file_name, schema) in contracts.MAPPINGS.items():
        path = data_path / file_name
        if not path.exists():
            if name in required_mappings:
                all_errors.append(f"[{name}] File not found: {path}")
            continue
        data = _load_yaml(path)
        errs = [f"[schema:{name}] {e}" for e in validate(data, str(schema))]
        if not errs:
            if sources is None:
                sources = {
                    "candidate": _read_text(Path(candidate_path or contracts.CANDIDATE_MD)),
                    "research": _read_text(data_path / "research.md"),
                }
            errs.extend(_check_quotes(name, data, sources))
        if name == "jd-to-profile" and not errs and kw_data:
            errs.extend(_check_mapping_terms(kw_data, data))
        all_errors.extend(errs)
        if not errs:
            mapping_data[name] = data

    if doc_type == "fit":
        all_errors.extend(_check_fit(data_path, candidate_path))

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
    if do_cv or do_cl:
        if not cl_data:
            cl_data = _load_yaml(data_path / "cl-data.yaml")
        if not cv_data:
            cv_data = _load_yaml(data_path / "cv-data.yaml")
        if cv_data and cl_data:
            all_errors.extend(_check_header_consistency(cv_data, cl_data))

    # JD keyword coverage: from jd-keywords.yaml + jd-to-profile.yaml when both
    # are valid, otherwise from the JD text (folders made before the mappers).
    input_md = data_path / "input.md"
    if do_cv and cv_data and kw_data and "jd-to-profile" in mapping_data:
        keywords = _merge_keywords(kw_data, mapping_data["jd-to-profile"])
        errs, warns = _check_keyword_coverage(cv_data, keywords)
        all_errors.extend(errs)
        all_warnings.extend(warns)
    elif do_cv and cv_data and input_md.exists():
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
        description="Validate an application folder's data files against the Netherlands rules"
    )
    parser.add_argument("folder", help="Application folder containing the data YAML files")
    parser.add_argument(
        "--type", default="both",
        choices=["cv", "cl", "both", "keywords", *_MAPPING_TYPES, "mappings", "fit"],
        help="What to validate: cv, cl, both (default), keywords, one mapping file, "
             "mappings (all three), or fit"
    )
    args = parser.parse_args()

    result = validate_output(doc_type=args.type, data_dir=args.folder)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
