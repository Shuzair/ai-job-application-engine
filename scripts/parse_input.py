#!/usr/bin/env python3
"""Parse an input.md into structured JSON.

Works on job-applications/input.md and on the snapshot an application folder
keeps (same format). The file is a list of `# Header` sections: Company, Link,
Role, Location, Job Description. Job Description is the last section and runs
to the end of the file, so a pasted posting may contain its own `#` lines.
Unknown headers (e.g. the snapshot's `# Generated On`) are ignored.

Usage:
    python scripts/run.py scripts/parse_input.py --input job-applications/input.md

Output: JSON to stdout with fields: company, link, role, location,
        job_description, date, valid, errors
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# Every application is for the Netherlands; Location only narrows it to a city.
DEFAULT_LOCATION = "Netherlands"

_FIELD_HEADERS = {
    "company": "company",
    "link": "link",
    "role": "role",
    "location": "location",
}
_JD_HEADER = "job description"

# Placeholder detection: bracketed text with hint phrases, em-dash, or >50 chars
_PLACEHOLDER_HINTS = re.compile(
    r"leave\s+empty|e\.g\.|paste\s+the|exactly\s+as|optional",
    re.IGNORECASE,
)


def _is_placeholder(value: str) -> bool:
    """Return True if value looks like a template placeholder."""
    stripped = value.strip()
    if not (stripped.startswith("[") and stripped.endswith("]")):
        return False
    if "\n" in stripped:  # template placeholders are one line; a pasted JD is not
        return False
    inner = stripped[1:-1]
    if "—" in inner:  # em-dash
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


def _split_sections(text: str) -> dict:
    """Return {field: raw text} for the known headers."""
    sections = {}
    current = None
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("# "):
            title = line[2:].strip().lower()
            if title == _JD_HEADER:
                sections["job_description"] = "\n".join(lines[i + 1:])
                break
            current = _FIELD_HEADERS.get(title)
            if current:
                sections[current] = ""
            continue
        if current:
            sections[current] += line + "\n"
    return sections


def letter_date(now: datetime = None) -> str:
    """Date as written on a Dutch letter: '27 October 2026'."""
    now = now or datetime.now()
    return f"{now.day} {now:%B %Y}"


def parse_input(input_path: str) -> dict:
    """Parse an input.md file and return structured data."""
    path = Path(input_path)
    if not path.exists():
        return {
            "company": "", "link": "", "role": "", "location": "",
            "job_description": "", "date": letter_date(),
            "valid": False, "errors": [f"File not found: {input_path}"],
        }

    sections = _split_sections(path.read_text(encoding="utf-8"))
    data = {
        key: _clean_value(sections.get(key, ""))
        for key in ("company", "link", "role", "location", "job_description")
    }
    data["location"] = data["location"] or DEFAULT_LOCATION
    data["date"] = letter_date()

    errors = []
    if not data["role"]:
        errors.append("Missing required field: Role")
    if not data["job_description"]:
        errors.append("Missing required field: Job Description")
    data["valid"] = not errors
    data["errors"] = errors
    return data


def main():
    parser = argparse.ArgumentParser(description="Parse input.md into structured JSON")
    parser.add_argument("--input", required=True, help="Path to input.md")
    args = parser.parse_args()

    result = parse_input(args.input)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()

    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
