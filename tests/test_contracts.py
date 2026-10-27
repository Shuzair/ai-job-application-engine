"""config/contracts.yaml is the single source of truth for cross-component
magic strings. These guard that the typed loader stays in sync with the file."""
import contracts


def test_constants_exposed():
    assert "skipped" in contracts.RESEARCH_SKIPPED.lower()
    assert contracts.RESEARCH_SKIPPED_TITLE == "Not Available"


def test_loader_matches_constants():
    c = contracts.load_contracts()
    assert c["style"]["cv_skill"] == contracts.CV_STYLE_SKILL
    assert c["research_placeholders"]["no_tech_stack"] == contracts.NO_TECH_STACK


def test_style_files_exist():
    for path in (contracts.CV_SCHEMA, contracts.CL_SCHEMA):
        assert path.exists(), path
    assert contracts.CV_SCHEMA.parent.name == "cv-style-netherlands"
    assert contracts.CL_SCHEMA.parent.name == "cl-style-netherlands"
