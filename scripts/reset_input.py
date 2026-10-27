#!/usr/bin/env python3
"""Reset input.md to the blank template.

Usage:
    python scripts/run.py scripts/reset_input.py --input job-applications/input.md

Writes the standard template with placeholder text.
"""

import argparse
import sys
from pathlib import Path

TEMPLATE = """# Company
[company name — leave empty if unknown]

# Link
[URL to the job posting — leave empty if unavailable]

# Role
[job title exactly as listed]

# Location
[city, e.g. Amsterdam — leave empty if just "Netherlands"]

# Job Description
[paste the full job description here]
""".lstrip()


def reset_input(input_path: str) -> None:
    """Write the blank template to the given path."""
    Path(input_path).write_text(TEMPLATE, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Reset input.md to the blank template"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to input.md to reset"
    )
    args = parser.parse_args()

    reset_input(args.input)
    print(f"Reset {args.input}", file=sys.stderr)


if __name__ == "__main__":
    main()
