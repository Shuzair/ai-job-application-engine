---
name: fit-verdict
description: "Decide how well the candidate fits a job before any CV or letter is written: strong, possible or weak, with strengths, gaps, blockers, seniority and a recommendation. Writes fit-verdict.yaml. Loaded by the fit-agent; /apply continues on its own only on strong, otherwise it asks the user."
user-invocable: false
---

# Fit Verdict

`fit-verdict.yaml` answers one question for the user: **is this job worth applying to?** It runs after the three mappings and before any writing. `/apply` continues on its own only when the verdict is `strong`; on `possible` or `weak` it stops and asks the user, who may still say go.

This file is for the user only. It may mention sponsorship and Dutch — nothing in it reaches the CV or cover letter.

---

## Step 1: The fixed facts (code)

```bash
python scripts/run.py scripts/fit_check.py <folder>
```

It returns the parts that must come out the same every time:

| Field | Meaning |
|---|---|
| `ceiling` | The best verdict the numbers allow. **Your verdict may be lower, never higher.** |
| `must_coverage` | 0–1: how much of the must-haves the candidate covers, weighted by evidence strength (shipped 1, built 0.8, tooling/certified 0.4, learning 0.2, planned 0.1; an analogue earns 70%) |
| `must_gaps`, `top_must_gaps` | Must-haves the candidate lacks; those among the top 5 ranks |
| `must_weak`, `top_must_weak` | Must-haves known only from tooling, a certificate, learning or a plan |
| `blockers` | Hard stops: Dutch required but not spoken; no sponsorship offered but needed. Copy them exactly. |
| `notes` | Things the user should check (e.g. sponsorship not mentioned) |

## Step 2: Your judgement

Read `jd-keywords.yaml`, the three mappings, `input.md` and `research.md`, and the experience dates in `candidate.md` (grep the `### Experience` headings — no need to read it all).

**Gaps — core or minor.** A gap is `core` when the posting puts it in the title or intro, among the top 5 musts, or it is the central skill of the role family (dbt and modelling for an analytics engineer; orchestration and pipelines for a data engineer). Everything else is `minor`. Include weak must-haves (`must_weak`) as gaps, with the strength in the note.

**Seniority.** Count the years of relevant data work from the experience dates (data, analytics and solutions roles that did data work). Dutch postings: medior ≈ 2–5 years, senior ≈ 5+ with ownership and mentoring. Compare with `role.seniority` and `years_required`:
- `fits`; `stretch` — one level up (e.g. medior candidate, senior post); `below` — clearly short; `above` — clearly overqualified.

**Lower the verdict** (never raise it) when:
- a `core` gap exists and the ceiling is `strong` → `possible`;
- seniority is `below`, or two levels away → one step down;
- the role is really something else than its title (mostly dashboards, mostly ML engineering, mostly on-call platform work) and the candidate's strengths do not fit that → one step down;
- research.md shows the job is not in the Netherlands → `weak`, and say so.

**Strengths** — 2–4, each in one line, from the strongest `profile-to-jd.yaml` highlights and the core keywords the candidate has shipped.

**Risks** — what an interviewer will probe: weak must-haves, analogues for named tools, a seniority stretch, a domain switch.

**Recommendation** — one or two sentences a person can act on: "Apply.", "Apply; expect dbt depth questions.", "Skip unless you can show Dutch at B1."

## Step 3: Write and check

Write `fit-verdict.yaml` in the application folder, matching `fit-verdict-schema.yaml`:

```yaml
verdict: possible
summary: "Strong on pipelines, SQL and modelling; dbt — a top must — only from tooling"
strengths:
  - point: "Production pipelines with standardised, config-driven ingestion"
    keywords: ["data pipelines", "standardise ingestion"]
  - point: "Data modelling on Snowflake and BigQuery, shipped"
    keywords: ["data modelling", "Snowflake", "BigQuery"]
gaps:
  - area: "dbt"
    severity: core
    note: "Rank 3 must; evidence is an agent that generates dbt models (tooling), no hand-built models"
blockers: []
seniority:
  posting: "medior, 3+ years"
  candidate_years: "5.5"
  assessment: fits
  note: "5+ years of data work; medior asks 3+"
risks:
  - "dbt depth: model design, tests, incremental models"
recommendation: "Apply; prepare to show dbt knowledge in the interview."
```

```bash
python scripts/run.py scripts/validate_output.py <folder> --type fit
```

It rejects a verdict above the ceiling and blockers that differ from `fit_check.py`'s. Fix and run again.

## Report

Return the verdict card in 5 lines: verdict and summary, the core gaps, the blockers, seniority, the recommendation.
