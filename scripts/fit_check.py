#!/usr/bin/env python3
"""The fixed part of the fit verdict: how much of the posting's must-haves the
candidate covers, and the hard blockers. Same answer on every run and machine.

Reads the application folder's jd-keywords.yaml and jd-to-profile.yaml, and two
places in candidate.md: the `## Languages` section (is Dutch there?) and the
`**Visa Note:**` line (does it say "Requires sponsorship"?). Neither ever goes
into the CV or cover letter; they only decide whether to apply.

The fit-agent adds judgement on top (seniority, which gaps are core) and may
lower the verdict, never raise it above `ceiling`.

Usage:
    python scripts/run.py scripts/fit_check.py <folder>

Output: JSON to stdout:
    {ceiling, must_coverage, nice_coverage, must_total, must_gaps[],
     top_must_gaps[], must_weak[], top_must_weak[], blockers[{code, message}], notes[]}
Exit 1 if jd-keywords.yaml or jd-to-profile.yaml is missing.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

import contracts

# Credit a keyword earns by its evidence strength (profile-mapping skill).
STRENGTH_CREDIT = {
    "shipped": 1.0,
    "built": 0.8,
    "certified": 0.4,
    "tooling": 0.4,
    "learning": 0.2,
    "planned": 0.1,
}
ANALOGUE_FACTOR = 0.7  # an analogue earns this share of its strength's credit

# The best verdict the numbers allow. Tune here.
FIT_RULES = {
    "strong_min_coverage": 0.8,    # ...and no missing or weak must among the top ranks
    "possible_min_coverage": 0.6,  # below this, or with a blocker: weak
    "top_ranks": 5,                # a top-5 must that is missing, or known only weakly
                                   # (tooling / certified / learning / planned), caps it at possible
}

VERDICTS = ("weak", "possible", "strong")  # worst → best


def _load_yaml(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _credit(mapping: dict) -> float:
    """0–1 credit for one keyword's mapping."""
    match = mapping.get("match")
    if match not in ("yes", "analogue"):
        return 0.0
    credit = STRENGTH_CREDIT.get(mapping.get("strength"), 0.0)
    return credit * ANALOGUE_FACTOR if match == "analogue" else credit


def _coverage(keywords: list, by_term: dict, priority: str):
    """Mean credit over the keywords of one priority, or None if there are none."""
    selected = [k for k in keywords if k.get("priority") == priority]
    if not selected:
        return None
    total = sum(_credit(by_term.get(k.get("term"), {})) for k in selected)
    return round(total / len(selected), 2)


def candidate_facts(text: str) -> dict:
    """What candidate.md says about Dutch and sponsorship (None = not stated)."""
    text = text.replace("\r\n", "\n")

    speaks_dutch = None
    section = re.search(r"^(#{1,6})\s*Languages\s*$", text, re.MULTILINE | re.IGNORECASE)
    if section:
        level = len(section.group(1))
        rest = text[section.end():]
        end = re.search(rf"^#{{1,{level}}}\s", rest, re.MULTILINE)
        body = rest[: end.start()] if end else rest
        speaks_dutch = re.search(r"\b(dutch|nederlands)\b", body, re.IGNORECASE) is not None

    needs_sponsorship = None
    visa = re.search(r"^\*\*Visa Note:\*\*(.*)$", text, re.MULTILINE | re.IGNORECASE)
    if visa:
        needs_sponsorship = re.search(
            r"\brequires?\s+(visa\s+)?sponsorship", visa.group(1), re.IGNORECASE
        ) is not None

    return {"speaks_dutch": speaks_dutch, "needs_sponsorship": needs_sponsorship}


def check_fit(folder, candidate_path=None) -> dict:
    """Coverage, blockers and the verdict ceiling for an application folder."""
    folder = Path(folder)
    kw_path = folder / contracts.KEYWORDS_FILE
    map_path = folder / contracts.MAPPINGS["jd-to-profile"][0]
    missing = [str(p) for p in (kw_path, map_path) if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Needed for the fit check: {', '.join(missing)}")

    kw_data = _load_yaml(kw_path)
    keywords = kw_data.get("keywords", [])
    role = kw_data.get("role", {})
    by_term = {m.get("keyword"): m for m in _load_yaml(map_path).get("mappings", [])}

    musts = sorted((k for k in keywords if k.get("priority") == "must"),
                   key=lambda k: k.get("rank", 0))
    must_gaps = [k["term"] for k in musts if _credit(by_term.get(k["term"], {})) == 0]
    top_terms = {k["term"] for k in musts[: FIT_RULES["top_ranks"]]}
    top_must_gaps = [t for t in must_gaps if t in top_terms]
    must_weak = [
        {"term": k["term"], "strength": by_term[k["term"]].get("strength")}
        for k in musts
        if by_term.get(k["term"], {}).get("match") in ("yes", "analogue")
        and by_term[k["term"]].get("strength") not in ("shipped", "built")
    ]
    top_must_weak = [w["term"] for w in must_weak if w["term"] in top_terms]

    cand_path = Path(candidate_path or contracts.CANDIDATE_MD)
    facts = candidate_facts(cand_path.read_text(encoding="utf-8")) if cand_path.exists() else {
        "speaks_dutch": None, "needs_sponsorship": None}

    blockers, notes = [], []
    dutch = role.get("dutch_required", "no")
    if dutch in ("yes", "nice"):
        if facts["speaks_dutch"] is None:
            notes.append("The posting asks for Dutch; candidate.md has no Languages section to check.")
        elif not facts["speaks_dutch"]:
            if dutch == "yes":
                blockers.append({"code": "dutch-required",
                                 "message": "The posting requires Dutch; candidate.md lists no Dutch."})
            else:
                notes.append("Dutch is a plus in the posting; candidate.md lists no Dutch.")

    sponsorship = role.get("sponsorship", "not-mentioned")
    if facts["needs_sponsorship"]:
        if sponsorship == "not-offered":
            blockers.append({"code": "no-sponsorship",
                             "message": "The posting says it does not sponsor visas; the Visa Note says sponsorship is needed."})
        elif sponsorship == "not-mentioned":
            notes.append("The posting does not say whether it sponsors visas — check the IND register of recognised sponsors.")

    must_coverage = _coverage(keywords, by_term, "must")
    coverage = must_coverage if must_coverage is not None else 0.0
    if blockers or coverage < FIT_RULES["possible_min_coverage"]:
        ceiling = "weak"
    elif coverage < FIT_RULES["strong_min_coverage"] or top_must_gaps or top_must_weak:
        ceiling = "possible"
    else:
        ceiling = "strong"

    return {
        "ceiling": ceiling,
        "must_coverage": must_coverage,
        "nice_coverage": _coverage(keywords, by_term, "nice"),
        "must_total": len(musts),
        "must_gaps": must_gaps,
        "top_must_gaps": top_must_gaps,
        "must_weak": must_weak,
        "top_must_weak": top_must_weak,
        "blockers": blockers,
        "notes": notes,
    }


def main():
    parser = argparse.ArgumentParser(description="Fixed fit facts for an application folder")
    parser.add_argument("folder", help="Application folder with jd-keywords.yaml and jd-to-profile.yaml")
    args = parser.parse_args()
    try:
        result = check_fit(args.folder)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
