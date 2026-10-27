#!/usr/bin/env python3
"""Render an application folder's CV and cover letter: YAML data → docx → pdf.

Uses the Netherlands style config and schema (config/contracts.yaml → style),
deep-merged with the folder's cv/cl-format-override.yaml if present.

For each document: validate the data against the schema, close the docx in
Word if it is open, write the docx, check every YAML value reached it, then
export the PDF through Word and check the page count. Any failure exits 1;
nothing is reported as generated unless the file was written.

Usage:
    python scripts/run.py scripts/render.py <folder> [--only cv|cl] [--no-pdf] [--no-open]
"""

import argparse
import sys
from pathlib import Path

import yaml

# Ensure scripts/ is on sys.path for sibling imports
_SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_SCRIPT_DIR))

import contracts  # noqa: E402

DOCS = {
    "cv": {
        "label": "CV",
        "data": "cv-data.yaml",
        "docx": "cv.docx",
        "config": contracts.CV_CONFIG,
        "schema": contracts.CV_SCHEMA,
        "override": contracts.CV_FORMAT_OVERRIDE,
    },
    "cl": {
        "label": "Cover Letter",
        "data": "cl-data.yaml",
        "docx": "cover-letter.docx",
        "config": contracts.CL_CONFIG,
        "schema": contracts.CL_SCHEMA,
        "override": contracts.CL_FORMAT_OVERRIDE,
    },
}


class RenderError(Exception):
    pass


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


def load_config(kind: str, data_dir: Path) -> dict:
    """Base style config for *kind*, with the folder's override merged on top."""
    spec = DOCS[kind]
    config = load_yaml(spec["config"])
    override_path = data_dir / spec["override"]
    if override_path.exists():
        override = load_yaml(override_path)
        if override:
            config = deep_merge(config, override)
            print(f"  Applied override: {override_path.name}")
    return config


def _render_docx(kind: str, data_dir: Path) -> tuple:
    """Validate, render and content-check one document. Returns (docx_path, config)."""
    from validate_schema import validate
    import render_validate
    from word import close_in_word

    spec = DOCS[kind]
    data_path = data_dir / spec["data"]
    docx_path = data_dir / spec["docx"]
    if not data_path.exists():
        raise RenderError(f"{data_path.name} not found in {data_dir}")

    data = load_yaml(data_path)
    config = load_config(kind, data_dir)

    errors = validate(data, str(spec["schema"]))
    if errors:
        lines = "\n".join(f"  - {e}" for e in errors)
        raise RenderError(f"{data_path.name} does not match the schema:\n{lines}")

    if sys.platform == "win32":
        for name in close_in_word([docx_path]):
            print(f"  Closed in Word: {Path(name).name}")

    if kind == "cv":
        from render_cv import render_cv as render
    else:
        from render_cl import render_cl as render
    try:
        render(data, config, str(docx_path))
    except PermissionError:
        raise RenderError(f"{docx_path.name} is open in another program. Close it and run again.")
    print(f"  Wrote {docx_path.name}")

    if not render_validate.validate(str(docx_path), str(data_path), spec["label"]):
        raise RenderError(f"{docx_path.name} is missing content from {data_path.name} (see the check above)")
    return docx_path, config


def render_folder(folder, only=None, pdf=True, open_docs=True) -> dict:
    """Render the folder's documents. Returns {"docs": [...], "warnings": [...]}."""
    data_dir = Path(folder).resolve()
    if not data_dir.is_dir():
        raise RenderError(f"Folder not found: {data_dir}")

    kinds = [only] if only else ["cv", "cl"]
    rendered = []
    for kind in kinds:
        print(f"\n[{DOCS[kind]['label']}]")
        docx_path, config = _render_docx(kind, data_dir)
        rendered.append({
            "kind": kind,
            "docx": str(docx_path),
            "max_pages": config.get("validation", {}).get("max_pages"),
        })

    warnings = []
    if pdf:
        from word import to_pdf
        print("\nExporting PDF through Word ...")
        try:
            pages = to_pdf([d["docx"] for d in rendered])
        except Exception as e:
            raise RenderError(
                f"PDF export failed: {e}\n"
                "If a PDF is open in a viewer, close it and run again."
            )
        for d in rendered:
            d["pdf"] = str(Path(d["docx"]).with_suffix(".pdf"))
            d["pages"] = pages[str(Path(d["docx"]).resolve())]
            if d["max_pages"] and d["pages"] > d["max_pages"]:
                warnings.append(
                    f"{Path(d['docx']).name} is {d['pages']} pages (limit {d['max_pages']})"
                )

    if open_docs:
        from word import open_in_word
        open_in_word([d["docx"] for d in rendered])

    return {"docs": rendered, "warnings": warnings}


def main():
    parser = argparse.ArgumentParser(description="Render CV/CL YAML data to docx and pdf")
    parser.add_argument("folder", help="Application folder containing cv-data.yaml / cl-data.yaml")
    parser.add_argument("--only", choices=["cv", "cl"], help="Render only one document")
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF export")
    parser.add_argument("--no-open", action="store_true", help="Do not open the docx in Word")
    args = parser.parse_args()

    try:
        result = render_folder(args.folder, args.only, not args.no_pdf, not args.no_open)
    except RenderError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)

    print("\nDone:")
    for d in result["docs"]:
        line = f"  {Path(d['docx']).name}"
        if "pdf" in d:
            limit = f" (limit {d['max_pages']})" if d["max_pages"] else ""
            line += f", {Path(d['pdf']).name}: {d['pages']} page(s){limit}"
        print(line)
    for w in result["warnings"]:
        print(f"WARNING: {w}")


if __name__ == "__main__":
    main()
