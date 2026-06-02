#!/usr/bin/env python3
"""Validate YAML data against a JSON Schema (stored as YAML).

Usage:
    python3 validate_schema.py <data.yaml> <schema.yaml>

Returns exit code 0 on success, 1 on validation errors.
"""

import sys
import yaml

try:
    import jsonschema
except ImportError:
    print("Error: jsonschema not installed. Run: pip install jsonschema", file=sys.stderr)
    sys.exit(1)


def validate(data, schema_path):
    """Return a list of human-readable error strings, empty if valid."""
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)

    format_checker = jsonschema.FormatChecker()
    validator = jsonschema.Draft7Validator(schema, format_checker=format_checker)
    errors = []
    for err in sorted(validator.iter_errors(data), key=lambda e: list(e.absolute_path)):
        path = " → ".join(str(p) for p in err.absolute_path) or "root"
        errors.append(f"{path}: {err.message}")
    return errors


def validate_file(data_path, schema_path):
    """Load a YAML file and validate it. Returns list of error strings."""
    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return validate(data, schema_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 validate_schema.py <data.yaml> <schema.yaml>", file=sys.stderr)
        sys.exit(1)

    errs = validate_file(sys.argv[1], sys.argv[2])
    if errs:
        print(f"Validation FAILED ({len(errs)} error(s)):")
        for e in errs:
            print(f"  ✗ {e}")
        sys.exit(1)
    else:
        print("Validation passed ✓")
