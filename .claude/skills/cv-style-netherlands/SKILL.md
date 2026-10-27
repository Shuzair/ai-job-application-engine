---
name: cv-style-netherlands
description: "Netherlands CV style. Complete, self-contained CV writing
  rules for Netherlands job applications. Loaded by the cv-agent for every
  application."
user-invocable: false
---

# Netherlands CV Style

This style covers CV writing rules for Netherlands job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

**One CV for every application.** This CV is the master CV: built once from candidate.md and sent unchanged with every Netherlands application. It is never tailored to one posting. Per-job tailoring lives in the cover letter. So write for the candidate's target roles, never for a single company or job ad: no company names you are applying to, no "this role", no terms that only one posting uses.

---

## Pre-work: Build the Target Profile

Before writing anything, build a **Target Profile** from candidate.md:

- **Target roles**: candidate.md → Target → Roles, in the order listed. The first is the lead role; the summary and header titles lead with it.
- **Core stack**: the technologies the candidate has used most, most recently, and in production. Recurrence across roles and depth of evidence beat a single mention.
- **Signature results**: the 5–8 strongest quantified achievements in candidate.md (scale, cost, latency, accuracy, time saved).
- **Domains**: the problem areas the candidate has real depth in (e.g. data pipelines, web scraping at scale, data quality, LLMs in production).

From it, build a **Target Signal List**: a ranked list of 10–15 skills, tools and responsibilities that Dutch postings for the target roles commonly ask for **and** that the candidate has hands-on evidence for. Reference this list throughout content generation. It replaces any single job description.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section.

### Skills — Evidence-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Keep**: skills that serve at least one target role and that the candidate has used hands-on (production work, a shipped project, or a certification). Reference your Target Signal List.
3. **Discard**: skills used once or trivially, and tools that no target role cares about. Breadth across the three roles is fine; padding is not.
4. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty, omit it entirely

### Certifications — Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Keep certifications that support a target role — map each to a named Target Signal List item. If you cannot, discard it.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by how strongly it shows the target roles' core work. Prioritize: quantified results, ownership, production scale, core-stack technologies
3. **Shape**: Write bullets in the standard industry terms recruiters and ATS filters search for (e.g. "data pipelines", "ETL/ELT", "data modelling", "data quality"), not internal project names
4. **Prioritize**: Place the strongest bullets first within each role. Cut the weakest when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-Target Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write a summary that positions the candidate for the lead target role while staying true for the others
3. **Quantify**: Include the single most impressive metric from candidate.md
4. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

The rendered order is set by `cv-format.yaml`: summary, experience, projects, education, skills, certifications, languages, interests. Generate the data for each section below.

### 1. Header

Include: full name, target role titles (lead role first), city (not full address), email, phone, LinkedIn URL, GitHub.

Add one line about relocation readiness if applying from outside the Netherlands.

**Dutch-specific header rules:**
- **Photo**: None. A photo is optional in the Netherlands and usually omitted for tech and international employers.
- **Date of birth**: Omit. Dutch law (WGBLA) prohibits age discrimination; modern guidance consistently says to omit.
- **Nationality, visa, sponsorship, work permit**: Omit. Follow the Visa Note in candidate.md — relocation readiness may be stated, work authorisation is discussed at interview.
- **Marital status**: Never include. Dutch law (AWGB) and all major Dutch career guides explicitly say to omit.
- **BSN (Burgerservicenummer)**: Never include. This sensitive national ID number is not provided until after a job offer; including it on a CV is contrary to Dutch privacy law.
- **Address**: City only (e.g., "Amsterdam, Netherlands"). Never include full street address.
- **LinkedIn**: Always include — LinkedIn is used by 69% of Dutch professionals for job searching and is considered a professional standard in the Netherlands.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-4 lines total:

1. **Who you are**: The lead target role. State years of experience and domain.
2. **What you do best**: Name 3-4 core-stack technologies or skills from the Target Signal List.
3. **Differentiator**: One quantified signature result.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Dutch tone for the summary**: Direct and factual. Avoid superlatives and marketing language. Dutch recruiters explicitly penalize over-selling and vague positivity. Use implied first person (no "I" at the start of sentences). State what you have done and what you bring — concisely.

- Good: "Data engineer with 6 years building real-time pipelines on AWS, reducing processing latency by 40%."
- Bad: "Passionate and highly motivated data professional with an exceptional track record of delivering cutting-edge solutions."

### 3. Skills

Follow the Skills data collection philosophy above (collect → keep → discard → distribute). Reference your Target Signal List to confirm each retained skill addresses a named signal.

Distribute surviving skills into up to 6 category buckets (omit empty buckets):

1. **Programming & Scripting** — languages (Python, SQL, Scala, Java, etc.)
2. **Cloud & Infrastructure** — cloud platforms (AWS, GCP, Azure, Kubernetes, Terraform, etc.)
3. **Data & Analytics** — data tools, warehouses, BI, ML frameworks (Spark, dbt, Snowflake, Airflow, etc.)
4. **DevOps & Tools** — CI/CD, monitoring, version control (Docker, GitHub Actions, Datadog, etc.)
5. **Databases** — relational and NoSQL databases (PostgreSQL, MongoDB, Redis, etc.)
6. **Core Competencies** — soft skills and methodologies (Agile/Scrum, Team Leadership, PRINCE2, etc.)

Note: English bucket names are standard for English-language CVs targeting Dutch employers. Dutch equivalents: "Technische Vaardigheden", "Competenties", "Soft Skills" (English loanterm fully adopted in NL).

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by target-role strength → shape with standard terms → prioritize).

**Date format**: Mon YYYY (e.g., "Jan 2022 – Mar 2024"). This is the standard Dutch CV date format. Use en-dash between dates.

**Bullet writing rules for Dutch CVs:**
- Max 18 words per bullet. Dutch preference for clarity and directness demands concise, factual bullets.
- Open with a strong past-tense action verb (built, reduced, migrated, designed, implemented, led, automated).
- Quantify wherever possible: percentages, numbers, time savings, scale. Dutch recruiters explicitly value quantified achievements.
- Use implied first person — write "Built a data pipeline" not "I built" and not "Responsible for building."
- Use the standard industry term for the work ("streaming pipelines", "data modelling"), not an internal name.
- No embellishment or superlatives. State the fact and the impact — nothing more.
- For combining multiple roles at the same company: list each title separately with its own date range and bullets. Do not merge roles into one entry.

**Bullets per role** (by position in the experience list; `validate_output.py` checks these against `cv-format.yaml` → `validation`):
- First (most recent) role: 4–5 bullets
- Second role: 3–4 bullets
- Third role and older: 2–3 bullets

**Good bullet example**: "Reduced ETL pipeline latency by 40% by migrating from batch processing to Apache Kafka streaming."

**Bad bullet example**: "Was responsible for significantly improving our team's data infrastructure in a very impactful way."

### 5. Education

**Dutch education system context:**
- WO (Wetenschappelijk Onderwijs) = Research university degree (equivalent to a UK/US university degree)
- HBO (Hoger Beroepsonderwijs) = University of Applied Sciences degree (professionally oriented; 240 ECTS)
- MBO = Vocational qualification (include only if no higher qualification exists)

**Format rules:**
- Include degree level and field, institution name, location, and year (YYYY or MM/YYYY – MM/YYYY).
- For Dutch degrees, you may note WO/HBO in parentheses after the degree name if applying internationally.
- **GPA**: Include ONLY if the Dutch score is 8.0+ (cum laude or near-cum laude). The Dutch grading scale is 1–10; a 7.5 is solid but not typically highlighted. Convert non-Dutch grades with a brief note if meaningful (e.g., "GPA 3.8/4.0" or "Cum Laude").
- For non-Dutch degrees targeting Dutch employers: mention Nuffic recognition or ECTS credits only if the degree origin is unfamiliar in the Netherlands.
- **High school (VWO/HAVO)**: Omit for experienced professionals (3+ years). Include only for recent graduates or entry-level roles where it fills a gap.
- **Thesis**: Include title only if it is directly relevant to a target role and demonstrates a concrete skill from the Target Signal List.

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only those supporting a target role — map each to a named Target Signal List item).

**Format**: Certification name · Issuing body · Month YYYY

**Certifications with high value in the Netherlands tech market:**
- Cloud: AWS (Associate/Professional), Google Cloud Professional, Azure (AZ-900, AZ-104, AZ-204)
- DevOps/Kubernetes: CKAD, CKA, CKS
- Project management: PRINCE2 (widely recognized in NL), Scrum Master, SAFe
- Enterprise architecture: TOGAF
- Cybersecurity: CISM, CISA (ISACA)
- Data: dbt Analytics Engineering, Databricks certifications

### 7. Languages

**Proficiency scale**: CEFR (A1–C2) is the standard in the Netherlands. Always include the CEFR level.

**Format**: Language · Level (e.g., Dutch · B2, English · C1 (IELTS 7.0))

**Dutch-specific guidance:**
- Always include Dutch if the candidate has any level (even A1/A2). Dutch employers value effort to learn the language, and many roles increasingly require at least conversational Dutch.
- English is a co-working language at most Dutch tech companies; C1/C2 is expected for Randstad/international roles.
- The Netherlands has one of the highest English proficiency rates in the world — native-level English is not a differentiator, but certifications (IELTS, TOEFL) can be included if they add credibility.

### 8. Projects (optional — include for tech roles)

Reference your Target Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. A technically impressive project that addresses no target role should be omitted.

The Dutch tech market (Tech-Careers.nl, Cresuma) explicitly values personal and side projects for tech roles. The Randstad tech ecosystem has a high density of international tech workers who share GitHub portfolios.

**Format per project** (`cv-data-schema.yaml` → `projects`):
- `name`, plus `url` if the project is public
- `description`: one line — what it is and the technology stack
- `bullets`: 1–2 — what you built and what it demonstrates

### 9. Interests (optional but recommended)

Include a brief interests section. Dutch employers explicitly value seeing the "whole person" and work-life balance is a core Dutch cultural value. A brief interests section signals cultural fit — not unprofessionalism.

Keep it to 3–5 items, inline (comma or dot separated). Gate lightly: omit only if space is critically tight.

- Good: "Distance running · Open-source contributions · Photography · Board games"
- Preferred types: team sports (show teamwork), creative activities (personality), community involvement (social values)
- Avoid: passive activities (watching TV, browsing Reddit)

---

## Critical Rules

- **Language**: Always English. English is standard for tech/Randstad/international roles, and the candidate does not speak Dutch (candidate.md → Languages).
- **Dutch directness**: Factual, precise, no embellishment. Over-selling is culturally off-putting to Dutch recruiters. State facts and impacts — never inflate.
- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. Dutch market uses Workday, SAP SuccessFactors, Greenhouse (multinationals) and Recruitee, Homerun, Bullhorn (Dutch-specific).
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **No per-job content**: nothing in the CV names or targets one employer or posting — that belongs in the cover letter.
- **Page limit**: Maximum 2 pages — `render.py` checks the exported PDF. Trim order if exceeding: oldest role bullets → interests → project context → bullet word count. Never cut certifications, education, or languages.
- **Anti-discrimination compliance**: Per Dutch AWGB and WGBLA legislation — never include marital status, religion, or BSN. Omit DOB and photo.
- **LinkedIn**: Always include the LinkedIn URL — it is a professional standard in the Netherlands and expected by Dutch recruiters.
- Use en-dash for date ranges (–), middle dot (·) for skill separators.
