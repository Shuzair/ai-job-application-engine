#!/usr/bin/env python3
"""Validate and resolve a style identifier for the /style command.

Handles Step 1 (parse, normalize, classify) and Step 2 (check existing)
of the /style skill, including fuzzy matching for misspelled inputs.

Usage:
    python3 scripts/validate_style_input.py --identifier "germny"
    python3 scripts/validate_style_input.py --identifier "Saudi Arabia"
    python3 scripts/validate_style_input.py --identifier "europe"

Output: JSON to stdout with fields:
    identifier     — normalized identifier (after correction if applicable)
    original       — original input before normalization
    type           — "country", "region", or "new"
    region         — parent region if type is "country", else null
    correction     — spelling correction applied, or null if exact match
    cv_style_exists — bool, whether cv-style-{id}/ folder exists
    cl_style_exists — bool, whether cl-style-{id}/ folder exists
    region_cv_style_exists — bool, whether cv-style-{region}/ exists (for scaffold cascade)
    region_cl_style_exists — bool, whether cl-style-{region}/ exists (for scaffold cascade)
    error          — error message if input is invalid, else null
"""

import argparse
import difflib
import json
import re
import sys
from pathlib import Path

import yaml


# Characters that must never appear in a style identifier
_UNSAFE_CHARS = re.compile(r"[/\\]|\.\.")


def _normalize(name: str) -> str:
    """Normalize: lowercase, strip, spaces to hyphens."""
    return name.strip().lower().replace(" ", "-")


def _load_config(config_path: Path) -> dict | None:
    """Load style-resolution.yaml. Returns None on parse error."""
    try:
        with open(config_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError:
        return None


def _build_known_names(cfg: dict) -> tuple[set, set, dict, dict]:
    """Build sets of known countries, regions, aliases, and country→region map.

    Returns:
        (countries, regions, aliases, country_to_region)
    """
    countries = set()
    regions = set()
    country_to_region = {}

    for region_name, region_data in (cfg.get("regions") or {}).items():
        regions.add(region_name)
        for country in (region_data.get("countries") if region_data else None) or []:
            countries.add(country)
            country_to_region[country] = region_name

    aliases = {}
    for alias, target in (cfg.get("aliases") or {}).items():
        aliases[alias] = target

    return countries, regions, aliases, country_to_region


def _fuzzy_match(name: str, candidates: list[str], cutoff: float = 0.6) -> str | None:
    """Find the closest match for a misspelled name.

    Returns the best match if similarity >= cutoff, else None.
    """
    matches = difflib.get_close_matches(name, candidates, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def validate_style_input(
    identifier: str,
    skills_dir: str = ".claude/skills",
    config_path: str = "config/style-resolution.yaml",
) -> dict:
    """Validate and resolve a style identifier.

    Args:
        identifier: Raw user input (e.g., "germny", "Saudi Arabia", "europe").
        skills_dir: Path to .claude/skills directory.
        config_path: Path to style-resolution.yaml.

    Returns:
        Result dict with identifier, type, region, correction, existence flags.
    """
    original = identifier.strip()

    if not original:
        return {
            "identifier": None,
            "original": "",
            "type": None,
            "region": None,
            "correction": None,
            "cv_style_exists": False,
            "cl_style_exists": False,
            "region_cv_style_exists": False,
            "region_cl_style_exists": False,
            "error": "No identifier provided. Usage: /style <country|region>",
        }

    normalized = _normalize(original)

    if _UNSAFE_CHARS.search(normalized):
        return {
            "identifier": None,
            "original": original,
            "type": None,
            "region": None,
            "correction": None,
            "cv_style_exists": False,
            "cl_style_exists": False,
            "region_cv_style_exists": False,
            "region_cl_style_exists": False,
            "error": f"Invalid characters in identifier: {original!r}",
        }

    config_file = Path(config_path)
    skills_path = Path(skills_dir)

    if not config_file.exists():
        return {
            "identifier": normalized,
            "original": original,
            "type": None,
            "region": None,
            "correction": None,
            "cv_style_exists": False,
            "cl_style_exists": False,
            "region_cv_style_exists": False,
            "region_cl_style_exists": False,
            "error": f"Config file not found: {config_path}",
        }

    cfg = _load_config(config_file)
    if cfg is None:
        return {
            "identifier": normalized,
            "original": original,
            "type": None,
            "region": None,
            "correction": None,
            "cv_style_exists": False,
            "cl_style_exists": False,
            "region_cv_style_exists": False,
            "region_cl_style_exists": False,
            "error": f"Failed to parse config file: {config_path}",
        }

    countries, regions, aliases, country_to_region = _build_known_names(cfg)

    # All known names for fuzzy matching
    all_known = sorted(countries | regions | set(aliases.keys()))

    correction = None
    resolved = normalized

    # ── Exact match checks ────────────────────────────────────────────────

    # Check aliases first (e.g., "eu" → "europe")
    if normalized in aliases:
        resolved = aliases[normalized]
        # The alias target is a region
        id_type = "region"
        region = None
    elif normalized in countries:
        id_type = "country"
        region = country_to_region.get(normalized)
    elif normalized in regions:
        id_type = "region"
        region = None
    else:
        # ── No exact match → try fuzzy matching ──────────────────────────
        best = _fuzzy_match(normalized, all_known)

        if best is not None:
            resolved = best

            # Resolve through alias if the match is an alias
            if resolved in aliases:
                resolved = aliases[resolved]
                id_type = "region"
                region = None
            elif resolved in countries:
                id_type = "country"
                region = country_to_region.get(resolved)
            elif resolved in regions:
                id_type = "region"
                region = None
            else:
                id_type = "new"
                region = None

            # Set correction to the final resolved value
            correction = resolved
        else:
            id_type = "new"
            region = None

    # ── Check existing style folders ──────────────────────────────────────
    cv_exists = (skills_path / f"cv-style-{resolved}").is_dir()
    cl_exists = (skills_path / f"cl-style-{resolved}").is_dir()

    # ── Check region style existence (for scaffold source cascade) ────────
    region_cv_exists = False
    region_cl_exists = False
    if region:
        region_cv_exists = (skills_path / f"cv-style-{region}").is_dir()
        region_cl_exists = (skills_path / f"cl-style-{region}").is_dir()

    return {
        "identifier": resolved,
        "original": original,
        "type": id_type,
        "region": region,
        "correction": correction,
        "cv_style_exists": cv_exists,
        "cl_style_exists": cl_exists,
        "region_cv_style_exists": region_cv_exists,
        "region_cl_style_exists": region_cl_exists,
        "error": None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Validate and resolve a style identifier for /style command."
    )
    parser.add_argument(
        "--identifier",
        required=True,
        help="Country or region name to validate (e.g., 'germany', 'Saudi Arabia').",
    )
    parser.add_argument(
        "--skills-dir",
        default=".claude/skills",
        help="Path to .claude/skills directory.",
    )
    parser.add_argument(
        "--config",
        default="config/style-resolution.yaml",
        help="Path to style-resolution.yaml.",
    )

    args = parser.parse_args()
    result = validate_style_input(
        identifier=args.identifier,
        skills_dir=args.skills_dir,
        config_path=args.config,
    )
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["error"] else 0)


if __name__ == "__main__":
    main()
