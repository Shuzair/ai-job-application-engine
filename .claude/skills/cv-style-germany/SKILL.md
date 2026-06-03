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
- The **core responsibility** from the first 2-3 requirement bullets (Aufgaben/Anforderungen)
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions relocation support or visa sponsorship
- **Language requirements**: Is the posting in German or English? This determines the CV language — match the posting language
- **JD Signal List**: Create a flat list of every named technology, methodology, domain term, and soft-skill keyword from the posting. This list is referenced by Skills, Certifications, Experience, and Interests sections as a relevance filter

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD (exact or synonym match). Reference your JD Signal List — a skill must map to a named signal
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related or similar skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Map each certification to a named signal from the JD Signal List. Keep ONLY certifications where the technology, domain, or methodology connects to a JD signal
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space. IHK and TÜV certifications carry particular weight in Germany — prioritize these if relevant

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "Daten-Pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary (German or English as posted) in the bullets
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

### 1. Header (Persönliche Daten)

Include: full name, location (city and country), email, phone, LinkedIn URL, GitHub (if relevant to the role).

**Photo**: German CVs are expected to include a professional headshot (Bewerbungsfoto). Despite the AGG (Allgemeines Gleichbehandlungsgesetz, 2006) making photos legally optional, ~82% of German recruiters still expect one. Include `photo_path` in the data if the candidate has a professional photo available.

**Date of birth**: Include in format DD.MM.YYYY (e.g., `15.03.1990`). Standard German convention. Birthplace (city) may also be included.

**Nationality**: Always include, especially for non-German applicants. Pair with work permit information for non-EU citizens.

**Work permit**: For non-EU citizens, include the permit type and authorization status (e.g., "EU Blue Card", "Niederlassungserlaubnis", "Chancenkarte"). EU/EEA citizens do not need to state this.

**Marital status**: Omit — increasingly outdated and unnecessary for modern German applications.

**Relocation**: Add one line about relocation readiness if applying from outside Germany (e.g., "Open to immediate relocation to Berlin").

### 2. Professional Summary (Profil / Kurzprofil)

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role.
4. **Availability**: Relocation readiness or availability statement if applicable.

**Tone**: Formal, direct, and factual. No "passionate," "dynamic," or "results-driven" — German recruiters consider these filler words. State your value plainly with evidence. Implied first person — never write "I" or "Ich." Keep it to 2-4 factual sentences. Example construction: "Senior Software Engineer with 8 years of experience in distributed systems and cloud infrastructure (AWS, Kubernetes). Expertise in Go and Ruby on Rails. Reduced deployment time by 40% through CI/CD pipeline optimization at [Company]."

### 3. Skills (Kenntnisse / IT-Kenntnisse)

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Distribute surviving skills into up to 5 category buckets (omit empty buckets). German job market terminology for tech roles:

- **Programming & Scripting** (Programmiersprachen): programming languages, scripting languages
- **Cloud & Infrastructure** (Cloud-Infrastruktur): cloud platforms, infrastructure tools, containerization
- **Data & Databases** (Datenbanken & Datenverarbeitung): databases, data processing frameworks, ETL tools
- **Frameworks & Libraries** (Frameworks & Bibliotheken): web frameworks, data science libraries, testing frameworks
- **DevOps & Tools** (DevOps & Werkzeuge): CI/CD, monitoring, version control, project management tools

Maximum 5 buckets. Avoid graphical skill bars or star ratings — they are not ATS-readable and considered informal in German professional culture. Use text-only skill lists with middle dot separators.

Do NOT use the outdated term "EDV-Kenntnisse" (Elektronische Datenverarbeitung) unless the JD uses it explicitly for ATS matching. Use "IT-Kenntnisse" or "Technische Kenntnisse" instead.

### 4. Professional Experience (Berufserfahrung)

Follow the Experience data collection philosophy above (collect all → rank by JD relevance → shape with JD terminology → prioritize).

**Date format**: MM/YYYY for date ranges (e.g., `03/2020 – 11/2023`). Current role: `04/2024 – Present`. Do NOT use "Mar 2020" or "March 2020" format — use numeric months.

**Company format**: Company name + city. For lesser-known companies, add a brief parenthetical descriptor (industry, size, stage): e.g., `Acme GmbH, Berlin (B2B SaaS, ~120 employees)`.

**Bullet writing rules**:
- Open with a past-tense action verb (implied first person — no "I"/"Ich"): "Developed," "Led," "Optimized," "Designed," "Implemented"
- Maximum 20 words per bullet — aim for 1-2 lines of precise, quantified impact
- Every bullet must include a measurable outcome where possible (percentages, Euro amounts, headcount, timeframes)
- Avoid superlatives ("best-in-class," "world-class") and promotional language ("spearheaded," "passionate about")
- Mirror exact JD terminology in bullets for ATS matching

**Bullets per role**:
- Most recent role: 4–5 bullets
- Previous roles (2–5 years ago): 3–4 bullets
- Older roles (5+ years ago): 2–3 bullets, sometimes one-line summary

**Multiple roles at same company**: List as separate entries with distinct date ranges under the same company header. Each role gets its own bullets.

**Employment gaps**: Any gap over 2-3 months should be briefly explained (parental leave, further education, etc.). Unexplained gaps are a red flag for German recruiters.

### 5. Education (Ausbildung)

List in reverse chronological order: degree, institution, location, dates.

**German grading system**: Germany uses an inverted 1.0–5.0 scale (1.0 = best). Include final grade (Gesamtnote) only if 2.5 or better. For experienced professionals (3+ years), omit grades entirely — professional track record takes precedence.

**Foreign degrees**: List as normally titled, then add German equivalent context if helpful (e.g., "Bachelor of Science in Computer Science"). The Modified Bavarian Formula converts foreign grades to the German scale.

**Thesis**: Include thesis topic (Thema der Abschlussarbeit) only if directly relevant to the target role. Especially valuable for academic, research, or technical positions.

**Abitur / High school**: German convention expects to see the complete education chain. For experienced professionals, retain as a single condensed line (school name, location, year) but do not elaborate. Can be omitted if space is very tight on a 2-page CV.

**Date format**: MM/YYYY for date ranges, matching the experience section format.

### 6. Certifications (Zertifikate / Weiterbildungen)

Follow the Certifications data collection philosophy above (keep only JD-relevant, discard the rest). Map each certification to a named signal from the JD Signal List — discard if you cannot map it.

**German-specific certifications that carry weight**:
- IHK (Industrie- und Handelskammer) certificates — nationally recognized vocational qualifications
- TÜV certifications (TÜV Rheinland, TÜV SÜD) — safety, quality management, data protection
- SCC certificates — occupational health and safety

**Format**: Certification name, issuing body, date (MM/YYYY). Include verification URL if available.

### 7. Languages (Sprachkenntnisse)

List each language with CEFR level AND German descriptor. CEFR is the de facto standard in Germany.

**Format**: `Language: German Descriptor (CEFR Level)` — e.g., `German: Fließend (B2)`, `English: Verhandlungssicher (C1)`

**CEFR to German descriptor mapping**:
- Native → Muttersprache (no CEFR code needed)
- C2 → Muttersprachler-Niveau
- C1 → Verhandlungssicher (business fluent)
- B2 → Fließend (fluent)
- B1 → Gute Kenntnisse (good working knowledge)
- A1/A2 → Grundkenntnisse (basic)

List native language first, then others from highest to lowest proficiency. German and English should always be listed. Include official test scores if available (e.g., "C1 — IELTS 7.0", "B2 — Goethe-Zertifikat B2").

Avoid graphical skill bars — not ATS-readable and ambiguous.

### 8. Interests (Hobbys / Interessen)

Optional section — include ONLY if interests demonstrate a transferable competency relevant to the role or reveal distinctive character traits.

Reference your JD Signal List. Include an interest only if it connects to a skill, domain, or cultural value from the JD or target company. Examples: competitive sports → resilience/discipline, team sports → collaboration, open-source contributions → technical community engagement.

Exclude generic interests (travel, cooking, music, reading) unless they are distinctive or role-relevant. For senior professionals, this section can be omitted entirely to save space.

Format: 3–5 brief phrases, displayed inline with separators.

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. German ATS platforms (Personio, SAP SuccessFactors, Softgarden, Workday) are widespread even at Mittelstand companies. Use standard section headings for parser compatibility.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: Maximum 2 pages. Trim order if exceeding: oldest role bullets → interests section → company descriptions → bullet word count. Never cut certifications, education, or languages.
- Use en-dash for date ranges, middle dot for skill separators.
- **Tone**: Formal, direct, factual, and modest. Not promotional. German CVs are factual documents, not marketing materials. Avoid superlatives, creative language, and Anglicisms like "spearheaded" or "passionate."
- **Pronouns**: Implied first person throughout. Never use "I"/"Ich" or third person.
- **Language**: Match the language of the job posting. If the posting is in German, write the CV in German (except section content which may be technical English). If in English, write in English.
- **AGG awareness**: The Allgemeines Gleichbehandlungsgesetz (2006) makes photo, DOB, nationality, and marital status legally optional. However, German market convention still expects photo, DOB, and nationality. Include them by default. Omit marital status.
- **DIN 5008 reference**: While DIN 5008 strictly governs business letters (Anschreiben), German CVs follow the same margin and formatting principles for consistency.
