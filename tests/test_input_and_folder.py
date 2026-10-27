"""Input parsing and folder naming: deterministic, and lossless for the JD."""
import os
import subprocess
import sys
from pathlib import Path

import parse_input as pi
import prepare_folder as pf
import reset_input as ri

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _write(tmp_path, text):
    f = tmp_path / "input.md"
    f.write_text(text, encoding="utf-8")
    return f


def test_parse_main_format(tmp_path):
    f = _write(tmp_path, (
        "# Company\nAcme\n\n"
        "# Role\nData Engineer\n\n"
        "# Location\nAmsterdam\n\n"
        "# Job Description\nBuild data pipelines.\n"
    ))
    data = pi.parse_input(str(f))
    assert data["company"] == "Acme"
    assert data["role"] == "Data Engineer"
    assert data["location"] == "Amsterdam"
    assert data["job_description"] == "Build data pipelines."
    assert data["valid"] is True


def test_location_defaults_to_netherlands(tmp_path):
    f = _write(tmp_path, "# Role\nData Engineer\n\n# Job Description\nx\n")
    data = pi.parse_input(str(f))
    assert data["valid"] is True
    assert data["location"] == "Netherlands"


def test_blank_template_is_invalid(tmp_path):
    f = tmp_path / "input.md"
    ri.reset_input(str(f))
    data = pi.parse_input(str(f))
    assert data["valid"] is False
    assert data["company"] == data["role"] == data["job_description"] == ""
    assert data["location"] == "Netherlands"
    assert any("Role" in e for e in data["errors"])
    assert any("Job Description" in e for e in data["errors"])


def test_jd_keeps_its_own_headings(tmp_path):
    jd = (
        "About us\n"
        "# Responsibilities\n"
        "- Build pipelines\n"
        "# Role\n"
        "**Location:** Rotterdam\n"
        "- Own the warehouse"
    )
    f = _write(tmp_path, f"# Role\nData Engineer\n\n# Location\nUtrecht\n\n# Job Description\n{jd}\n")
    data = pi.parse_input(str(f))
    assert data["job_description"] == jd
    assert data["role"] == "Data Engineer"
    assert data["location"] == "Utrecht"


def test_bracketed_multiline_jd_is_not_a_placeholder(tmp_path):
    jd = "[Acme] is hiring a Data Engineer.\nYou will build pipelines for our clients.\n[Apply now]"
    f = _write(tmp_path, f"# Role\nData Engineer\n\n# Job Description\n{jd}\n")
    assert pi.parse_input(str(f))["job_description"] == jd


def test_letter_date_is_day_first():
    from datetime import datetime
    assert pi.letter_date(datetime(2026, 10, 7)) == "7 October 2026"


def test_folder_naming_and_versioning(tmp_path):
    inp = _write(tmp_path, (
        "# Company\nCafé Acme B.V.\n\n"
        "# Role\nSenior Data Engineer (Platform)\n\n"
        "# Job Description\nx\n"
    ))
    out = tmp_path / "out"
    first = pf.prepare_folder(str(inp), str(out))
    second = pf.prepare_folder(str(inp), str(out))
    assert first["folder_name"] == "cafe-acme-bv_senior-data-engineer-platform_v1"
    assert second["folder_name"] == "cafe-acme-bv_senior-data-engineer-platform_v2"


def test_folder_naming_no_company(tmp_path):
    inp = _write(tmp_path, "# Role\nAnalytics Engineer\n\n# Job Description\nx\n")
    res = pf.prepare_folder(str(inp), str(tmp_path / "out"))
    assert res["folder_name"] == "no-name_analytics-engineer_v1"


def test_snapshot_round_trips(tmp_path):
    jd = "Intro\n# Requirements\n**Company:** NotThis\n- SQL"
    inp = _write(tmp_path, (
        "# Company\nAcme\n\n# Link\nhttps://acme.nl/jobs/1\n\n"
        f"# Role\nData Engineer\n\n# Location\nAmsterdam\n\n# Job Description\n{jd}\n"
    ))
    res = pf.prepare_folder(str(inp), str(tmp_path / "out"))
    snap = pi.parse_input(str(Path(res["folder_path"]) / "input.md"))
    for key in ("company", "link", "role", "location", "job_description"):
        assert snap[key] == res["parsed"][key], key
    assert snap["job_description"] == jd


def test_non_ascii_jd_does_not_crash_on_windows_console(tmp_path):
    """The Windows console is cp1252; run.py must force UTF-8 for its child."""
    f = _write(tmp_path, "# Role\nData Engineer\n\n# Job Description\nShip it → fast ✅ \U0001F680\n")
    env = {k: v for k, v in os.environ.items() if k not in ("PYTHONIOENCODING", "PYTHONUTF8")}
    proc = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "run.py"),
         str(PROJECT_ROOT / "scripts" / "parse_input.py"), "--input", str(f)],
        capture_output=True, env=env, cwd=PROJECT_ROOT,
    )
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    assert "\U0001F680" in proc.stdout.decode("utf-8")
