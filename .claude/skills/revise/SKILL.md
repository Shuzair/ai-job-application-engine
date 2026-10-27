---
name: revise
description: Make targeted text edits to an existing CV or cover letter — wording, what is included, order within a section. The layout is fixed. Re-renders docx and pdf after every edit.
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
- **Layout requests** (fonts, sizes, margins, colors, spacing, headings, section order, skill category names): the layout is fixed and the same for every application (`scripts/nl_template.py`). Say so and do not change it for one application. If the user wants it changed for every document from now on, change the constant in `nl_template.py` (and the schema enum for skill categories), run the tests, and re-render.
- **Content** is everything else: rewording, adding or removing bullets, skills, projects, reordering items within a section. "Reorder skills to put Python first" is content; "move education above experience" is layout.

## Step 2: Edit the Text

1. Read the data file (`cv-data.yaml` or `cl-data.yaml`) and the folder's `input.md`. For a CL edit, also read `cv-data.yaml` so the two stay consistent.
2. Read the rules that apply from `.claude/skills/cv-style-netherlands/SKILL.md` or `.claude/skills/cl-style-netherlands/SKILL.md`.
3. Any new fact must trace to `candidate.md`: grep it for the specific role, project or metric rather than reading the whole file. Never fabricate.
4. Edit only the fields the feedback names; keep the schema shape (`cv-data-schema.yaml` / `cl-data-schema.yaml` in the same style folder) and valid YAML.
5. Validate:
   ```bash
   python scripts/run.py scripts/validate_output.py <folder> --type <cv|cl>
   ```
   Fix any `errors`. Fix any *over* limit your edit caused. Report `warnings`.

## Step 3: Render

```bash
python scripts/run.py scripts/render.py <folder> --only <cv|cl>
```

(No `--only` when both documents changed.) This closes the docx in Word if it is open, re-renders, re-exports the PDF and reopens the docx. If it prints a page-limit `WARNING`, tell the user and offer a trim.

## Step 4: Report Back

- What changed (sections, bullets, paragraphs), confirmation that nothing else did, the new word count for a cover letter.
- Page counts from the render output.
