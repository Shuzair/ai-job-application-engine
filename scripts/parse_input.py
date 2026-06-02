#!/usr/bin/env python3
"""Parse job-applications/input.md into structured JSON.

Handles two formats:
  1. Main input.md — markdown # headers with content below each
  2. Snapshot input.md — **Key:** Value format under # Application Input

Usage:
    python3 scripts/parse_input.py --input job-applications/input.md
    python3 scripts/parse_input.py --input job-applications/output/folder/input.md

Output: JSON to stdout with fields: company, link, role, location, style,
        job_description, date, format, valid, errors
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# Placeholder detection: bracketed text with hint phrases, em-dash, or >50 chars
_PLACEHOLDER_HINTS = re.compile(
    r"leave\s+empty|e\.g\.|paste\s+the|exactly\s+as|optional|override",
    re.IGNORECASE,
)


def _is_placeholder(value: str) -> bool:
    """Return True if value looks like a template placeholder."""
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return False
    inner = stripped[1:-1]
    if "\u2014" in inner:  # em-dash
        return True
    if len(inner) > 50:
        return True
    if _PLACEHOLDER_HINTS.search(inner):
        return True
    return False


def _clean_value(value: str) -> str:
    """Strip whitespace and remove placeholder text."""
    value = value.strip()
    if _is_placeholder(value):
        return ""
    return value


def _detect_format(text: str) -> str:
    """Detect whether the file is main format or snapshot format."""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("# Application Input"):
            return "snapshot"
        if line.startswith("#"):
            return "main"
    return "main"


def _parse_main_format(text: str) -> dict:
    """Parse the # Header section format used in job-applications/input.md."""
    sections = {}
    current_key = None
    current_lines = []

    for line in text.splitlines():
        if line.startswith("# ") and not line.startswith("## "):
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line[2:].strip()
            current_lines = []
        else:
            if current_key is not None:
                current_lines.append(line)

    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()

    return {
        "company": _clean_value(sections.get("Company", "")),
        "link": _clean_value(sections.get("Link", "")),
        "role": _clean_value(sections.get("Role", "")),
        "location": _clean_value(sections.get("Location", "")),
        "style": _clean_value(sections.get("Style", "")),
        "job_description": _clean_value(sections.get("Job Description", "")),
    }


def _parse_snapshot_format(text: str) -> dict:
    """Parse the **Key:** Value format used in output folder snapshots."""
    fields = {}

    # Extract **Key:** Value pairs
    for match in re.finditer(r"\*\*(\w[\w\s]*?):\*\*\s*(.*)", text):
        key = match.group(1).strip()
        value = match.group(2).strip()
        fields[key] = value

    # Extract Job Description from ## Job Description section
    jd_match = re.search(r"## Job Description\s*\n(.*)", text, re.DOTALL)
    jd_text = jd_match.group(1).strip() if jd_match else ""

    # Normalize snapshot values
    def _snap_value(val: str) -> str:
        if val in ("Not specified", "Auto", "auto", ""):
            return ""
        return val.strip()

    return {
        "company": _snap_value(fields.get("Company", "")),
        "link": _snap_value(fields.get("Link", "")),
        "role": _snap_value(fields.get("Role", "")),
        "location": _snap_value(fields.get("Location", "")),
        "style": _snap_value(fields.get("Style", "")),
        "job_description": jd_text,
    }


def parse_input(input_path: str) -> dict:
    """Parse an input.md file and return structured data.

    Args:
        input_path: Path to the input.md file.

    Returns:
        Dictionary with keys: company, link, role, location, style,
        job_description, date, format, valid, errors
    """
    path = Path(input_path)
    if not path.exists():
        return {
            "company": "",
            "link": "",
            "role": "",
            "location": "",
            "style": "",
            "job_description": "",
            "date": datetime.now().strftime("%B %d, %Y"),
            "format": "unknown",
            "valid": False,
            "errors": [f"File not found: {input_path}"],
        }

    text = path.read_text(encoding="utf-8")
    fmt = _detect_format(text)

    if fmt == "snapshot":
        data = _parse_snapshot_format(text)
    else:
        data = _parse_main_format(text)

    # Add metadata
    data["date"] = datetime.now().strftime("%B %d, %Y")
    data["format"] = fmt

    # Validate required fields
    errors = []
    if not data["role"]:
        errors.append("Missing required field: Role")
    if not data["location"]:
        errors.append("Missing required field: Location")
    if not data["job_description"]:
        errors.append("Missing required field: Job Description")

    data["valid"] = len(errors) == 0
    data["errors"] = errors

    return data


def main():
    parser = argparse.ArgumentParser(
        description="Parse input.md into structured JSON"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input.md (main format or snapshot format)"
    )
    args = parser.parse_args()

    result = parse_input(args.input)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()  # trailing newline

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
