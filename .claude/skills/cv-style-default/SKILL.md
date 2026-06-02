---
name: cv-style-default
description: "Default CV style. Complete, self-contained CV writing rules used as the universal fallback when no region-specific or country-specific style exists. Covers section structure, bullet writing rules, ATS compliance, and factual integrity. Use this as the structural template when creating new styles."
user-invocable: false
---

# Default CV Style

This is the universal baseline CV style. It defines section structure, writing rules, and quality standards that apply regardless of geography. When a region-specific or country-specific style exists for the target location, that style is used instead — not in addition to this one.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: "required"/"essential"/"mandatory" are non-negotiable. "preferred"/"ideally"/"bonus" are nice-to-haves
- **Cultural signals**: any indicators about team structure, work style, or company culture
- Whether the posting mentions relocation support or visa sponsorship

After extracting, compile a **JD Signal List**: a numbered list of the specific technologies, domains, and role characteristics the JD names. Label each `[MUST]` or `[NICE]`. Reference this list when filtering every section below — if an item from `candidate.md` cannot be mapped to a named signal, it does not belong in the CV.

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).

Add one line about relocation readiness if applying to a different country: "Open to immediate relocation to [Country]."

Do not include: photo, date of birth, marital status, nationality — unless the target country's norms specifically require them (in which case, a country-specific style skill should be used instead of this default).

### 2. Professional Summary

Write exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves. Only list technologies from candidate.md.
3. **Differentiator**: One quantified achievement from candidate.md that maps to a `[MUST]` signal in your JD Signal List.
4. **Availability**: Relocation readiness or availability statement if applicable.

Use implied first person (no "I"). Be factual, direct, quantified.

Never use: "passionate," "rockstar," "guru," "seeking new challenges," or vague filler.

Rewrite this section for every application — never reuse a generic version.

### 3. Skills

Use this format exactly: `**Category:** Skill · Skill · Skill`

Use middle dots (·) as separators — never pipes (|).

**Filter first**: Reference your JD Signal List. Include a skill only if it maps to a named signal (exact or synonym). Do not include skills because they are generally technical — they must connect to a specific named signal. Reorder skills within each category so `[MUST]` signals appear first.

Categories:
- Programming & Scripting
- Data Processing & Frameworks
- Cloud & Big Data Platforms
- Databases & Warehousing
- Workflow & Orchestration
- AI/ML Support & Analytics (if relevant)
- Data Quality & Governance
- Soft Skills (one line only)

Reorder skills within each category so JD must-haves appear first.

Never use proficiency bars, star ratings, or percentage scales. Never fabricate skills.

### 4. Professional Experience

For each role, use this exact structure:
```
**Job Title**                                            Mon YYYY – Mon YYYY
Company (HQ: City, Country) — Candidate City, Country (Work Model)
*One-line company description in italics*

- [Action Verb] + [What] + [Scale/Context]
```

- **Job Title**: bold, left-aligned. Date range right-aligned on the same line.
- **Company line**: company name, HQ in parentheses, candidate's working location, work model (Remote / On-site / Hybrid).
- **Company description**: one italic line — factual descriptor from candidate.md or research.md. Required.

**Bullet rules:**
- Maximum 1 line per bullet. Absolute maximum 15-18 words. No exceptions.
- Each bullet is a snapshot: `[Action Verb] + [What] + [Scale/Context]`
- Action verbs: Architected, Designed, Built, Developed, Implemented, Optimized, Automated, Migrated, Orchestrated, Deployed, Scaled, Monitored, Streamlined, Integrated, Maintained
- Bullets per role: Most recent 4-6, previous 3-4, oldest 2-3

**Combining roles at the same company:** If candidate.md lists multiple roles at the same company, combine into one entry. Use the senior title with promotion noted. Merge bullets (4-6 total). Prioritize senior role bullets.

**Customization:** Reference your JD Signal List when ranking. `[MUST]` signal bullets go first; experience that maps to no named signal should be cut first when trimming for space. Ensure every `[MUST]` technology appears verbatim in at least one bullet (ATS matching). Use exact tool names.

### 5. Education

```
Degree Title - University Name
City, Country | Year
```

Most recent first. No high school.

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
Language: Level · Language: Level
```

Include this section if languages are relevant to the target location or role.

---

## Critical Rules

**ATS-safe characters only.** No decorative unicode symbols, arrows, checkmarks, or stars. Use standard ASCII plus:
- **En-dash (–)** for date ranges only
- **Middle dot (·)** for skill and language separators only

**Factual integrity.** Never fabricate experiences, skills, metrics, or achievements. Never invent technologies. Never inflate numbers. Framing and wordplay are encouraged — fabrication is not. If the JD requires a skill the candidate lacks, highlight the closest transferable experience instead.

**Page length.** 2 pages maximum.

To stay within 2 pages, apply cuts in this order:
1. Trim oldest role bullets to 2 (max 3)
2. Trim experience bullets to 15 words or fewer
3. Never cut certifications, education, or languages

If the data is still at risk of overflowing 2 pages when rendered, note the trimming decisions in your report back to the orchestrator.
