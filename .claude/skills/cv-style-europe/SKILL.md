---
name: cv-style-europe
description: "Regional CV style: Europe. Complete, self-contained CV writing rules for European job applications (Germany, Netherlands, Belgium, Denmark, Sweden, and all EU countries). Loaded automatically when style resolution matches a European country and no country-specific style exists. This is a full style skill — not a partial override."
user-invocable: false
---

# European CV Style

This skill defines how to write CV content for European job applications. It covers section structure, writing rules, and regional norms. It does NOT cover visual formatting (fonts, spacing, layout) — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Cultural signals**: "flat hierarchy" = Nordic culture; "structured processes" = German orientation; "cross-functional" = stakeholder-facing
- **Must-haves vs nice-to-haves**: "required"/"essential"/"mandatory" are non-negotiable. "preferred"/"ideally"/"bonus" are nice-to-haves
- Whether the posting mentions "relocation support" or "visa sponsorship"

After extracting, compile a **JD Signal List**: a numbered list of the specific technologies, domains, and role characteristics the JD names. Label each `[MUST]` or `[NICE]`. Reference this list when filtering every section below — if an item from `candidate.md` cannot be mapped to a named signal, it does not belong in the CV.

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).

Country-specific additions:
- **Germany**: Photo expected (professional headshot). Date of birth and nationality commonly included. Date format: DD.MM.YYYY
- **Netherlands**: Photo optional but common. Date of birth customary. Nationality relevant for non-EU applicants
- **Denmark/Sweden**: No photo. No personal details beyond contact info. Equality-focused culture
- **Belgium**: Photo optional. Note language preferences from the posting

**Default for international tech companies**: No photo, no date of birth, no marital status. When unsure, omit — it's safer for ATS and avoids bias.

For non-EU applicants, add one line about work authorization if relevant: "Eligible for Germany Chancenkarte" or "EU work visa: requires sponsorship."

### 2. Professional Summary

Write exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves. Only list technologies from candidate.md.
3. **Differentiator**: One quantified achievement from candidate.md that maps to a `[MUST]` signal in your JD Signal List.
4. **Availability**: "Open to immediate relocation to [target country]."

Use implied first person (no "I"). Be factual, direct, quantified — European tone, not US marketing language.

Never use: "passionate," "rockstar," "guru," "seeking new challenges," or vague filler.

Rewrite this section for every application — never reuse a generic version.

### 3. Skills

Use this format exactly: `**Category:** Skill · Skill · Skill`

Use middle dots (·) only as separators — never pipes (|). Pipes are reserved for other sections.

Categories:
- Programming & Scripting
- Data Processing & Frameworks
- Cloud & Big Data Platforms
- Databases & Warehousing
- Workflow & Orchestration
- AI/ML Support & Analytics (if relevant)
- Data Quality & Governance
- Soft Skills (one line only)

**Filter first**: Reference your JD Signal List. Include a skill only if it maps to a named signal (exact or synonym). Do not include skills because they are generally technical or data-relevant — they must connect to a specific named signal. Then reorder so `[MUST]` signals appear first within each category. If the role leans Analytics Engineer, promote dbt, data modeling, BI tools. If Data Engineer, promote Spark, Airflow, infrastructure.

Always include "GDPR Awareness" under Data Quality & Governance for European applications.

Never use proficiency bars, star ratings, or percentage scales. Never fabricate skills.

Include a Languages line with CEFR levels (e.g., "English: C1 · Urdu: Native"). European employers expect the CEFR scale.

### 4. Professional Experience

For each role, use this exact structure:
```
**Job Title**                                            Mon YYYY – Mon YYYY
Company (HQ: City, Country) — Candidate City, Country (Work Model)
*One-line company description in italics*

- [Action Verb] + [What] + [Scale/Context]
```

- **Job Title**: bold, left-aligned. Date range right-aligned on the same line. Use en-dash (–) between dates.
- **Company line**: company name, then HQ in parentheses, then em-dash, then candidate's actual working location, then work model in parentheses (Remote / On-site / Hybrid). Read company HQ and description from candidate.md or research.md.
- **Company description**: one italic line — a brief factual descriptor (e.g., revenue, customer count, product category). Source from candidate.md or research.md. Required — do not omit.

**Bullet length is critical.** Maximum 1 line per bullet. Absolute maximum 15-18 words. No exceptions. If a bullet exceeds 18 words, split it or cut words.

Each bullet is a snapshot, not an explanation. The formula: `[Action Verb] + [What] + [Scale/Context]`

**Good examples:**
```
- Design and maintain 15+ Airflow pipelines processing 2TB+ daily from 8 source systems
- Manage Snowflake data warehouse serving 50+ business users across 3 departments
- Optimize PySpark transformation layers for multi-tenant data filtering and PII masking
- Collaborate with US-based data science team to define data contracts and quality standards
```

**Bad examples (too long — never write bullets like these):**
```
- Architect bespoke analytical solutions for 25+ enterprise clients by joining 2-15 Snowflake tables across IoT telemetry, operational transactions, and business metadata
- Manage PySpark transformation layers for Motive Data Bridge, filtering multi-tenant data, masking PII for SOC 2 compliance, and pre-aggregating complex metrics
```

These cram entire achievements into one bullet. Break them apart. Details and impact numbers belong in Projects, not here.

**Bullets per role:** Most recent: 4-6. Previous: 3-4. Oldest: 2-3.

**Combining roles at the same company:** If candidate.md lists multiple roles at the same company (e.g., Associate DE then DE), combine into one entry. Use the senior title with promotion noted. Use the full date range. Merge bullets into one set (4-6 total). Prioritize senior role bullets.

**Customization:** Reference your JD Signal List when ranking. `[MUST]` signal bullets go first; experience that maps to no named signal should be cut first when trimming for space. Use action verbs: Architected, Designed, Built, Developed, Implemented, Optimized, Automated, Migrated, Orchestrated, Deployed, Scaled, Monitored, Streamlined, Integrated, Maintained.

Ensure every `[MUST]` technology appears verbatim in at least one bullet across all roles (ATS matching). Use exact tool names: "Apache Airflow" not "workflow orchestration."

### 5. Education

```
Degree Title - University Name
City, Country | Year
```

Most recent first. For non-European degrees, add equivalence note if helpful. Include grades only if exceptional (Germany: 2.0 or below; Netherlands: 7.0 or above). No high school.

### 6. Certifications

```
Certification Name - Issuing Organization (Year)
```

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Map to JD Signal List**: For each cert, name the specific signal from your JD Signal List it addresses. If you cannot name one, discard it.
3. **Anti-pattern**: Do not keep a cert because it involves a data technology or sounds impressive. It must address a technology, domain, or characteristic explicitly named in the JD Signal List.

Most recent first.

### 7. Languages

```
English: C1 · Urdu: Native
```

Always include this section for European applications. Use CEFR scale.

---

## Critical Rules

**ATS-safe characters only.** No decorative unicode symbols, arrows, checkmarks, or stars. Use standard ASCII plus these two exceptions:
- **En-dash (–)** for date ranges only
- **Middle dot (·)** for skill and language separators only — never pipes in the Skills section

All other text must be plain ASCII. Hyphens (-) for inline dashes.

**Factual integrity.** Never fabricate experiences, skills, metrics, or achievements. Never invent technologies. Never inflate numbers. Framing and wordplay are encouraged — fabrication is not. If the JD requires a skill the candidate lacks, highlight the closest transferable experience instead.

**European tone by country:**
- Germany: Thorough, precise metrics, no timeline gaps
- Netherlands: Direct, quantified, results-oriented, concise
- Denmark/Sweden: Collaborative tone, emphasize teamwork over individual heroics
- Belgium: Note language preferences from the posting

Never use "outsourced," "offshore," or "remote contractor."

**Page length.** 2 pages maximum. 1 page acceptable in Netherlands for concise profiles.

To stay within 2 pages, apply cuts in this order:
1. Trim oldest role bullets to 2 (max 3)
2. Trim experience bullets to 15 words or fewer
3. Never cut certifications, education, or languages

If the data is still at risk of overflowing 2 pages when rendered, note the trimming decisions in your report back to the orchestrator.