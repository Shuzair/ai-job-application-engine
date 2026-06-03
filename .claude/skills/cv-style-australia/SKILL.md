---
name: cv-style-australia
description: "Australia CV style. Complete, self-contained CV writing
  rules for Australia job applications. Loaded when style resolution
  matches australia. This is a full style skill — not a partial override."
user-invocable: false
---

# Australia CV Style

This style covers CV writing rules for Australia job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

Use **Australian English** throughout: organisation, colour, programme, labour, analyse, recognised, finalise, behaviour, centre. American spelling is a visible red flag to Australian recruiters.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Work rights signals**: whether citizenship or permanent residency is required
- **Industry context**: mining/resources, finance, tech, healthcare, government — each has distinct norms

Build a **JD Signal List**: top 8–12 keywords and technologies the JD emphasises most. Every section references this list for inclusion/exclusion decisions.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD Signal List (exact or synonym match)
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related or similar skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organise the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Map each certification to a named signal on the JD Signal List. If you cannot map it to a JD signal, discard it
3. **Prioritise**: Australian-specific compliance certifications (White Card, AHPRA, Working with Children Check, etc.) always go first if relevant

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyse**: Rank each piece of experience by relevance to the JD Signal List. Prioritise: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary
4. **Prioritise**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules in ### 4 below. Quantify every achievement where data exists

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesise**: Write an optimal summary that positions the candidate for THIS specific role
3. **Mirror**: Use the job title and key terms from the JD Signal List
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Format**: Follow the structure and tone rules in ### 2 below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location (Suburb, State only — e.g., "South Yarra, VIC"), email, phone, LinkedIn URL, GitHub (if the role is technical and candidate has one).

**Fields to include:**
- Location: Suburb and state abbreviation only. Do NOT include full street address (privacy standard). For candidates based overseas applying to Australia, include current city/country plus relocation intent.
- Work rights: Include a brief statement if the candidate is not an Australian citizen — e.g., "Australian Permanent Resident — full working rights" or "Subclass 482 TSS Visa — full working rights." Place this in the contact line or relocation field. This helps ATS systems that screen for work eligibility.
- Relocation: If applying to a different city or state, include a one-line statement: "Available to relocate to Sydney."

**Fields to EXCLUDE (legal and cultural norms):**
- Photo: Strongly discouraged. Anti-discrimination law makes appearance irrelevant to hiring decisions. Only include for roles where appearance is a genuine occupational requirement (acting, modelling).
- Date of birth: Do NOT include. The Age Discrimination Act 2004 (Cth) prohibits age-based discrimination.
- Nationality as demographic: Do NOT include "Nationality: Pakistani" or similar. Work rights statement is the appropriate substitute.
- Marital status, gender, religion: Do NOT include — prohibited under Sex Discrimination Act 1984 and Australian Human Rights Commission Act 1986.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as 3–5 lines, approximately 50–100 words:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3–5 technologies or capabilities matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role — the number does the talking.
4. **Availability** (if applicable): Work rights or relocation readiness.

**Tone:** Direct, professional, and evidence-led. Avoid superlatives ("world-class," "passionate," "dynamic") — these read poorly in the Australian market due to tall poppy syndrome. Confident but not boastful; let the quantified achievements carry the weight. Implied first person — do NOT write "I" in the summary.

**Good example:** "Senior Data Engineer with 7 years building real-time analytics pipelines across finance and e-commerce. Proficient in Python, Spark, and AWS. Reduced data latency by 60% at [Company], supporting 2M daily active users. Available to relocate to Melbourne."

**Bad example:** "Dynamic and results-driven world-class data professional with exceptional passion for transforming organisations through innovative data solutions."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Reference your JD Signal List. Only include skills that map to a named signal on that list.

Distribute surviving skills into up to 6 category buckets (omit empty buckets). Australian tech job market standard bucket names:

1. **Programming & Scripting** — languages (Python, SQL, Java, Go, etc.)
2. **Cloud & Infrastructure** — AWS, Azure, GCP, Kubernetes, Terraform, etc.
3. **Data & Analytics** — Spark, Kafka, dbt, Airflow, Tableau, etc.
4. **Databases & Storage** — PostgreSQL, Snowflake, Redshift, DynamoDB, etc.
5. **DevOps & Tooling** — Docker, CI/CD, Git, Jira, etc.
6. **Professional Skills** — Agile, Stakeholder Management, Technical Documentation, etc. (only if JD explicitly calls for these)

Adjust bucket names to match the role's domain — engineering, data, finance, healthcare etc. may use different groupings. Maximum 6 buckets. Omit soft-skills bucket if the JD does not signal them.

Separator between skills within a bucket: middle dot (·). No proficiency ratings — Australian market does not conventionally use self-rated proficiency scales in the skills section.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD Signal List → shape with JD terminology → prioritise).

**Date format:** Mon YYYY – Mon YYYY (e.g., "Mar 2021 – Nov 2023" or "Present"). Three-letter month abbreviation.

**Company description:** Include a one-line description for employers that are not major Australian or global brands. Example: "A $50M B2B SaaS startup providing supply chain analytics to retail clients." This is specifically recommended by Hays Australia for international candidates whose employers may be unfamiliar to local recruiters. Omit for well-known brands.

**Bullet writing rules:**
- Start every bullet with a strong past-tense action verb (current role: present tense)
- Formula: Action Verb + Task + Outcome/Metric
- Quantify every achievement where data exists: percentages, dollar amounts, headcount, time savings, volume
- Maximum 20 words per bullet — aim for 15
- Implied first person — no "I" or "He/She"
- No trailing periods (consistent within the document)
- Australian English spelling throughout

**Bullets per role:**
- Current or most recent role: up to 5 bullets
- Previous roles (1–5 years ago): 3–4 bullets
- Older roles (5+ years): 2–3 bullets, or summarise briefly

**Action verbs to favour:** Led, Delivered, Implemented, Developed, Designed, Reduced, Increased, Managed, Streamlined, Established, Coordinated, Drove, Built, Deployed, Optimised

**Tone:** Achievement-oriented, evidence-led, professionally direct. Less aggressive than US resumes. Let the numbers speak rather than adjectives. Balance between the UK's understated style and the US's promotional approach.

### 5. Education

List in reverse chronological order.

**Degree format:** Degree name, Major (if applicable), Institution, City (if not obvious), Country (mandatory for overseas institutions), Year graduated or expected.

**Australian grading system:**
- HD (High Distinction) = 85–100%
- D (Distinction) = 75–84%
- C (Credit) = 65–74%
- P (Pass) = 50–64%

**WAM / GPA:**
- Include WAM (Weighted Average Mark, a percentage) if ≥70% and graduated within 5 years
- Include GPA on a 7.0 scale if ≥5.5/7.0 and graduated within 5 years
- Drop once significant professional experience is established (5+ years)
- Label clearly: "WAM: 74.2" or "GPA: 6.1/7.0"

**Thesis:** Include title if directly relevant to the target role.

**High school / ATAR:** Omit once a university degree is held. Include ATAR only for school-leavers or very recent graduates where it is exceptionally high (90+).

**Overseas qualifications:** State the country for all non-Australian institutions. For regulated professions (medicine, engineering, teaching, nursing), note professional recognition status (e.g., "Engineers Australia assessment: Professional Engineer").

### 6. Certifications

Follow the Certifications data collection philosophy above (map each cert to a JD Signal List item — discard if no match).

**Australia-specific certifications of high value** (always include if relevant to the role):
- White Card (Construction Induction) — mandatory for all construction site work, lifelong
- AHPRA Registration — healthcare professionals; include registration number
- Blue Card / Working with Children Check — education, childcare, social services
- High Risk Work Licence — construction/mining (forklift, crane, rigging)
- First Aid Certificate — include expiry date
- Standard 11 — NSW mine safety
- CPA Australia / CA ANZ — accounting/finance
- Engineers Australia membership — engineering roles

**Format:** Certification name, Issuing body, Month YYYY (or expiry date if applicable).

### 7. Languages

Australia is a monolingual market. Include this section only when:
- The role explicitly requires another language
- The candidate is demonstrating English proficiency as a non-native speaker (e.g., IELTS 7.5)
- The employer services multilingual communities

**Proficiency scale:** IELTS band scores are the dominant standard in Australia for English proficiency (9-band scale). For other languages, CEFR levels are acceptable. Format: "English — Native" or "English — IELTS 7.5 (Full Professional Proficiency)."

If the candidate is a native English speaker applying to an English-only role, omit this section entirely.

### 8. Referees

Australia is distinctive in that a Referees section is a standard CV component, unlike most other English-speaking markets.

**Recommended approach:** "Referees available upon request." This is the current professional consensus (Hays Australia, Richard Lloyd Recruitment) — it protects referee privacy and maintains flexibility.

**When to list referees by name:** In academic, research, or government/public sector applications where the employer explicitly expects them on the CV. If listing: include full name, job title, company, phone, and email. Obtain permission before listing. Provide 2–3 referees (at least one professional/supervisory).

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers for content. Tables in decorative two-column skill layouts will fail ATS parsing — use plain text skills sections.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: 2 pages for private sector. Government/public sector: up to 4 pages. Trim order if exceeding: oldest role bullets → weakest bullet within a role → company descriptions of well-known brands → bullet word count. Never cut certifications, education, or languages.
- **Australian English**: Every word. Spellcheck for AU locale. "Organisation," not "organization." "Analyse," not "analyze."
- **Tall poppy syndrome**: The Australian cultural norm of not overselling. Quantified data is acceptable and respected; superlatives and self-descriptions ("world-class," "visionary," "guru") read as boastful. Stick to evidence.
- **Referees**: Default to "available upon request." Add names only for academic/government applications or when explicitly requested.
- **Work rights**: If the candidate is on a visa or has permanent residency, include a brief work rights note in the header. Many ATS systems pre-screen for work eligibility.
- **Formatting**: Use en-dash (–) for date ranges. Use middle dot (·) for skill separators. No trailing periods on bullets.
- **File naming**: Name the file FirstLast-Resume.pdf when saving (per Australian recruiter convention).
