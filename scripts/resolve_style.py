#!/usr/bin/env python3
"""Resolve CV and CL style for a job application.

Implements the 4-step cascade:
  1. Explicit --style override
  2. Country-specific skill folder (cv-style-{country})
  3. Region fallback via style-resolution.yaml
  4. Default (cv-style-default / cl-style-default)

Usage:
    python3 scripts/resolve_style.py --location "Berlin, Germany"
    python3 scripts/resolve_style.py --location "Remote (EU)" --style denmark
    python3 scripts/resolve_style.py --location "Germany, Netherlands" \
        --skills-dir .claude/skills --config config/style-resolution.yaml

Output: JSON with cv_style, cl_style, and paths to all config/schema files.
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml


# ── Location parsing ──────────────────────────────────────────────────────────

_REMOTE_RE = re.compile(r"remote\s*\(([^)]+)\)", re.IGNORECASE)
_HYBRID_RE = re.compile(r"hybrid\s*\(([^)]+)\)", re.IGNORECASE)


def _normalize(name: str) -> str:
    """Normalize a country/region name: lowercase, spaces to hyphens."""
    return name.strip().lower().replace(" ", "-")


def extract_country(location: str) -> str:
    """Extract the primary country from a location string.

    Rules:
      - "Berlin, Germany" → germany
      - "Germany, Netherlands, Belgium" → germany (first country)
      - "Remote (EU)" → eu
      - "Remote (Germany)" → germany
      - "Remote (Worldwide)" → worldwide
      - "Hybrid (Germany)" → germany
      - "Spain" → spain
    """
    location = location.strip()

    # Remote(...)
    m = _REMOTE_RE.search(location)
    if m:
        return _normalize(m.group(1))

    # Hybrid(...)
    m = _HYBRID_RE.search(location)
    if m:
        inner = m.group(1)
        # Could be "Germany" or "DE-NL"
        parts = re.split(r"[,\-]", inner)
        return _normalize(parts[0])

    # "Berlin, Germany" or "Germany" or "Germany, Netherlands, Belgium"
    parts = [p.strip() for p in location.split(",")]
    if len(parts) >= 2:
        # Check if last part looks like a country (no digits → not a city+country pair?)
        # Heuristic: "Berlin, Germany" → 2 parts, take last
        # "Germany, Netherlands, Belgium" → 3+ parts, take first
        if len(parts) == 2:
            # Could be "City, Country" or "Country1, Country2"
            # Take the last element as the country
            return _normalize(parts[-1])
        else:
            # Multiple countries → take first
            return _normalize(parts[0])

    return _normalize(parts[0])


# ── Style resolution ─────────────────────────────────────────────────────────

def _load_region_map(config_path: Path) -> dict:
    """Load style-resolution.yaml and build country→region lookup."""
    with open(config_path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    country_to_region = {}
    for region_name, region_data in cfg.get("regions", {}).items():
        for country in region_data.get("countries", []):
            country_to_region[country] = region_name

    # Add region aliases (e.g., "eu" → "europe")
    aliases = cfg.get("aliases", {})
    for alias, region in aliases.items():
        country_to_region[alias] = region

    # Common aliases not in config
    if "eu" not in country_to_region:
        country_to_region["eu"] = "europe"

    return country_to_region


def _style_exists(skills_dir: Path, prefix: str, identifier: str) -> bool:
    """Check if a style skill folder exists (e.g., cv-style-denmark)."""
    return (skills_dir / f"{prefix}-style-{identifier}").is_dir()


def _build_paths(skills_dir: Path, cv_id: str, cl_id: str) -> dict:
    """Build config and schema file paths for resolved styles."""
    cv_dir = skills_dir / f"cv-style-{cv_id}"
    cl_dir = skills_dir / f"cl-style-{cl_id}"

    return {
        "cv_style": cv_id,
        "cl_style": cl_id,
        "cv_style_skill": f"cv-style-{cv_id}",
        "cl_style_skill": f"cl-style-{cl_id}",
        "cv_skill_dir": str(cv_dir),
        "cl_skill_dir": str(cl_dir),
        "cv_config": str(cv_dir / "cv-format.yaml"),
        "cl_config": str(cl_dir / "cl-format.yaml"),
        "cv_schema": str(cv_dir / "cv-data-schema.yaml"),
        "cl_schema": str(cl_dir / "cl-data-schema.yaml"),
    }


def resolve_style(
    location: str,
    style_override: str = "",
    skills_dir: str = ".claude/skills",
    config_path: str = "config/style-resolution.yaml",
) -> dict:
    """Resolve CV and CL style using the 4-step cascade.

    Args:
        location: Location string from input.md.
        style_override: Explicit style override (from Style field).
        skills_dir: Path to .claude/skills directory.
        config_path: Path to style-resolution.yaml.

    Returns:
        Dictionary with cv_style, cl_style, and all config/schema paths.
    """
    skills_path = Path(skills_dir)
    config_file = Path(config_path)

    resolution_steps = []

    # Step 1: Explicit override
    if style_override:
        sid = _normalize(style_override)
        resolution_steps.append(f"explicit override: {sid}")
        cv_exists = _style_exists(skills_path, "cv", sid)
        cl_exists = _style_exists(skills_path, "cl", sid)
        if cv_exists and cl_exists:
            result = _build_paths(skills_path, sid, sid)
            result["resolution"] = resolution_steps
            return result
        # If only one exists, still use it for that type and cascade for the other
        # For simplicity, both must exist; fall through otherwise
        resolution_steps.append(f"  style '{sid}' not fully available, continuing cascade")

    # Extract country from location
    country = extract_country(location)
    resolution_steps.append(f"extracted country: {country}")

    # Step 2: Country-specific
    if country and country != "worldwide":
        if _style_exists(skills_path, "cv", country) and _style_exists(skills_path, "cl", country):
            resolution_steps.append(f"country match: {country}")
            result = _build_paths(skills_path, country, country)
            result["resolution"] = resolution_steps
            return result

    # Step 3: Region fallback
    if config_file.exists():
        country_to_region = _load_region_map(config_file)
        region = country_to_region.get(country)
        if region:
            resolution_steps.append(f"region lookup: {country} → {region}")
            if _style_exists(skills_path, "cv", region) and _style_exists(skills_path, "cl", region):
                resolution_steps.append(f"region match: {region}")
                result = _build_paths(skills_path, region, region)
                result["resolution"] = resolution_steps
                return result
    else:
        resolution_steps.append(f"config not found: {config_file}")

    # Step 4: Default
    resolution_steps.append("fallback: default")
    result = _build_paths(skills_path, "default", "default")
    result["resolution"] = resolution_steps
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Resolve CV/CL style from location and optional override"
    )
    parser.add_argument(
        "--location", required=True,
        help="Location string (e.g., 'Berlin, Germany', 'Remote (EU)')"
    )
    parser.add_argument(
        "--style", default="",
        help="Explicit style override (e.g., 'denmark')"
    )
    parser.add_argument(
        "--skills-dir", default=".claude/skills",
        help="Path to skills directory (default: .claude/skills)"
    )
    parser.add_argument(
        "--config", default="config/style-resolution.yaml",
        help="Path to style-resolution.yaml (default: config/style-resolution.yaml)"
    )
    args = parser.parse_args()

    result = resolve_style(
        location=args.location,
        style_override=args.style,
        skills_dir=args.skills_dir,
        config_path=args.config,
    )

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
