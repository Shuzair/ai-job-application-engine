---
name: cv-style-netherlands
description: "Netherlands CV style. Complete, self-contained CV writing
  rules for Netherlands job applications. Loaded by the cv-agent for every
  application."
user-invocable: false
---

# Netherlands CV Style

Rules for writing the CV of an international data / analytics engineer (5–6 years' experience) applying to jobs in the Netherlands.

The layout is fixed: `scripts/nl_template.py` renders every CV the same way — A4, Calibri 11 pt, one column, no photo, no tables or graphics, fixed section order and skill categories. You write the text only; you never choose fonts, sizes, order or headings.

## The Dutch standard in one paragraph

Dutch recruiters expect a CV of **at most two A4 pages**, in **reverse-chronological** order, written in **short bullets** that are **direct, factual and quantified** — over-selling and vague self-praise count against you. CVs are usually screened by an applicant tracking system (ATS) and then skimmed in well under a minute, so the posting's own keywords must be visible, in the posting's own wording. English is accepted for international roles. Europass is not the Dutch norm; this format is.

## Your three inputs

| File | What it gives you |
|---|---|
| `jd-keywords.yaml` (application folder) | What the employer wants: the role's title, family (analytics / data engineer / hybrid) and seniority, and the ranked keywords — each with `match` (yes / analogue / no), the candidate's `use_as` term, `evidence` in candidate.md, and `place` (which sections use it). **This is your keyword list. Do not build your own.** |
| `candidate.md` | What the candidate has done. The only source of facts. |
| `research.md` | Context on the company, for the company-descriptor lines and framing. |

Two rules hold for every section:

1. **Every fact traces to candidate.md.** A keyword with `match: "no"` is a gap: never claim it, never list it as a skill (the validator rejects that). For `match: analogue`, write the candidate's own tool (`use_as`), never the posting's.
2. **Use the posting's exact words** for what the candidate has. If the posting says "data pipelines", write "data pipelines", not "ETL flows".

## Role emphasis

`role.family` in jd-keywords.yaml decides what leads. The layout does not change — only which skills, bullets and projects come first.

| | analytics-engineer | data-engineer | hybrid |
|---|---|---|---|
| Summary leads with | modelling, dbt, trusted metrics for the business | pipelines, platform, scale and reliability | both, in the posting's order |
| First skills in each category | dbt, SQL, dimensional modelling, BI tool, data quality tests | Python, orchestration, warehouse/lake, streaming, cloud, IaC | the posting's top-ranked |
| Bullets come first when they show | data models used by teams, metric definitions, self-service, stakeholder work, test coverage | pipelines built, volume/latency/cost numbers, reliability, migrations, automation | the top-ranked keywords |
| Projects to prefer | modelling, analytics, dashboards | ingestion, orchestration, infrastructure | either |

**Seniority** (`role.seniority`): Dutch postings say junior / medior / senior. With 5–6 years the candidate fits medior and senior.

- **senior / lead**: show ownership and influence — designed, led, set the standard, mentored, chose the architecture, worked across teams.
- **medior**: show solid independent delivery — built, shipped, improved, owned a component.
- Never put a seniority word in a title the candidate did not hold.

---

## Section by section

For each section: what to take from the posting (via jd-keywords.yaml), what to take from candidate.md, and how to write it.

### 1. Header

**From the posting:** `role.title`.
**From candidate.md:** name, city, email, phone, LinkedIn, GitHub, relocation readiness (Visa Note), the candidate's actual job titles.

**Write:**
- `titles`: 1–2 titles. The first is the posting's role name **without the seniority word** ("Analytics Engineer" for "Medior Analytics Engineer"), used only if the candidate's real roles support it. Add the candidate's own current title second if it differs ("Analytics Engineer · Data Engineer").
- `location`: city and country only.
- `linkedin`: always. `github`: if candidate.md has one and it shows relevant work.
- `relocation`: one line such as "Open to relocation to the Netherlands" when the candidate is abroad.

**Never include:** photo, date of birth or age, nationality, visa / sponsorship / work-permit status, marital status, religion, full street address, BSN (Dutch citizen service number). Dutch law forbids hiring decisions on age, religion, marital status or origin, and international tech employers do not expect these details; leaving them out costs nothing.

### 2. Summary

**From the posting:** `role.title`, `role.family`, `role.seniority`, and the keywords whose `place` includes `summary` (the top 3–4 musts).
**From candidate.md:** total years of relevant experience, the domains worked in, the single strongest metric that matches a top must, the Personal Narrative for framing.

**Write** 3–4 lines, **40–80 words**, implied first person (no "I"), in four parts:

1. **Who:** the posting's role name, years of experience, domain — "Analytics engineer with 6 years in e-commerce and fintech data".
2. **Core stack:** 3–4 of the top-ranked keywords the candidate has, in the posting's words (`use_as` for analogues).
3. **Proof:** one quantified result that backs the top must.
4. **Availability:** relocation readiness, if abroad.

- Good: "Analytics engineer with 6 years building dbt and SQL data models on Snowflake for finance and marketing teams. Cut monthly reporting time from 3 days to 4 hours by modelling a single revenue source of truth. Open to relocation to the Netherlands."
- Bad: "Passionate, results-driven data professional with a proven track record of delivering cutting-edge solutions."

No adjectives about the candidate (passionate, motivated, dynamic, results-driven, expert).

### 3. Technical skills

**From the posting:** every keyword of type `tool` or `skill` with `match` yes or analogue **whose `place` includes `skills`**, in rank order. When the keyword file leaves `skills` out of `place`, the evidence is too thin for a skills-list claim: show it in a bullet that says exactly what was done, and do not list it.
**From candidate.md:** the candidate's skills, to confirm each and to add a few closely related ones that support the role.

**Write:** sort into the six fixed categories — exact names, each at most once, empty ones left out. They render in this order whatever order you write them:

1. **Programming** — Python, SQL, PySpark, Bash
2. **Data Warehousing & Databases** — Snowflake, BigQuery, Databricks, PostgreSQL, DuckDB
3. **Pipelines & Orchestration** — Airflow, dbt, Fivetran, ETL/ELT, streaming
4. **Data Modelling & BI** — dimensional modelling, data quality, Tableau, Power BI, Looker
5. **Cloud & DevOps** — AWS, GCP, Azure, Docker, Terraform, GitHub Actions, CI/CD
6. **AI & LLMs** — LLM pipelines, Vertex AI, Claude, Gemini

- Within a category: the posting's must-haves first (by rank), then nice-to-haves, then supporting skills.
- Use the posting's spelling for what the candidate has ("Google BigQuery" if the posting writes it so).
- Analogue: list `use_as` (Snowflake), never the posting's term (Redshift).
- Gap (`match: "no"`): never listed.
- Supporting skills: only those candidate.md shows and the role plausibly uses; drop unrelated tools. Aim for about 20–30 items in total.
- Items are tool or technique names ("Airflow", "dimensional modelling"), not phrases or results ("Airflow DAG scheduling", "CLV segmentation"); those go in the bullets.
- No soft skills here — they go in the bullets.

### 4. Work experience

The main section. Reverse-chronological, every role from candidate.md that falls in the last ~10 years.

**From the posting:** keywords whose `place` includes `experience` — tools, skills, responsibilities, domains, soft skills — and their `evidence` pointers.
**From candidate.md:** for each role: title, company, dates, location, work model, what the company does, and every achievement with its numbers.

**Write per role:**
- Fields: `title`, `company`, `hq`, `location`, `work_model` (Remote / On-site / Hybrid), `company_description`, `date_start`, `date_end`.
- `company_description`: one factual line — what the company does and its scale ("Online grocery delivery platform, 2M customers in 5 countries"). Dutch recruiters rarely know employers abroad; this line tells them.
- Dates: `Mon YYYY` with an en-dash range in the rendering ("Jan 2022 – Present").
- Each title at the same company is its own entry with its own dates.

**Bullets:**
- Count by position: most recent role 4–5, previous role 3–4, every older role 2–3.
- Max 18 words each. Start with a past-tense action verb (present tense for a current role is also fine, but be consistent): built, designed, migrated, modelled, automated, reduced, led.
- Pattern: **action + what (in the posting's words) + tool + result with a number**. "Migrated 40 batch ETL jobs to Airflow on GCP, cutting pipeline failures by 60%."
- Order inside a role: bullets that prove the highest-ranked musts first.
- Coverage: every must-have the candidate has should be proven by at least one bullet somewhere — use the `evidence` pointer to find the achievement. Spread keywords naturally; a bullet carries one to three, never a list.
- Soft skills appear as achievements: "Ran weekly metric reviews with 4 business teams", not "Excellent communicator".
- Numbers only as candidate.md states them. No number in candidate.md → describe scope instead (teams served, sources integrated, models owned).
- Avoid: "responsible for", "helped with", "worked on", "various", "etc.", superlatives.

### 5. Projects (optional)

**From the posting:** keywords whose `place` includes `projects`, and musts the jobs do not prove well.
**From candidate.md:** side and open-source projects.

**Write** 0–2 projects, each: `name`, `url` if public, `description` (one line: what it is + stack), 1–2 bullets (what was built and what it shows). Include a project only if it proves a ranked keyword the experience section does not already prove. With 5–6 years of experience, the jobs carry the CV; projects support it.

### 6. Education

**From candidate.md:** degree, institution, location, years.

**Write:** degree with level and field ("BSc Computer Science"), institution, city and country, years. Leave out secondary school. Add a grade only if it is a distinction (cum laude, or 8.0+ on the Dutch 1–10 scale, or the home-country equivalent). Add the thesis title only if it proves a ranked keyword.

### 7. Certifications

**From the posting:** keywords whose `place` includes `certifications`; the cloud and tools the posting names.
**From candidate.md:** certifications with issuer, date and verification link.

**Write** only certifications that support a keyword in the posting — a cloud certification for the posting's cloud, a dbt or Databricks certification for those tools. Format: name, issuer, `Month YYYY`, `url` only if candidate.md gives one. Drop the rest; an unrelated certification is noise.

### 8. Languages

**From the posting:** `role.dutch_required`.
**From candidate.md:** languages and levels.

**Write** each language with a CEFR level (A1–C2) or "Native": "English · C1 (IELTS 7.0)". List Dutch whenever candidate.md shows any level, even A1 — Dutch employers value the effort. Never overstate a level, even when `dutch_required` is "yes"; the orchestrator tells the user about that gap.

### 9. Interests (optional)

**From candidate.md:** hobbies and activities.

**Write** 3–5 short items on one line, only from candidate.md. Prefer active ones (sport, making things, community work). Leave the section out first when space is tight.

---

## Fitting two pages

`render.py` checks the PDF. If over two pages, trim in this order: oldest role's bullets (to 2) → interests → projects → the weakest bullet in each role → bullet length. Never cut education, certifications that match the posting, languages, or a bullet that is the only proof of a must-have.

## Final check before writing the YAML

- Every must-have keyword with `match` yes or analogue appears in the skills section (tools/skills) **and** in at least one bullet or the summary — `validate_output.py` warns about any that do not.
- No gap keyword appears as a skill — `validate_output.py` rejects it.
- Every number and claim traces to candidate.md.
- No photo, date of birth, nationality, visa or sponsorship anywhere.
- Plain characters; en-dash (–) for date ranges.
