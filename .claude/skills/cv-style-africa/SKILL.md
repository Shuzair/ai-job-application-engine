---
name: cv-style-africa
description: "Africa CV style. Complete, self-contained CV writing
  rules for Africa job applications. Loaded when style resolution
  matches africa. This is a full style skill — not a partial override."
user-invocable: false
---

# Africa CV Style

This style covers CV writing rules for English-language African job applications (South Africa, Nigeria, Kenya, Ghana, Rwanda, Ethiopia). It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language requirements**: English is standard across all primary markets; French is required for Morocco and Francophone West Africa roles

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD (exact or synonym match)
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related or similar skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Keep ONLY certifications relevant to the job description — the technology, domain, or methodology must connect to what the role requires
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space
4. **Highlight**: If the candidate holds any locally-recognised African certifications that are relevant (CA(SA)/SAICA, ACCA, CIMA, CPA(K)/ICPAK, ICAN, CIPM, PMP, HPCSA, AWS/Azure/GCP), prioritise them prominently

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary in the bullets
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below (word count, action verbs, tone)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role. The summary should read as if this candidate is a natural fit for the job
3. **Mirror**: Use the job title and key terms from the JD. If the JD says "Senior Data Engineer," the summary should echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, city/country (not full address), email, phone, LinkedIn URL, GitHub (if relevant to the role).

**Field conventions for English-language African markets:**
- **Photo**: Optional — omit by default. Including a passport-style photo (formal attire, plain background) is more expected in Nigeria and Ghana for traditional/corporate roles. South African modern guides recommend against photos due to Employment Equity Act anti-bias norms. For international company applications in any market, omit.
- **Date of birth**: Never include — modern guidance across all markets explicitly deprecates DOB to prevent age discrimination.
- **Nationality**: Optional — include only if applying cross-border or if work authorisation context is relevant.
- **Marital status / gender / religion / tribe / state of origin**: Never include. Explicitly deprecated across SA (Employment Equity Act), Nigeria, Kenya, and Ghana professional norms.
- **ID number**: Never include — South Africa POPIA guidelines; identity theft risk across all markets.
- **Address**: City and country only (e.g., "Lagos, Nigeria" or "Nairobi, Kenya") — no full street address.
- **Relocation**: Add a brief note if applying to a different country (e.g., "Open to relocation to South Africa").

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-4 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies or competencies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Tone and language:**
- Professional but not stiff — "professional yet natural" is the stated standard in CVJury SA, Robert Walters Africa, and Jobberman Nigeria guides.
- Use British English spelling throughout: organise, labour, centre, recognised, favour, programme.
- Do not use "I" in the CV summary — implied first person only (e.g., "Results-driven engineer with 6 years..." not "I am a results-driven engineer...").
- Avoid clichés: "team player," "hardworking," "dynamic," "passionate" — African career guides explicitly flag these as overused.
- State achievements with numbers where possible: percentages, revenue impact, team size, timeframe.

**Good example**: "Data Engineer with 6 years' experience designing scalable pipelines in financial services. Proficient in Python, Spark, and AWS. Reduced data processing latency by 40% at current role. Open to relocation within East Africa."

**Bad example**: "Passionate and hardworking data professional who is a dynamic team player and always delivers outstanding results."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Distribute surviving skills into up to 5 category buckets (omit empty buckets):

1. **Technical Skills** — programming languages, software tools, domain-specific technologies
2. **Cloud & Infrastructure** — cloud platforms (AWS, Azure, GCP), DevOps, infrastructure tools
3. **Data & Analytics** — databases, BI tools, data processing frameworks, analytics platforms
4. **Professional Skills** — project management, business analysis, industry-specific methodologies (accounting, legal, engineering)
5. **Soft Skills** — communication, leadership, stakeholder management (optional — embed in summary instead if the list would be thin)

**Notes:**
- GitHub profile in the header is increasingly common for software/data roles in Kenyan and Nigerian tech markets — include if candidate has one and it's relevant.
- Professional certifications (SAICA, ACCA, ICPAK, ICAN, PMP) belong in the Certifications section, not Skills.
- Kiswahili/Swahili proficiency is a strong signal for East African roles — list in Languages, not Skills.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format**: Abbreviated month + year: "Jan 2022 – Mar 2024". Use "Present" for current role. Full DD/MM/YYYY dates are for formal documents only, not CV employment dates.

**Bullet writing rules:**
- Begin each bullet with a strong action verb: past tense for previous roles, present tense for current
- Maximum 2 lines per bullet (approximately 20 words)
- Do not start with "I" — implied subject
- Quantify wherever possible: "Increased revenue by 20%", "Managed team of 12", "Reduced processing time by 35%"
- Mirror JD keywords in phrasing: if the JD says "client engagement," use that phrase
- 4–5 bullets for current/recent roles; 2–3 for older roles

**Preferred action verbs (per Robert Walters Africa, Jobberman Nigeria, AtomCareer Kenya)**: achieved, managed, led, developed, implemented, reduced, increased, designed, delivered, trained, coordinated, launched, streamlined, negotiated, secured, deployed, restructured

**Tone**: Direct and results-focused. No hedging language ("helped to," "assisted with," "was involved in"). Every bullet should demonstrate impact or output.

**Company description**: Include a single-line factual descriptor for each employer (industry, size, brief context) — especially important if the company is not a household name in the target market.

### 5. Education

- List in reverse chronological order
- Degree name, institution, location, years attended
- **Grade**: Include if strong — use the institution's own grading term: "First Class Honours" (Nigeria/Ghana/Kenya), "Cum Laude" (South Africa), "Distinction" (SA percentage-based, 75%+), GPA if on a 4.0 scale. Omit if unremarkable.
- **High school / Matric / WAEC / KCSE**: Include if it is the highest qualification or if less than 3 years post-graduation. Once multiple tertiary qualifications exist, reduce to institution name and year only.
- **Thesis/Dissertation**: Mention title only if directly relevant to the JD (e.g., research-heavy or data-science roles).

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest).

**Format**: Certification name, issuing body, year (e.g., "AWS Solutions Architect — Associate, Amazon Web Services, 2023").

**Locally valued certifications by market (prioritise if relevant):**
- **South Africa**: CA(SA) — SAICA, SAIPA, HPCSA, ECSA (engineering), B-BBEE auditor credentials
- **Kenya**: CPA(K) — ICPAK, LSK (Law Society of Kenya), EBK (Engineers Board of Kenya)
- **Nigeria**: ICAN, CIPM, NSE (Nigerian Society of Engineers), NIM (Nigerian Institute of Management)
- **Pan-African**: ACCA, CIMA/CGMA, PMP, PRINCE2, AWS/Azure/GCP professional certs, ISACA (CISA/CISM), Cisco (CCNA/CCNP)

### 7. Languages

**Proficiency scale**: Use plain English descriptors — NOT CEFR levels unless the employer's posting specifically requests them. Standard African CV convention: Native / Fluent / Professional Working Proficiency / Conversational / Basic.

**When this section is critical:**
- Always include if the candidate speaks 2+ languages
- Kiswahili is a strong signal for East African (Kenya, Tanzania, Uganda) roles — list even at Conversational level
- French is essential for Morocco, relevant for Rwanda, and valued for pan-continental roles
- Arabic required for Egypt and Morocco; Amharic for Ethiopian public sector

### 8. Volunteer Work / Community Involvement (optional)

Include if the candidate has relevant volunteer experience. Particularly valued in Kenya and Rwanda (NGO/development sector is a major employer) and South Africa (community development aligns with Employment Equity values). Format: Role, Organisation, year(s), 1–2 impact bullets.

### 9. Hobbies & Interests (optional)

Include only if hobbies are genuinely relevant to the role or add meaningful professional dimension. Generic lists ("reading, travelling, socialising") should be omitted. This section remains common in traditional Nigerian, Ghanaian, and Kenyan formats — include if the role or sector context suggests a more traditional format is expected.

### 10. Referees

The correct African-English term is **"Referees"** (not "References").

**Baseline**: "Referees available on request." — Accepted across all major markets for professional roles; the modern default in South Africa.

**When to list full referee details** (name, title, company, phone, email):
- Government and public sector applications (Kenya, South Africa)
- NGO and development sector applications
- Senior roles where the employer explicitly requests referee details
- Long-form applications (Ethiopia, traditional Ghanaian sector)

If listing referees: provide 2–3 referees — Name, Title, Organisation, Phone, Email.

---

## Critical Rules

- **ATS compliance**: Standard characters only. No tables, columns, graphics, or headers/footers in the content area. Single-column layout. South African and Kenyan large employers are ATS-enabled; Nigerian and Ghanaian multinationals increasingly so.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **British English**: Use British spelling throughout — universal across all English-language African markets.
- **No personal information**: Never include date of birth, ID number, marital status, gender, religion, tribe, state of origin, or physical descriptions. Per SA Employment Equity Act and professional norms across all markets.
- **"Referees" not "References"**: This is the African-English CV convention.
- **Page limit**: Target 2 pages. 1 page for graduates (under 3 years' experience). Up to 3 pages for senior professionals (10+ years). Trim order: oldest role bullets → hobbies → volunteer detail → bullet word count. Never cut certifications, education, or languages.
- The document is called "CV" (Curriculum Vitae) — never "résumé" in any African market.
- Use en-dash (–) for date ranges, middle dot (·) for skill separators.
