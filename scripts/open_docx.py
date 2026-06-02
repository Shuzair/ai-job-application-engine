#!/usr/bin/env python3
"""Cross-platform open/reload for docx files.

Opens a docx file in the default word processor. If the file is already open,
closes and reopens it so the user sees the latest version.

Usage:
    python scripts/run.py scripts/open_docx.py <path> [<path2> ...]

Supports macOS (Microsoft Word via AppleScript), Windows (Word via PowerShell
COM automation), and Linux (xdg-open — LibreOffice auto-detects file changes).
"""

import platform
import subprocess
import sys
from pathlib import Path


def _open_macos(filepath: str):
    script = f'''
    tell application "System Events"
        set wordRunning to (name of every process) contains "Microsoft Word"
    end tell

    if wordRunning then
        tell application "Microsoft Word"
            repeat with doc in documents
                if full name of doc is "{filepath}" then
                    close doc saving no
                end if
            end repeat
            open "{filepath}"
            activate
        end tell
    else
        do shell script "open " & quoted form of "{filepath}"
    end if
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        subprocess.run(["open", filepath])


def _open_windows(filepath: str):
    ps_script = f'''
    $filepath = "{filepath}"
    try {{
        $word = [System.Runtime.InteropServices.Marshal]::GetActiveObject("Word.Application")
        foreach ($doc in $word.Documents) {{
            if ($doc.FullName -eq $filepath) {{
                $doc.Close([ref]$false)
                break
            }}
        }}
        $word.Documents.Open($filepath) | Out-Null
        $word.Activate()
    }} catch {{
        Start-Process $filepath
    }}
    '''
    try:
        subprocess.run(
            ["powershell", "-NoProfile", "-Command", ps_script],
            check=True, capture_output=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        import os
        os.startfile(filepath)


def _open_linux(filepath: str):
    subprocess.Popen(
        ["xdg-open", filepath],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def open_docx(filepath: str):
    path = Path(filepath).resolve()
    if not path.exists():
        print(f"Error: {path} not found")
        sys.exit(1)

    filepath_str = str(path)
    system = platform.system()

    if system == "Darwin":
        _open_macos(filepath_str)
    elif system == "Windows":
        _open_windows(filepath_str)
    elif system == "Linux":
        _open_linux(filepath_str)
    else:
        print(f"Warning: unsupported OS '{system}', trying generic open")
        subprocess.run(["open", filepath_str])

    print(f"Opened: {path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/open_docx.py <path> [<path2> ...]")
        sys.exit(1)

    for filepath in sys.argv[1:]:
        open_docx(filepath)


if __name__ == "__main__":
    main()
