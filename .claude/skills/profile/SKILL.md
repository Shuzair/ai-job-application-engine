---
name: profile
description: Create, improve, audit, or add to the candidate.md profile. Use this skill when the user wants to build or refine their professional profile. Suggested keywords in user message — Create, Improve, Audit, Add — but natural language works too.
disable-model-invocation: true
---

# /profile — Manage Candidate Profile

You manage `candidate.md` — the single source of truth for all CV and cover letter generation.

Read the user's message after `/profile` to determine intent. Suggested keywords:
- **Create** — build candidate.md from scratch via guided interview
- **Improve** — rewrite for quality AND fill gaps in one pass
- **Audit** — read-only analysis, report what's missing or weak
- **Add** — append a new experience, project, certification, education, or language

If the intent is ambiguous, ask the user which mode they want.

---

## Candidate.md Structure

The agents expect these sections in this exact order and format. Every mode must produce output matching this structure. Consistency across users is critical — the agents parse by header levels and `**Key:** Value` patterns.

### Header Hierarchy

- `#` — document title only (`# Candidate Profile`)
- `##` — top-level sections (Personal Details, Target, Communication Style, Personal Narrative, Professional Experience, Personal Projects, Education, Certifications, Languages)
- `###` — individual entries within a section (each job, each project, each certification)
- `####` — sub-areas within an entry (responsibilities, projects within a job)
- `#####` — named sub-projects within a sub-area

### Key-Value Fields

Always use `**Key:** Value` on a single line. No variations (no colons without bold, no bullet-prefixed keys). This makes extraction reliable.

### Section Separators

Use `---` between top-level `##` sections only. Never within a section.

### Exact Template

Every `candidate.md` must follow this structure. Items in `[brackets]` are placeholders.

```markdown
# Candidate Profile

## Personal Details

**Name:** [Full Name]
**Location:** [City, Country]
**Email:** [email@example.com]
**Phone:** [+country code number]
**LinkedIn:** [full LinkedIn URL]
**GitHub:** [full GitHub URL or "N/A"]

---

## Target

**Roles:** [Role 1, Role 2, Role 3]
**Target Regions:** [Country 1, Country 2, Country 3]
**Relocation:** [e.g. "Ready to relocate to Europe" or "Already based in Germany"]
**Visa Note:** [e.g. "EU citizen" or "Eligible for Germany Chancenkarte" or "Requires sponsorship"]

---

## Communication Style

- [Tone preference 1]
- [Tone preference 2]
- [Tone preference 3]

---

## Personal Narrative

Personal stories that give cover letters and CVs a genuine human angle. Each entry is a short paragraph (2-5 sentences) under a descriptive `###` heading. There is no fixed list — add whatever stories are relevant to the candidate.

Common themes include (but are not limited to): origin story, career motivation, relocation reasons, defining career moments, workplace values, why a specific industry, mentorship philosophy, side passions that inform work, cultural background, personal challenges overcome.

### [Story Title]
[2-5 sentences — the real version, not the polished one]

### [Story Title]
[2-5 sentences]

---

## Professional Experience

### Experience 1: [Job Title] at [Company Name] ([Month Year] – [Month Year or Present])

**HQ:** [Company HQ city, Country — or leave empty]
**Location:** [Candidate's physical work location, city/country — or leave empty]
**Work Model:** [Remote / Hybrid / On-site — or leave empty]

[1-2 paragraph company context: what the company does, product, size, industry, team structure, reporting line]

#### 1. [Responsibility or Project Area Name]

- [Bullet describing what was done, with scale/metrics]
- [Bullet describing what was done, with scale/metrics]

##### I. [Named Sub-Project] (if applicable)

[1-2 line context: what the problem was, why it mattered]

- [Action + result bullet with metrics]
- [Action + result bullet with metrics]

### Experience 2: [Job Title] at [Company Name] ([Month Year] – [Month Year])

**HQ:** [Company HQ city, Country — or leave empty]
**Location:** [Candidate's physical work location, city/country — or leave empty]
**Work Model:** [Remote / Hybrid / On-site — or leave empty]

[Same structure as above]

---

## Personal Projects

### 1. [Project Name]

**GitHub:** [URL or "Private"]
**Tech Stack:** [Tool 1, Tool 2, Tool 3]
**Status:** [Complete / In Progress / Early Stages]

[1-2 paragraph description: what it is, what problem it solves, architecture overview]

#### I. [Sub-area or feature] (if applicable)

- [Detail bullet]
- [Detail bullet]

---

## Education

**[Degree Title]** — [University Name]
[City, Country] | [Year or Expected Year]

**[Degree Title]** — [University Name]
[City, Country] | [Year]

---

## Certifications

### 1. [Certification Name]

**Issuing Body:** [Organization]
**Issued:** [Month Year] | **Expires:** [Month Year or "No expiry"]
**Credential ID:** [ID]
**Verify:** [URL]

---

## Languages

**[Language]:** [CEFR Level] · **[Language]:** [CEFR Level or "Native"]
```

### Structure Rules

1. **Experiences are numbered sequentially** — `### Experience 1`, `### Experience 2`, etc. Most recent first.
2. **Sub-areas within an experience use `####`** with Arabic numerals — `#### 1.`, `#### 2.`
3. **Named sub-projects use `#####`** with Roman numerals — `##### I.`, `##### II.`
4. **Personal projects are numbered** — `### 1.`, `### 2.`
5. **Every experience must include:** job title, company name, date range in the `###` header, **HQ** / **Location** / **Work Model** fields (all three must be present even if left empty), company context paragraph, at least one `####` sub-area
6. **Every project must include:** GitHub link (or "Private"), tech stack as comma-separated list, status field
7. **Certifications are numbered** — `### 1.`, `### 2.`
8. **Education entries use bold degree, em-dash, university** on one line
9. **Languages are on a single line** separated by middle dots (·)
10. **Personal Narrative entries use `###`** with descriptive titles. Each is a short paragraph (2-5 sentences), not bullets. No fixed list — any number of stories is valid.

---

## Mode: Create

Build `candidate.md` from scratch through a guided interview. Walk through each section one at a time.

**Escape hatch:** If the user pastes a full resume, LinkedIn export, or bulk text instead of answering questions, parse it directly into the candidate.md structure. Then run depth coaching on each section to fill gaps before writing the file.

### Interview Flow

Ask questions for one section at a time. Do NOT move to the next section until the current one has enough depth. After each section, summarize what you captured and confirm with the user before proceeding.

**Section 1 — Personal Details:**
- Full name
- Current location (city, country)
- Email, phone
- LinkedIn URL, GitHub URL (if applicable)

**Section 2 — Target:**
- What roles are you targeting? (e.g., Data Engineer, Analytics Engineer)
- Which countries or regions? (e.g., Netherlands, Germany, EU-wide)
- Are you ready to relocate? Timeline?
- Visa status — do you have EU work authorization, Chancenkarte, or need sponsorship?

**Section 3 — Communication Style:**
- How do you want your cover letters to sound? (e.g., direct, warm, technical, concise)
- Any phrases or tones you want to avoid?

**Section 4 — Personal Narrative:**

This section captures the human stories behind the career — material the cover letter agent uses to make openings and closings feel genuine and personal.

There is no fixed list of stories. Ask open-ended questions to surface what's real and personal. Start with:

1. **How did you get into this field?** What's the real story — not the resume version?
2. **What drives you?** What kind of problems make you lose track of time?
3. **Is there a personal reason behind your job search?** (relocation, career change, industry switch, lifestyle — whatever applies)
4. **Was there a turning point in your career?** A risk you took, a failure you learned from, a moment that changed how you work?
5. **What matters to you in a workplace?** (autonomy, mentorship, ownership, craft, impact — whatever resonates)
6. **Anything else that shapes who you are professionally?** (side passions, cultural background, personal challenges, mentorship philosophy)

Not every question will apply to every candidate. Skip what doesn't resonate. Add follow-ups for what does. The goal is 3-6 authentic stories, each 2-5 sentences.

Title each story descriptively based on what the user shares (e.g., "How I Found Data Engineering", "Why I Value Autonomy", "Moving to Europe") — not generic labels.

**Section 5 — Professional Experience (repeat per role):**

Start with: "Let's go through your work experience, starting with your most recent role."

For each role, ask:
1. Job title and company name
2. Date range (month/year to month/year)
3. **HQ, location, and work model:** Where is the company headquartered? Where did you physically work from? Was the role remote, hybrid, or on-site? All three fields are optional — if the candidate doesn't want to include any of them, leave that field empty in the profile.
4. **Company context:** What does the company do? What's their product? How big is the company? What industry?
5. **Team structure:** How large was your team? Who did you report to? Matrix or direct reporting?
6. **Day-to-day scope:** What were your core responsibilities? What systems/tools did you work with daily?
7. **Key projects:** Walk me through 2-3 significant things you built or delivered.

For each project, apply **depth coaching** (see below).

After capturing all roles, ask: "Any other roles, or should we move on?"

**Section 6 — Personal Projects:**

For each project:
1. What is it? What problem does it solve?
2. What's the tech stack?
3. What's the current status — complete, in progress, early stages?
4. GitHub link?

Apply depth coaching for architecture and technical decisions.

**Section 7 — Education:**
- Degree title, university name, city/country, year
- Multiple degrees? Most recent first.
- Any exceptional grades worth mentioning?

**Section 8 — Certifications:**
- Certification name, issuing body, date, expiry (if any)
- Credential ID and verification link

**Section 9 — Languages:**
- Which languages do you speak?
- For each: what CEFR level? (If the user doesn't know CEFR, help them estimate: "Can you hold a professional meeting in German?" → B2+)

### After all sections

Write `candidate.md` to the project root. Then run the **Audit checklist** (see below) against the file you just created and report any remaining gaps.

---

## Mode: Improve

**Backup:** Before making any changes, copy the current `candidate.md` to `candidate.backup.md` in the project root. If `candidate.backup.md` already exists, overwrite it. This ensures the user can recover the previous version if the rewrite goes wrong.

Read the existing `candidate.md`. Then do two things in one pass:

### 1. Rewrite for quality

- Strengthen vague language — "worked on data pipelines" → "managed 25 data pipelines processing 5M+ records daily"
- Ensure consistent structure across all experience entries
- Add company context paragraphs where missing
- Verify each project has: situation/problem, what was built, measurable result
- Check bullet phrasing uses strong action verbs

### 2. Fill gaps via depth coaching

For each experience and project, check:
- Are there quantified metrics? (data volume, runtime reduction, cost savings, team size, user count)
- Is the tech stack explicitly named? (not "cloud platform" but "AWS Lambda, Step Functions, S3")
- Is the business impact stated? (not just "built X" but "built X which reduced Y by Z%")
- Is the team context clear? (size, reporting structure, individual vs team contribution)

For every gap found, ask the user directly:
> "Your [role/project] at [company] mentions [vague claim]. Can you tell me:
> - How much data / how many users / what scale?
> - What was the before vs after?
> - Were you leading this or contributing as part of a team?"

Wait for the user's answers before rewriting. Do NOT invent details.

After collecting answers, rewrite the affected sections and present the changes for confirmation before writing to file.

---

## Mode: Audit

Read `candidate.md` but do NOT modify it. Analyze and report:

### Completeness Checklist

Check each section exists and has content:
- [ ] Personal Details (name, location, email, phone, LinkedIn)
- [ ] Target (roles, regions, relocation, visa)
- [ ] Communication Style
- [ ] Personal Narrative (at least 3 personal stories with descriptive titles)
- [ ] Professional Experience (at least one role)
- [ ] Personal Projects (at least one)
- [ ] Education (at least one entry)
- [ ] Certifications (if any — note if section is missing)
- [ ] Languages with CEFR levels

### Depth Analysis — per experience entry

For each role, check and report:
- Has company context paragraph? (what the company does, size, industry)
- Has team structure? (team size, reporting line)
- Has date range? (month/year format)
- Has quantified metrics? (count how many bullets have numbers)
- Has explicit tech stack? (named tools, not categories)
- Has business impact? (revenue, cost, performance, efficiency outcomes)
- Number of projects/sub-sections under this role

### Depth Analysis — per project

For each personal project, check:
- Has problem statement?
- Has tech stack listed?
- Has current status?
- Has GitHub link?

### Holes and Weaknesses

Flag specific problems:
- "Your role at [Company] has no metrics — the CV agent will have nothing to quantify"
- "Project [X] lists no tech stack — the CV agent needs this for ATS keyword matching"
- "Education section has no dates — European CVs require these"
- "No Languages section — European employers expect CEFR levels"
- "Personal Narrative is missing — the cover letter agent needs personal stories to write authentic openings"
- "Personal Narrative has only 1 entry — aim for at least 3 to give the cover letter agent enough material to choose from"
- "Experience at [Company] has 8 bullets but none mention scale or impact"

### Score

Give an overall readiness score:
- **Ready** — all sections present, all experiences have depth, agents can produce strong output
- **Mostly ready** — minor gaps that won't block output but will weaken it
- **Needs work** — significant gaps that will produce generic CVs. List what to fix first.

---

## Mode: Add

**Backup:** Before making any changes, copy the current `candidate.md` to `candidate.backup.md` in the project root. If `candidate.backup.md` already exists, overwrite it.

The user wants to append a new entry to an existing section. Determine what they want to add from their message:
- New experience/role
- New project
- New certification
- New education entry
- New language
- New personal narrative entry (or update an existing one)

### Process

1. Read the existing `candidate.md` to understand the current structure and depth level
2. Ask guided questions for the new entry — same depth as Create mode
3. Apply **depth coaching** — push for metrics, tech stack, team context, business impact
4. Match the writing style and structure of existing entries in the file
5. Present the new section to the user for confirmation
6. Append it in the correct location within `candidate.md` (experiences in reverse chronological order, projects numbered sequentially, etc.)

The new entry must meet the same quality bar as existing content. If the user gives thin answers, push back:
> "This is lighter than your other entries. Your [existing role] has company context, team structure, and 3 detailed projects with metrics. Can we add similar depth here?"

---

## Depth Coaching Questions

Use these when detail is insufficient during Create, Improve, or Add. Ask the relevant subset, not all at once.

**For any project or responsibility:**
- What problem were you solving? Why did it matter to the business?
- What was the scale? (data volume, user count, number of systems, team size)
- What tech stack did you use? Name specific tools and frameworks.
- What did you personally own vs what was team effort?
- What was the measurable outcome? (before/after metrics, cost savings, time reduction, revenue impact)
- How long did this take? (timeline context)

**For leadership/mentorship claims:**
- How many people did you mentor/lead?
- What was the outcome of mentorship? (Did they become independent? Get promoted?)
- Was this formal or informal?

**For migrations/optimizations:**
- What was the before state? (old tech, old performance numbers)
- What was the after state? (new tech, new performance numbers)
- What was the percentage improvement?
- Any downtime or data loss during transition?

**For client-facing work:**
- How many clients? What size/industry?
- What was the revenue impact or ARR involved?
- Any direct client feedback worth recording?

---

## Hard Rules

- **NEVER fabricate** details. You can rephrase and restructure the user's words, but every fact must come from the user.
- **NEVER invent** metrics, technologies, project outcomes, or team sizes.
- During Create and Add, if the user gives vague answers, ask follow-up questions — do not fill in plausible-sounding details.
- During Improve, flag gaps and ask — do not silently add information.
- Always confirm changes with the user before writing to `candidate.md`.
