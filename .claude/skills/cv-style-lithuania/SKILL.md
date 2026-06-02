---
name: cv-style-lithuania
description: "Lithuania CV style. Complete, self-contained CV writing
  rules for Lithuania job applications. Loaded when style resolution
  matches lithuania. This is a full style skill — not a partial override."
user-invocable: false
---

# Lithuania CV Style

This style covers CV writing rules for Lithuania job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

**Language:** Write in English for international companies (fintech, IT, shared services — the dominant international employer categories in Lithuania). Write in Lithuanian only if the posting explicitly requires it or if applying to a local Lithuanian employer.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language requirements**: local language needed or English-only acceptable

Build a **JD Signal List**: a prioritized list of the top 8–12 skills, technologies, and domain terms from the job description. Reference this list throughout all sections below.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD Signal List (exact or synonym match)
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related or similar skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Map**: For each certification, identify whether it maps to a named signal from the JD Signal List — the technology, domain, or methodology must connect to what the role requires
3. **Discard**: Remove all certifications that don't map to a named JD signal. Do not include them just to fill space

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD Signal List. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role. The summary should read as if this candidate is a natural fit for the job
3. **Mirror**: Use the job title and key terms from the JD Signal List. If the JD says "Senior Data Engineer," the summary should echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, city + country of residence, email, phone (with country code), LinkedIn URL, GitHub (for tech roles).

**Nationality**: Include nationality — this is standard in Lithuanian CVs (per Lithuanian Employment Service and recruiter guidance). Example: "Pakistani — open to relocation."

**Photo**: Do NOT include a photo unless the job posting explicitly requests one. Photos are optional and conditional in Lithuania, not the default expectation.

**Date of birth**: Omit. Modern Lithuanian practice and the Law on Equal Treatment (2003) make this inappropriate in most contexts.

**Marital status**: Omit. Protected under Lithuania's Law on Equal Treatment.

**Address**: City and country only. Example: "Lahore, Pakistan" or "Vilnius, Lithuania." Full street address is not needed.

**Relocation**: Include one line about relocation readiness when applying from abroad. Example: "Open to relocation to Lithuania."

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves (from the JD Signal List).
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Tone**: Direct, concise, factual, and modest. Lithuanian employers value evidence-based claims over self-promotional language. Avoid superlatives ("best," "exceptional," "passionate"). Write in implied first person — no "I" in bullet points, but a professional summary in prose form is acceptable with "I." Keep metrics front-and-center.

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Reference your JD Signal List. Keep only skills that appear on it or that are clearly required by the role's domain.

Distribute surviving skills into up to 6 category buckets (omit empty buckets):

- **Data Engineering & Processing** — pipeline frameworks, workflow tools, streaming (e.g., PySpark, Airflow, dbt, Kafka, Fivetran)
- **Cloud & Infrastructure** — cloud providers, managed services, IaC (e.g., AWS, GCP, Azure, Lambda, Glue, Terraform)
- **Databases & Storage** — warehouses, databases, storage layers (e.g., Snowflake, PostgreSQL, DynamoDB, S3, Redshift)
- **Programming & Scripting** — languages and their libraries (e.g., Python, SQL, Scala, Bash)
- **Analytics & Visualization** — BI tools, dashboarding, reporting (e.g., Tableau, Looker, Power BI)
- **DevOps & Collaboration** — CI/CD, version control, monitoring, methodology tools (e.g., Git, Docker, Jira, Agile)

Separate items within each bucket using " · " (middle dot). Proficiency ratings are not standard in Lithuanian CVs — list skills without levels.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD Signal List relevance → shape with JD terminology → prioritize).

**Date format**: MM/YYYY (e.g., "09/2022 – Present"). Use en-dash between dates. This follows the Europass format widely adopted in Lithuania.

**Bullet rules**:
- Start every bullet with a strong action verb (past tense for ended roles, present tense for current role)
- Maximum 18 words per bullet
- 3–5 bullets for recent roles; 2–3 bullets for older roles
- Lead with quantified impact where available — Lithuanian recruiters respond to measurable results
- No personal pronouns in bullets (implied subject)
- Mirror the JD's technical vocabulary directly

**Good example**: "Reduced pipeline latency by 50% by migrating 12 batch jobs to Airflow-orchestrated streaming workflows."
**Bad example**: "I was responsible for working on improving our data pipeline performance using various tools."

**Company description**: One brief line is acceptable for context (especially if the company is not well-known internationally). Keep it to one fact — industry, scale, or product. Omit for well-known brands.

**Tone**: Pragmatic and evidence-driven. Lithuanian workplace culture values demonstrated competence and concrete delivery over enthusiasm. No self-promotional adjectives — let the metrics speak.

**Multiple roles at same company**: List as separate role blocks, most recent first.

### 5. Education

List in reverse chronological order. Include: degree name, institution, location, start year – end year.

**Grading**: Lithuania uses a 10-point scale (10 = Puikiai/Excellent). Include GPA only if it is strong (8.0+/10.0 or equivalent) and if you graduated within the last 5 years. For older degrees or where the system may not translate clearly, omit GPA or add a brief context note.

**High school**: Omit once any university degree exists. The Brandos atestatas is not listed on professional CVs.

**Thesis**: Include only if directly relevant to the target role.

### 6. Certifications

Follow the Certifications data collection philosophy above (map each cert to a named JD signal — discard if you can't).

**Format**: Certification name | Issuing body | Month YYYY

**High-value certifications in Lithuania's IT/fintech market** (include if in candidate.md and JD-relevant):
- Cloud: AWS (any level), Google Cloud, Azure certifications
- Data: Databricks certifications (highly valued in data engineering roles)
- Finance/Compliance: ACCA, CFA (valued in Lithuania's 265+ licensed fintech sector)
- Project Management: PRINCE2 (common in European/UK-affiliated firms in Lithuania), PMP
- IT Service: ITIL (relevant for BPO/shared services roles)

### 7. Languages

List using CEFR scale (A1–C2), which is the EU standard and explicitly used in Lithuania. Format each as: Language — Level (CEFR), e.g., "English — C1 (IELTS 7.0)."

Lithuanian language proficiency at any level is valued and should be noted — it signals cultural integration. Even "A1 (beginner)" is worth including if accurate.

Multilingual skills are highly valued in Lithuania's international job market — 30% of job postings require multilingual candidates.

### 8. Interests

**Include this section.** Per the Lithuanian Employment Service official guidance, a CV must include hobbies/interests (Pomėgiai). This is more strongly expected than in most Western European markets — it is listed as a required component, not optional decoration.

List 3–5 interests that reflect intellectual curiosity, teamwork, or relevant technical hobbies. For a tech candidate, interests that connect to the profession (e.g., data analytics for personal projects, open-source contributions) are particularly effective.

Format: inline, comma-separated or middle-dot-separated keywords.

### 9. References

**Include a references line.** Per Lithuanian Employment Service guidance, the references section (Rekomendacijos) is expected. Either:
- List 1–2 professional references with name, title, company, and contact details, OR
- Write "References available upon request"

The second option is acceptable for international applications where sharing contacts upfront is uncomfortable.

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. Lithuanian fintech and international IT companies use ATS systems — keyword mirroring from the JD is essential.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages. 1 page for candidates with under 10 years experience. Trim order if exceeding: oldest role bullets → weakest project → project context → bullet word count. Never cut certifications, education, or languages.
- **Modesty principle**: Lithuanian employers respond to measured confidence backed by data, not superlatives or self-promotional claims. Quantify achievements instead of describing them with adjectives.
- **No discrimination data**: Do not include marital status, date of birth, or family planning information. Lithuania's Law on Equal Treatment (2003) prohibits employers from using this information — its inclusion creates unnecessary risk.
- **Photo**: Only include if the posting explicitly requests it.
- Use en-dash for date ranges, middle dot for skill separators.
- **CV is called "Gyvenimo aprašymas" in Lithuanian** — but "CV" is universally understood and appropriate for all international applications.
