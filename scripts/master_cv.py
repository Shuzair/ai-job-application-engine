#!/usr/bin/env python3
"""The master CV: one Netherlands CV, built once by /cv and sent unchanged
with every application.

It lives in master-cv/ (config/contracts.yaml → master_cv.dir) as
cv-data.yaml, an optional cv-format-override.yaml, and the rendered cv.docx
and cv.pdf. /apply copies those files into the application folder, so each
folder records exactly the CV that was sent.

Usage:
    python scripts/run.py scripts/master_cv.py status
    python scripts/run.py scripts/master_cv.py copy <folder>
    python scripts/run.py scripts/master_cv.py backup

Output: JSON to stdout; exit 1 when the command cannot do its job.
"""

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import contracts

DATA = "cv-data.yaml"
RENDERED = ("cv.docx", "cv.pdf")
BACKUP = "cv-data.previous.yaml"


def _mtime(path: Path) -> float:
    return path.stat().st_mtime if path.exists() else 0.0


def _stamp(t: float) -> str:
    return datetime.fromtimestamp(t).strftime("%Y-%m-%d %H:%M") if t else ""


def status(master_dir: Path = None, candidate: Path = None) -> dict:
    """Is there a master CV, is its docx/pdf current, and is it older than candidate.md?"""
    master_dir = Path(master_dir or contracts.MASTER_CV_DIR)
    candidate = Path(candidate or contracts.CANDIDATE_PATH)
    data = master_dir / DATA
    inputs = max(_mtime(data), _mtime(master_dir / contracts.CV_FORMAT_OVERRIDE))
    rendered = data.exists() and all(
        _mtime(master_dir / name) >= inputs for name in RENDERED
    )
    stale = data.exists() and _mtime(candidate) > _mtime(data)
    return {
        "folder": str(master_dir),
        "exists": data.exists(),
        "rendered": rendered,
        "stale": stale,
        "built_at": _stamp(_mtime(data)),
        "candidate_updated_at": _stamp(_mtime(candidate)),
    }


def copy_to(folder, master_dir: Path = None) -> list:
    """Copy the master CV (data, override if any, docx, pdf) into *folder*."""
    master_dir = Path(master_dir or contracts.MASTER_CV_DIR)
    folder = Path(folder)
    st = status(master_dir)
    if not st["exists"]:
        raise RuntimeError(f"No master CV in {master_dir}. Run /cv to build it.")
    if not st["rendered"]:
        raise RuntimeError(
            f"The master CV's docx/pdf are older than its data. Render it first:\n"
            f"python scripts/run.py scripts/render.py {master_dir} --only cv"
        )
    if not folder.is_dir():
        raise RuntimeError(f"Folder not found: {folder}")

    if sys.platform == "win32":
        from word import close_in_word
        close_in_word([folder / "cv.docx"])

    names = [DATA, *RENDERED]
    override = master_dir / contracts.CV_FORMAT_OVERRIDE
    if override.exists():
        names.append(override.name)
    elif (folder / override.name).exists():
        (folder / override.name).unlink()  # stale override from an older master
    for name in names:
        shutil.copy2(master_dir / name, folder / name)
    return [str(folder / name) for name in names]


def backup(master_dir: Path = None) -> str:
    """Keep the current cv-data.yaml as cv-data.previous.yaml before a rebuild."""
    master_dir = Path(master_dir or contracts.MASTER_CV_DIR)
    data = master_dir / DATA
    if not data.exists():
        return ""
    shutil.copy2(data, master_dir / BACKUP)
    return str(master_dir / BACKUP)


def main():
    usage = "Usage: master_cv.py status | copy <folder> | backup"
    if len(sys.argv) < 2 or sys.argv[1] not in ("status", "copy", "backup"):
        print(usage)
        sys.exit(1)

    cmd = sys.argv[1]
    try:
        if cmd == "status":
            result = status()
        elif cmd == "copy":
            if len(sys.argv) != 3:
                print(usage)
                sys.exit(1)
            result = {"copied": copy_to(sys.argv[2])}
        else:
            result = {"backup": backup()}
    except (RuntimeError, OSError) as e:
        json.dump({"error": str(e)}, sys.stdout, indent=2, ensure_ascii=False)
        print()
        sys.exit(1)

    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()


if __name__ == "__main__":
    main()
