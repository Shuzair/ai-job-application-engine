"""fit_check.py is the fixed part of the fit verdict: coverage, blockers and the
ceiling must come out the same every time, and the fit-agent may never go
above the ceiling."""
import yaml

import fit_check as fc
import validate_output as vo

CANDIDATE = (
    "# Candidate Profile\r\n"
    "**Visa Note:** Requires sponsorship — do NOT surface in CV or cover letter.\r\n"
    "## Experience\r\n### Experience 1: Data Engineer at Acme (Jan 2020 – Present)\r\n"
    "## Languages\r\n\r\n**English:** C1 · **Urdu:** Native\r\n"
)


def _kw(term, rank, priority="must", type_="tool"):
    return {"term": term, "type": type_, "priority": priority, "rank": rank}


def _map(term, match="yes", strength="shipped", **extra):
    m = {"keyword": term, "match": match}
    if match in ("yes", "analogue"):
        m.update(strength=strength, place=["experience"],
                 evidence=[{"where": "Experience 1", "quote": "Data Engineer at Acme"}])
    m.update(extra)
    return m


def _folder(tmp_path, keywords, mappings, role=None, candidate=CANDIDATE):
    folder = tmp_path / "app"
    folder.mkdir()
    role = {"title": "Analytics Engineer", "family": "analytics-engineer", "seniority": "medior",
            "posting_language": "English", "dutch_required": "no", **(role or {})}
    (folder / "jd-keywords.yaml").write_text(
        yaml.safe_dump({"role": role, "keywords": keywords}), encoding="utf-8")
    (folder / "jd-to-profile.yaml").write_text(
        yaml.safe_dump({"mappings": mappings}), encoding="utf-8")
    cand = tmp_path / "candidate.md"
    cand.write_text(candidate, encoding="utf-8")
    return folder, cand


TEN_MUSTS = [_kw(f"t{i}", i) for i in range(1, 11)]


def test_full_shipped_coverage_is_strong(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS])
    r = fc.check_fit(folder, cand)
    assert r["must_coverage"] == 1.0 and r["ceiling"] == "strong"


def test_credit_by_strength_and_analogue():
    assert fc._credit({"match": "yes", "strength": "built"}) == 0.8
    assert fc._credit({"match": "analogue", "strength": "shipped"}) == 0.7
    assert fc._credit({"match": "yes", "strength": "tooling"}) == 0.4
    assert fc._credit({"match": "no"}) == 0.0
    assert fc._credit({}) == 0.0


def test_top_ranked_gap_caps_at_possible(tmp_path):
    maps = [_map(k["term"]) for k in TEN_MUSTS]
    maps[1] = _map("t2", match="no")                       # rank 2 missing; coverage 0.9
    folder, cand = _folder(tmp_path, TEN_MUSTS, maps)
    r = fc.check_fit(folder, cand)
    assert r["top_must_gaps"] == ["t2"] and r["ceiling"] == "possible"


def test_top_ranked_weak_must_caps_at_possible(tmp_path):
    maps = [_map(k["term"]) for k in TEN_MUSTS]
    maps[2] = _map("t3", strength="tooling")               # like dbt known from tooling only
    folder, cand = _folder(tmp_path, TEN_MUSTS, maps)
    r = fc.check_fit(folder, cand)
    assert r["top_must_weak"] == ["t3"] and r["ceiling"] == "possible"


def test_low_ranked_gap_does_not_cap(tmp_path):
    maps = [_map(k["term"]) for k in TEN_MUSTS]
    maps[9] = _map("t10", match="no")                      # rank 10; coverage 0.9
    folder, cand = _folder(tmp_path, TEN_MUSTS, maps)
    assert fc.check_fit(folder, cand)["ceiling"] == "strong"


def test_low_coverage_is_weak(tmp_path):
    maps = [_map(k["term"], match="no") if i >= 5 else _map(k["term"])
            for i, k in enumerate(TEN_MUSTS)]               # coverage 0.5
    folder, cand = _folder(tmp_path, TEN_MUSTS, maps)
    assert fc.check_fit(folder, cand)["ceiling"] == "weak"


def test_nice_to_haves_do_not_count_toward_must_coverage(tmp_path):
    kws = TEN_MUSTS + [_kw("n1", 11, priority="nice")]
    maps = [_map(k["term"]) for k in TEN_MUSTS] + [_map("n1", match="no")]
    folder, cand = _folder(tmp_path, kws, maps)
    r = fc.check_fit(folder, cand)
    assert r["must_coverage"] == 1.0 and r["nice_coverage"] == 0.0 and r["ceiling"] == "strong"


def test_dutch_required_without_dutch_is_a_blocker(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS],
                           role={"dutch_required": "yes"})
    r = fc.check_fit(folder, cand)
    assert [b["code"] for b in r["blockers"]] == ["dutch-required"] and r["ceiling"] == "weak"


def test_dutch_in_languages_section_clears_the_blocker(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS],
                           role={"dutch_required": "yes"},
                           candidate=CANDIDATE + "**Dutch:** A2\r\n")
    assert fc.check_fit(folder, cand)["blockers"] == []


def test_dutch_mentioned_outside_languages_does_not_count():
    text = "## Experience\nWorked with Dutch clients.\n## Languages\n**English:** C1\n"
    assert fc.candidate_facts(text)["speaks_dutch"] is False


def test_dutch_as_a_plus_is_only_a_note(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS],
                           role={"dutch_required": "nice"})
    r = fc.check_fit(folder, cand)
    assert r["blockers"] == [] and any("Dutch is a plus" in n for n in r["notes"])


def test_no_sponsorship_offered_is_a_blocker_when_needed(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS],
                           role={"sponsorship": "not-offered"})
    r = fc.check_fit(folder, cand)
    assert [b["code"] for b in r["blockers"]] == ["no-sponsorship"]


def test_sponsorship_not_mentioned_is_a_note(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS])
    r = fc.check_fit(folder, cand)
    assert r["blockers"] == [] and any("IND" in n for n in r["notes"])


def test_candidate_facts_parse_visa_note():
    assert fc.candidate_facts(CANDIDATE)["needs_sponsorship"] is True
    assert fc.candidate_facts("**Visa Note:** EU citizen, no sponsorship needed.")["needs_sponsorship"] is False
    assert fc.candidate_facts("# nothing here")["needs_sponsorship"] is None


def test_missing_files_raise(tmp_path):
    try:
        fc.check_fit(tmp_path)
    except FileNotFoundError:
        return
    raise AssertionError("expected FileNotFoundError")


# ── validate_output.py --type fit ────────────────────────────────────────────

VERDICT = {
    "verdict": "possible",
    "summary": "Good match; one top must only from tooling",
    "strengths": [{"point": "Shipped pipelines", "keywords": ["t1"]}],
    "gaps": [{"area": "t3", "severity": "core", "note": "tooling only"}],
    "blockers": [],
    "seniority": {"posting": "medior", "candidate_years": "6", "assessment": "fits", "note": "ok"},
    "recommendation": "Apply.",
}


def _fit_folder(tmp_path, verdict, role=None):
    maps = [_map(k["term"]) for k in TEN_MUSTS]
    maps[2] = _map("t3", strength="tooling")               # ceiling: possible
    folder, cand = _folder(tmp_path, TEN_MUSTS, maps, role=role)
    (folder / "fit-verdict.yaml").write_text(yaml.safe_dump(verdict), encoding="utf-8")
    return vo.validate_output("fit", str(folder), candidate_path=str(cand))


def test_fit_verdict_within_ceiling_is_valid(tmp_path):
    result = _fit_folder(tmp_path, VERDICT)
    assert result["valid"], result["errors"]


def test_fit_verdict_above_ceiling_is_rejected(tmp_path):
    result = _fit_folder(tmp_path, {**VERDICT, "verdict": "strong"})
    assert any("above what fit_check.py allows" in e for e in result["errors"])


def test_fit_verdict_may_be_lower_than_ceiling(tmp_path):
    assert _fit_folder(tmp_path, {**VERDICT, "verdict": "weak"})["valid"]


def test_fit_verdict_missing_blocker_is_rejected(tmp_path):
    result = _fit_folder(tmp_path, {**VERDICT, "verdict": "weak"}, role={"dutch_required": "yes"})
    assert any("Blockers must be exactly" in e for e in result["errors"])


def test_fit_verdict_with_the_right_blocker_is_valid(tmp_path):
    verdict = {**VERDICT, "verdict": "weak",
               "blockers": [{"code": "dutch-required", "message": "Dutch required"}]}
    result = _fit_folder(tmp_path, verdict, role={"dutch_required": "yes"})
    assert result["valid"], result["errors"]


def test_fit_type_requires_the_file(tmp_path):
    folder, cand = _folder(tmp_path, TEN_MUSTS, [_map(k["term"]) for k in TEN_MUSTS])
    result = vo.validate_output("fit", str(folder), candidate_path=str(cand))
    assert any("not found" in e for e in result["errors"])
