---
name: cv-style-saudi-arabia
description: "Saudi Arabia CV style. Complete, self-contained CV writing
  rules for Saudi Arabia job applications. Loaded when style resolution
  matches saudi-arabia. This is a full style skill — not a partial override."
user-invocable: false
---

# Saudi Arabia CV Style

This style covers CV writing rules for Saudi Arabia job applications. It does NOT cover visual formatting — that is controlled by the style's `cv-format.yaml` in this folder.

The CV is called **السيرة الذاتية** (Al-Sira Al-Dhatiya) in Arabic. "CV" is the universally preferred English term in Saudi Arabia — not "resume."

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, Saudi market context
- Whether the posting mentions Vision 2030 alignment, Saudization/Nitaqat considerations, or sector-specific credentials (SOCPA, SCFHS, PMP, NEBOSH)
- **Sector context**: Is this Oil & Gas (Aramco/SABIC), Finance, Tech/NEOM, Government, Healthcare, or Construction? Each has different credential hierarchies
- **Language requirements**: Arabic required or English sufficient?
- Whether the employer is Saudi government, semi-government, or private sector multinational — affects tone and language choices

**Build your JD Signal List:** A ranked list of the top 8-12 skills, technologies, and domain terms from the job description. This list drives all filtering decisions in every section below.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD (exact or synonym match). Reference your JD Signal List.
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related skill, include that similar skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills that have no relevance to the JD or company's domain
5. **Distribute**: Organize the surviving skills into the category buckets defined below. If a bucket ends up empty after filtering, omit it entirely

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Keep ONLY certifications relevant to the job description — the technology, domain, or methodology must connect to what the role requires. Map each cert to a named signal from your JD Signal List; discard if you cannot make that connection.
3. **Discard**: Remove all certifications with no relevance to the target role. Do not include them just to fill space.
4. **Saudi priority note**: Sector-specific credentials carry outsized weight in Saudi ATS systems (SAP SuccessFactors, Taleo). If the JD is for Oil & Gas, NEBOSH/PMP/IOSH should be prominently placed. For Finance: SOCPA/CFA/ACCA. For Healthcare: SCFHS classification is mandatory. Place certifications section before Languages in the document.

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD Signal List. Prioritize: matching technologies, matching responsibilities, matching scale/domain
3. **Shape**: Write bullet points using terminology and keywords from the JD. If the JD says "data pipelines," use that phrase — not a synonym. Mirror the JD's technical vocabulary. For Saudi ATS systems, use both English and Arabic keywords for bilingual role postings.
4. **Prioritize**: Place the most JD-relevant bullets first within each role. Cut the least relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined in the style section below (CAR method, action verbs, SAR currency for financial metrics)

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary that positions the candidate for THIS specific role
3. **Mirror**: Use the job title and key terms from the JD Signal List. If the JD says "Senior Data Engineer," echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md that aligns with the role
5. **Vision 2030**: If the role is with a Vision 2030-aligned organisation (NEOM, giga-projects, national banks, tech transformation), include a brief reference to relevant experience with digital transformation, localization, or sector-specific initiatives
6. **Format**: Follow the structure and tone rules defined in the style section below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, professional headline (target job title), location (city + country), email, phone (with +966 international code if in Saudi Arabia), LinkedIn URL, GitHub (for tech roles).

**Saudi Arabia-specific header fields:**
- **Photo**: Include a photo path. Photos are expected for most Saudi roles. Professional headshot: formal attire, neutral background, passport-style. Omit only for explicitly ATS-optimised submissions to tech multinationals.
- **Date of Birth**: Include in DD/MM/YYYY format (e.g., 15/03/1990). Expected in Saudi CVs — do not omit.
- **Nationality**: Include. Practically mandatory due to Nitaqat/Saudization. Saudi nationals: "Saudi National." Expats: state nationality.
- **Marital Status**: Include. Expected in Saudi Arabia — married with dependents signals stability for expat hires.
- **Iqama/Visa Statement** (expats): Essential — most cited reason for expat CV rejection when missing. Use relocation field. Examples:
  - "Iqama: Transferable (Profession: Software Engineer, valid 04/2027)"
  - "Employment Visa — NOC available from current employer"
  - "Applying from abroad — requires employment visa sponsorship"
  - "Premium Residency holder — no employer sponsorship required" (if applicable — highlight this as a major advantage)

**Do not include**: Saudi National ID or Iqama number on paper/email CVs (include only on official company portals like Aramco's SAP system if requested).

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as exactly 4 components in 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain.
2. **What you do best**: Name 3-5 technologies or competencies matching the JD's must-haves.
3. **Differentiator**: One quantified achievement most relevant to this role (use SAR for Saudi-based financial metrics where applicable).
4. **Availability/Fit**: Iqama status or relocation readiness if applicable; Vision 2030 alignment if role is with a national initiative.

**Tone**: Formal, professional, achievement-oriented. Implied first person — no "I." Not boastful; indirect and respectful in register. Team contributions valued, but individual achievements must still be quantified.

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute). Reference your JD Signal List.

Distribute surviving skills into up to 6 category buckets (omit empty buckets):

- **Technical Skills** (المهارات التقنية) — core hard skills specific to the role
- **Programming Languages** (لغات البرمجة) — e.g., Python, SQL, Java, R
- **Frameworks & Libraries** (الأطر والمكتبات) — e.g., TensorFlow, React, Spring Boot
- **Cloud & DevOps** (السحابة والتطوير) — e.g., AWS, Azure, GCP, Kubernetes, Terraform
- **Databases** (قواعد البيانات) — e.g., PostgreSQL, MongoDB, Snowflake, Redshift
- **Software & Tools** (البرامج والأدوات) — e.g., SAP, Salesforce, Tableau, Power BI, Jira

Adapt bucket names to the sector: for Oil & Gas, use "Engineering Software"; for Finance, use "Financial Systems & Platforms"; for Cybersecurity (NCA-aligned roles), use "Security Tools & Frameworks."

Do NOT include generic soft skills (e.g., "teamwork," "communication") in the Skills section — these belong in the Summary or bullet points if relevant.

### 4. Professional Experience

Follow the Experience data collection philosophy above (collect all → rank by JD Signal List → shape with JD terminology → prioritize).

**Date format**: Month YYYY (e.g., "January 2022 – March 2024" or abbreviated "Jan 2022 – Mar 2024"). Gregorian calendar only — never use Hijri calendar dates.

**Bullet writing rules (CAR method)**:
- Open with a strong action verb: Led, Developed, Implemented, Managed, Reduced, Increased, Coordinated, Delivered, Engineered, Architected, Deployed, Automated
- Never use passive constructions ("was responsible for," "duties included")
- Quantify: percentages, SAR amounts (e.g., "SAR 850M portfolio"), team sizes, project budgets, timelines
- Max ~18 words per bullet — concise but complete
- Mirror JD terminology exactly; spell out acronyms on first mention

**Bullets per role**:
- Recent roles (last 5 years): 5–6 bullets
- Older roles: 2–3 bullets

**Company description**: Include a one-line company context for less well-known organisations. Global brands (Saudi Aramco, SABIC, McKinsey, NEOM) do not need a description.

**Multiple roles at same company**: Group under the company name with separate date ranges and bullet sets per role.

### 5. Education

List in reverse chronological order.

**GPA**: Include if 3.5/5.0 or higher (Saudi universities primarily use 5.0 scale; KFUPM uses 4.0). Always state the scale explicitly (e.g., "4.5/5.0") to avoid confusion with Western 4.0 scales. For internationally ranked universities, optionally note the QS ranking (e.g., "QS Ranked #200").

**High school (Tawjihiyah)**: Exclude once you hold a university degree and have professional experience. Include only for entry-level candidates with no university degree.

**Thesis/coursework**: Include thesis only if directly relevant to the target role or if applying for research/academic positions. Relevant coursework is low-priority for experienced professionals — omit unless compensating for limited work experience (recent graduates only).

**Degree attestation**: If your degree has been attested by the Saudi Ministry of Education, you may note this — it signals readiness for Iqama and work permit processing.

**Format**: Degree Title, Major, Institution Name (Country if outside Saudi Arabia), Year.

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD-relevant, map each to a JD Signal List item, discard the rest).

**High-value Saudi certifications by sector:**
- **Finance/Accounting**: SOCPA (Saudi Organization for Certified Public Accountants — mandatory for regulated finance roles), CFA, CPA (AICPA), ACCA
- **Engineering**: Saudi Council of Engineers registration (mandatory for licensed engineers in KSA), PE (NCEES)
- **Healthcare**: SCFHS (Saudi Commission for Health Specialties) classification — gatekeeping credential; without it, healthcare CVs cannot proceed to hiring
- **Project Management**: PMP — described as "nearly mandatory" for senior project roles across all sectors in Saudi Arabia
- **HSE/Safety**: NEBOSH IGC, IOSH Managing Safely — carry automated ATS weight for Aramco and energy sector applications
- **HR**: CIPD (Levels 3–7), SHRM-CP/SCP
- **IT/Cybersecurity**: CISSP, CISM, AWS/Azure certifications, NCA (National Cybersecurity Authority) aligned certs
- **Finance/Tech**: Aramco-specific certifications where applicable

**Format**: Certification Name · Issuing Body · Date (Month Year)

**Aramco note**: For Saudi Aramco applications, Arabic language version of the CV is expected or strongly preferred.

### 7. Languages

List all languages with proficiency level. Always include Arabic, even at basic level.

**Proficiency levels (self-descriptive — no CEFR required, though CEFR is understood):**
- Native
- Fluent
- Professional Working Proficiency
- Conversational
- Basic

**Arabic note**: Distinguish between Modern Standard Arabic (MSA — used in formal/written contexts) and Gulf Arabic (spoken dialect) if relevant to the role. Fluency in Arabic is essential for government entities, legal roles, banking, customer-facing roles, Aramco, SABIC. Even "Basic Arabic" is noted positively.

**Format example**: Arabic: Native · English: Professional Working Proficiency

---

## Critical Rules

- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, headers/footers. Saudi Arabia has high ATS adoption — SAP SuccessFactors and Taleo are dominant. Keyword density matters for Bayt.com and Naukrigulf.com profile parsing.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: 2 pages for mid-career professionals. 1–2 pages for graduates. 3 pages acceptable for senior executives (10+ years). Aramco and government roles accept longer CVs. Trim order if exceeding: oldest role bullets → least-JD-relevant project → bullet word count. Never cut certifications, education, or languages.
- **Gregorian calendar only**: Do not mix Hijri dates into employment history or education.
- **Nitaqat/Saudization awareness**: Saudi nationals should prominently state their nationality — it is a genuine hiring advantage under Saudization quotas. Expats must clearly state Iqama status, transferability, and NOC availability. Verify target role is not in a Saudi-only restricted category before applying.
- **Wasta (referrals)**: If referred by a known professional contact, note the referral in the cover letter (not CV). Do not note it in the CV itself.
- **Aramco applications**: An Arabic version of the CV is expected or strongly preferred when applying directly to Saudi Aramco.
- **Regional context**: Riyadh roles tend toward government/finance — use conservative dark colors, formal tone. Dammam/Eastern Province (Aramco belt) — NEBOSH/PMP/IOSH credentials prominently placed, technical certifications front-loaded. Jeddah — slightly more flexible formatting acceptable for trade/tourism/retail sectors.
- **Vision 2030 alignment**: Where genuinely applicable, reference alignment with Vision 2030 initiatives (digital transformation, localization, national talent development, renewable energy, NEOM). Do not force it where it does not apply.
- Use en-dash for date ranges. Middle dot for skill separators.
