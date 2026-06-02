---
name: cv-style-germany
description: "Germany CV style. Complete, self-contained CV writing
  rules for Germany job applications. Loaded when style resolution
  matches germany. This is a full style skill — not a partial override."
user-invocable: false
---

# Germany CV Style (Lebenslauf)

This style covers CV writing rules for Germany job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language requirement**: German or English posting — determines language of the Anschreiben

Compile a **JD Signal List**: the top 8–12 skills, tools, domains, and role keywords from the posting. Every section below references this list to gate content.

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
2. **Filter**: Keep ONLY certifications relevant to the job description — map each certification to a named signal from your JD Signal List. If you cannot map it, discard it.
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. Mirror the JD's technical vocabulary in the bullets. Reference your JD Signal List when choosing which achievements to include.
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight.
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role
3. **Mirror**: Use the job title and key terms from the JD. If the JD says "Senior Data Engineer," the summary should echo that framing.
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, current city and country, phone with international dialing code (+49 or current country code), professional email, LinkedIn URL, XING profile URL (relevant for German market, especially traditional sectors), GitHub (if relevant to the role).

**Personal data fields (Persönliche Daten) — German employers expect:**
- **Photo (Bewerbungsfoto)**: Include a professional headshot path in the `photo_path` field. ~82% of German recruiters still expect one. Placement is top-right corner. Requirements: neutral background, business attire, direct gaze, studio quality. Photo is legally optional under AGG but culturally expected — especially for traditional companies (automotive, finance, engineering). For Berlin startup/international roles, still common but slightly relaxed. Per Tier 2 research (gluckglobal.com, fintiba.com).
- **Date of birth (Geburtsdatum)**: Include in format `DD.MM.YYYY` (e.g., 15.03.1990). Also include place of birth (Geburtsort). Still expected by the majority of German employers despite AGG making it legally optional. Per Tier 2 research (novoresume.com, airesume.guru).
- **Nationality (Staatsangehörigkeit)**: Include. Important for non-EU applicants so recruiters can assess work permit status early.
- **Marital status**: Omit by default for tech and modern company applications. Include only if the company is highly traditional (automotive, civil service).
- **Full address**: Street, postal code, city is the German norm. For international applicants not yet in Germany: city + country + relocation statement.

Add a relocation statement on one line if applying from abroad: "Open to immediate relocation to Germany" or "Currently based in [City, Country] — available for relocation."

Do NOT include: visa status (address in cover letter), health information, religion, ethnicity, political affiliation. These are protected categories under AGG (Allgemeines Gleichbehandlungsgesetz).

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3–5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3–5 technologies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**German tone rules for the summary:**
- Formal and factual. No buzzwords: avoid "passionate," "driven," "results-oriented," "dynamic."
- Implied first person only — no "I" pronouns. Write "Senior Data Engineer with 7 years of experience," not "I am a Senior Data Engineer."
- Quantify concretely: "reduced pipeline latency by 40%" not "improved performance significantly."
- 40–90 words maximum. German recruiters value brevity and substance over narrative.
- Good example: "Senior Data Engineer with 8 years of experience in cloud-native data platforms (AWS, dbt, Snowflake). Built pipelines processing 2B+ events/day; reduced ingestion latency by 35%. Open to immediate relocation to Munich."
- Bad example: "I am a passionate and results-driven data professional who loves tackling complex challenges."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute). Reference your JD Signal List: include only skills that map to a named signal. Omit empty buckets.

Distribute surviving skills into up to 6 category buckets:

1. **Programmiersprachen & Scripting** (Programming Languages & Scripting) — e.g., Python, SQL, Scala, Java, Bash
2. **Datenbanken & Datenspeicher** (Databases & Data Storage) — e.g., PostgreSQL, Snowflake, BigQuery, Redshift, MongoDB
3. **Cloud & Infrastruktur** (Cloud & Infrastructure) — e.g., AWS, Azure, GCP, Terraform, Kubernetes, Docker
4. **Datenverarbeitung & Frameworks** (Data Processing & Frameworks) — e.g., dbt, Apache Spark, Airflow, Kafka, Pandas
5. **Tools & Methoden** (Tools & Methods) — e.g., Git, JIRA, Scrum, CI/CD, Grafana, Power BI
6. **Softskills** (Soft Skills) — use sparingly; only if concrete and credible; German employers are sceptical of generic claims

Separator: middle dot " · " between items. Do NOT use proficiency ratings, bar charts, or stars — they are not standard in German tech CVs and break ATS parsing.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format**: MM.YYYY — European format for date ranges (e.g., `03.2021 – 08.2025`). For current roles: `06.2023 – Present`. Use en-dash (–) for ranges, not hyphen (-). Per Tier 2 research (StepStone, fintiba.com).

**Bullet writing rules:**
- Start each bullet with a strong action verb: *Developed, Implemented, Optimized, Led, Designed, Reduced, Increased, Introduced, Automated, Coordinated, Built, Migrated, Deployed, Architected*
- Past tense for past roles; present tense for current role.
- Maximum 20 words per bullet. German preference: concrete, specific, results-first.
- Prioritize quantified achievements: "Reduced API latency by 40% through query optimization" over "Responsible for API optimization."
- Implied first person only. No "I" — bullets read as direct statements.
- Avoid narrative language: "was tasked with," "worked on," "helped to." Start with the action.
- Mirror exact JD keywords in the bullet phrasing where factually correct.

**Bullets per role:**
- Recent roles (last 5 years): 3–5 bullets
- Older roles (5+ years ago): 1–2 bullets

**Company description**: Include a one-line descriptor in parentheses for non-famous companies: "(FinTech startup, 200 employees, Berlin)" or "(Global automotive supplier, ~10,000 employees)." Omit for universally known companies (SAP, BMW, Siemens, Deutsche Bank, Bosch, Volkswagen).

### 5. Education

**Include Abitur (German high school equivalent)**: German employers expect the full education chain from Abitur (or equivalent) onward. List institution, city, year of completion, and final grade if 2.5 or better (1.0 scale).

**German grading system (1.0–5.0 scale):**
- 1.0–1.5: sehr gut (excellent)
- 1.6–2.5: gut (good)
- 2.6–3.5: befriedigend (satisfactory)
- 3.6–4.0: ausreichend (passing)
- Include grade only if 2.5 or better. Note: higher number = worse grade (opposite of percentage systems).

**Degree equivalence:**
- Diplom / Magister = Master-level qualification (pre-Bologna 5-year degree); list as Master-level
- Ausbildung = vocational training; highly respected in Germany; include if relevant
- International degrees: list as-is; German recruiters are familiar with Bologna-era Bachelor/Master

**Thesis**: Include Master/Diplom thesis title if relevant to the target role. Format: "Masterarbeit: [Title]" or "Thesis: [Title]" below the degree name. Bachelor thesis: include only if directly relevant to the role.

**High school**: Always include for German market — list institution, city, year, and qualification name (Abitur, IB, A-levels, etc.).

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest). Map each certification to a named signal from your JD Signal List; discard if you cannot.

**Highly valued certifications in the German job market:**
- Cloud: AWS Certified Solutions Architect / Developer / Data Engineer, Azure certifications, Google Cloud Professional Data Engineer
- Data: dbt Certified, Databricks certifications (Spark, ML)
- SAP: Any SAP module certification carries premium value in German enterprise (SAP HQ: Walldorf, Germany; SAP is ubiquitous in German corporate stack)
- DevOps/Infra: CKA/CKAD (Kubernetes), Terraform Associate, Docker Certified Associate
- Project management: PMP, PRINCE2, Scrum (PSM/CSM), SAFe
- IT Service: ITIL Foundation
- Security: ISO 27001, CISSP, CompTIA Security+
- Testing: ISTQB
- Language certifications: TestDaF, DSH, Goethe-Zertifikat (German), IELTS/TOEFL (English) — include if JD has language requirements

**Format**: Certification name, Issuer, Month Year (e.g., "AWS Certified Solutions Architect – Associate, Amazon Web Services, April 2026").

### 7. Languages

Use CEFR levels with German labels for clarity on German CVs:

| CEFR | German Label | Meaning |
|------|-------------|---------|
| Native | Muttersprache | Native speaker |
| C2 | Verhandlungssicher | Business/negotiation fluent |
| C1 | Fließend | Fluent |
| B2 | Gute Kenntnisse | Good working knowledge |
| B1/A2 | Grundkenntnisse | Basic knowledge |

**Format**: "German — Fließend (C1)" or "English — Muttersprache (Native)"

**Why this section matters**: German is required or strongly preferred for most non-Berlin/non-international roles. B2+ German is a strong positive signal even for English-posted roles. Always include official test results if available (TestDaF, Goethe, DSH for German; IELTS/TOEFL for English). Per Tier 2 research (StepStone, iamexpat.de).

### 8. Interests

Include 3–5 interests in a single inline line. German employers value the "whole person" (Persönlichkeit) and expect this section — it is a standard German CV element. Per Tier 2 research (gluckglobal.com, novoresume.com).

**Good interests for German CVs**: Active hobbies (running, cycling, swimming, hiking, climbing), music (instrument), volunteering (Ehrenamt), coaching, open source contributions, hackathons, language learning.

**Avoid**: "Travel" (too generic), "watching movies/TV," video games (perceived negatively in conservative sectors like automotive, finance, law).

For tech roles: include GitHub projects or open source contributions only if the project directly demonstrates a skill from your JD Signal List. A technically impressive project that maps to no named JD signal should be omitted.

---

## Critical Rules

- **ATS compliance**: Standard characters only. Avoid tables, columns, graphics, skill rating bars, icons. These break German ATS parsing. German ATS (used at large companies) parse section headings — use standard headings.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages. Junior (<3 years experience): 1 page. Mid/senior: 2 pages. Trim order if exceeding: oldest role bullets → weakest interest → bullet word count → project context. Never cut certifications, education, or languages.
- **Language**: English for English-posted/international roles. German for German-posted roles (if candidate's German is B2+). Berlin/startup: English broadly accepted.
- **DIN 5008**: German business correspondence standard. Key rules: left-aligned text (block format), no paragraph indentation, consistent spacing. The cv-format.yaml reflects DIN 5008 margin guidance (left 2.5cm, right 2.0cm). Per Tier 1 (DIN standard), Tier 2 (joblers.net, tutkit.com).
- **AGG compliance**: Do NOT include religion, political affiliation, union membership, health conditions, or ethnicity. Photo, DOB, and nationality are voluntarily included — culturally expected but legally optional.
- **Lebenslauf signature line**: Traditional German CVs close with city, date, and a handwritten/digital signature ("Frankfurt, 29.05.2026"). This is declining in digital submissions — omit from YAML data.
- Use en-dash for date ranges, middle dot for skill separators.
- **No "Ich" as first word** anywhere in the document. German professional writing convention.
