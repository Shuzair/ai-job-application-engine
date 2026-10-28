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


# ── jd-keywords.yaml + jd-to-profile.yaml ────────────────────────────────────

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

CANDIDATE = """# Candidate
## Experience
### Acme
- Built **120 dbt models** in SQL on Snowflake for finance \u2013 and marketing.
- Apache Airflow for pipeline orchestration (DAGs in Docker)
"""

RESEARCH = """# Company Research: Beta
Beta monitors industrial energy use per machine with wireless sensors.
"""


def _kw(term, match="yes", priority="must", type_="tool", place=None, strength="shipped", **extra):
    """One merged keyword: jd-keywords fields + jd-to-profile fields."""
    kw = {"term": term, "type": type_, "priority": priority, "rank": 1, "match": match}
    if match in ("yes", "analogue"):
        kw["strength"] = strength
    if place is not None:
        kw["place"] = place
    kw.update(extra)
    return kw


def _coverage(*keywords, cv=DE_CV):
    return vo._check_keyword_coverage(cv, list(keywords))


def test_coverage_silent_when_musts_are_covered():
    errs, warns = _coverage(
        _kw("dbt", place=["summary", "skills", "experience"]),
        _kw("SQL", place=["skills", "experience"]),
    )
    assert errs == [] and warns == []


def test_coverage_warns_when_must_missing_from_prose():
    _, warns = _coverage(_kw("Airflow", place=["skills", "experience"]))
    assert any("not shown" in w and "airflow" in w for w in warns)


def test_coverage_warns_when_must_missing_from_skills():
    _, warns = _coverage(_kw("Python", place=["skills"]),
                         _kw("Kafka", place=["skills", "experience"]))
    assert any("skills section" in w and "kafka" in w for w in warns)
    assert not any("python" in w for w in warns if "skills section" in w)


def test_skills_list_is_not_required_to_hold_practices():
    # A must-have practice ("skill" type) shown in a bullet need not be listed as
    # a skill — only tools are required in the skills list.
    cv = yaml.safe_load(yaml.safe_dump(DE_CV))
    cv["experience"][0]["bullets"].append("Added troubleshooting runbooks for every pipeline.")
    _, warns = _coverage(_kw("troubleshooting", type_="skill", place=["skills", "experience"]), cv=cv)
    assert warns == []


def test_coverage_warns_when_summary_placement_missed():
    _, warns = _coverage(_kw("SQL", place=["summary", "skills"]))
    assert any("summary lacks" in w and "sql" in w for w in warns)


def test_analogue_is_checked_by_the_candidates_term():
    errs, warns = _coverage(_kw("Redshift", match="analogue", use_as="Snowflake",
                                place=["skills", "experience"]))
    assert errs == [] and warns == []


def test_gap_listed_as_skill_is_an_error():
    errs, _ = _coverage(_kw("Airflow", match="no"))
    assert errs and "airflow" in errs[0].lower()


def test_weak_evidence_listed_as_skill_is_an_error():
    # dbt known only from tooling around it must not sit in the skills list.
    errs, _ = _coverage(_kw("dbt", strength="tooling", place=["experience"]))
    assert errs and "tooling" in errs[0]
    errs, _ = _coverage(_kw("dbt", strength="built", place=["skills", "experience"]))
    assert errs == []


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


def test_merge_joins_on_term():
    merged = vo._merge_keywords(
        {"keywords": [{"term": "dbt", "type": "tool", "priority": "must", "rank": 1}]},
        {"mappings": [{"keyword": "dbt", "match": "yes", "strength": "tooling"}]},
    )
    assert merged == [{"term": "dbt", "type": "tool", "priority": "must", "rank": 1,
                       "match": "yes", "strength": "tooling"}]


def test_quote_matching_ignores_formatting_but_not_words():
    src = vo._normalise(CANDIDATE)
    assert vo._quote_found("Built 120 dbt models in SQL on Snowflake", src)       # ** dropped
    assert vo._quote_found("for finance - and marketing", src)                   # en dash
    assert vo._quote_found("Built 120 dbt models ... DAGs in Docker", src)       # fragments
    assert not vo._quote_found("Built 150 dbt models in SQL", src)               # changed number
    assert not vo._quote_found("Built 120 dbt models ... in Kubernetes", src)    # bad fragment


KEYWORDS = {
    "role": {"title": "Medior Analytics Engineer", "family": "analytics-engineer",
             "seniority": "medior", "posting_language": "English", "dutch_required": "no"},
    "keywords": [
        {"term": "dbt", "type": "tool", "priority": "must", "rank": 1},
        {"term": "Prefect", "type": "tool", "priority": "must", "rank": 2},
        {"term": "Looker", "type": "tool", "priority": "nice", "rank": 3},
    ],
}

EV_DBT = [{"where": "Experience → Acme", "quote": "Built 120 dbt models in SQL on Snowflake"}]
EV_AIRFLOW = [{"where": "Experience → Acme", "quote": "Apache Airflow for pipeline orchestration"}]

JD_TO_PROFILE = {
    "mappings": [
        {"keyword": "dbt", "match": "yes", "strength": "shipped", "evidence": EV_DBT,
         "place": ["summary", "skills", "experience"]},
        {"keyword": "Prefect", "match": "analogue", "use_as": "Airflow", "strength": "shipped",
         "evidence": EV_AIRFLOW, "place": ["skills", "experience"]},
        {"keyword": "Looker", "match": "no"},
    ]
}

PROFILE_TO_JD = {
    "highlights": [
        {"rank": 1, "title": "dbt models", "strength": "shipped", "evidence": EV_DBT,
         "why": "The role models data in dbt", "keywords": ["dbt"], "use_in": ["experience"]},
    ],
    "leave_out": [{"item": "Cricket project", "reason": "Not relevant"}],
}

COMPANY_TO_PROFILE = {
    "research_available": True,
    "links": [
        {"company_fact": "Beta monitors energy per machine",
         "research_quote": "monitors industrial energy use per machine",
         "candidate_evidence": EV_AIRFLOW, "strength": "shipped",
         "connection": "Pipelines for machine data", "use_in": ["cover-letter"]},
    ],
}


def _copy(data):
    return yaml.safe_load(yaml.safe_dump(data))


def _write(folder, name, data):
    (folder / name).write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")


def _folder(tmp_path, **files):
    """An application folder with research.md and the given YAML files, plus a
    candidate.md next to it. Returns (folder, candidate_path)."""
    folder = tmp_path / "app"
    folder.mkdir()
    (folder / "research.md").write_text(RESEARCH, encoding="utf-8")
    candidate = tmp_path / "candidate.md"
    candidate.write_text(CANDIDATE, encoding="utf-8")
    for name, data in files.items():
        _write(folder, name, data)
    return folder, candidate


def _run(doc_type, folder, candidate):
    return vo.validate_output(doc_type, str(folder), candidate_path=str(candidate))


ALL_MAPPINGS = {
    "jd-keywords.yaml": KEYWORDS,
    "jd-to-profile.yaml": JD_TO_PROFILE,
    "profile-to-jd.yaml": PROFILE_TO_JD,
    "company-to-profile.yaml": COMPANY_TO_PROFILE,
}


def test_keywords_schema_accepts_valid_file(tmp_path):
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": KEYWORDS})
    result = _run("keywords", folder, cand)
    assert result["valid"], result["errors"]


def test_keywords_file_has_no_candidate_fields(tmp_path):
    # The keyword agent never reads candidate.md: match/evidence are not allowed.
    bad = _copy(KEYWORDS)
    bad["keywords"][0]["match"] = "yes"
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": bad})
    assert not _run("keywords", folder, cand)["valid"]


def test_keywords_duplicate_terms_rejected(tmp_path):
    bad = _copy(KEYWORDS)
    bad["keywords"].append(dict(bad["keywords"][0]))
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": bad})
    errors = _run("keywords", folder, cand)["errors"]
    assert any("more than once" in e for e in errors)


def test_keywords_type_requires_the_file(tmp_path):
    folder, cand = _folder(tmp_path)
    result = _run("keywords", folder, cand)
    assert not result["valid"] and "not found" in result["errors"][0]


def test_all_mappings_valid(tmp_path):
    folder, cand = _folder(tmp_path, **ALL_MAPPINGS)
    result = _run("mappings", folder, cand)
    assert result["valid"], result["errors"]


def test_each_mapper_validates_only_its_own_file(tmp_path):
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": KEYWORDS,
                                         "profile-to-jd.yaml": PROFILE_TO_JD})
    assert _run("profile-to-jd", folder, cand)["valid"]
    errors = _run("mappings", folder, cand)["errors"]
    assert any("jd-to-profile" in e and "not found" in e for e in errors)


def test_mapping_requires_evidence_strength_and_use_as(tmp_path):
    bad = _copy(JD_TO_PROFILE)
    del bad["mappings"][0]["evidence"]
    del bad["mappings"][1]["use_as"]
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": KEYWORDS, "jd-to-profile.yaml": bad})
    errors = _run("jd-to-profile", folder, cand)["errors"]
    assert any("evidence" in e for e in errors)
    assert any("use_as" in e for e in errors)


def test_mapping_must_cover_every_keyword_exactly(tmp_path):
    bad = _copy(JD_TO_PROFILE)
    bad["mappings"][2]["keyword"] = "looker"          # wrong case → unknown + missing
    folder, cand = _folder(tmp_path, **{"jd-keywords.yaml": KEYWORDS, "jd-to-profile.yaml": bad})
    errors = _run("jd-to-profile", folder, cand)["errors"]
    assert any("no mapping: Looker" in e for e in errors)
    assert any("not in jd-keywords.yaml" in e for e in errors)


def test_invented_candidate_quote_is_an_error(tmp_path):
    bad = _copy(PROFILE_TO_JD)
    bad["highlights"][0]["evidence"][0]["quote"] = "Built 500 dbt models in SQL on Snowflake"
    folder, cand = _folder(tmp_path, **{"profile-to-jd.yaml": bad})
    errors = _run("profile-to-jd", folder, cand)["errors"]
    assert any("quote not found in candidate file" in e for e in errors)


def test_invented_research_quote_is_an_error(tmp_path):
    bad = _copy(COMPANY_TO_PROFILE)
    bad["links"][0]["research_quote"] = "Beta is the market leader in Europe"
    folder, cand = _folder(tmp_path, **{"company-to-profile.yaml": bad})
    errors = _run("company-to-profile", folder, cand)["errors"]
    assert any("quote not found in research file" in e for e in errors)


def test_empty_company_links_are_valid(tmp_path):
    folder, cand = _folder(tmp_path, **{"company-to-profile.yaml":
                                        {"research_available": False, "links": []}})
    assert _run("company-to-profile", folder, cand)["valid"]


def test_missing_candidate_file_is_reported(tmp_path):
    folder, cand = _folder(tmp_path, **{"profile-to-jd.yaml": PROFILE_TO_JD})
    result = vo.validate_output("profile-to-jd", str(folder),
                                candidate_path=str(tmp_path / "missing.md"))
    assert any("candidate file not found" in e for e in result["errors"])


def test_cv_validation_uses_the_mapping(tmp_path):
    mapping = _copy(JD_TO_PROFILE)
    mapping["mappings"][2] = {"keyword": "Looker", "match": "no"}
    cv = _copy(DE_CV)
    cv["skills"][2]["items"].append("Looker")          # a gap listed as a skill
    folder, cand = _folder(tmp_path, **{"cv-data.yaml": cv, "jd-keywords.yaml": KEYWORDS,
                                         "jd-to-profile.yaml": mapping})
    result = _run("cv", folder, cand)
    assert not result["valid"]
    assert any("looker" in e.lower() for e in result["errors"])
