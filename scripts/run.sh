#!/usr/bin/env bash
# Legacy wrapper — delegates to run.py for cross-platform compatibility.
exec python3 "$(dirname "$0")/run.py" "$@"
