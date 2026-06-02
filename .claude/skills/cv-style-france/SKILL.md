---
name: cv-style-france
description: "France CV style. Complete, self-contained CV writing rules for French
  job applications. Loaded when style resolution matches France. This is a full
  style skill — not a partial override."
user-invocable: false
---

# France CV Style

This skill defines how to write CV content for French job applications. It covers section structure, writing rules, and French-specific norms for both domestic and international tech companies. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: "requis"/"indispensable"/"obligatoire" are non-negotiable; "souhaité"/"idéalement"/"un plus" are nice-to-haves
- **Language requirements**: many French postings require French fluency — note whether English-only is acceptable
- **Cultural signals**: "environnement exigeant" = high-performance culture; "esprit d'équipe" = teamwork emphasis; "autonomie" = independence valued; "grande école" preference signals academic prestige matters
- Whether the posting mentions "visa sponsorship" or "titre de séjour"
- Whether the posting is in French or English — match your CV language accordingly

After extracting, compile a **JD Signal List**: a numbered list of the specific technologies, domains, and role characteristics the JD names. Label each `[MUST]` or `[NICE]`. Reference this list when filtering every section below — if an item from `candidate.md` cannot be mapped to a named signal, it does not belong in the CV.

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).

**Photo:** Expected in France. Include `photo_path` in the data. Professional headshot, passport-style. Photo display settings are in `cv-format.yaml`. If applying to a large international tech company (Google, Meta, etc.) that explicitly discourages photos, omit it.

**Date of birth:** Common but increasingly optional, especially in tech. Include if candidate is comfortable; omit for international tech companies or when anti-discrimination concerns apply. Format: DD/MM/YYYY.

**Nationality:** Include for non-EU applicants — employers need to know visa/work permit status. For EU citizens, optional but may help signal freedom to work.

**Address:** City and country sufficient. Full street address not required in modern French CVs.

**Do NOT include:** Marital status, number of children, religion, social security number. These are considered private under French labor law (Code du Travail, Articles L1132-1 to L1132-4 on non-discrimination).

For non-EU applicants, add one line about work authorization: "Titulaire d'un visa de travail" or "Eligible for Passeport Talent visa."

### 2. Professional Summary (Profil)

Write exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies matching the JD's must-haves. Only list technologies from candidate.md.
3. **Differentiator**: One quantified achievement from candidate.md that maps to a `[MUST]` signal in your JD Signal List.
4. **Availability**: "Disponible pour relocalisation à [city]" or "Open to immediate relocation to [city]" depending on CV language.

Use implied first person (no "I" / "Je"). Be factual, structured, and precise — French employers value clarity and intellectual rigor over marketing language.

Never use: "passionné," "passionnée," "guru," "rockstar," "ninja," vague superlatives, or empty filler like "dynamique et motivé(e)."

Rewrite this section for every application — never reuse a generic version.

### 3. Skills (Compétences)

Use this format exactly: `**Category:** Skill · Skill · Skill`

Use middle dots (·) as separators — never pipes (|).

Categories:
- Programming & Scripting (Programmation & Scripting)
- Data Processing & Frameworks
- Cloud & Big Data Platforms
- Databases & Warehousing
- Workflow & Orchestration
- AI/ML Support & Analytics (if relevant)
- Data Quality & Governance
- Soft Skills (one line only — e.g., "Cross-functional collaboration · Stakeholder communication · Technical mentoring")

**Filter first**: Reference your JD Signal List. Include a skill only if it maps to a named signal (exact or synonym). Do not include skills because they are generally technical or data-relevant — they must connect to a specific named signal. Then reorder so `[MUST]` signals appear first within each category. Always include "GDPR / RGPD Compliance" under Data Quality & Governance — France enforces GDPR strictly through the CNIL.

Never use proficiency bars, star ratings, or percentage scales — they are not ATS-friendly and are considered imprecise by French recruiters.

### 4. Professional Experience (Expérience Professionnelle)

For each role, use this exact structure:
```
**Job Title**                                            Mon YYYY – Mon YYYY
Company (HQ: City, Country) — Candidate City, Country (Work Model)
*One-line company description in italics*

- [Action Verb] + [What] + [Scale/Context]
```

- **Date format**: Mon YYYY (e.g., Sep 2024). Use en-dash (–) between dates. French CVs also accept MM/YYYY but Mon YYYY is more readable for international roles.
- **Company line**: company name, then HQ in parentheses, then em-dash, then candidate's working location, then work model (Remote / On-site / Hybrid / Télétravail).
- **Company description**: one italic line — brief factual descriptor (revenue, employee count, product). Required — French employers value context about the company.

**Bullet writing rules:**

Maximum 1 line per bullet. Absolute maximum 15-18 words. No exceptions.

Each bullet: `[Action Verb] + [What] + [Scale/Context]`

**Good examples:**
```
- Concevoir et maintenir 15+ pipelines Airflow traitant 2 To+ de données quotidiennes
- Optimiser les couches de transformation PySpark pour le filtrage multi-tenant et le masquage PII
- Collaborer avec l'équipe data science pour définir les contrats de données et standards qualité
```

Or in English for international companies:
```
- Design and maintain 15+ Airflow pipelines processing 2TB+ daily from 8 source systems
- Optimize PySpark transformation layers for multi-tenant data filtering and PII masking
```

**Bullets per role:** Most recent: 4-6. Previous: 3-4. Oldest: 2-3.

**Combining roles at the same company:** If candidate.md lists multiple roles at the same company, combine into one entry. Use the senior title with promotion noted. Use the full date range. Merge bullets into one set (4-6 total).

**Customization:** Reference your JD Signal List when ranking. `[MUST]` signal bullets go first; experience that maps to no named signal should be cut first when trimming for space. Use action verbs: Concevoir, Développer, Architecting, Implémenter, Optimiser, Automatiser, Migrer, Orchestrer, Déployer, Monitorer, Intégrer. For English CVs: Architected, Designed, Built, Developed, Implemented, Optimized, Automated, Migrated.

Ensure every `[MUST]` technology appears verbatim in at least one bullet across all roles (ATS matching). Use exact tool names: "Apache Airflow" not "outil d'orchestration."

### 5. Education (Formation)

```
Degree Title — Institution Name
City, Country | Year
```

Most recent first. Education is highly valued in France — this section deserves more detail than in Anglo-Saxon CVs.

**French degree equivalences:**
- Bac+2: BTS / DUT (≈ Associate's)
- Bac+3: Licence (≈ Bachelor's)
- Bac+5: Master / Diplôme d'Ingénieur (≈ Master's)
- Bac+8: Doctorat (≈ PhD)

For foreign degrees, add Bac+N equivalence in parentheses: "BSc Computer Science (Bac+3 equivalent)."

**Grades:** Include if notable. French system uses Mention: Très Bien (>16/20), Bien (14-16/20), Assez Bien (12-14/20). For foreign GPAs, include if above 3.5/4.0 or equivalent distinction.

Include thesis topics or major projects if relevant to the target role. Grande école graduates should mention their école name prominently — it carries significant weight in France.

Do not include high school (lycée) unless the Baccalauréat has a distinctive mention or specialization relevant to the role.

### 6. Certifications

```
Certification Name — Issuing Organization (Year)
```

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Map to JD Signal List**: For each cert, name the specific signal from your JD Signal List it addresses. If you cannot name one, discard it.
3. **Anti-pattern**: Do not keep a cert because it involves a data technology or sounds impressive. It must address a technology, domain, or characteristic explicitly named in the JD Signal List.

Most recent first.

Certifications valued in France: cloud provider certs (AWS, GCP, Azure), Databricks, Snowflake, ITIL (popular in France), PMP, Agile/Scrum certifications, DELF/DALF for French language.

### 7. Languages (Langues)

```
English: C1 · French: B2 · Urdu: Native
```

Always include this section — it is critical for French applications. Use CEFR scale (A1-C2), which is the European standard and well-understood in France.

For French language specifically, also reference DELF/DALF certification if held: "French: B2 (DELF B2)."

List French first if applying to French companies. List the language of the posting first otherwise.

France is less English-friendly than Nordic or Dutch markets — French language proficiency is often a deciding factor, even in tech.

### 8. Hobbies & Interests (Centres d'intérêt)

This section is **valued** in France and expected on most CVs. French employers use it to gauge personality and cultural fit.

Format as a keyword list: `Photography · Trail Running · Chess · Volunteering at Code.org`

**Rules:**
- 3-6 items maximum
- Be specific: "Trail running in the Alps" is better than "Sports"
- Include at least one cultural or intellectual pursuit — French culture values intellectual curiosity
- Team sports show collaboration; individual pursuits show discipline
- Community involvement and volunteering (bénévolat) are viewed positively
- Avoid generic entries: "Reading" alone is too vague — "Reading: science fiction and behavioral economics" is better

---

## Critical Rules

**ATS-safe characters only.** No decorative unicode symbols, arrows, checkmarks, or stars. Use standard ASCII plus:
- **En-dash (–)** for date ranges only
- **Middle dot (·)** for skill, language, and interest separators only

**Factual integrity.** Never fabricate experiences, skills, metrics, or achievements. Never invent technologies. Never inflate numbers. If the JD requires a skill the candidate lacks, highlight the closest transferable experience instead.

**French tone:** Formal, structured, precise. Value clarity and intellectual rigor. Avoid excessive self-promotion — let achievements speak. More conservative and structured than US resumes, but not stiff. French employers appreciate well-organized information presented logically.

**Page length.** 1 page for candidates with <10 years experience. 2 pages maximum for senior professionals. French recruiters expect brevity.

To stay within limits, apply cuts in this order:
1. Trim oldest role bullets to 2
2. Trim experience bullets to 15 words or fewer
3. Reduce Hobbies to 3 items
4. Never cut certifications, education, or languages

**Anti-discrimination law:** French law (Code du Travail, L1132-1) prohibits employment discrimination. Never include religion, political affiliation, union membership, sexual orientation, health status, or pregnancy status on a CV. While photo, age, and nationality are still common, they are technically voluntary.

**Language matching:** Write the CV in the same language as the job posting. If the posting is in French, the CV should be in French. If in English, write in English.
