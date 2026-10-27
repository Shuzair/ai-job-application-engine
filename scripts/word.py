#!/usr/bin/env python3
"""Microsoft Word automation (Windows): close, convert and open .docx files.

Word locks a document while it is open, so a re-render must close it first.
PDFs are exported by a private, hidden Word instance, which also reports the
page count so the page limits in the format configs can be checked.

Usage:
    python scripts/run.py scripts/word.py open <path> [<path2> ...]
"""

import os
import sys
from pathlib import Path

WD_DO_NOT_SAVE = 0
WD_STATISTIC_PAGES = 2
WD_FORMAT_PDF = 17


def _same_file(a: str, b: str) -> bool:
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def close_in_word(paths) -> list:
    """Close the given documents in the user's running Word, without saving.

    Matches on the full path, so another application's cv.docx is left alone.
    Returns the paths that were closed (empty if Word is not running).
    """
    try:
        import win32com.client
        word = win32com.client.GetActiveObject("Word.Application")
    except Exception:
        return []
    closed = []
    for doc in list(word.Documents):
        full_name = doc.FullName
        if any(_same_file(full_name, p) for p in paths):
            doc.Close(WD_DO_NOT_SAVE)
            closed.append(full_name)
    return closed


def to_pdf(docx_paths) -> dict:
    """Export each .docx to a .pdf beside it. Returns {docx_path: page_count}.

    Raises on failure: a PDF that was not written is never reported as done.
    """
    import pythoncom
    import win32com.client

    pythoncom.CoInitialize()
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0
    pages = {}
    try:
        for docx in docx_paths:
            docx = str(Path(docx).resolve())
            pdf = str(Path(docx).with_suffix(".pdf"))
            doc = word.Documents.Open(docx, ReadOnly=True, AddToRecentFiles=False)
            try:
                pages[docx] = doc.ComputeStatistics(WD_STATISTIC_PAGES)
                doc.SaveAs(pdf, FileFormat=WD_FORMAT_PDF)
            finally:
                doc.Close(WD_DO_NOT_SAVE)
            if not Path(pdf).exists():
                raise RuntimeError(f"Word did not write {pdf}")
    finally:
        word.Quit()
    return pages


def open_in_word(paths) -> None:
    """Open documents in the default application (Word) for preview."""
    for p in paths:
        os.startfile(str(Path(p).resolve()))


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != "open":
        print("Usage: python scripts/run.py scripts/word.py open <path> [<path2> ...]")
        sys.exit(1)
    open_in_word(sys.argv[2:])
