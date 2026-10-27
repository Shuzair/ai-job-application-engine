#!/usr/bin/env python3
"""Render an application folder's CV and cover letter: YAML data → docx → pdf.

The layout is fixed (scripts/nl_template.py); the data is checked against
the Netherlands schemas (config/contracts.yaml → style).

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
        "schema": contracts.CV_SCHEMA,
        "max_pages": 2,
    },
    "cl": {
        "label": "Cover Letter",
        "data": "cl-data.yaml",
        "docx": "cover-letter.docx",
        "schema": contracts.CL_SCHEMA,
        "max_pages": 1,
    },
}


class RenderError(Exception):
    pass


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _render_docx(kind: str, data_dir: Path) -> Path:
    """Validate, render and content-check one document. Returns the docx path."""
    from validate_schema import validate
    import nl_template
    import render_validate
    from word import close_in_word

    spec = DOCS[kind]
    data_path = data_dir / spec["data"]
    docx_path = data_dir / spec["docx"]
    if not data_path.exists():
        raise RenderError(f"{data_path.name} not found in {data_dir}")

    data = load_yaml(data_path)

    errors = validate(data, str(spec["schema"]))
    if errors:
        lines = "\n".join(f"  - {e}" for e in errors)
        raise RenderError(f"{data_path.name} does not match the schema:\n{lines}")

    if sys.platform == "win32":
        for name in close_in_word([docx_path]):
            print(f"  Closed in Word: {Path(name).name}")

    render = nl_template.render_cv if kind == "cv" else nl_template.render_cl
    try:
        render(data, str(docx_path))
    except PermissionError:
        raise RenderError(f"{docx_path.name} is open in another program. Close it and run again.")
    print(f"  Wrote {docx_path.name}")

    if not render_validate.validate(str(docx_path), str(data_path), spec["label"]):
        raise RenderError(f"{docx_path.name} is missing content from {data_path.name} (see the check above)")
    return docx_path


def render_folder(folder, only=None, pdf=True, open_docs=True) -> dict:
    """Render the folder's documents. Returns {"docs": [...], "warnings": [...]}."""
    data_dir = Path(folder).resolve()
    if not data_dir.is_dir():
        raise RenderError(f"Folder not found: {data_dir}")

    kinds = [only] if only else ["cv", "cl"]
    rendered = []
    for kind in kinds:
        print(f"\n[{DOCS[kind]['label']}]")
        docx_path = _render_docx(kind, data_dir)
        rendered.append({
            "kind": kind,
            "docx": str(docx_path),
            "max_pages": DOCS[kind]["max_pages"],
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
