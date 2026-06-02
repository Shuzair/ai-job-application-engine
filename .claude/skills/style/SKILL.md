---
name: style
description: "Create a new country or region-specific CV and cover letter style. Scaffolds 6 template files from the best available base, researches local norms online, then edits each file with country-specific customizations. Each generated style is complete and standalone — no inheritance."
disable-model-invocation: true
argument-hint: "<country|region>"
---

User-provided arguments: $ARGUMENTS

# /style — Create Country/Region Style

Scaffolds style files from the best available base, researches CV and cover letter conventions, then edits each file with country-specific customizations. Every generated file is self-contained — no style inherits from or overrides another.

**Philosophy:** Template files are created first (always valid defaults), then research drives targeted edits. If research is insufficient for any section, the default value remains — the style is always functional.

**Error handling:** If any step fails, stop and tell the user what went wrong.

## Step 1: Validate Input

```bash
python scripts/run.py scripts/validate_style_input.py --identifier "$ARGUMENTS"
```

**Handle the result:**

- **`error` is not null** → show the error message and stop.
- **`correction` is not null** → ask: "Did you mean **{correction}**? (yes/no)". Stop if no.
- **`cv_style_exists` or `cl_style_exists` is true** → ask: "Style files for `{identifier}` already exist. Overwrite? (yes/no)". Stop if no.

Save `identifier`, `type`, `region`, `region_cv_style_exists`, and `region_cl_style_exists` from the output — used by later steps.

## Step 2: Scaffold Template Files

```bash
python scripts/run.py scripts/scaffold_style.py --identifier "{identifier}" --type "{type}" [--region "{region}"]
```

This creates 6 files by copying from the best available base:
- **Country**: copies from region style if it exists, otherwise from default
- **Region**: copies from default

Files created:
- `.claude/skills/cv-style-{identifier}/SKILL.md` — CV writing rules (stub with `[CUSTOMIZE]` markers)
- `.claude/skills/cv-style-{identifier}/cv-format.yaml` — CV visual config (copied from base, with `[CUSTOMIZE]` hints injected on key lines)
- `.claude/skills/cv-style-{identifier}/cv-data-schema.yaml` — CV data validation (copied from base)
- `.claude/skills/cl-style-{identifier}/SKILL.md` — CL writing rules (stub with `[CUSTOMIZE]` markers)
- `.claude/skills/cl-style-{identifier}/cl-format.yaml` — CL visual config (copied from base, with `[CUSTOMIZE]` hints injected on key lines)
- `.claude/skills/cl-style-{identifier}/cl-data-schema.yaml` — CL data validation (copied from base)

All files are immediately valid — they're working defaults that will be customized in Step 3.

**Handle the result:**
- If `error` is not null, show the error message and stop.
- Otherwise, proceed to Step 3.

## Step 3: Research & Edit

Research the country/region's CV and CL conventions online, organized by topic. For each topic: research first, then apply findings by editing the scaffolded files.

### Source Hierarchy

Search in priority order. Tier 1 findings override lower tiers when they conflict.

**Tier 1 — Official:** Government career portals, national labor ministry guidelines, national standards (e.g., DIN 5008), national qualification frameworks.

**Tier 2 — Authoritative:** Major job platforms (StepStone, Indeed, LinkedIn regional, XING, Bayt, local equivalents), top university career services, Europass, professional recruitment associations.

**Tier 3 — Expert Opinion:** International recruitment firms (Hays, Robert Half, Michael Page), expat platforms (Expatica, InterNations), established career coaching sites.

### Topic A: Page Setup & Typography

**Research:** Page size (A4 vs Letter), popular fonts (list 3-5 alternatives), standard font sizes (with min–max ranges), margin sizes (with ranges), line spacing, color usage (list 3-4 popular hex values). Also research header formatting norms: name sizing ranges, whether bold/uppercase names are standard, sub-header font size ranges, whether relocation statements are common.

**Comment format:** Every comment MUST include **suggested ranges or alternatives**, not just explanations. Examples:
- Margins: `# cm — Suggested range: 1.5–2.5cm. AFNOR recommends minimum 2cm`
- Font sizes: `# pt — Suggested range: 14–20pt. French standard: 16pt`
- Fonts: `# Popular heading fonts in France: Calibri, Garamond, Arial, Cambria`
- Colors: `# Popular in France: #1F3864 (dark navy), #2E74B5 (steel blue), #2C3E50 (charcoal blue)`
- Options: `# French preference: uppercase. Options: upper, title, as-is`

**Edit files:**
- `cv-format.yaml` → update `page`, `header` (all font sizes, colors, bold, case, show_titles, relocation fields), `typography`, `skills` (separator), `languages` (separator), `colors` sections. Every `[CUSTOMIZE]` hint must be replaced with a country-specific comment that includes **suggested ranges, alternative values, or option lists**
- `cl-format.yaml` → mirror the CV values across all matching sections (`page`, `header`, `typography`, `colors`). Every CL `[CUSTOMIZE]` hint must get a comment with ranges/alternatives (or "Must match CV" with the matching range)

### Topic B: Header & Personal Information

**Research:** Is a photo required/expected/discouraged? Date of birth — yes/no + format? Nationality, marital status, address format? Visa/work permit statement? Any other country-specific header fields?

**Edit files:**
- CV `SKILL.md` → edit the Header section (### 1. Header) — replace `[CUSTOMIZE]` with specific field requirements
- `cv-format.yaml` → if photos are expected, uncomment and configure the `header.photo` block
- `cv-data-schema.yaml` → add/remove header properties (photo_path, date_of_birth, nationality, etc.)
- `cl-data-schema.yaml` → adjust header properties if needed

### Topic C: CV Structure & Sections

**Research:** Standard section order? Country-specific sections (Hobbies/Interests, References, Self-PR, Military Service, Volunteer Work, Personal Statement)? What detail level for each? Section heading names (local language AND English equivalents)? How many skill category buckets are standard (max 6)? What are the local bucket names for the job market (e.g., technical vs soft skills grouping)?

**Edit files:**
- `cv-format.yaml` → **Add or remove sections** from `sections.order` based on research (the base only provides a starting point — you MUST customize it for the country). Add local-language heading names as inline comments next to each heading (e.g., `experience: "Work Experience"  # Erhvervserfaring`). Add `section_types` entries for any new sections (inline/list/paragraph)
- `cv-data-schema.yaml` → add properties for any country-specific sections (choose correct data type: string array for keyword lists, string for paragraphs, object array for structured entries like references)
- CV `SKILL.md` → add subsections for each country-specific section after Languages. Define the skill bucket names in ### 3 (Skills) — replace the `[CUSTOMIZE]` marker with up to 6 country-appropriate category names. Do NOT change the data collection philosophy (collect → match → expand → discard → distribute) or the JD Signal List back-reference in the Match step — only customize the bucket names and count.
- **Projects section**: If research shows this country's job market values personal or side projects (common in tech-forward markets like Denmark, Netherlands, Nordic region), add a `### Projects` section modeled on `cv-style-denmark`. Gate projects by JD Signal List: "Reference your JD Signal List. Include a project only if it directly demonstrates a skill or domain from a named signal. A technically impressive project that addresses no named JD signal should be omitted." If the market does not value side projects (e.g., France, Germany, traditional corporate markets), omit this section — projects can be referenced as bullets within Professional Experience instead.

### Topic D: Professional Experience & Tone

**Research:** Date format (DD.MM.YYYY, MM/YYYY, Mon YYYY)? Bullet writing rules — max words, action verbs, quantification norms? Bullets per role (recent vs older roles)? Company description norms? Tone — formal/direct/humble/team-oriented? Personal pronouns — implied first person, "I", or third person? ATS adoption level? How should JD terminology be mirrored in bullet phrasing?

**Edit files:**
- CV `SKILL.md` → edit Professional Summary (### 2), Professional Experience (### 4) sections — replace `[CUSTOMIZE]` markers with country-specific presentation rules. Do NOT change the data collection philosophy or the JD Signal List back-references in the ranking/prioritization steps — only customize format (date style, word count, bullet count, tone, action verbs, pronoun usage).
- `cv-format.yaml` → update `experience.show_company_description`, `experience.max_bullets_per_role`, `validation` limits

### Topic E: Education, Certifications & Languages

**Research:** Local grading system? When to include GPA? Degree equivalence? Thesis/coursework inclusion? High school — include or exclude? Country-specific certifications that carry weight? Language proficiency scale (CEFR, JLPT, TOPIK, IELTS)?

**Edit files:**
- CV `SKILL.md` → edit Education (### 5), Certifications (### 6), Languages (### 7) sections — replace `[CUSTOMIZE]` markers with country-specific format rules. For Certifications, do NOT change the JD Signal List mapping gate (the "map each cert to a named signal, discard if you can't" logic) — only customize display format and add locally-valued cert examples. **Preserve the inherited architecture**: do NOT move the gate from a Data Collection Philosophy section into CV Sections (or vice versa) — the gate's location is determined by the base style and must remain as-is.

### Topic F: Cover Letter Conventions

**Research:** Expected length — word count range + page limit? Paragraph count (3, 4, 5-6)? Addressing conventions — formal title, first name, "Dear Sir/Madam", local equivalent? Sign-off phrases — local language + English? Tone — formal/warm/direct/humble? Is English acceptable or must it be in the local language? Content expectations — what must be included, what is inappropriate? Is a cover letter always expected or sometimes optional? Date placement (left or right)? Paragraph spacing norms?

**Edit files:**
- CL `SKILL.md` → edit Structure section (adjust paragraph count/word range), each Paragraph subsection, Addressing and Sign-off, Tone Rules, What NOT to Include — replace all `[CUSTOMIZE]` markers
- `cl-format.yaml` → update `date` (alignment), `body` (paragraph spacing), `sign_off` (closing_text — provide local language + English), `validation` limits (min/max paragraphs, word counts). Every `[CUSTOMIZE]` hint must be replaced with a comment that includes **suggested ranges or alternatives** (e.g., `# Suggested range: 100–160 twips`, `# Alternatives: "Cordialement,", "Kind regards,"`)
- `cl-data-schema.yaml` → update `paragraphs.minItems`/`maxItems`, `date.description`, `salutation.description`, `sign_off.properties.closing.description`

### Topic G: Additional Country-Specific Norms

**Research:** Look for anything NOT covered by Topics A-F that is specific to this country's job application culture. Examples:
- Whether CVs are called something different locally (Lebenslauf, 履歴書, السيرة الذاتية)
- Anti-discrimination laws that affect CV content
- Cultural taboos in job applications
- Industry-specific norms (if the country has dominant industries)
- Specific formatting standards or regulations (DIN 5008 in Germany, etc.)
- Whether handwritten cover letters are ever expected
- Regional differences within the country

**Edit files:** Apply findings to whichever files they affect — CV `SKILL.md` Critical Rules section, CL `SKILL.md` Critical Rules section, or format/schema files as needed.

### Quality Standards for Edits

- Every edit must be backed by research — cite the source inline (e.g., "Per DIN 5008, left margin should be 2.5cm")
- **Every `[CUSTOMIZE]` marker must be replaced with a country-specific comment — NEVER delete a marker without adding a comment.** Even if the default value is kept unchanged, add a comment explaining why it's appropriate
- **Format YAML comments MUST include actionable suggestions**, not just explanations:
  - **Numeric fields** (font sizes, margins, spacing): include `Suggested range: X–Y` (e.g., `# pt — Suggested range: 9–12pt. Danish standard: 11pt`)
  - **Font fields**: list 3-5 popular alternatives (e.g., `# Popular in Denmark: Calibri, Arial, Garamond, Cambria`)
  - **Color fields**: list 2-4 popular hex values with names (e.g., `# Popular: #1F3864 (dark navy), #2E74B5 (steel blue), #2C3E50 (charcoal)`)
  - **Boolean/enum fields**: list all options (e.g., `# Options: upper, title, as-is`)
  - **String fields** (closing_text, separator): provide local language + English alternatives
- After editing each format YAML section, scan for any remaining fields WITHOUT comments and add one — no field should be left uncommented
- Include good vs bad examples where country norms differ significantly from defaults
- If a country norm conflicts with ATS best practices, note the tension and recommend a pragmatic approach
- After all edits, verify no `[CUSTOMIZE]` markers remain in any file
- **JD Signal List integrity check**: Verify the CV `SKILL.md` Pre-work section still contains the JD Signal List instruction, and that the Skills, Certifications, Experience, and Projects sections still reference it. These must never be removed during customization — they are the core filtering mechanism.

## Step 4: Update style-resolution.yaml

```bash
python scripts/run.py scripts/update_style_resolution.py --identifier "{identifier}" --type "{type}" [--region "{region}"] [--countries "country1,country2"] [--alias "alias:target"]
```

- **Country**: adds it to the region's country list alphabetically. If `--region` was not provided by Step 1 (type was "new"), determine the region from research and pass it.
- **Region**: creates the region key with a countries list populated from research. Add relevant aliases if applicable (e.g., `--alias "gcc:middle-east"`).

The script is idempotent — it skips if the entry already exists.

**Handle the result:**
- If `error` is not null, show the error message and stop.
- Check the `updated` field: if false and error is null, it means the entry already existed. That's fine — proceed to Step 5.
- Otherwise, proceed to Step 5.

## Step 5: Report

Tell the user:

1. **Files created:** List all 6 file paths
2. **Base used:** Which style was used as the scaffold source (e.g., "Copied from `cv-style-europe`")
3. **Research summary:** 8-12 bullet points covering the most important findings
4. **Key differences from base style:** What was customized vs left at defaults
5. **Sources used:** Group by tier
6. **Sections left at defaults:** List any sections where research was insufficient and defaults remain
7. **style-resolution.yaml:** Whether it was updated and what was changed

Then ask:
> Please review the generated files. If any changes are needed, tell me and I'll update them now.

If the user requests changes, apply them directly to the relevant files. Do NOT re-run research — make targeted edits based on feedback.
