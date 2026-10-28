#!/usr/bin/env python3
"""Typed access to config/contracts.yaml — the single source of truth for
cross-component "magic strings" (style folders, keyword and mapping files, research.md placeholders).

Import as a sibling module from any script in scripts/:

    from contracts import CV_SCHEMA, RESEARCH_SKIPPED

Auto-locates the project root (parent of scripts/), so it works regardless of
the current working directory.
"""

from pathlib import Path

import yaml

_SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = _SCRIPT_DIR.parent
CONTRACTS_PATH = PROJECT_ROOT / "config" / "contracts.yaml"


def load_contracts(path: Path = CONTRACTS_PATH) -> dict:
    """Load and return the raw contracts mapping.

    Raises a clear error if the file is missing — it is required, since it
    defines the shared strings other components depend on.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Required contracts file not found: {path}\n"
            "It defines cross-component shared strings (style folders, "
            "research placeholders). Restore config/contracts.yaml."
        ) from e


_C = load_contracts()

# ── Style (Netherlands) ─────────────────────────────────────────────────────
SKILLS_DIR = PROJECT_ROOT / ".claude" / "skills"
CV_STYLE_SKILL = _C["style"]["cv_skill"]
CL_STYLE_SKILL = _C["style"]["cl_skill"]
CV_SCHEMA = SKILLS_DIR / CV_STYLE_SKILL / "cv-data-schema.yaml"
CL_SCHEMA = SKILLS_DIR / CL_STYLE_SKILL / "cl-data-schema.yaml"

# ── JD keywords ─────────────────────────────────────────────────────────────
KEYWORDS_SKILL = _C["keywords"]["skill"]
KEYWORDS_FILE = _C["keywords"]["file"]
KEYWORDS_SCHEMA = SKILLS_DIR / KEYWORDS_SKILL / "jd-keywords-schema.yaml"

# ── Profile mapping ─────────────────────────────────────────────────────────
MAPPING_SKILL = _C["mappings"]["skill"]
# name (as used by validate_output.py --type) → (file in the application folder, schema)
MAPPINGS = {
    name: (_C["mappings"][key], SKILLS_DIR / MAPPING_SKILL / f"{name}-schema.yaml")
    for name, key in (
        ("jd-to-profile", "jd_to_profile"),
        ("profile-to-jd", "profile_to_jd"),
        ("company-to-profile", "company_to_profile"),
    )
}

# ── Fit verdict ─────────────────────────────────────────────────────────────
FIT_SKILL = _C["fit"]["skill"]
FIT_FILE = _C["fit"]["file"]
FIT_SCHEMA = SKILLS_DIR / FIT_SKILL / "fit-verdict-schema.yaml"

# ── Candidate profile ───────────────────────────────────────────────────────
CANDIDATE_MD = PROJECT_ROOT / _C["candidate_file"]

# ── research.md placeholders ────────────────────────────────────────────────
RESEARCH_SKIPPED = _C["research_placeholders"]["skipped"]
RESEARCH_SKIPPED_TITLE = _C["research_placeholders"]["skipped_title"]
NO_TECH_STACK = _C["research_placeholders"]["no_tech_stack"]
NO_RECENT_NEWS = _C["research_placeholders"]["no_recent_news"]
NO_ENGINEERING_CULTURE = _C["research_placeholders"]["no_engineering_culture"]


if __name__ == "__main__":
    import json
    import sys

    json.dump(_C, sys.stdout, indent=2, ensure_ascii=False)
    print()
