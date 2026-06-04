#!/usr/bin/env python3
"""Typed access to config/contracts.yaml — the single source of truth for
cross-component "magic strings" (override filenames, research.md placeholders,
scan conventions).

Import as a sibling module from any script in scripts/:

    from contracts import CV_FORMAT_OVERRIDE, RESEARCH_SKIPPED

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
            "It defines cross-component shared strings (override filenames, "
            "research placeholders, scan conventions). Restore config/contracts.yaml."
        ) from e


_C = load_contracts()

# ── Override files ──────────────────────────────────────────────────────────
CV_FORMAT_OVERRIDE = _C["override_files"]["cv_format_override"]
CL_FORMAT_OVERRIDE = _C["override_files"]["cl_format_override"]

# ── research.md placeholders ────────────────────────────────────────────────
RESEARCH_SKIPPED = _C["research_placeholders"]["skipped"]
RESEARCH_SKIPPED_TITLE = _C["research_placeholders"]["skipped_title"]
NO_TECH_STACK = _C["research_placeholders"]["no_tech_stack"]
NO_RECENT_NEWS = _C["research_placeholders"]["no_recent_news"]
NO_ENGINEERING_CULTURE = _C["research_placeholders"]["no_engineering_culture"]

# ── Scan conventions ────────────────────────────────────────────────────────
CAREERS_PAGE_COLUMN = _C["scan"]["careers_page_column"]
MATCHED_JOBS_FILENAME = _C["scan"]["matched_jobs_filename"]


if __name__ == "__main__":
    import json
    import sys

    json.dump(_C, sys.stdout, indent=2, ensure_ascii=False)
    print()
