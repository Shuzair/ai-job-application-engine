---
name: revise
description: Make targeted edits to an existing CV or cover letter draft — content or formatting. Content edits change text in the YAML data (e.g., "reword the summary", "add metrics"). Format edits change visual settings like fonts, sizes, margins, colors, and spacing (e.g., "make font bigger", "reduce margins"). Auto-re-renders the docx after every edit.
disable-model-invocation: true
argument-hint: "<cv|cl> [folder_name] \"feedback\""
---

User-provided arguments: $ARGUMENTS

# /revise — Targeted Draft Revision (Content & Formatting)

Make targeted edits to an existing draft based on user feedback. Unlike `/rerun`, this does NOT regenerate from scratch — it modifies the existing draft while preserving everything the user hasn't asked to change.

Supports two types of edits:
- **Content edits:** Change text in `cv-data.yaml` or `cl-data.yaml` (e.g., "reword the summary", "add metrics to Afiniti role")
- **Format edits:** Change visual settings in a per-application override file (e.g., "make font bigger", "reduce margins", "change heading color"). Format changes are scoped to the current application only — they do not modify the global style.

**Error handling:** If any step fails, stop and tell the user what went wrong.

## Step 1: Parse Arguments

Parse `$ARGUMENTS` to extract:
- `agent` — which draft to revise: `cv` or `cl`
- `folder` — optional folder name in `job-applications/output/`
- `feedback` — the user's revision instructions (everything after the agent and optional folder)

**Argument validation:** The first word MUST be `cv` or `cl`. If it's not, stop and tell the user:
> Usage: `/revise <cv|cl> [folder_name] "your feedback here"`
>
> Examples:
> - `/revise cv "make the summary more technical"`
> - `/revise cl germany_wemolo_senior-analytics-partner-operations_v1 "tone down the opening paragraph"`

If no folder is provided:
- Scan `job-applications/output/` for the most recently modified folder
- Confirm with the user: "Revising **$agent** draft in **[folder_name]** — is that correct?"

If the folder doesn't exist, stop and list available folders.

## Step 2: Validate Prerequisites

Before reading, check that required files exist:
- `candidate.md` must exist at the project root
- The target data file must exist: `cv-data.yaml` (if revising `cv`) or `cl-data.yaml` (if revising `cl`)
- `input.md` must exist in the application folder
- If revising `cl`, `cv-data.yaml` must also exist (needed for consistency checks)

If any file is missing, stop and tell the user which file is missing and why it's needed. For a missing data file, suggest running `/rerun <agent> [folder]` first to generate it.

## Step 3: Read Context

Read these files:
1. `candidate.md` from the project root — to verify any new claims are factually grounded
2. The target data file (`cv-data.yaml` or `cl-data.yaml`) from the application folder
3. `input.md` from the application folder — for JD context
4. `research.md` from the application folder — for company context

If revising `cl`, also read `cv-data.yaml` to maintain consistency between documents.

## Step 4: Load Style Skill

Resolve and load the correct style skill using the script. Parse `input.md` from the folder first:

```bash
python scripts/run.py scripts/parse_input.py --input <folder_path>/input.md
python scripts/run.py scripts/resolve_style.py --location "<location>" [--style "<style>"]
```

- If revising `cv`: Load the resolved CV style skill (the `cv_style_skill` value from the script output, e.g., `cv-style-europe`). Apply its rules throughout.
- If revising `cl`: Load the resolved CL style skill (the `cl_style_skill` value from the script output, e.g., `cl-style-europe`). Apply its rules throughout.

## Step 5: Classify Edit Type

Scan the user's feedback text to determine whether this is a **content edit** or a **format edit**.

**Format keywords** — if the feedback contains any of these, it is a format edit:
font, size, margin, spacing, color, bold, underline, italic, heading, order, layout, bigger, smaller, wider, narrower, separator, alignment, pt, cm, indent, case, upper, lower, title, photo, border, line height, line-spacing, gap, padding

**Content keywords** — if none of the above are present, it is a content edit:
summary, paragraph, bullet, skills, experience, tone, rewrite, add, remove, shorten, lengthen, technical, metrics, reword, rephrase

If truly ambiguous (e.g., "make the headings better" could mean restyle or rewrite), ask the user: "Are you asking to change the content or the visual formatting?"

- If **content edit** → proceed to Step 6-C
- If **format edit** → proceed to Step 6-F

## Step 6-C: Apply Content Revisions

Apply the user's feedback as targeted edits to the YAML data:

- **Only change what the user asked to change.** Do not rewrite sections the user didn't mention.
- **Preserve the YAML structure** — same keys, same schema, valid YAML syntax.
- **Verify factual integrity** — any new claims must trace back to `candidate.md`. Never fabricate.
- **Maintain ATS compliance** — don't remove JD keywords that were intentionally placed.
- **Keep within length limits** — CV: content for 2 pages max. Cover letter: 250-400 words across paragraphs.

Common revision types:
- "Make the summary more technical" → rewrite only the `summary` field
- "Change paragraph 2 to focus on X" → rewrite only `paragraphs[1]`
- "Tone down the opening" → rewrite only `paragraphs[0]`
- "Add more metrics to the Afiniti section" → edit only those `bullets` in the relevant experience entry
- "Reorder skills to emphasize Python" → reorder only the `skills` entries

Write the updated data file (`cv-data.yaml` or `cl-data.yaml`). Ensure valid YAML.

Then proceed to Step 7.

## Step 6-F: Apply Format Revisions

Format edits create or update a **per-application override file** in the application folder. This override is deep-merged on top of the base style config at render time. The global style files are never modified.

1. Read the base format config from the resolved style path:
   - If revising `cv`: read the file at `cv_config` path from Step 4
   - If revising `cl`: read the file at `cl_config` path from Step 4

2. Read the existing override file from the application folder if it exists:
   - CV: `<folder_path>/cv-format-override.yaml`
   - CL: `<folder_path>/cl-format-override.yaml`
   - If no override exists yet, start with an empty dict

3. Map the user's natural language request to specific YAML config keys. The override file uses the same nested structure as the base format config. Examples:

   | User says | Override YAML |
   |-----------|--------------|
   | "make font bigger" / "increase font size" | `typography: { body_size: <current + 1> }` |
   | "use 11pt font" | `typography: { body_size: 11 }` |
   | "use Arial" | `typography: { heading_font: Arial, body_font: Arial }` |
   | "reduce margins" | `page: { margins: { top: <current - 0.5>, bottom: <-0.5>, left: <-0.5>, right: <-0.5> } }` |
   | "set left margin to 1.5cm" | `page: { margins: { left: 1.5 } }` |
   | "change heading color to navy" | `colors: { primary: "#001F3F" }` |
   | "make headings not underlined" | `sections: { heading_underline: false }` |
   | "increase line spacing" | `typography: { line_spacing: <current + 0.15> }` |
   | "move education before experience" | `sections: { order: [summary, skills, certifications, education, experience, languages] }` |
   | "make name bigger" | `header: { name_font_size: <current + 2> }` |
   | "hide company descriptions" | `experience: { show_company_description: false }` |

   When a user says "bigger" / "smaller" without a specific value, read the current value from the base config (or existing override) and adjust by a reasonable increment.

4. Merge the new changes into the existing override dict (preserving previous overrides for other keys).

5. Write the override file to the application folder as `cv-format-override.yaml` or `cl-format-override.yaml`.

Then proceed to Step 7.

## Step 7: Re-render and Open

After any edit (content or format), re-render the affected document. Use the style paths from Step 4:

```bash
python scripts/run.py scripts/render.py --type <cv|cl> \
  --data-dir <folder_path> \
  --cv-config <cv_config> \
  --cl-config <cl_config> \
  --cv-schema <cv_schema> \
  --cl-schema <cl_schema>
```

Note: Always pass both `--cv-config`/`--cv-schema` and `--cl-config`/`--cl-schema` even when rendering only one type — the script ignores unused ones. The `--type` flag controls which document is actually rendered.

Then open the re-rendered file:

```bash
open <folder_path>/cv.docx       # if revising cv
open <folder_path>/cover-letter.docx  # if revising cl
```

## Step 8: Report Back

Tell the user:

**For content edits:**
1. What was changed (list specific sections/paragraphs modified)
2. What was preserved (confirm untouched sections)
3. If revising the cover letter, note the updated word count
4. "Document re-rendered and opened."
5. "Run `/format [folder]` when ready to finalize as PDF."

**For format edits:**
1. What settings were changed — show old → new values (e.g., `body_size: 10pt → 11pt`)
2. Print the full format settings summary using this template (reading values from the base config merged with the override):

```
--- Format Settings (<style_name>) ---
Page:         <size>, margins <top>/<bottom>/<left>/<right> cm
Fonts:        <heading_font> (headings), <body_font> (body)
Sizes:        <body_size>pt body, <heading_size>pt headings, <name_font_size>pt name
Spacing:      <line_spacing>x line
Colors:       primary <primary>, body <body>, link <link>
CV Sections:  <order joined with " > ">
Headings:     <heading_case>, bold=<yes/no>, underline=<yes/no>
Experience:   max <n> bullets/role, descriptions=<shown/hidden>
CL Paragraphs: <min>-<max> paragraphs
```

3. "Document re-rendered and opened."
4. "Run `/format [folder]` when ready to finalize as PDF."
