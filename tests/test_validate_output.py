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
