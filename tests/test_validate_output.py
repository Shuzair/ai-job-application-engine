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
