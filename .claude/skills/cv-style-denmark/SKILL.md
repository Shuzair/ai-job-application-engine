---
name: cv-style-denmark
description: "Denmark CV style. Complete, self-contained CV writing
  rules for Denmark job applications. Loaded when style resolution
  matches denmark. This is a full style skill — not a partial override."
user-invocable: false
---

# Denmark CV Style

This style covers CV writing rules for Denmark job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

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

After extracting, compile a **JD Signal List**: a numbered list of the specific technologies, domains, and role characteristics the JD names. Label each `[MUST]` or `[NICE]`. Reference this list when filtering every section below — if an item from `candidate.md` cannot be mapped to a named signal, it does not belong in the CV.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Reference your JD Signal List. Keep skills that map to a named signal (exact or synonym). Do not include skills that are broadly data-relevant but absent from the JD Signal List.
3. **Expand**: If the JD names a technology the candidate lacks but they have a close analogue, include the analogue (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake). The analogue must still map to a named signal.
4. **Discard**: Remove all remaining skills that do not map to any named signal.
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely.

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Map to JD Signal List**: For each cert, name the specific signal from your JD Signal List it addresses. If you cannot name one, discard it.
3. **Anti-pattern**: Do not keep a cert because it involves a data technology or sounds impressive. It must address a technology, domain, or characteristic explicitly named in the JD Signal List.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Reference your JD Signal List. Rank each piece of experience by how directly it addresses a `[MUST]` signal first, then `[NICE]` signals. Experience that touches no named signal should be deprioritized and cut first when trimming for space.
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets.
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight.
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role. The summary should read as if this candidate is a natural fit for the job.
3. **Mirror**: Use the job title and key terms from your JD Signal List. If the JD says "Senior Data Engineer," the summary should echo that framing.
4. **Quantify**: Include the single most impressive metric from candidate.md that maps to a `[MUST]` signal in your JD Signal List.
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).

Add one line about relocation readiness if applying from a different country.

**Danish header requirements:**
- **Photo**: Include a professional headshot — culturally expected in Denmark (standard practice per The Local Denmark and Workindenmark.dk). Professional attire, natural smile, neutral background. Black and white acceptable. Include `photo_path` in cv-data.yaml.
- **Address**: Use Danish format: Street + Number, Postal code City (4-digit postal code), Denmark. E.g., `Vesterbrogade 42, 1620 København V, Denmark`. For international candidates without a Danish address, include current city and country with a relocation statement.
- **LinkedIn URL**: Required — 70% of large Danish companies use LinkedIn in recruitment and 58% actively check candidate profiles (Workindenmark.dk). Include as a full URL.
- **Date of birth**: Omit — per 2022 Danish anti-discrimination updates (Act on Prohibition of Differences of Treatment), DOB should not be required. Omitting is current best practice.
- **Nationality / marital status**: Omit for international-facing companies (Maersk, Novo Nordisk, Vestas, tech). Traditional Danish SMEs sometimes include it; omitting is always safe and legally compliant.
- **Relocation statement**: Include for international candidates — Danish employers explicitly value visible commitment to relocating (Workindenmark.dk). E.g., "Open to immediate relocation to Denmark."
- **Visa status**: Do NOT include visa or work permit requirements in the CV. Address in interviews only.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Danish tone for the summary:**
- Direct, factual, collaborative — Denmark's flat-hierarchy culture expects confidence without boasting.
- **Janteloven awareness**: Avoid language like "top performer," "exceptional talent," "best in class," "highly motivated," "passionate." These phrases actively harm Danish applications. Let quantified results speak instead.
- Use implied first person (no explicit "I" at the start of bullets). First-person sentences are acceptable in the narrative summary section.
- One quantified achievement that speaks directly to the role's core challenge.
- For international candidates: briefly signal relocation readiness in the final component.
- **Bad**: "I am a passionate, highly motivated data engineering expert with exceptional skills and a proven track record..."
- **Good**: "Data Engineer with 6 years building production pipelines at scale — led a platform migration that cut infrastructure costs by 30%. Open to relocation to Copenhagen."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Distribute surviving skills into up to 4 category buckets (omit empty buckets):

1. **Programming & Languages** (Python, SQL, Scala, Go, Bash, etc.)
2. **Cloud & Infrastructure** (AWS, GCP, Azure, Kubernetes, Terraform, Docker, etc.)
3. **Data Engineering & Analytics** (dbt, Spark, Airflow, Kafka, Snowflake, BigQuery, etc.)
4. **Tools & Methods** (Git, CI/CD, Agile/Scrum, GitHub Actions, etc.)

**Danish skills norms:**
- Soft skills are embedded in the profile summary — do NOT create a "Soft Skills" bucket.
- Proficiency ratings (beginner/intermediate/advanced) are not commonly used in Danish CVs — list skill names only.
- Separator: middle dot ( · ) preferred over pipe.
- 4 buckets maximum; fewer is fine if the JD doesn't require more.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format**: `Mon YYYY – Mon YYYY` (abbreviated 3-letter month + year). E.g., `Jan 2022 – Mar 2024`. Use "Present" for current roles. Use en-dash (–) for date ranges.

**Bullet rules**:
- Start every bullet with a strong action verb: Led, Built, Designed, Reduced, Implemented, Migrated, Automated, Delivered, Optimized, Architected, Streamlined.
- No explicit "I" at the start of bullets — implied first person throughout.
- Max 18 words per bullet. Concise and outcome-focused.
- Quantify wherever possible — use actual numbers from candidate.md (%, $, rows/sec, team size, etc.).
- Avoid adjective-heavy openers ("Successfully managed...", "Efficiently implemented..."). Go straight to the action.
- 4–5 bullets for recent roles (past 5 years), 2–3 for older roles.

**Tone**: Direct, collaborative. Denmark's flat-hierarchy culture values team framing alongside individual impact. Where authentic, frame results in terms of team/business outcomes — e.g., "Led cross-functional migration of X, cutting infrastructure costs by Y%" rather than purely "I achieved X alone."

**Company descriptions**: Include a one-line company descriptor for non-Danish or unfamiliar companies. Helps Danish employers contextualize the candidate's background. Omit for globally recognized companies (Google, Microsoft, Amazon). Format: one italicized line after company name, before bullets.

**JD keyword mirroring**: Use exact terminology from the JD. Per Jobindex.dk, tailoring CV language to the job ad is explicitly recommended. If the JD says "event-driven architecture," do not write "streaming systems."

**ATS guidance**: Large Danish employers (Novo Nordisk, Maersk, Vestas, Danske Bank, Ørsted) use ATS. Use plain text bullets, JD-matched keywords, avoid tables/graphics. Danish SMEs are less likely to use ATS but still value clarity.

### 5. Projects

Reference your JD Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. A technically impressive project that addresses no named JD signal should be omitted.

**Format**: Each project is a plain string in `projects` (array of strings). Use this inline format:

```
"**Project Name** (Tech, Stack): One or two sentences. Outcome or what it demonstrates."
```

**Rules**:
- Max 40 words per project entry — Danish CVs prize scannability over narrative
- Lead with the project name in bold, then tech stack in parentheses
- One sentence describing what was built; optionally a second sentence on a quantified outcome or what it proves
- No long prose, no bullet sub-lists, no buzzwords
- Include GitHub or demo URL as a trailing note only if the link is live and directly relevant
- List in order of JD relevance, not chronologically
- Side/personal projects are welcome in tech roles — include when they directly prove a skill the JD requires

**Example**:
```yaml
projects:
  - "**Metadata-Driven Pipeline** (Snowflake, Fivetran, Airflow): Self-service metric framework for C-level dashboards — reduced implementation from 1 hour of engineering to 5 minutes of config."
  - "**Cricket Analytics Platform** (PostgreSQL, dbt, Python): End-to-end dbt semantic layer over hierarchical cricket data with multi-schema warehouse and version-controlled SQL models."
```

### 6. Education

**Danish grading**: If grades are from Danish institutions, show both scales: `GPA: 10/12 (ECTS: B — Very good)`. Danish 7-point scale: 12=A (Excellent), 10=B (Very good), 7=C (Good), 4=D (Fair), 02=E (Adequate). For non-Danish degrees, include your country's scale (e.g., `GPA: 3.7/4.0`). Only include GPA if strong — equivalent to Danish 10 or 12 (ECTS A or B).

**Degree equivalence**:
- Kandidat (2 years, 120 ECTS) → Master's degree
- Bachelor (3 years, 180 ECTS) → Bachelor's degree
- Professionsbachelor → Professional Bachelor's (note: vocational, not equivalent to university bachelor's)
- Diplomuddannelse → Post-graduate Diploma

**Thesis**: Include thesis title if directly relevant to the target role. Format: `Thesis: [Title]` as a line below the degree.

**High school**: Omit for candidates with 5+ years of work experience and a university degree.

**Format**: Reverse chronological. Include: degree name, institution, location, dates, GPA if strong.

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest).

**Format**: `Certification Name — Issuer (Month YYYY)`. Include verification URL if available.

**Highly valued in Denmark**:
- Cloud: AWS (SAA, SAP, DAE), Azure (AZ-900 to AZ-305), GCP (ACE, PDE) — valued across all major Danish sectors
- Project management: PMP, PRINCE2 (Maersk, Novo Nordisk, government-aligned projects)
- Agile: PSM I/II, CSM — broadly valued across sectors
- Data: dbt certification, Databricks (DE Associate/Professional), Snowflake SnowPro
- Language: IELTS/TOEFL for non-native English speakers; Studieprøven or Danskprøve 3 for Danish competency

**Relevance gate**: Only include certifications relevant to the JD. Omit others even if prestigious.

### 7. Languages

**Scale**: CEFR (A1–C2) is the explicit standard in Denmark (per Jobakademiet, alphatrad.dk). Use CEFR levels for all languages.

**Format**: Language name followed by CEFR level, with score if available and impressive.
- Example: `Danish — A1 (Beginner, actively learning)`
- Example: `English — C2 (Native/Fluent)`
- Example: `English — C1 (IELTS 7.5)`

**When critical**: Danish employers value English fluency — it is the de facto working language at international Danish companies (Maersk, Novo Nordisk, Vestas). For non-native English speakers, include IELTS/TOEFL score alongside CEFR. If learning Danish, note it explicitly — it signals commitment to integrating in Denmark and is received positively.

**Separator**: Middle dot ( · ) between entries on the same line.

### 8. Interests

Include a brief 2–4 line interests section. Culturally valued in Denmark — employers care about who candidates are as people, consistent with the flat-hierarchy culture. Include relevant hobbies, sports, community involvement, or volunteer activities.

Keep factual and specific. Avoid generic filler ("reading," "music," "travel"). Good examples: team sports, open-source contributions, hackathons, professional communities, charity work.

### 9. References

End with a references section. Two options:
- List 1–2 professional references with name, title, company, and contact (always obtain consent first).
- Write "References available upon request" (`Anbefalinger kan fås ved nærmere henvendelse` in Danish).

The second option is safe and widely accepted. Only include actual references if the job posting requests them or if the candidate explicitly has strong references to offer.

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers for body content.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages. For pharma/life sciences roles (Novo Nordisk, LEO Pharma), 2 pages is standard and expected. Trim order if exceeding: oldest role bullets → weakest project → project context → bullet word count. Never cut certifications, education, or languages.
- Use en-dash (–) for date ranges, middle dot ( · ) for skill separators.
- **Janteloven**: Never use superlatives or boastful language. Let quantified facts speak. No "top," "best," "exceptional," "highly motivated," "passionate" without a factual basis immediately following.
- **Photo**: Denmark expects a professional headshot. Always include `photo_path` in cv-data.yaml.
- **LinkedIn**: Always include the full LinkedIn URL — it is treated as a live extension of the CV by Danish recruiters.
- **PDF submission**: Always deliver as PDF. This is the Danish standard to preserve layout.
- **Tailoring is non-negotiable**: Jobindex.dk explicitly states that generic CVs are discarded. Every CV must reflect the specific JD's language, priorities, and keywords.
- **Language**: If the job ad is in English, write the CV in English. If in Danish and the candidate does not speak Danish well, English is acceptable — per Copenhagen Post guidance, "an excellently written application in English will have a fair chance even if the job ad was in Danish."
- **"CV" is the correct term** in Denmark — not "Résumé" or "Curriculum Vitae."
- **Anti-discrimination compliance**: Do NOT include date of birth, religion, political affiliation, or marital status unless the candidate voluntarily chooses to include them.
