#!/usr/bin/env python3
"""Cross-platform venv wrapper. Replaces run.sh.

Usage: python scripts/run.py <script.py> [args...]

Automatically creates the venv and installs dependencies if missing.
"""
import os
import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
VENV_DIR = PROJECT_ROOT / "venv"

if sys.platform == "win32":
    PYTHON = VENV_DIR / "Scripts" / "python.exe"
    PIP = VENV_DIR / "Scripts" / "pip.exe"
else:
    PYTHON = VENV_DIR / "bin" / "python3"
    PIP = VENV_DIR / "bin" / "pip"


def main():
    if not PYTHON.exists():
        print(f"Creating virtual environment in {VENV_DIR} ...")
        subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])

    marker = VENV_DIR / ".deps-installed"
    req = PROJECT_ROOT / "requirements.txt"
    if not marker.exists() or req.stat().st_mtime > marker.stat().st_mtime:
        print("Installing dependencies from requirements.txt ...")
        subprocess.check_call([str(PIP), "install", "-q", "-r", str(req)])
        marker.touch()

    if sys.platform != "win32":
        os.execv(str(PYTHON), [str(PYTHON)] + sys.argv[1:])
    else:
        result = subprocess.run([str(PYTHON)] + sys.argv[1:])
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
