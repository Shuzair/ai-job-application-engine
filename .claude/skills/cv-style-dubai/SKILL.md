---
name: cv-style-dubai
description: "Dubai CV style. Complete, self-contained CV writing
  rules for Dubai job applications. Loaded when style resolution
  matches dubai. This is a full style skill — not a partial override."
user-invocable: false
---

# Dubai CV Style

This style covers CV writing rules for Dubai/UAE job applications. Visual formatting is controlled by `cv-format.yaml` in this folder.

Read `candidate.md` before writing any CV content. Every claim, skill, and metric must be traceable to that file. Never fabricate.

---

## Pre-work: Decode the Job Posting First

Before writing anything, analyze the job posting and extract:

- The **top 3 technologies** mentioned most prominently
- The **core responsibility** from the first 2-3 requirement bullets
- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus
- **Cultural signals**: team structure, work style, company culture indicators
- Whether the posting mentions visa sponsorship or Emiratization requirements
- **Language requirements**: English-only (most free zones, MNCs) or Arabic required (government, semi-government)
- **Regulatory context**: relevant UAE zone or regulator (DIFC, ADGM, RERA, DHA, CBUAE, KHDA, JAFZA, DMCC) — use these acronyms as ATS keywords where applicable

**Build a JD Signal List**: Extract the 6-8 most important keywords, technologies, and domain terms from the JD. Use these as a checklist when writing every section — skills must map to them, bullet highlights must reference them, and the summary must echo them.

---

## Data Collection Philosophy

These rules define HOW to collect and filter data from candidate.md for each section. They are fixed across all styles — only the presentation rules (bucket names, bullet format, tone) vary by country.

### Skills — Relevance-First Filtering

1. **Collect**: Read ALL skills from `candidate.md`
2. **Match**: Keep skills that appear in the JD Signal List (exact or synonym match)
3. **Expand**: If the JD mentions a skill the candidate lacks exactly but has a closely related skill, include that related skill (e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)
4. **Discard**: Remove all remaining skills with no relevance to the JD or company's domain
5. **Distribute**: Organize surviving skills into the category buckets defined below. Omit empty buckets

### Certifications — Strict Relevance Gate

1. **Collect**: Read ALL certifications from `candidate.md`
2. **Filter**: Keep ONLY certifications that map to a named signal in the JD Signal List — the technology, domain, or methodology must connect to what the role requires
3. **Prioritize UAE-valued credentials**: PMP, ACCA, CFA, CMA, AWS/Azure/GCP, RERA, UAE VAT Certificate, CISSP, CISA — these carry strong weight in the Dubai market and should be retained if role-relevant
4. **Discard**: Remove all certifications with no relevance to the target role. Do not include them to fill space

### Experience — Maximum Context, Then Rank

1. **Collect**: Read ALL experience details from `candidate.md` — roles, projects, technologies, metrics, achievements, context
2. **Analyze**: Rank each piece of experience by relevance to the JD Signal List. Prioritize: matching technologies, matching responsibilities, GCC regional experience, AED-scale metrics
3. **Shape**: Write bullets using terminology from the JD Signal List. If the JD says "data pipelines," use that phrase — not a synonym. Mirror JD vocabulary. Include UAE/GCC market signals where authentic (GCC regulatory experience, regional scale, AED-denominated metrics)
4. **Prioritize**: Place most JD-relevant bullets first within each role. Cut least-relevant bullets when space is tight
5. **Format**: Follow the bullet writing rules defined below

### Summary — Candidate-Meets-JD Synthesis

1. **Read**: Study the full candidate profile — experience arc, strongest skills, key achievements, career trajectory
2. **Synthesize**: Write an optimal summary positioning the candidate for THIS specific role
3. **Mirror**: Use the job title and key terms from the JD Signal List. If the JD says "Senior Data Engineer," the summary should echo that framing
4. **Quantify**: Include the single most impressive metric from candidate.md aligned with the role — AED-denominated where authentic
5. **Format**: Follow the structure and tone rules defined below

---

## CV Sections

Generate these sections in this exact order.

### 1. Header

Include: full name, professional headline (current/target title), location, nationality, email, phone, LinkedIn URL.

**Mandatory UAE fields** — include on every Dubai/UAE CV:
- **Visa/availability line**: State current visa type and notice period/availability on one line. Per Labeeb.ae 2026, vague or missing availability is treated as unavailable by UAE employers who need to assess sponsorship. Format examples:
  - "Employment Visa · Available in 30 days"
  - "Visit Visa · Available Immediately · Open to Sponsorship"
  - "Golden Visa · Available Immediately"
  - "Spouse/Dependent Visa · Available Immediately"
- **Nationality**: State plainly — "British National," "Pakistani National." UAE employers require this for visa sponsorship and Emiratization compliance assessment. List both if dual nationality.

**Recommended UAE fields** — include unless specifically targeting MNCs or tech free zones where these are optional:
- **UAE Driving License**: Include if held — widely expected for many roles in Dubai per GulfTalent
- **Date of Birth**: Include for traditional/local UAE companies and regional firms. Format: DD/MM/YYYY. For MNC-targeting applications, this may be omitted per modern international best practice
- **Marital status**: Include for traditional/local UAE companies. Omit for MNCs and tech companies

**Photo**: Include a professional headshot for most UAE applications:
- Effectively required: customer-facing roles (hospitality, aviation, retail, cabin crew — often specified in the JD)
- Strongly recommended: local/traditional UAE companies, regional enterprises, most mid-size firms
- Optional: senior/executive roles (LinkedIn photo often substitutes), MNCs and multinational tech companies
- Photo standard: professional headshot, business attire, neutral background, modest professional dress; no selfies or casual photos

**Exclude always**: religion, passport number, Emirates ID number

GitHub: include if relevant (engineering, data, tech roles).

Relocation statement: if currently outside UAE, add one line — "Relocating to Dubai, [Month Year]" — and include it in the visa/availability line.

### 2. Professional Summary

Follow the Summary data collection philosophy above, then format as 3-5 lines total:

1. **Who you are**: Mirror the job title from the posting. State years of experience and domain. Implied first person — no "I" or "my."
2. **What you do best**: 3-5 technologies or capabilities matching JD Signal List must-haves.
3. **Differentiator**: One standout quantified achievement most relevant to this role. AED-denominated or %-quantified metrics preferred.
4. **UAE market fit** (include if authentic): One line signaling GCC/UAE relevance — GCC regional experience, UAE regulatory awareness, multicultural team leadership, Arabic language capability, UAE Golden Visa status.

Tone: Achievement-oriented, direct, concise. No "passionate," "results-driven," "dynamic team player," or filler phrases. No passive voice. Implied first person throughout.

Avoid generic openings: lead with the job title and strongest credential — not "Experienced professional with..."

### 3. Skills

Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).

Reference the JD Signal List. Include a skill category only if it contains at least one named signal match.

Distribute surviving skills into up to 4 category buckets (omit empty buckets):

1. **Technical Skills** — programming languages, frameworks, data tools, engineering platforms
2. **Tools & Platforms** — specific software, cloud platforms (AWS/Azure/GCP), BI tools, SaaS products, industry systems
3. **Domain Expertise** — functional areas, industry knowledge, UAE/GCC regulatory knowledge (VAT, CBUAE, DFSA, RERA, AML-CFT where role-relevant)
4. **Core Competencies** — professional skills, methodologies, leadership capabilities relevant to the role

Alternative for non-tech or finance roles: "Core Competencies," "Software & Systems," "Regulatory Knowledge," "Industry Expertise."

Per Labeeb.ae and GulfTalent: a flat competency list of 8-12 items is also widely used and ATS-effective. Use buckets when they add clarity; use a flat list for roles with highly diverse skill types.

### 4. Professional Experience

**Date format**: "Mar 2022 – Feb 2024" (3-letter abbreviated month + 4-digit year, en-dash). Use "Present" for active roles. Consistency across all roles is mandatory per Labeeb.ae.

**Bullet formula**: Strong action verb + task/scope + quantified result.
- Lead with: Managed, Reduced, Built, Improved, Delivered, Led, Launched, Deployed, Designed, Negotiated, Streamlined
- Avoid: "Responsible for," "Helped with," "Assisted in," "I," "my"
- Quantify with AED amounts, percentages, team sizes, volume, time saved — AED-denominated metrics are especially powerful in a UAE context
- Target 1 line per bullet, 2 lines maximum; approximately 20-30 words

**Bullet count**:
- Current/most recent role: 4–6 bullets
- Roles 2–3 in history: 3–4 bullets
- Older roles (3+ years prior): 2–3 bullets
- Very early career (5+ years prior): 1–2 bullets or a summary sentence

**Company description**: Include a one-line descriptor for employers not widely recognized in the UAE market. Per GulfTalent, this is explicitly recommended. Format: "CompanyName — [origin]-headquartered [industry] company ([stage/size], [region])." Example: "TechCorp — Germany-based SaaS platform (Series C, 400 employees, DACH region)"

**Combining roles**: If the candidate held multiple titles at the same company, group them under the company name with separate date ranges per title.

**UAE/GCC signals**: Where authentic, include context that signals GCC relevance — "GCC-wide deployment," "UAE regulatory environment," "Dubai-based team," "multicultural team of [N] nationalities," "AED [amount]." These double as ATS signals on Bayt, Naukrigulf, and government portals.

### 5. Education

**Format**: Degree title, Institution name, Location, Graduation year.

**GPA**: Include if 3.5/4.0 or above, or equivalent honors (Distinction, First Class, With Honors). Per Bayt.com, "impressive = Excellent, Very Good." Always state the scale: "GPA: 3.7/4.0." Below 3.0: omit.

**Unknown institutions**: Add a brief descriptor for universities not recognized in the UAE — same principle as company descriptions. Example: "University of Salford (UK, AACSB-accredited)"

**High school**: Exclude if the candidate holds a bachelor's degree or higher.

**Thesis**: Include title only if directly relevant to the target role.

**Attestation note** (regulated professions only): For roles requiring professional licensing (healthcare/DHA, education/KHDA, engineering, law), note MOHESR attestation status if applicable — "(MOHESR attested)" — as UAE employers in regulated sectors require this.

### 6. Certifications

Follow the Certifications data collection philosophy above (keep only JD Signal List–relevant, discard the rest).

**Format**: Certification name, Issuing body, Month Year. Include verification URL where available.

**High-value Dubai/UAE credentials** — retain if role-relevant:
- Project management: PMP (PMI), PRINCE2, Agile/Scrum certifications
- Finance/accounting: ACCA, CPA, CMA, CFA, UAE VAT Certificate, UAE Corporate Tax Certificate
- Tech: AWS Solutions Architect, Azure/GCP equivalents, CISSP, CISA, TOGAF
- Real estate: RERA license (mandatory for any real estate role in Dubai; include RERA number)
- Healthcare: DHA/HAAD license (mandatory for regulated healthcare roles)
- Financial services: DFSA-recognized qualifications for DIFC/ADGM roles

### 7. Languages

**Format**: Language — Proficiency Level

Use CEFR scale (A1–C2) or LinkedIn-style descriptors (Native, Fluent, Professional Working, Conversational). Either is recognized in UAE; use one consistently. Adding IELTS/TOEFL score in parentheses adds credibility: "English — C1 (IELTS 7.5)."

**Arabic proficiency**: A significant differentiator in Dubai. Approximately 14.5% of UAE job postings explicitly require Arabic (per Coursetakers.ae); far more list it as preferred. For public sector and Abu Dhabi government roles, Arabic is effectively required. Include even basic Arabic ability — "Arabic — A2 (Basic)" is better than omitting it entirely. Native Arabic speakers should note this prominently, ideally also in the Professional Summary.

### 8. Projects (optional — include for tech/digital/engineering roles)

The Dubai tech market values demonstrated applied skills. Include a Projects section when the candidate has personal or professional projects that directly map to the JD Signal List.

Gate: Reference the JD Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. Omit technically impressive projects that address no JD signal.

**Format**: Project name, brief technology/domain description, 1-3 bullets with quantified outcomes or scope.

### 9. Interests (optional — include for culture-fit signal)

In the UAE's relationship-oriented business culture, interests can demonstrate cultural fit and international outlook. Keep neutral and professional — avoid politically sensitive topics. Format: comma-separated inline list. Keep to one line.

---

## Critical Rules

- **ATS compliance**: Single-column layout mandatory. No tables, text boxes, graphics, headers/footers, shaded cells, or multi-column designs. ATS adoption is high across all mid-to-large UAE employers (Taleo, Workday, government portals, LinkedIn, Bayt, Naukrigulf). Per Labeeb.ae, multi-column and table-based layouts are the leading cause of ATS rejection in UAE applications.
- **Factual integrity**: Never fabricate experience, skills, or metrics not in candidate.md.
- **Page limit**: 1 page (0–3 years experience), 2 pages (4–10 years), up to 3 pages (10+ years, senior roles). Per Labeeb.ae 2026.
- **Visa and nationality are required**: These fields are not optional for UAE applications. Employers need them for sponsorship assessment and Emiratization compliance. Never omit.
- **Implied first person**: No "I," "my," or third-person references throughout.
- **AED-denominated metrics**: Where authentic, financial metrics in AED rather than foreign currencies signal local market familiarity and are ATS-positive on regional portals.
- **UAE/GCC keyword signals**: Naturally embed GCC/UAE-relevant keywords where authentic — "Vision 2031," "UAE D33 agenda," "Emiratisation-aware," "GCC regional," zone names (DIFC/ADGM/RERA/DHA/CBUAE, role-relevant only).
- **Cultural guidelines**: Do not mention religion on the CV. Do not reference personal connections (wasta). Do not use UAE flag colors (green #00732F) as a CV design accent. Avoid any content that could be construed as political commentary.
- **En-dash for date ranges**, middle dot (·) for skill separators.
- **Arabic name**: السيرة الذاتية (al-sīra al-dhātiyya) is the Arabic term; "CV" is the universal English term used across all UAE platforms and should be used in English-language documents.
