#!/usr/bin/env python3
"""Create a versioned output folder for a job application.

Reads and parses input.md, derives the folder name `<company>_<role>_v<n>`,
creates the directory, and writes a snapshot of the input as the folder's
input.md (same format as job-applications/input.md, so parse_input.py reads
both).

Usage:
    python scripts/run.py scripts/prepare_folder.py --input job-applications/input.md --output-dir job-applications/output

Output: JSON to stdout with folder_path, folder_name, version, and parsed input.
"""

import argparse
import json
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path

from parse_input import parse_input

_MAX_SEGMENT = 60


def _normalize_segment(text: str) -> str:
    """Normalize a text segment for folder naming: lowercase ASCII, hyphens for spaces."""
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = text.lower().strip()
    text = re.sub(r"[&/]+", "-", text)
    text = re.sub(r"[^a-z0-9\s\-]", "", text)
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"-{2,}", "-", text)
    return text[:_MAX_SEGMENT].strip("-")


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
                max_v = max(max_v, int(m.group(1)))
    return max_v + 1


def _write_snapshot(folder: Path, data: dict) -> None:
    """Write a snapshot input.md in the output folder."""
    lines = [
        "# Company", data.get("company", ""), "",
        "# Link", data.get("link", ""), "",
        "# Role", data["role"], "",
        "# Location", data["location"], "",
        "# Generated On", datetime.now().strftime("%Y-%m-%d"), "",
        "# Job Description", data["job_description"], "",
    ]
    (folder / "input.md").write_text("\n".join(lines), encoding="utf-8")


def prepare_folder(input_path: str, output_dir: str) -> dict:
    """Parse input and create a versioned output folder."""
    data = parse_input(input_path)

    if not data["valid"]:
        return {
            "folder_path": "",
            "folder_name": "",
            "version": 0,
            "valid": False,
            "errors": data["errors"],
        }

    role = _normalize_segment(data["role"]) or "role"
    company = _normalize_segment(data["company"]) if data["company"] else ""
    prefix = f"{company or 'no-name'}_{role}"

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
    parser.add_argument("--input", required=True, help="Path to input.md")
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
