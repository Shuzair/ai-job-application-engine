---
name: cv-style-pakistan
description: "Pakistan CV style. Complete, self-contained CV writing
  rules for Pakistan job applications. Loaded when style resolution
  matches pakistan. This is a full style skill — not a partial override."
user-invocable: false
---

# Pakistan CV Style

This style covers CV writing rules for Pakistan job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language requirements**: local language needed or English-only acceptable
- **Sector**: corporate/multinational, IT/tech startup, government/public sector, NGO — sector determines how traditional or modern the CV format should lean

Build a **JD Signal List**: a flat list of the 10–15 most important technical skills, domain terms, and responsibilities extracted from the posting. All Skills, Certifications, Experience, and Projects filtering steps below reference this list.

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
2. **Filter**: Map each certification to a named signal from the JD Signal List. Keep ONLY certifications where the technology, domain, or methodology connects to what the role requires
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD Signal List. Prioritize: matching technologies, matching responsibilities, matching scale/domain
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

Generate these sections in this exact order.

### 1. Header

Include: full name, city and country (not full street address), email, phone, LinkedIn URL, GitHub (if relevant to the role).

**Pakistan-specific header rules (per pakjobbazar.com, resumeflex.com — Tier 2):**
- **Do NOT include**: full home address, CNIC number, father's name, religion, marital status, nationality, date of birth — these are traditional "biodata" fields discouraged for modern private-sector CVs
- **Photo**: Omit unless the job posting explicitly requests one. If required (some government or traditional sectors), use a passport-size professional headshot, formal attire, plain light blue or white background, placed top-right
- **City only**: "Lahore, Pakistan" or "Karachi, Pakistan" — not street/postal address
- **LinkedIn URL**: Include for corporate and tech roles. LinkedIn profile is considered important alongside the CV (professionalcv.pk)
- **Government/traditional sector exception**: Father's name, CNIC, and date of birth may be required — include only when the job posting explicitly states this

Add one line about relocation readiness if applying to a role outside the candidate's current city.

### 2. Professional Summary

**For experienced professionals (3+ years):** Write a Professional Summary of 3–5 lines (40–90 words). Follow the Summary data collection philosophy above, then format as exactly 4 components:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3–5 technologies or skills matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**For fresh graduates (0–2 years experience):** Write a Career Objective of 2–3 lines (30–60 words). Focus on: field/specialization, 2–3 relevant skills, and the type of contribution the candidate aims to make. Avoid generic objectives ("seeking a challenging position") — be specific to the role and company.

**Tone:** Formal and professional throughout. Implied first person — bullets and phrases begin with action verbs or descriptors; never use "I" explicitly. Concise, specific, results-oriented. Avoid aggressive self-promotion; Pakistani hiring culture values substance over bravado. (Cultural Atlas, Tier 3; resumeflex.com, Tier 2)

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Distribute surviving skills into up to 6 category buckets (omit empty buckets). Use these bucket names appropriate for Pakistan's job market (adjust based on role):

- **Programming & Scripting** (Python, SQL, Java, etc.)
- **Cloud & Infrastructure** (AWS, Azure, GCP, Docker, Kubernetes)
- **Data & Analytics** (Spark, Kafka, dbt, Tableau, Power BI)
- **Databases** (PostgreSQL, MySQL, MongoDB, Snowflake, Redshift)
- **Tools & Platforms** (Git, Jira, CI/CD tools, etc.)
- **Core Competencies** (soft skills: leadership, communication, stakeholder management — include only if JD Signal List explicitly requires them)

For non-tech roles, replace with domain-appropriate buckets (e.g., "Financial Analysis", "Project Management", "ERP Systems"). Do NOT force a technical bucket structure onto a non-technical role.

Use middle dot separator (·) between items within a bucket. Do not add proficiency ratings (e.g., "Advanced") — list skills flat.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format:** Month YYYY – Month YYYY (e.g., "March 2021 – June 2023" or "January 2022 – Present"). Per pakjobbazar.com (Tier 2): do not use DD/MM/YYYY for employment date ranges.

**Bullet writing rules:**
- Begin each bullet with a strong past-tense action verb (Developed, Implemented, Led, Designed, Reduced, Increased, Delivered, Managed, Coordinated, Achieved)
- Maximum 18 words per bullet — keep bullets concise and specific
- Quantify wherever possible: percentages, volumes, team sizes, time saved, revenue impact
- Good: "Reduced monthly reporting time by 40% by automating ETL pipeline with Apache Airflow"
- Bad: "Was responsible for various reporting tasks and helped the team with different things"
- Implied first person — no "I" at start of bullets
- Formal, professional tone. Balance achievement-focus with respectful framing; avoid boastful language

**Bullets per role:**
- Recent role (current/last): up to 5 bullets
- Roles 2–3 years old: 3–4 bullets
- Older roles (4+ years ago): 2–3 bullets

**Company description:** Include a one-line factual descriptor (industry, scale, notable clients or products). This helps ATS and recruiters with unfamiliar company names.

**Multiple roles at same company:** List the company once, then show each title as a sub-entry with its own date range and bullets.

### 5. Education

List in reverse chronological order (most recent first).

**Pakistan-specific rules:**

- **Degree name**: Use full formal name (e.g., "BS (Hons) Computer Science", "MBA", "BBA (Hons)")
- **4-year BS (Hons)**: Equivalent to MA/MSc per HEC — list it as such if applying to international-facing roles
- **GPA / Percentage**: Include CGPA if 3.0 or above (out of 4.0). Include percentage if it represents First Division (60%+) or Distinction (75%+). Omit if weak. HEC scale: A = 4.0 (85%+), A- (70–84%), B (55–69%)
- **Matric/Intermediate (Grade 10/12)**: Omit for experienced professionals (3+ years). Include for fresh graduates and government applications
- **Thesis/Final Year Project**: Include the title if it is directly relevant to the JD Signal List; omit otherwise
- **Institution prestige**: LUMS, IBA Karachi, NUST, FAST, UET, and Aga Khan University are recognized by recruiters — include the full official name

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest).

**Format:** Certification Name | Issuing Body | Month Year

**Certifications that carry weight in Pakistan's job market:**
- Cloud: AWS (SAA, SAP, DA), Google Cloud (ACE, PCA), Microsoft Azure (AZ-900, DP-900)
- Data: Databricks, Snowflake, dbt Certified, Tableau Desktop Specialist
- Project management: PMP, Prince2, Scrum (PSM, CSM)
- Finance: ACCA, CFA, CMA, ICMA Pakistan
- IT Security: CISSP, CEH, CompTIA Security+

Include the verification URL if available.

### 7. Languages

List languages with proficiency level. Pakistan context:
- **Urdu**: Native for most Pakistani candidates — state "Native" or "Mother tongue"
- **English**: Critical for private sector. Use descriptors: Native, Fluent (C1–C2), Professional Working Proficiency (B2), Conversational (B1), Basic (A1–A2). Include IELTS/TOEFL score if available and above band 7.0 / score 100
- **Other languages** (Arabic, Chinese, etc.): Include if relevant to the role or company
- CEFR levels (A1–C2) are understood at multinationals but are not the domestic standard — using "Fluent / Professional / Conversational / Basic" descriptors is equally acceptable in Pakistan

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. ATS adoption is growing in corporate/tech sectors (hrbs.com.pk — Tier 2).
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages for experienced professionals. 1 page for fresh graduates (0–2 years). Trim order: oldest role bullets → weakest bullet → company description → bullet word count. Never cut certifications, education, or languages sections.
- **Language**: English throughout for private sector, multinationals, and tech. Do not switch to Urdu.
- **JD Signal List**: All filtering decisions (skills, certifications, experience bullets, projects) must reference the JD Signal List built in Pre-work. Do not include any item that cannot be mapped to a named signal.
- **Modern vs traditional sectors**: For government, public sector, or traditional industries, include father's name, CNIC, DOB, and photo if the job posting requires or implies this. For private sector and multinationals, these are omitted by default.
- **"Sifarish" awareness**: Personal references and networking carry significant cultural weight in Pakistan's job market. If a reference section is requested by the employer, add "References available upon request" — never list named references inline on the CV itself unless explicitly required.
- Use en-dash (–) for date ranges, middle dot (·) for skill separators.
- Do not title the document "CV" or "Curriculum Vitae" — per ilm.com.pk, the candidate's name is the document header.
