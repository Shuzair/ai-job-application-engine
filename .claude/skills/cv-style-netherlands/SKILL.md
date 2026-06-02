---
name: cv-style-netherlands
description: "Netherlands CV style. Complete, self-contained CV writing
  rules for Netherlands job applications. Loaded when style resolution
  matches netherlands. This is a full style skill — not a partial override."
user-invocable: false
---

# Netherlands CV Style

This style covers CV writing rules for Netherlands job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language**: is the posting in Dutch or English? Write the CV in the same language

Build a **JD Signal List** — a ranked list of the top 8–12 skills, tools, domain terms, and buzzwords from the posting. Reference this list throughout content generation.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD (exact or synonym match). Reference your JD Signal List.
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related or similar skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Keep ONLY certifications relevant to the job description — map each cert to a named signal from the JD Signal List. If you cannot map it to a signal, discard it.
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD Signal List. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role. The summary should read as if this candidate is a natural fit for the job
3. **Mirror**: Use the job title and key terms from the JD Signal List. If the JD says "Senior Data Engineer," the summary should echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order (for experienced professionals).

### 1. Header

Include: full name, city (not full address), email, phone, LinkedIn URL, GitHub (if relevant to the role).

Add one line about relocation readiness if applying from outside the Netherlands.

**Dutch-specific header rules:**
- **Photo**: Optional. If the application targets a traditional Dutch company (non-tech, non-startup), include a professional headshot (neutral background, business attire, top-right corner). For international tech companies and Randstad startups, omit unless requested. Never fabricate — only include if the candidate has provided a photo path.
- **Date of birth**: Omit. Dutch law (WGBLA) prohibits age discrimination; modern guidance consistently says to omit. If the candidate's profile includes it and they strongly prefer to include it, format as day-month-year (e.g., 15 April 1990).
- **Nationality**: Include. It is a standard personal information item in Dutch CVs and provides useful context, especially for international applicants.
- **Marital status**: Never include. Dutch law (AWGB) and all major Dutch career guides explicitly say to omit.
- **BSN (Burgerservicenummer)**: Never include. This sensitive national ID number is not provided until after a job offer; including it on a CV is contrary to Dutch privacy law.
- **Address**: City only (e.g., "Amsterdam, Netherlands"). Never include full street address.
- **LinkedIn**: Always include — LinkedIn is used by 69% of Dutch professionals for job searching and is considered a professional standard in the Netherlands.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-4 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-4 technologies or skills matching the JD's must-haves from the JD Signal List.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Dutch tone for the summary**: Direct and factual. Avoid superlatives and marketing language. Dutch recruiters explicitly penalize over-selling and vague positivity. Use implied first person (no "I" at the start of sentences). State what you have done and what you bring — concisely.

- Good: "Data engineer with 6 years building real-time pipelines on AWS, reducing processing latency by 40%."
- Bad: "Passionate and highly motivated data professional with an exceptional track record of delivering cutting-edge solutions."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute). Reference your JD Signal List to confirm each retained skill addresses a named signal.

Distribute surviving skills into up to 6 category buckets (omit empty buckets):

1. **Programming & Scripting** — languages (Python, SQL, Scala, Java, etc.)
2. **Cloud & Infrastructure** — cloud platforms (AWS, GCP, Azure, Kubernetes, Terraform, etc.)
3. **Data & Analytics** — data tools, warehouses, BI, ML frameworks (Spark, dbt, Snowflake, Airflow, etc.)
4. **DevOps & Tools** — CI/CD, monitoring, version control (Docker, GitHub Actions, Datadog, etc.)
5. **Databases** — relational and NoSQL databases (PostgreSQL, MongoDB, Redis, etc.)
6. **Core Competencies** — soft skills and methodologies (Agile/Scrum, Team Leadership, PRINCE2, etc.)

Note: English bucket names are standard for English-language CVs targeting Dutch employers. Dutch equivalents: "Technische Vaardigheden", "Competenties", "Soft Skills" (English loanterm fully adopted in NL).

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format**: Mon YYYY (e.g., "Jan 2022 – Mar 2024"). This is the standard Dutch CV date format. Use en-dash between dates.

**Bullet writing rules for Dutch CVs:**
- Max 18 words per bullet. Dutch preference for clarity and directness demands concise, factual bullets.
- Open with a strong past-tense action verb (built, reduced, migrated, designed, implemented, led, automated).
- Quantify wherever possible: percentages, numbers, time savings, scale. Dutch recruiters explicitly value quantified achievements.
- Use implied first person — write "Built a data pipeline" not "I built" and not "Responsible for building."
- Mirror JD Signal List terminology exactly. If the JD says "streaming pipelines," use that phrase.
- No embellishment or superlatives. State the fact and the impact — nothing more.
- For combining multiple roles at the same company: list each title separately with its own date range and bullets. Do not merge roles into one entry.

**Bullets per role:**
- Recent/current role: 4–5 bullets
- Previous role (2–5 years ago): 3–4 bullets
- Older roles (5+ years): 2–3 bullets

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
- **Thesis**: Include title only if it is directly relevant to the role and demonstrates a concrete skill from the JD Signal List.

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest — map each to a named JD Signal List item).

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

Reference your JD Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. A technically impressive project that addresses no named JD signal should be omitted.

The Dutch tech market (Tech-Careers.nl, Cresuma) explicitly values personal and side projects for tech roles. The Randstad tech ecosystem has a high density of international tech workers who share GitHub portfolios.

**Format per project:**
- Project name (with GitHub link if public)
- One-line description: what it is and the technology stack
- 1–2 bullet points: what you built and what it demonstrates

### 9. Interests (optional but recommended)

Include a brief interests section. Dutch employers explicitly value seeing the "whole person" and work-life balance is a core Dutch cultural value. A brief interests section signals cultural fit — not unprofessionalism.

Keep it to 3–5 items, inline (comma or dot separated). Gate lightly: omit only if space is critically tight.

- Good: "Distance running · Open-source contributions · Photography · Board games"
- Preferred types: team sports (show teamwork), creative activities (personality), community involvement (social values)
- Avoid: passive activities (watching TV, browsing Reddit)

---

## Critical Rules

- **Language match**: Write the CV in the same language as the job posting. English is standard for tech/Randstad/international roles. Dutch is expected for government, education, and traditional regional employers.
- **Dutch directness**: Factual, precise, no embellishment. Over-selling is culturally off-putting to Dutch recruiters. State facts and impacts — never inflate.
- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. Dutch market uses Workday, SAP SuccessFactors, Greenhouse (multinationals) and Recruitee, Homerun, Bullhorn (Dutch-specific).
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages (1 page for entry-level). Trim order if exceeding: oldest role bullets → interests → project context → bullet word count. Never cut certifications, education, or languages.
- **Anti-discrimination compliance**: Per Dutch AWGB and WGBLA legislation — never include marital status, religion, or BSN. Omit DOB by default. Photos are optional and the candidate decides.
- **LinkedIn**: Always include the LinkedIn URL — it is a professional standard in the Netherlands and expected by Dutch recruiters.
- Use en-dash for date ranges (–), middle dot (·) for skill separators.
