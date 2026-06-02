---
name: cv-style-usa
description: "Usa CV style. Complete, self-contained CV writing
  rules for Usa job applications. Loaded when style resolution
  matches usa. This is a full style skill — not a partial override."
user-invocable: false
---

# USA Resume Style

This style covers resume writing rules for USA job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

**Important:** In the US, this document is called a **resume** (not a CV) for all non-academic, non-research positions. The term "CV" is reserved for academic, medical, and research roles. Write as a resume.

Read `candidate.md` before writing any content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators (startup vs enterprise, agile vs structured)
- Whether the posting mentions relocation support or visa sponsorship
- **ATS signals**: exact phrases, acronyms, and technical terms used in the JD — mirror these precisely

Build a **JD Signal List**: a prioritized list of the top 8–12 skills, tools, and domain keywords from the JD. Every section decision (which skills to show, which bullets to write, which certifications to include) must be validated against this list.

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
2. **Filter**: Map each certification to a named signal in the JD Signal List. Keep ONLY certifications where the technology, domain, or methodology directly connects to what the role requires
3. **Discard**: Remove all certifications with no JD Signal List match. Do not include them just to fill space

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD Signal List. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using exact terminology and keywords from the JD Signal List. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules in the style section below

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

Include: full name, city and state (not full street address — privacy norm in US), email, phone, LinkedIn URL, GitHub (if relevant to the role).

**US legal requirements:** Do NOT include photo, date of birth, nationality, race, religion, marital status, gender, or disability status. These are protected class characteristics under Title VII, the ADEA, the ADA, and EEO laws — including them exposes the candidate to discrimination and is considered unprofessional.

**Work authorization:** Include "Authorized to work in the US without sponsorship" or "Requires visa sponsorship" only if relevant to the application. Many US employers use ATS filters on visa status, so clarity helps.

**Relocation:** Include a relocation statement (e.g., "Open to relocation to San Francisco, CA") if applying outside current location.

**Address format:** City and State only (e.g., "Austin, TX" or "Remote — Austin, TX"). Never include street address or ZIP code.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3–4 sentences total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3–4 technologies or skills matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Tone:** Direct, confident, first-person implied (no "I"). Results-oriented language. No buzzword padding ("seasoned," "dynamic," "thought leader"). Lead with impact, not job duties.

**Bad:** "Experienced engineer with a passion for technology and a proven track record."
**Good:** "Senior Data Engineer with 7 years building ELT pipelines and analytics platforms at Series B–D startups. Reduced data latency 60% at XYZ Inc by migrating to dbt + Snowflake. Available for immediate relocation."

### 3. Technical Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Reference your JD Signal List. Distribute surviving skills into up to 6 category buckets (omit empty buckets):

1. **Programming & Scripting** — Python, SQL, Java, Scala, Go, Bash, R
2. **Cloud Platforms** — AWS, GCP, Azure, and their managed services
3. **Data Engineering & Warehousing** — Spark, Kafka, Airflow, dbt, Snowflake, Redshift, BigQuery, Databricks
4. **Databases & Storage** — PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, DynamoDB
5. **DevOps & Infrastructure** — Docker, Kubernetes, Terraform, CI/CD, GitHub Actions, Jenkins
6. **Monitoring & Analytics** — Grafana, Datadog, Looker, Tableau, Power BI, Amplitude

**US norms:** Proficiency ratings (e.g., "Python (Advanced)") are NOT standard in US tech resumes — just list the skill. Recruiters assume proficiency; the bullets prove it. No soft skills bucket unless explicitly asked by the JD.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD Signal List relevance → shape with JD terminology → prioritize).

**Date format:** "Jan 2022 – Present" or "Jan 2022 – Mar 2024" (3-letter month + year). Never DD/MM/YYYY or any European format.

**Bullet writing rules:**
- Start every bullet with a strong past-tense action verb (current role: present tense). Examples: Built, Designed, Led, Reduced, Increased, Migrated, Automated, Implemented, Architected, Deployed, Optimized
- Structure: **Action verb + What you did + Quantified result/impact**. Example: "Reduced query latency by 40% by indexing 50M-row PostgreSQL tables and rewriting 12 slow analytical queries"
- Max 18 words per bullet. Aim for 13–16 words. Every word must earn its place
- Include dollar amounts, percentages, user counts, team sizes, time savings, scale metrics wherever possible — US employers expect quantification
- Use JD Signal List keywords naturally within bullets — exact phrase matching helps ATS parsing
- Past tense for previous roles; present tense for current role only
- No personal pronouns — never "I", "we", "our team"

**Bullets per role:**
- Current/most recent role: 4–5 bullets
- Roles 2–3: 3–4 bullets
- Older roles (>5 years ago): 2–3 bullets maximum

**Company description:** One concise line for companies not in the Fortune 500 / widely known. Format: "[Company] is a [stage] [industry] company [notable fact]." Omit for FAANG, big banks, or household names.

**Multiple roles at same company:** Group under one company block; list each title separately with its own dates and bullets.

### 5. Projects

Reference your JD Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. A technically impressive project that addresses no named JD signal should be omitted.

**US norms:** The US tech job market highly values demonstrable side projects, open source contributions, and portfolio work — especially for software engineering, data engineering, and ML roles. Include 1–3 projects that show technical depth.

Format each project as:
- **Project Name** — brief one-line description
- 1–2 bullets: what you built, what tech was used, what impact or insight it produced
- Include GitHub link or live URL if available

Omit this section entirely if no projects are relevant to the JD Signal List or if experience section is already dense.

### 6. Education

**GPA:** Include if 3.5 or higher AND graduated within the last 5 years. After 5+ years of work experience, omit GPA entirely — work history takes precedence.

**High school:** Omit entirely if you have a college/university degree.

**Degree format:** "Bachelor of Science in Computer Science" or "B.S., Computer Science" — spell out degree type or abbreviate consistently.

**Date:** Graduation year only, or "Expected May 2026" for in-progress degrees. No month needed for completed degrees.

**Coursework/thesis:** Only include if directly relevant to the role AND within the last 3 years.

**Foreign degrees:** Include the degree as-earned. Add "Equivalent to US Bachelor's in Computer Science" only if the institution is not internationally recognized.

### 7. Certifications

Follow the Certifications data collection philosophy above (keep only JD Signal List-relevant, discard the rest).

**High-value US certifications by domain:**
- Cloud: AWS Solutions Architect, AWS Data Engineer, GCP Professional Data Engineer, Azure DP-203, Azure AZ-900
- Data: dbt Certified Analytics Engineer, Databricks Certified Associate/Professional
- DevOps: CKA (Kubernetes), HashiCorp Terraform Associate, AWS DevOps Engineer
- Analytics: Google Analytics, Tableau Certified

**Format:** Certification Name | Issuing Body | Month Year (e.g., "AWS Certified Solutions Architect – Associate | Amazon Web Services | Mar 2024")

**Date:** Include. US employers value recency — certifications older than 3 years carry less weight unless still valid/renewed.

### 8. Languages

**Proficiency scale:** US does NOT use CEFR. Use: Native, Fluent, Professional Working Proficiency (C1 equivalent), Conversational (B1–B2), Basic (A1–A2).

**When to include:** Always include if the JD mentions language requirements or if the candidate speaks 2+ languages relevant to the role or company's markets.

**Format:** One line per language. Example: "Spanish — Professional Working Proficiency | English — Native"

**English:** If English is the candidate's native language, omit it from this section (assumed). If applying as a non-native English speaker, include "English — Fluent" or "English — Professional Working Proficiency."

---

## Critical Rules

- **ATS compliance**: US ATS adoption is the highest in the world (99%+ of Fortune 500 companies use ATS, per Jobscan). Use plain text bullets, standard section headings, no tables, no columns, no text boxes, no graphics. Never use Word headers/footers for contact info — put contact directly in the document body
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md
- **Page limit**: 1 page for candidates with <10 years experience; 2 pages for 10+ years. For senior tech candidates (Staff+, Principal, Director), 2 pages is standard. Never 3 pages for non-academic roles
- **No protected class info**: No photo, DOB, nationality, race, religion, gender, marital status, disability status — per EEO, Title VII, ADEA, ADA
- **Quantification imperative**: US hiring managers expect numbers. Every role should have at least 2 quantified bullets. No quantification = red flag
- **Action verbs**: All bullets start with strong action verbs. Never start with "Responsible for" or "Duties included"
- **Language**: English only. Spell-check for American English (color not colour, analyze not analyse)
- **File format**: Always provide as PDF unless instructed otherwise. Filename: "FirstName-LastName-Resume.pdf"
