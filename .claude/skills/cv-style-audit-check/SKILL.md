---
name: cv-style-audit-check
description: "Audit Check CV style. Complete, self-contained CV writing
  rules for Audit Check job applications. Loaded when style resolution
  matches audit-check. This is a full style skill — not a partial override."
user-invocable: false
---

# Audit Check CV Style

This style covers CV writing rules for Audit Check job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

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
3. **Expand**: If the JD names a technology the candidate lacks but they have a close analogue, include the analogue. The analogue must still map to a named signal.
4. **Discard**: Remove all remaining skills that do not map to any named signal.
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Map to JD Signal List**: For each cert, name the specific signal from your JD Signal List it addresses. If you cannot name one, discard it.
3. **Anti-pattern**: Do not keep a cert because it involves a data technology or sounds impressive. It must address a technology, domain, or characteristic explicitly named in the JD Signal List.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Reference your JD Signal List. Rank each piece of experience by how directly it addresses a `[MUST]` signal first, then `[NICE]` signals. Experience that touches no named signal should be deprioritized and cut first when trimming for space.
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role. The summary should read as if this candidate is a natural fit for the job
3. **Mirror**: Use the job title and key terms from the JD. If the JD says "Senior Data Engineer," the summary should echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md that maps to a `[MUST]` signal in your JD Signal List.
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).

Add one line about relocation readiness if applying to a different country.

[CUSTOMIZE: specify which personal info fields are required/expected/discouraged for Audit Check — photo, DOB, nationality, marital status, address format]

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

[CUSTOMIZE: adjust tone — formal/direct/humble, pronoun usage, country-specific phrasing]

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Distribute surviving skills into up to 6 category buckets (omit empty buckets):

[CUSTOMIZE: define the bucket names for Audit Check job market — examples: "Programming & Scripting", "Cloud Platforms", "Databases", "Data Processing", "DevOps & Tools", "Soft Skills". Adjust to local job-market terminology, separator style, whether proficiency ratings are used. Maximum 6 buckets]

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

[CUSTOMIZE: specify date format, bullet writing rules, max words per bullet, max bullets per role (recent vs older), company description norms, tone for bullets, action verb preferences, rules for combining multiple roles at the same company]

### 5. Education

[CUSTOMIZE: specify local grading system, when to include GPA, degree equivalence guidance, whether to include thesis/coursework, high school inclusion rules]

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest).

[CUSTOMIZE: specify format, country-specific certifications that carry weight, date display format]

### 7. Languages

[CUSTOMIZE: specify proficiency scale (CEFR, JLPT, etc.), format (inline vs list), when this section is critical]

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages. Trim order if exceeding: oldest role bullets → weakest project → project context → bullet word count. Never cut certifications, education, or languages.
- Use en-dash for date ranges, middle dot for skill separators.

[CUSTOMIZE: add country-specific tone summary, cultural sensitivities, legal requirements]
