#!/usr/bin/env python3
"""CLI entry point for rendering CV and cover letter documents.

Usage:
    python3 scripts/render.py --type cv   --data-dir <folder> --cv-config <path> --cv-schema <path> [--pdf]
    python3 scripts/render.py --type cl   --data-dir <folder> --cl-config <path> --cl-schema <path> [--pdf]
    python3 scripts/render.py --type both --data-dir <folder> --cv-config <path> --cv-schema <path> --cl-config <path> --cl-schema <path> [--pdf]

The script auto-locates the project root (parent of scripts/), so it works
regardless of the current working directory.
"""

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

# Ensure scripts/ is on sys.path for sibling imports
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

PROJECT_ROOT = _SCRIPT_DIR.parent


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def validate_data(data, schema_path):
    """Run schema validation; exit on failure."""
    from validate_schema import validate
    errors = validate(data, str(schema_path))
    if errors:
        print(f"Schema validation FAILED ({len(errors)} error(s)):")
        for e in errors:
            print(f"  ✗ {e}")
        sys.exit(1)


def convert_to_pdf(docx_path):
    docx_path = Path(docx_path)
    pdf_path = docx_path.with_suffix(".pdf")

    # Try docx2pdf first (uses Microsoft Word via AppleScript on macOS)
    try:
        import time
        from docx2pdf import convert
        for attempt in range(2):
            try:
                convert(str(docx_path), str(pdf_path))
                print(f"  Generated: {pdf_path}")
                return
            except (Exception, SystemExit):
                if attempt == 0:
                    time.sleep(3)
                    continue
                raise
    except ImportError:
        pass
    except (Exception, SystemExit) as e:
        print(f"  Warning: docx2pdf failed: {e}")

    # Fall back to LibreOffice (try common binary names and macOS app path)
    soffice_candidates = [
        "soffice",
        "libreoffice",
        "/Applications/LibreOffice.app/Contents/MacOS/soffice",
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for binary in soffice_candidates:
        try:
            subprocess.run(
                [binary, "--headless", "--convert-to", "pdf",
                 "--outdir", str(docx_path.parent), str(docx_path)],
                check=True, capture_output=True,
            )
            print(f"  Generated: {pdf_path}")
            return
        except FileNotFoundError:
            continue
        except subprocess.CalledProcessError as e:
            print(f"  Warning: PDF conversion failed: {e.stderr.decode()}")
            return
    print("  Warning: PDF conversion failed — neither docx2pdf nor LibreOffice available.")


def render_cv_doc(data_dir, cv_config_path, cv_schema_path, output_dir, gen_pdf):
    from render_cv import render_cv

    data_path = data_dir / "cv-data.yaml"
    output_path = output_dir / "cv.docx"

    if not data_path.exists():
        print(f"Error: {data_path} not found"); sys.exit(1)

    from contracts import CV_FORMAT_OVERRIDE

    data = load_yaml(data_path)
    config = load_yaml(cv_config_path)

    override_path = data_dir / CV_FORMAT_OVERRIDE
    if override_path.exists():
        override = load_yaml(override_path)
        if override:
            config = deep_merge(config, override)
            print(f"  Applied override: {override_path}")

    validate_data(data, cv_schema_path)

    render_cv(data, config, str(output_path))
    print(f"  Generated: {output_path}")

    if gen_pdf:
        convert_to_pdf(output_path)


def render_cl_doc(data_dir, cl_config_path, cl_schema_path, output_dir, gen_pdf):
    from render_cl import render_cl

    data_path = data_dir / "cl-data.yaml"
    output_path = output_dir / "cover-letter.docx"

    if not data_path.exists():
        print(f"Error: {data_path} not found"); sys.exit(1)

    from contracts import CL_FORMAT_OVERRIDE

    data = load_yaml(data_path)
    config = load_yaml(cl_config_path)

    override_path = data_dir / CL_FORMAT_OVERRIDE
    if override_path.exists():
        override = load_yaml(override_path)
        if override:
            config = deep_merge(config, override)
            print(f"  Applied override: {override_path}")

    validate_data(data, cl_schema_path)

    render_cl(data, config, str(output_path))
    print(f"  Generated: {output_path}")

    if gen_pdf:
        convert_to_pdf(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Render CV/CL from structured YAML data + config → docx/pdf"
    )
    parser.add_argument("--type", choices=["cv", "cl", "both"], required=True,
                        help="Which document(s) to render")
    parser.add_argument("--data-dir", required=True,
                        help="Folder containing cv-data.yaml and/or cl-data.yaml")
    parser.add_argument("--cv-config", default=None,
                        help="Path to cv-format.yaml (required for cv/both)")
    parser.add_argument("--cl-config", default=None,
                        help="Path to cl-format.yaml (required for cl/both)")
    parser.add_argument("--cv-schema", default=None,
                        help="Path to cv-data-schema.yaml (required for cv/both)")
    parser.add_argument("--cl-schema", default=None,
                        help="Path to cl-data-schema.yaml (required for cl/both)")
    parser.add_argument("--output-dir", default=None,
                        help="Where to write output (default: same as --data-dir)")
    parser.add_argument("--pdf", action="store_true",
                        help="Also convert docx → pdf via LibreOffice")

    args = parser.parse_args()

    data_dir = Path(args.data_dir).resolve()
    output_dir = Path(args.output_dir).resolve() if args.output_dir else data_dir

    # Validate required config/schema args based on --type
    if args.type in ("cv", "both"):
        if not args.cv_config or not args.cv_schema:
            parser.error("--cv-config and --cv-schema are required when --type is cv or both")
    if args.type in ("cl", "both"):
        if not args.cl_config or not args.cl_schema:
            parser.error("--cl-config and --cl-schema are required when --type is cl or both")

    print(f"Rendering from: {data_dir}")
    print(f"Output dir:     {output_dir}\n")

    if args.type in ("cv", "both"):
        cv_config = Path(args.cv_config).resolve()
        cv_schema = Path(args.cv_schema).resolve()
        print(f"CV config:      {cv_config}")
        print(f"CV schema:      {cv_schema}")
        render_cv_doc(data_dir, cv_config, cv_schema, output_dir, args.pdf)
    if args.type in ("cl", "both"):
        cl_config = Path(args.cl_config).resolve()
        cl_schema = Path(args.cl_schema).resolve()
        print(f"CL config:      {cl_config}")
        print(f"CL schema:      {cl_schema}")
        render_cl_doc(data_dir, cl_config, cl_schema, output_dir, args.pdf)

    print("\nDone.")


if __name__ == "__main__":
    main()
