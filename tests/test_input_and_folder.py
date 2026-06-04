"""Regression guards for the deterministic input-parsing and folder-naming
logic the refactor must not have disturbed."""
import parse_input as pi
import prepare_folder as pf


def test_parse_main_format(tmp_path):
    f = tmp_path / "input.md"
    f.write_text(
        "# Role\nData Engineer\n\n"
        "# Location\nBerlin, Germany\n\n"
        "# Job Description\nBuild data pipelines.\n",
        encoding="utf-8",
    )
    data = pi.parse_input(str(f))
    assert data["role"] == "Data Engineer"
    assert data["location"] == "Berlin, Germany"
    assert data["valid"] is True


def test_missing_required_fields_invalid(tmp_path):
    f = tmp_path / "input.md"
    f.write_text("# Role\nData Engineer\n", encoding="utf-8")
    data = pi.parse_input(str(f))
    assert data["valid"] is False
    assert any("Location" in e for e in data["errors"])


def test_folder_naming(tmp_path):
    inp = tmp_path / "input.md"
    inp.write_text(
        "# Company\nAcme\n\n"
        "# Role\nData Engineer\n\n"
        "# Location\nBerlin, Germany\n\n"
        "# Job Description\nx\n",
        encoding="utf-8",
    )
    out = tmp_path / "out"
    res = pf.prepare_folder(str(inp), str(out))
    assert res["folder_name"] == "germany_acme_data-engineer_v1"


def test_folder_naming_no_company(tmp_path):
    inp = tmp_path / "input.md"
    inp.write_text(
        "# Role\nNurse\n\n"
        "# Location\nRemote (EU)\n\n"
        "# Job Description\nx\n",
        encoding="utf-8",
    )
    out = tmp_path / "out"
    res = pf.prepare_folder(str(inp), str(out))
    assert res["folder_name"] == "remote(eu)_no-name_nurse_v1"
