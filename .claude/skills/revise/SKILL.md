---
name: revise
description: Make targeted edits to an existing CV or cover letter — content (wording, what is included) or formatting (fonts, sizes, margins, colors, spacing, section order). Re-renders docx and pdf after every edit.
disable-model-invocation: true
argument-hint: "[cv|cl] [folder_name] feedback"
---

User-provided arguments: $ARGUMENTS

# /revise — Targeted Revision

Change only what the user asked for and keep everything else as it is. This never regenerates a document from scratch.

**Error handling:** If a step fails, stop and say what went wrong.

## Step 1: Work Out the Target

From `$ARGUMENTS`:
- **Folder:** a folder name in `job-applications/output/` if given; otherwise the most recently modified folder there. Say which folder you used — do not ask. If a named folder doesn't exist, list the available ones and stop.
- **Document:** `cv` or `cl` if given; otherwise infer it from the feedback ("summary", "bullets", "skills" → CV; "opening", "paragraph", "letter" → CL). Feedback can touch both.
- **Kind of edit**, by meaning, not by keyword:
  - **Format** — how the page looks: fonts, sizes, margins, colors, spacing, heading style, section order.
  - **Content** — what the text says or which items are included: rewording, adding or removing bullets, skills, projects, reordering items within a section.
  - "Reorder skills to put Python first" is content; "move education above experience" is format. If it could be either, pick the likelier one and say what you assumed.

## Step 2-C: Content Edit

1. Read the data file (`cv-data.yaml` or `cl-data.yaml`) and the folder's `input.md`. For a CL edit, also read `cv-data.yaml` so the two stay consistent.
2. Read the rules that apply from `.claude/skills/cv-style-netherlands/SKILL.md` or `.claude/skills/cl-style-netherlands/SKILL.md`.
3. Any new fact must trace to `candidate.md`: grep it for the specific role, project or metric rather than reading the whole file. Never fabricate.
4. Edit only the fields the feedback names; keep the schema shape (`cv-data-schema.yaml` / `cl-data-schema.yaml` in the same style folder) and valid YAML.
5. Validate:
   ```bash
   python scripts/run.py scripts/validate_output.py <folder> --type <cv|cl>
   ```
   Fix any `errors`. Fix any *over* limit your edit caused. Report `warnings`.

## Step 2-F: Format Edit

Format changes go into a per-application override file in the folder — `cv-format-override.yaml` or `cl-format-override.yaml` (names from `config/contracts.yaml` → `override_files`). It is deep-merged on top of the style config at render time; the style files are never changed.

1. Read the base config: `.claude/skills/cv-style-netherlands/cv-format.yaml` or `.claude/skills/cl-style-netherlands/cl-format.yaml`, and the existing override file if there is one.
2. Map the request to config keys, using the same nested structure:

   | User says | Override YAML |
   |-----------|--------------|
   | "make font bigger" | `typography: { body_size: <current + 1> }` |
   | "use Arial" | `typography: { heading_font: Arial, body_font: Arial }` |
   | "reduce margins" | `page: { margins: { top: <current - 0.5>, bottom: <-0.5>, left: <-0.5>, right: <-0.5> } }` |
   | "change heading color to navy" | `colors: { primary: "#001F3F" }` |
   | "no underline on headings" | `sections: { heading_underline: false }` |
   | "move education before experience" | `sections: { order: [summary, education, experience, projects, skills, certifications, languages, interests] }` |
   | "make name bigger" | `header: { name_font_size: <current + 2> }` |

   "Bigger"/"smaller" without a value: adjust the current value by a reasonable step.
3. Merge into the existing override (keep earlier overrides) and write the file.

## Step 3: Render

```bash
python scripts/run.py scripts/render.py <folder> --only <cv|cl>
```

(No `--only` when both documents changed.) This closes the docx in Word if it is open, re-renders, re-exports the PDF and reopens the docx. If it prints a page-limit `WARNING`, tell the user and offer a trim.

## Step 4: Report Back

- **Content:** what changed (sections, bullets, paragraphs), confirmation that nothing else did, the new word count for a cover letter.
- **Format:** each setting changed, old → new (e.g. `body_size: 10 → 11`).
- Page counts from the render output.
