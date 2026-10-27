"""The JD keyword check must be profession-agnostic: its vocabulary comes from
the candidate's own documented skills, not a hardcoded tech-keyword list.
These tests use a non-technical (nurse) profile to prove that."""
import validate_output as vo

NURSE_CV = {
    "header": {"name": "Jane Doe"},
    "summary": "Registered nurse focused on patient care and triage.",
    "skills": [
        {"category": "Clinical", "items": ["Triage", "Phlebotomy", "Patient Care"]}
    ],
    "experience": [
        {
            "company": "City Hospital",
            "title": "Nurse",
            "bullets": ["Performed triage for 40+ patients daily."],
        }
    ],
}


def test_warns_for_skill_in_jd_but_not_surfaced():
    # Phlebotomy is a listed skill the JD asks for, but it never appears in the
    # summary/bullets -> should be flagged so the candidate surfaces it.
    jd = "We need a nurse skilled in triage and phlebotomy."
    warns = vo._check_jd_keywords(NURSE_CV, jd)
    assert any("phlebotomy" in w.lower() for w in warns)
    assert not any("triage" in w.lower() for w in warns)  # triage is in a bullet


def test_silent_when_skill_is_surfaced():
    jd = "We need a nurse skilled in triage."
    assert vo._check_jd_keywords(NURSE_CV, jd) == []


def test_no_jd_means_no_warnings():
    assert vo._check_jd_keywords(NURSE_CV, "") == []


def test_no_skills_means_no_warnings():
    assert vo._check_jd_keywords({"summary": "x"}, "anything") == []


def test_hardcoded_tech_keyword_list_is_gone():
    # The old domain-coupled TECH_KEYWORDS set must not exist anymore.
    assert not hasattr(vo, "TECH_KEYWORDS")


def test_word_boundary_no_substring_false_negative():
    # "sql" listed as a skill, JD says "sql", prose only mentions "mysql".
    # Substring matching would wrongly treat it as surfaced; word-boundary
    # matching correctly flags it.
    cv = {
        "skills": [{"category": "Data", "items": ["SQL"]}],
        "summary": "Worked with MySQL databases.",
        "experience": [],
    }
    warns = vo._check_jd_keywords(cv, "We need strong SQL skills.")
    assert any("sql" in w.lower() for w in warns)


def test_word_boundary_no_substring_false_positive():
    # Skill "Go" must not be considered "mentioned" just because the JD/prose
    # contain words like "category" or "ongoing".
    assert vo._mentions("go", "category ongoing goals") is False
    assert vo._mentions("go", "we use Go and python".lower()) is True


def test_mentions_handles_special_chars():
    assert vo._mentions("c++", "experience in c++ required") is True
    assert vo._mentions("ci/cd", "owns ci/cd pipelines") is True
    assert vo._mentions("sql", "mysql postgresql") is False


def _role(n_bullets):
    return {"company": "C", "title": "T", "bullets": ["Did a thing."] * n_bullets}


def _bullet_limits(*counts):
    cv = {"summary": "", "experience": [_role(n) for n in counts]}
    _, limits = vo._validate_cv(cv, str(vo.contracts.CV_SCHEMA))
    return [l for l in limits if "bullets (max" in l]


def test_bullet_limit_depends_on_role_position():
    assert _bullet_limits(5, 4, 3, 3) == []
    assert _bullet_limits(6, 4, 3) == ["[cv] T @ C: 6 bullets (max 5 for most recent role)"]
    assert _bullet_limits(5, 5, 3) == ["[cv] T @ C: 5 bullets (max 4 for previous role)"]
    assert _bullet_limits(5, 4, 4) == ["[cv] T @ C: 4 bullets (max 3 for older role)"]


# ── jd-keywords.yaml coverage ────────────────────────────────────────────────

import yaml

DE_CV = {
    "header": {"name": "Sam Doe", "email": "sam@example.com"},
    "summary": "Analytics engineer with 6 years building dbt models on Snowflake.",
    "skills": [
        {"category": "Programming", "items": ["SQL", "Python"]},
        {"category": "Data Warehousing & Databases", "items": ["Snowflake"]},
        {"category": "Pipelines & Orchestration", "items": ["dbt", "Airflow"]},
    ],
    "experience": [
        {
            "title": "Analytics Engineer", "company": "Acme",
            "date_start": "Jan 2022", "date_end": "Present",
            "bullets": ["Built 120 dbt models in SQL on Snowflake."],
        }
    ],
    "education": [{"degree": "BSc CS", "institution": "Uni"}],
}


def _kw(term, match="yes", priority="must", type_="tool", place=None, **extra):
    kw = {"term": term, "type": type_, "priority": priority, "rank": 1, "match": match}
    if match in ("yes", "analogue"):
        kw["evidence"] = "candidate.md"
    if place is not None:
        kw["place"] = place
    kw.update(extra)
    return kw


def _coverage(*keywords, cv=DE_CV):
    return vo._check_keyword_coverage(cv, {"keywords": list(keywords)})


def test_coverage_silent_when_musts_are_covered():
    errs, warns = _coverage(
        _kw("dbt", place=["summary", "skills", "experience"]),
        _kw("SQL", place=["skills", "experience"]),
    )
    assert errs == [] and warns == []


def test_coverage_warns_when_must_missing_from_prose():
    # Airflow is a listed skill but no bullet or summary shows it.
    _, warns = _coverage(_kw("Airflow", place=["skills", "experience"]))
    assert any("not shown" in w and "airflow" in w for w in warns)


def test_coverage_warns_when_must_missing_from_skills():
    _, warns = _coverage(_kw("Python", place=["skills"]),
                         _kw("Kafka", place=["skills", "experience"]))
    assert any("skills section" in w and "kafka" in w for w in warns)
    assert not any("python" in w for w in warns if "skills section" in w)


def test_coverage_warns_when_summary_placement_missed():
    _, warns = _coverage(_kw("SQL", place=["summary", "skills"]))
    assert any("summary lacks" in w and "sql" in w for w in warns)


def test_analogue_is_checked_by_the_candidates_term():
    # Posting asks for Redshift; the candidate's analogue Snowflake is shown.
    errs, warns = _coverage(_kw("Redshift", match="analogue", use_as="Snowflake",
                                place=["skills", "experience"]))
    assert errs == [] and warns == []


def test_gap_listed_as_skill_is_an_error():
    errs, _ = _coverage(_kw("Airflow", match="no"))
    assert errs and "airflow" in errs[0].lower()


def test_gap_not_listed_is_fine_and_nice_to_haves_are_not_required():
    errs, warns = _coverage(_kw("Looker", match="no"),
                            _kw("Kafka", priority="nice", place=["skills"]))
    assert errs == [] and warns == []


def test_free_text_types_are_not_matched_literally():
    errs, warns = _coverage(_kw("stakeholder management", type_="soft-skill",
                                place=["experience", "cover-letter"]))
    assert errs == [] and warns == []


def test_aliases_count_as_the_keyword():
    _, warns = _coverage(_kw("data build tool", aliases=["dbt"], place=["skills", "experience"]))
    assert warns == []


VALID_KEYWORDS = {
    "role": {"title": "Medior Analytics Engineer", "family": "analytics-engineer",
             "seniority": "medior", "posting_language": "English", "dutch_required": "no"},
    "keywords": [
        _kw("dbt", place=["summary", "skills", "experience"]),
        _kw("Redshift", match="analogue", use_as="Snowflake", place=["skills"]),
        _kw("Looker", match="no", priority="nice"),
    ],
}


def _write(folder, name, data):
    (folder / name).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def test_keywords_schema_accepts_valid_file(tmp_path):
    _write(tmp_path, "jd-keywords.yaml", VALID_KEYWORDS)
    result = vo.validate_output("keywords", str(tmp_path))
    assert result["valid"], result["errors"]


def test_keywords_schema_requires_evidence_and_use_as(tmp_path):
    bad = yaml.safe_load(yaml.safe_dump(VALID_KEYWORDS))
    del bad["keywords"][0]["evidence"]           # yes without evidence
    del bad["keywords"][1]["use_as"]             # analogue without use_as
    _write(tmp_path, "jd-keywords.yaml", bad)
    errors = vo.validate_output("keywords", str(tmp_path))["errors"]
    assert any("evidence" in e for e in errors)
    assert any("use_as" in e for e in errors)


def test_keywords_unquoted_yes_fails_schema(tmp_path):
    # Unquoted `match: yes` loads as a boolean — the skill says to quote it.
    (tmp_path / "jd-keywords.yaml").write_text(
        "role: {title: T, family: data-engineer, seniority: senior, posting_language: English}\n"
        "keywords:\n  - {term: SQL, type: tool, priority: must, rank: 1, match: yes, evidence: x}\n",
        encoding="utf-8",
    )
    assert not vo.validate_output("keywords", str(tmp_path))["valid"]


def test_keywords_type_requires_the_file(tmp_path):
    result = vo.validate_output("keywords", str(tmp_path))
    assert not result["valid"] and "not found" in result["errors"][0]


def test_cv_validation_uses_keyword_file_when_present(tmp_path):
    _write(tmp_path, "cv-data.yaml", DE_CV)
    kws = yaml.safe_load(yaml.safe_dump(VALID_KEYWORDS))
    kws["keywords"].append(_kw("Airflow", match="no"))
    _write(tmp_path, "jd-keywords.yaml", kws)
    result = vo.validate_output("cv", str(tmp_path))
    assert not result["valid"]
    assert any("airflow" in e.lower() for e in result["errors"])
