"""Render a full Netherlands CV + cover letter to docx (no Word needed: no PDF,
no opening) and check what reaches the page, in the fixed layout."""
import copy

import pytest
import yaml
from docx import Document
from docx.oxml.ns import qn

import nl_template
import render
import validate_output as vo

CV = {
    "header": {
        "name": "Jan Jansen",
        "titles": ["Data Engineer"],
        "location": "Lahore, Pakistan",
        "email": "jan@example.com",
        "phone": "+31 6 12345678",
        "linkedin": "https://www.linkedin.com/in/jan/",
        "github": "https://github.com/jan",
        "relocation": "Open to relocation to the Netherlands",
    },
    "summary": " ".join(["Data engineer building batch and streaming pipelines on AWS."] * 6),
    "skills": [
        {"category": "Cloud & DevOps", "items": ["Docker", "AWS"]},
        {"category": "Programming", "items": ["Python", "SQL"]},
    ],
    "experience": [
        {
            "title": "Data Engineer", "company": "Acme", "location": "Remote",
            "work_model": "Remote", "date_start": "Jan 2024", "date_end": "Present",
            "bullets": ["Built a Kafka pipeline processing 2M events a day."],
        },
    ],
    "projects": [
        {
            "name": "Cricket Analytics Platform",
            "url": "https://github.com/jan/cricket",
            "description": "Ball-by-ball analytics on dbt and DuckDB",
            "bullets": ["Modelled 1M deliveries into a star schema.", "Served win-probability charts."],
        }
    ],
    "education": [{"degree": "BSc Computer Science", "institution": "FAST NUCES"}],
    "languages": [{"language": "English", "level": "C1 (IELTS 7.0)"}],
    "interests": ["Cricket", "Hiking", "Chess"],
}

CL = {
    "header": {"name": "Jan Jansen", "email": "jan@example.com"},
    "date": "27 October 2026",
    "salutation": "Dear Hiring Manager,",
    "paragraphs": [" ".join(["Concrete sentence about the role."] * 12)] * 4,
    "sign_off": {"closing": "Kind regards,", "name": "Jan Jansen"},
}


def _folder(tmp_path, cv=CV, cl=CL):
    (tmp_path / "cv-data.yaml").write_text(yaml.safe_dump(cv, allow_unicode=True), encoding="utf-8")
    (tmp_path / "cl-data.yaml").write_text(yaml.safe_dump(cl, allow_unicode=True), encoding="utf-8")
    return tmp_path


def _text(docx_path):
    doc = Document(str(docx_path))
    return "\n".join(
        "".join(n.text or "" for n in p._p.iter() if n.tag == qn("w:t"))
        for p in doc.paragraphs
    )


def test_renders_both_documents_with_projects(tmp_path):
    folder = _folder(tmp_path)
    result = render.render_folder(folder, pdf=False, open_docs=False)
    assert [d["kind"] for d in result["docs"]] == ["cv", "cl"]

    cv_text = _text(folder / "cv.docx")
    assert "PROJECTS" in cv_text
    assert "Cricket Analytics Platform" in cv_text
    assert "Modelled 1M deliveries into a star schema." in cv_text
    assert "github.com/jan/cricket" in cv_text
    assert "['" not in cv_text
    assert "Cricket · Hiking · Chess" in cv_text

    cl_text = _text(folder / "cover-letter.docx")
    assert "27 October 2026" in cl_text and "Kind regards," in cl_text


def test_schema_gate_blocks_fields_the_style_forbids(tmp_path):
    cv = copy.deepcopy(CV)
    cv["header"]["nationality"] = "Pakistani"
    folder = _folder(tmp_path, cv=cv)
    with pytest.raises(render.RenderError, match="nationality"):
        render.render_folder(folder, only="cv", pdf=False, open_docs=False)
    assert not (folder / "cv.docx").exists()


def test_cv_sections_and_skill_categories_follow_the_fixed_order(tmp_path):
    folder = _folder(tmp_path)
    render.render_folder(folder, only="cv", pdf=False, open_docs=False)
    text = _text(folder / "cv.docx")
    order = ["PROFESSIONAL SUMMARY", "TECHNICAL SKILLS", "PROFESSIONAL EXPERIENCE",
             "PROJECTS", "EDUCATION", "LANGUAGES", "INTERESTS"]
    assert [text.index(h) for h in order] == sorted(text.index(h) for h in order)
    # Programming comes first even though the data lists Cloud & DevOps first.
    assert text.index("Programming: Python · SQL") < text.index("Cloud & DevOps: Docker · AWS")


def test_schema_categories_match_the_template():
    schema = yaml.safe_load(render.contracts.CV_SCHEMA.read_text(encoding="utf-8"))
    enum = schema["properties"]["skills"]["items"]["properties"]["category"]["enum"]
    assert enum == nl_template.SKILL_CATEGORIES
    assert set(schema["properties"]) == {key for key, _ in nl_template.CV_SECTIONS} | {"header"}


@pytest.mark.parametrize("change, match", [
    (lambda cv: cv.update(volunteer_work=["Coached juniors"]), "volunteer_work"),
    (lambda cv: cv["skills"].append({"category": "Soft Skills", "items": ["Talking"]}), "Soft Skills"),
])
def test_schema_gate_blocks_anything_outside_the_fixed_format(tmp_path, change, match):
    cv = copy.deepcopy(CV)
    change(cv)
    folder = _folder(tmp_path, cv=cv)
    with pytest.raises(render.RenderError, match=match):
        render.render_folder(folder, only="cv", pdf=False, open_docs=False)


def test_validator_rejects_a_repeated_skill_category(tmp_path):
    cv = copy.deepcopy(CV)
    cv["skills"].append({"category": "Programming", "items": ["Bash"]})
    result = vo.validate_output("cv", str(_folder(tmp_path, cv=cv)))
    assert any("listed twice: Programming" in e for e in result["errors"])


def test_validator_reads_jd_and_passes_clean_data(tmp_path):
    folder = _folder(tmp_path)
    (folder / "input.md").write_text("# Role\nData Engineer\n\n# Job Description\nWe use Python and SQL.\n",
                                     encoding="utf-8")
    result = vo.validate_output("both", str(folder))
    assert result["valid"] is True, result
    assert result["errors"] == []
    assert any("python" in w and "sql" in w for w in result["warnings"])
