"""The master CV: built once, copied unchanged into every application folder."""
import os

import pytest

import master_cv
import render
from test_render import CV, CL, _folder


def _touch(path, t):
    os.utime(path, (t, t))


@pytest.fixture
def master(tmp_path):
    """A rendered master CV (docx only — no Word needed) plus a candidate.md."""
    mdir = tmp_path / "master-cv"
    mdir.mkdir()
    _folder(mdir)
    (mdir / "cl-data.yaml").unlink()
    render.render_folder(mdir, only="cv", pdf=False, open_docs=False)
    (mdir / "cv.pdf").write_bytes(b"%PDF-1.7 stand-in")
    candidate = tmp_path / "candidate.md"
    candidate.write_text("# Candidate Profile\n", encoding="utf-8")
    _touch(candidate, 1_000)
    _touch(mdir / "cv-data.yaml", 2_000)
    for name in ("cv.docx", "cv.pdf"):
        _touch(mdir / name, 3_000)
    return mdir, candidate


def test_status_of_missing_master(tmp_path):
    st = master_cv.status(tmp_path / "master-cv", tmp_path / "candidate.md")
    assert st["exists"] is False and st["rendered"] is False and st["stale"] is False


def test_status_rendered_and_current(master):
    mdir, candidate = master
    st = master_cv.status(mdir, candidate)
    assert st == {**st, "exists": True, "rendered": True, "stale": False}


def test_status_detects_unrendered_edit_and_override(master):
    mdir, candidate = master
    _touch(mdir / "cv-data.yaml", 4_000)
    assert master_cv.status(mdir, candidate)["rendered"] is False

    _touch(mdir / "cv-data.yaml", 2_000)
    (mdir / "cv-format-override.yaml").write_text("typography:\n  body_size: 9\n", encoding="utf-8")
    _touch(mdir / "cv-format-override.yaml", 4_000)
    assert master_cv.status(mdir, candidate)["rendered"] is False


def test_status_stale_when_candidate_changed(master):
    mdir, candidate = master
    _touch(candidate, 5_000)
    assert master_cv.status(mdir, candidate)["stale"] is True


def test_copy_puts_identical_cv_in_folder(master, tmp_path):
    mdir, _ = master
    app = tmp_path / "acme_data-engineer_v1"
    app.mkdir()
    copied = master_cv.copy_to(app, mdir)
    assert sorted(os.path.basename(p) for p in copied) == ["cv-data.yaml", "cv.docx", "cv.pdf"]
    for name in ("cv-data.yaml", "cv.docx", "cv.pdf"):
        assert (app / name).read_bytes() == (mdir / name).read_bytes()


def test_copy_carries_override_and_drops_a_stale_one(master, tmp_path):
    mdir, _ = master
    app = tmp_path / "app"
    app.mkdir()
    override = mdir / "cv-format-override.yaml"
    override.write_text("typography:\n  body_size: 9\n", encoding="utf-8")
    _touch(override, 2_000)
    master_cv.copy_to(app, mdir)
    assert (app / override.name).read_text(encoding="utf-8") == override.read_text(encoding="utf-8")

    override.unlink()
    master_cv.copy_to(app, mdir)
    assert not (app / override.name).exists()


def test_copy_refuses_missing_or_unrendered_master(master, tmp_path):
    mdir, _ = master
    app = tmp_path / "app"
    app.mkdir()
    with pytest.raises(RuntimeError, match="/cv"):
        master_cv.copy_to(app, tmp_path / "nowhere")
    _touch(mdir / "cv-data.yaml", 4_000)
    with pytest.raises(RuntimeError, match="Render it first"):
        master_cv.copy_to(app, mdir)
    assert not (app / "cv-data.yaml").exists()


def test_backup_keeps_previous_data(master):
    mdir, _ = master
    path = master_cv.backup(mdir)
    assert (mdir / "cv-data.previous.yaml").read_bytes() == (mdir / "cv-data.yaml").read_bytes()
    assert path.endswith("cv-data.previous.yaml")
    assert master_cv.backup(mdir.parent / "empty") == ""


def test_keyword_warning_clears_when_the_letter_mentions_the_skill(tmp_path):
    import copy as _copy
    import validate_output as vo

    folder = _folder(tmp_path)
    (folder / "input.md").write_text("# Role\nData Engineer\n\n# Job Description\nWe use Python and SQL.\n",
                                     encoding="utf-8")
    warns = vo.validate_output("cl", str(folder))["warnings"]
    assert any("python" in w for w in warns)

    cl = _copy.deepcopy(CL)
    cl["paragraphs"] = [cl["paragraphs"][0] + " I write Python and SQL daily."] + cl["paragraphs"][1:]
    _folder(tmp_path, cl=cl)
    assert vo.validate_output("cl", str(folder))["warnings"] == []
