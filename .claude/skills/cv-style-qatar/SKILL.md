---
name: cv-style-qatar
description: "Qatar CV style. Complete, self-contained CV writing
  rules for Qatar job applications. Loaded when style resolution
  matches qatar. This is a full style skill — not a partial override."
user-invocable: false
---

# Qatar CV Style

This style covers CV writing rules for Qatar job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

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
- **Industry sector**: oil & gas, finance, construction, healthcare, government — each has sector-specific terminology to mirror
- **Employer type**: QFC-registered / multinational vs local / semi-government — affects photo, personal info fields, and Qatarization framing

Build a **JD Signal List** — the extracted must-haves, technologies, and key phrases from this posting. Every section below references this list.

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
2. **Map each cert to a named signal from the JD Signal List** — the technology, domain, or methodology must connect to what the role requires
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

Include: full name, professional title, location (current city and country — use "Doha, Qatar" if already in-country), email, phone (+974 local number preferred if in Qatar), LinkedIn URL, GitHub (if relevant).

**Qatar-specific personal information fields:**

- **Professional photo**: Include a professional headshot (passport-style, formal attire, white or neutral background). A photo is expected across most Qatar sectors — local employers, oil & gas, hospitality, finance, healthcare, and government. Exception: if applying to a visibly Western-headquartered multinational or a QFC-registered company with global HR policies, the photo may be omitted. When in doubt, include it.
- **Date of birth**: Include in format DD/MM/YYYY (e.g., 15/06/1990). Expected by local, semi-government, and government employers.
- **Nationality**: Include. Required by Qatar employers to assess visa sponsorship needs and Qatarization compliance.
- **Marital status**: Include for local, semi-government, and government employers (e.g., "Married" or "Single"). Optional for multinational QFC-registered employers.
- **QID / visa status**: If residing in Qatar with a valid QID, state: "Valid QID – NOC available" or "Valid QID – transferable visa." If relocating from abroad, state visa eligibility and willingness to relocate clearly.
- **Notice period**: Include if already based in Qatar (e.g., "Available immediately" or "Notice period: 30 days").
- **Relocation**: If applying from abroad, add one line: "Currently based in [City, Country] — open to immediate relocation to Qatar."
- **Qatari nationals**: Highlight Qatari nationality prominently, near the name or at the top of the personal information block — this is a direct differentiator under Qatarization policy.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the JD Signal List. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies or competencies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or QID/availability statement if applicable.

**Tone**: Formal and achievement-oriented. Direct, results-focused language. Implied first person — no pronouns ("Delivered…" not "I delivered…"). Avoid hyperbolic claims ("world-class," "visionary leader"). Measured phrasing over bold self-promotion — Qatari business culture values modesty combined with substance. Use British English spelling throughout (e.g., "organisation," "optimisation," "programme").

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute → reference JD Signal List).

Distribute surviving skills into up to 5 category buckets (omit empty buckets):

1. **Technical Skills / Core Competencies** — domain-specific hard skills (e.g., engineering standards, programming languages, analytical methods)
2. **Software & IT Proficiency** — platforms, tools, enterprise software, cloud platforms
3. **Management & Leadership** — project management, team management, stakeholder engagement (include only if the candidate has relevant management experience)
4. **Industry-Specific Skills** — sector terminology aligned with dominant Qatar industries: LNG/oil & gas (EPC, FEED, HSE, API, ASME, LNG operations), finance (IFRS, risk management, treasury), construction (BIM, QA/QC, mega-project delivery), healthcare (QCHP, patient safety), government (policy, procurement, regulatory compliance)
5. **Certifications & Professional Qualifications** — may be listed briefly here if a dedicated Certifications section follows, or merged into that section

Separator between skill items: middle dot (·). No skill bars or visual proficiency ratings — ATS-unfriendly in Gulf markets.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD Signal List → shape with JD terminology → prioritize).

**Date format**: Mon YYYY – Mon YYYY (British-abbreviated month, e.g., "Jan 2022 – Mar 2024"). Use "Present" for the current role end date.

**Bullet writing rules**:
- Lead with a strong action verb: Achieved, Managed, Delivered, Led, Reduced, Increased, Implemented, Coordinated, Executed, Streamlined, Negotiated, Oversaw
- Quantify wherever possible: team size, budget scope, percentage improvements, contract value, project duration
- No personal pronouns. Implied first person throughout. Never use "I", "my", "he/she"
- Avoid "Responsible for…" and "Duties included…" — Gulf employers penalise responsibility-heavy framing (DubaiJobNow, GulfTalent)
- Maximum 20 words per bullet; aim for 15. Concise and impact-driven
- Maximum 5 bullets per recent role (last 5 years); maximum 3 for older roles
- Mention seniority indicators explicitly: team size, budget managed, reporting lines (e.g., "Led a team of 12," "Managed $4M EPC contract")
- Include a company description if the organisation is not a well-known brand in the Qatar/GCC market — one line after the company name (e.g., "Acme Engineering — Doha-based EPC contractor specialising in LNG infrastructure"). Major brands (QatarEnergy, Qatar Airways, Ooredoo, HSBC, Shell, Exxon) need no description

**Tone**: Formal, direct, achievement-oriented. Hierarchy and seniority indicators are respected in Qatari business culture — make scope of responsibility explicit rather than implied. British English spelling throughout.

### 5. Education

- List in reverse chronological order: most recent degree first
- Include: degree name, institution, location, graduation year (or date range)
- Include GPA if 3.0/4.0 or above; omit GPA for experienced professionals (5+ years)
- Note the grading scale when using a non-standard system (e.g., "GPA: 3.7/4.0" or "IB Diploma: 36/45")
- Qatar University and local institutions use a 4.0 GPA scale
- Qatar Foundation's Education City institutions (Georgetown, CMU, Northwestern, Texas A&M, etc.) carry high local prestige — name them explicitly
- Include high school only for recent graduates (0–3 years experience) or if the institution has significant prestige. Omit otherwise
- Western degrees (UK, US, Canadian, Australian) are well-respected in Qatar. No explanation needed at major employers. Lesser-known institutions benefit from a brief context line

### 6. Certifications

Follow the Certifications data collection philosophy above (map each cert to a named signal from the JD Signal List, discard if you can't).

**Format**: Certification Name — Issuing Body (Month Year)

**Certifications that carry significant weight in Qatar's job market:**
- **PMP** (Project Management Professional) — highly valued across all sectors; often decisive for project roles
- **NEBOSH / IOSH** — essential for HSE roles in oil & gas and construction
- **ACCA / CPA / CMA** — finance and accounting; ACCA is prominent in Big 4 and multinationals
- **API certifications** — oil & gas sector standard
- **RICS** — construction and real estate
- **CIPS** — procurement
- **QCHP registration** — mandatory for healthcare professionals; always include if held
- **AWS / Azure / Google Cloud** — tech roles
- **CCNA / CISSP** — IT/networking
- **Six Sigma / Lean** — operations and manufacturing
- **CFA** — finance/investment (QIA, banks, asset management)

### 7. Languages

**Format**: Language: Proficiency Level (Certification if applicable)

**Proficiency scale**: IELTS and TOEFL are the primary reference frameworks in Qatar and are more immediately legible to local employers than CEFR alone. State both where possible: "English: C1 (IELTS 7.5)". CEFR is accepted at multinational and QFC-registered employers.

**Arabic**: Include any level of Arabic proficiency — even conversational Arabic is positively received and adds breadth, especially for government, semi-government, and public-facing roles. Format: "Arabic: Native" / "Arabic: Professional proficiency" / "Arabic: Conversational."

**Layout**: Inline, separated by middle dot (·). Example:
`English: C1 (IELTS 7.5) · Arabic: Native · French: B2 (DELF)`

### 8. References

Include as the final section. Either list 1–2 professional references (name, title, organisation, contact information) or write: "References available upon request."

Gulf CVs include references more commonly than Western resumes. If the candidate has appropriate professional references and is comfortable sharing them at submission stage, list them. Otherwise, "References available upon request" is fully acceptable.

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers, text boxes, skill bars. ATS adoption is high in Qatar — major employers use Workday, Taleo, SAP SuccessFactors, Oracle HCM, and platform-native ATS on Bayt.com and Naukrigulf.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: 2 pages for 0–10 years experience; up to 3 pages for senior professionals (10+ years) with extensive certifications. Trim order if exceeding: oldest role bullets → weakest certification → project context → bullet word count. Never cut certifications, education, or languages.
- **British English**: Use British spelling throughout — "organisation," "optimisation," "programme," "colour," "behaviour," "specialise."
- **Qatarization awareness** (expat candidates): Frame experience to emphasise knowledge transfer, mentoring, and capacity building for local talent. Qatarization policy favours roles that complement Qatari workforce development goals. Avoid framing that reads as competitive with local talent.
- **Industry terminology**: Mirror exact sector-specific terms from the JD — "EPC contracts," "FEED studies," "HSE management," "ASME standards," "IFRS compliance," "QA/QC procedures," "LNG train operations."
- **Wasta referrals**: If the candidate was referred by a mutual professional contact at the target organisation, mention this in the cover letter (not the CV): "I was referred to this opportunity by [Name], [Title] at your organisation." Wasta is culturally significant in Qatar's hiring culture.
- **CV terminology**: The CV is called السيرة الذاتية (Al-Seerah Al-Zatiyah) in Arabic; in professional business contexts, "CV" is universally understood.
- Use en-dash for date ranges (–), middle dot (·) for skill separators.
