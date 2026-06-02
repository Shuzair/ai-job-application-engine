#!/usr/bin/env python3
"""Create a versioned output folder for a job application.

Reads and parses input.md, derives a normalized folder name, creates the
directory, and writes a snapshot of the input as the folder's input.md.

Usage:
    python3 scripts/prepare_folder.py --input job-applications/input.md \
        --output-dir job-applications/output

Output: JSON to stdout with folder_path, folder_name, version, and parsed input.
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

from parse_input import parse_input


def _normalize_segment(text: str) -> str:
    """Normalize a text segment for folder naming: lowercase, hyphens for spaces."""
    text = text.lower().strip()
    # Remove special chars except hyphens and parens
    text = re.sub(r"[&]+", "-", text)
    text = re.sub(r"[^a-z0-9\s\-()]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text.strip("-")


# ISO 3166-1 alpha-2 codes for common countries
_ISO_CODES = {
    "germany": "de", "netherlands": "nl", "belgium": "be", "france": "fr",
    "spain": "es", "italy": "it", "portugal": "pt", "austria": "at",
    "switzerland": "ch", "denmark": "dk", "sweden": "se", "norway": "no",
    "finland": "fi", "poland": "pl", "ireland": "ie", "greece": "gr",
    "czech-republic": "cz", "czechia": "cz", "romania": "ro", "hungary": "hu",
    "croatia": "hr", "luxembourg": "lu", "estonia": "ee", "latvia": "lv",
    "lithuania": "lt", "slovakia": "sk", "slovenia": "si", "bulgaria": "bg",
    "uk": "uk", "united-kingdom": "uk",
    "usa": "us", "united-states": "us", "canada": "ca", "mexico": "mx",
    "japan": "jp", "south-korea": "kr", "china": "cn", "india": "in",
    "australia": "au", "new-zealand": "nz", "singapore": "sg",
    "saudi-arabia": "sa", "uae": "ae", "united-arab-emirates": "ae",
    "turkey": "tr", "israel": "il", "brazil": "br", "argentina": "ar",
}


def _country_code(name: str) -> str:
    """Return ISO 2-letter code for a country, or first 2 chars as fallback."""
    normalized = _normalize_segment(name)
    return _ISO_CODES.get(normalized, normalized[:2])


def _normalize_location(location: str) -> str:
    """Normalize location for folder naming.

    Rules:
      - Single country: "Berlin, Germany" → "germany"
      - "Germany, Netherlands, Belgium" → "de-nl-be"
      - "Remote (EU)" → "remote(eu)"
      - "Remote (Germany)" → "remote(germany)"
      - "Remote (Worldwide)" → "remote(worldwide)"
      - "Hybrid (Germany)" → "hybrid(germany)"
      - "Hybrid (DE-NL)" → "hybrid(de-nl)"
    """
    loc = location.strip()

    # Remote(...)
    m = re.match(r"remote\s*\(([^)]+)\)", loc, re.IGNORECASE)
    if m:
        inner = _normalize_segment(m.group(1))
        return f"remote({inner})"

    # Hybrid(...)
    m = re.match(r"hybrid\s*\(([^)]+)\)", loc, re.IGNORECASE)
    if m:
        inner = _normalize_segment(m.group(1))
        return f"hybrid({inner})"

    # Multiple countries: use ISO 2-letter codes
    parts = [p.strip() for p in loc.split(",")]
    if len(parts) >= 3:
        codes = [_country_code(p) for p in parts]
        return "-".join(codes)

    # "City, Country" → just the country
    if len(parts) == 2:
        return _normalize_segment(parts[-1])

    # Single value
    return _normalize_segment(parts[0])


def _next_version(output_dir: Path, prefix: str) -> int:
    """Find the next version number for folders matching the prefix."""
    if not output_dir.exists():
        return 1

    max_v = 0
    pattern = re.compile(re.escape(prefix) + r"_v(\d+)$")
    for entry in output_dir.iterdir():
        if entry.is_dir():
            m = pattern.match(entry.name)
            if m:
                v = int(m.group(1))
                if v > max_v:
                    max_v = v
    return max_v + 1


def _write_snapshot(folder: Path, data: dict) -> None:
    """Write a snapshot input.md in the output folder."""
    lines = [
        "# Application Input",
        "",
        f"**Company:** {data.get('company') or 'Not specified'}",
        f"**Link:** {data.get('link') or 'Not specified'}",
        f"**Role:** {data['role']}",
        f"**Location:** {data['location']}",
        f"**Style:** {data.get('style') or 'Auto'}",
        f"**Generated on:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "## Job Description",
        "",
        data["job_description"],
        "",
    ]
    (folder / "input.md").write_text("\n".join(lines), encoding="utf-8")


def prepare_folder(input_path: str, output_dir: str) -> dict:
    """Parse input and create a versioned output folder.

    Args:
        input_path: Path to input.md.
        output_dir: Path to the output directory (e.g., job-applications/output).

    Returns:
        Dictionary with folder_path, folder_name, version, and parsed input data.
    """
    data = parse_input(input_path)

    if not data["valid"]:
        return {
            "folder_path": "",
            "folder_name": "",
            "version": 0,
            "valid": False,
            "errors": data["errors"],
        }

    role = _normalize_segment(data["role"])
    company = _normalize_segment(data["company"]) if data["company"] else "no-name"
    location = _normalize_location(data["location"])

    prefix = f"{location}_{company}_{role}"

    out_path = Path(output_dir)
    version = _next_version(out_path, prefix)
    folder_name = f"{prefix}_v{version}"
    folder_path = out_path / folder_name

    folder_path.mkdir(parents=True, exist_ok=True)
    _write_snapshot(folder_path, data)

    return {
        "folder_path": str(folder_path),
        "folder_name": folder_name,
        "version": version,
        "valid": True,
        "errors": [],
        "parsed": data,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Create a versioned output folder for a job application"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input.md"
    )
    parser.add_argument(
        "--output-dir", required=True,
        help="Path to output directory (e.g., job-applications/output)"
    )
    args = parser.parse_args()

    result = prepare_folder(args.input, args.output_dir)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
