#!/usr/bin/env python3
"""Update style-resolution.yaml with a new country or region entry.

Adds a country to its region's country list (alphabetically), or adds
a new region with an initial country list.

Usage:
    python3 scripts/update_style_resolution.py --identifier spain --type country --region europe
    python3 scripts/update_style_resolution.py --identifier middle-east --type region --countries "saudi-arabia,uae,qatar"
    python3 scripts/update_style_resolution.py --identifier spain --type country --region europe --alias "es:europe"

Output: JSON to stdout with fields:
    updated        — bool, whether the file was modified
    action         — description of what was done (or why nothing changed)
    error          — error message if something failed, else null
"""

import argparse
import json
import sys
from pathlib import Path

import yaml


def _find_region_country_range(lines: list[str], region: str) -> tuple[int, int, list[str]]:
    """Find the line range of a region's countries list and return existing countries.

    Returns:
        (start_idx, end_idx, existing_countries)
        start_idx: line index of first country entry
        end_idx: line index after last country entry (insertion point for new entries)
        existing_countries: list of country names already present
    """
    # Find the region key line
    region_line = -1
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == f"{region}:":
            region_line = i
            break

    if region_line == -1:
        return -1, -1, []

    # Find "countries:" under this region
    countries_line = -1
    for i in range(region_line + 1, len(lines)):
        stripped = lines[i].strip()
        if stripped == "countries:":
            countries_line = i
            break
        # If we hit another region key or top-level key, stop
        if stripped and not stripped.startswith("#") and not stripped.startswith("-"):
            if not lines[i].startswith("      ") and not lines[i].startswith("    "):
                break

    if countries_line == -1:
        return -1, -1, []

    # Detect the indentation used for list items
    existing = []
    start_idx = countries_line + 1
    end_idx = start_idx
    for i in range(start_idx, len(lines)):
        stripped = lines[i].strip()
        if stripped.startswith("- "):
            existing.append(stripped[2:])
            end_idx = i + 1
        elif stripped == "" or stripped.startswith("#"):
            end_idx = i + 1
            continue
        else:
            break

    return start_idx, end_idx, existing


def _detect_country_indent(lines: list[str], start_idx: int, end_idx: int) -> str:
    """Detect the indentation used for country list items."""
    for i in range(start_idx, end_idx):
        stripped = lines[i].strip()
        if stripped.startswith("- "):
            return lines[i][:lines[i].index("-")]
    return "      "  # default: 6 spaces


def update_style_resolution(
    identifier: str,
    id_type: str,
    region: str | None = None,
    countries: list[str] | None = None,
    aliases: list[str] | None = None,
    config_path: str = "config/style-resolution.yaml",
) -> dict:
    """Update style-resolution.yaml with a new entry using text-level edits.

    Preserves original file formatting by inserting lines rather than
    round-tripping through yaml.dump.

    Args:
        identifier: Normalized identifier (e.g., "spain", "middle-east").
        id_type: "country", "region", or "new".
        region: Target region for country identifiers.
        countries: Initial country list for new regions.
        aliases: List of "alias:target" strings to add.
        config_path: Path to style-resolution.yaml.

    Returns:
        Result dict with updated flag, action description, and error.
    """
    config_file = Path(config_path)

    if not config_file.exists():
        return {"updated": False, "action": None, "error": f"Config file not found: {config_path}"}

    try:
        text = config_file.read_text(encoding="utf-8")
        cfg = yaml.safe_load(text)
    except yaml.YAMLError:
        return {"updated": False, "action": None, "error": f"Failed to parse: {config_path}"}

    if cfg is None:
        cfg = {}

    lines = text.split("\n")
    actions = []
    modified = False

    # ── Handle country type ───────────────────────────────────────────────
    if id_type == "country" or (id_type == "new" and region):
        if not region:
            return {"updated": False, "action": None, "error": "Country type requires --region"}

        # Check if already listed anywhere
        for r_name, r_data in (cfg.get("regions") or {}).items():
            r_countries = ((r_data or {}).get("countries") or [])
            if identifier in r_countries:
                return {
                    "updated": False,
                    "action": f"'{identifier}' already listed under region '{r_name}'",
                    "error": None,
                }

        # Find the region's country list
        start, end, existing = _find_region_country_range(lines, region)

        if start == -1:
            # Region doesn't exist — add it before aliases section
            alias_line = -1
            for i, line in enumerate(lines):
                if line.strip() == "aliases:" or line.strip().startswith("aliases:"):
                    alias_line = i
                    break

            insert_at = alias_line if alias_line != -1 else len(lines)

            # Detect indent from existing regions instead of hardcoding
            indent = "      "  # fallback: 6 spaces
            for r_name in (cfg.get("regions") or {}):
                s, e, _ = _find_region_country_range(lines, r_name)
                if s != -1:
                    indent = _detect_country_indent(lines, s, e)
                    break

            new_block = [
                f"  {region}:",
                "    countries:",
                f"{indent}- {identifier}",
            ]
            lines[insert_at:insert_at] = new_block
            actions.append(f"Created new region '{region}'")
            actions.append(f"Added '{identifier}' to region '{region}'")
            modified = True
        else:
            # Insert country alphabetically into existing list
            indent = _detect_country_indent(lines, start, end)
            new_line = f"{indent}- {identifier}"

            # Find correct alphabetical position
            insert_at = end  # default: append at end
            for i in range(start, end):
                stripped = lines[i].strip()
                if stripped.startswith("- ") and stripped[2:] > identifier:
                    insert_at = i
                    break

            lines.insert(insert_at, new_line)
            actions.append(f"Added '{identifier}' to region '{region}'")
            modified = True

    # ── Handle region type ────────────────────────────────────────────────
    elif id_type == "region" or (id_type == "new" and not region):
        if identifier in (cfg.get("regions") or {}):
            return {
                "updated": False,
                "action": f"Region '{identifier}' already exists",
                "error": None,
            }

        # Find insertion point before aliases
        alias_line = -1
        for i, line in enumerate(lines):
            if line.strip() == "aliases:" or line.strip().startswith("aliases:"):
                alias_line = i
                break

        insert_at = alias_line if alias_line != -1 else len(lines)

        # Detect indentation from existing regions
        indent = "      "
        for r_name in (cfg.get("regions") or {}):
            s, e, _ = _find_region_country_range(lines, r_name)
            if s != -1:
                indent = _detect_country_indent(lines, s, e)
                break

        initial_countries = sorted(countries) if countries else []
        new_block = [f"  {identifier}:", "    countries:"]
        for c in initial_countries:
            new_block.append(f"{indent}- {c}")
        lines[insert_at:insert_at] = new_block
        actions.append(f"Created region '{identifier}' with {len(initial_countries)} countries")
        modified = True

    # ── Add aliases ───────────────────────────────────────────────────────
    if aliases:
        existing_aliases = cfg.get("aliases") or {}
        for alias_pair in aliases:
            if ":" not in alias_pair:
                continue
            alias_key, alias_target = alias_pair.split(":", 1)
            alias_key = alias_key.strip()
            alias_target = alias_target.strip()
            if alias_key and alias_target and alias_key not in existing_aliases:
                # Append at end of file
                lines.append(f"  {alias_key}: {alias_target}")
                actions.append(f"Added alias '{alias_key}' → '{alias_target}'")
                modified = True

    # ── Write back ────────────────────────────────────────────────────────
    if not modified:
        return {"updated": False, "action": "No changes needed", "error": None}

    config_file.write_text("\n".join(lines), encoding="utf-8")

    return {
        "updated": True,
        "action": "; ".join(actions),
        "error": None,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Update style-resolution.yaml with a new country or region."
    )
    parser.add_argument(
        "--identifier",
        required=True,
        help="Normalized style identifier.",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["country", "region", "new"],
        help="Whether the identifier is a country, region, or new entry.",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="Target region for country identifiers.",
    )
    parser.add_argument(
        "--countries",
        default=None,
        help="Comma-separated initial country list for new regions.",
    )
    parser.add_argument(
        "--alias",
        action="append",
        default=None,
        help="Alias to add, format: 'alias:target'. Can be repeated.",
    )
    parser.add_argument(
        "--config",
        default="config/style-resolution.yaml",
        help="Path to style-resolution.yaml.",
    )

    args = parser.parse_args()

    country_list = None
    if args.countries:
        country_list = [c.strip() for c in args.countries.split(",") if c.strip()]

    result = update_style_resolution(
        identifier=args.identifier,
        id_type=args.type,
        region=args.region,
        countries=country_list,
        aliases=args.alias,
        config_path=args.config,
    )
    print(json.dumps(result, indent=2))
    sys.exit(1 if result["error"] else 0)


if __name__ == "__main__":
    main()
