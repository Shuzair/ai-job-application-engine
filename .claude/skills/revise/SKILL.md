---
name: revise
description: Make targeted edits to the master CV or an application's cover letter — content (wording, what is included) or formatting (fonts, sizes, margins, colors, spacing, section order). Re-renders docx and pdf after every edit.
disable-model-invocation: true
argument-hint: "[cv|cl] [folder_name] feedback"
---

User-provided arguments: $ARGUMENTS

# /revise — Targeted Revision

Change only what the user asked for and keep everything else as it is. This never regenerates a document from scratch.

**Where edits go.** The CV is the master CV in `master-cv/`, the same for every application, so **every CV edit is made there** and then copied into the current application folder; older application folders keep the CV that was sent with them. Cover letter edits go to the application folder.

**Error handling:** If a step fails, stop and say what went wrong.

## Step 1: Work Out the Target

From `$ARGUMENTS`:
- **Folder:** a folder name in `job-applications/output/` if given; otherwise the most recently modified folder there. Say which folder you used — do not ask. If a named folder doesn't exist, list the available ones and stop. For a CV-only edit with no application folders yet, there is no folder: edit the master only.
- **Document:** `cv` or `cl` if given; otherwise infer it from the feedback ("summary", "bullets", "skills" → CV; "opening", "paragraph", "letter" → CL). Feedback can touch both.
- **Kind of edit**, by meaning, not by keyword:
  - **Format** — how the page looks: fonts, sizes, margins, colors, spacing, heading style, section order.
  - **Content** — what the text says or which items are included: rewording, adding or removing bullets, skills, projects, reordering items within a section.
  - "Reorder skills to put Python first" is content; "move education above experience" is format. If it could be either, pick the likelier one and say what you assumed.

## Step 2-C: Content Edit

1. Read the data file: `master-cv/cv-data.yaml` for the CV, or the folder's `cl-data.yaml` and `input.md` for the letter. For a CL edit, also read the folder's `cv-data.yaml` so the two stay consistent. The CV must stay free of anything specific to one employer or posting — if the feedback asks for that, put it in the letter instead and say so.
2. Read the rules that apply from `.claude/skills/cv-style-netherlands/SKILL.md` or `.claude/skills/cl-style-netherlands/SKILL.md`.
3. Any new fact must trace to `candidate.md`: grep it for the specific role, project or metric rather than reading the whole file. Never fabricate.
4. Edit only the fields the feedback names; keep the schema shape (`cv-data-schema.yaml` / `cl-data-schema.yaml` in the same style folder) and valid YAML.
5. Validate:
   ```bash
   python scripts/run.py scripts/validate_output.py master-cv --type cv
   python scripts/run.py scripts/validate_output.py <folder> --type cl
   ```
   Fix any `errors`. Fix any *over* limit your edit caused. Report `warnings`.

## Step 2-F: Format Edit

Format changes go into an override file — `cv-format-override.yaml` in `master-cv/`, or `cl-format-override.yaml` in the application folder (names from `config/contracts.yaml` → `override_files`). It is deep-merged on top of the style config at render time; the style files are never changed.

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

**CV** — render the master, then copy it into the application folder (skip the copy when there is no folder):

```bash
python scripts/run.py scripts/render.py master-cv --only cv --no-open
python scripts/run.py scripts/master_cv.py copy <folder>
python scripts/run.py scripts/word.py open <folder>/cv.docx
```

With no folder, open `master-cv/cv.docx` instead.

**Cover letter:**

```bash
python scripts/run.py scripts/render.py <folder> --only cl
```

Rendering closes the docx in Word if it is open, re-renders, re-exports the PDF and (unless `--no-open`) reopens the docx. If it prints a page-limit `WARNING`, tell the user and offer a trim.

## Step 4: Report Back

- **Content:** what changed (sections, bullets, paragraphs), confirmation that nothing else did, the new word count for a cover letter.
- **CV edits:** that the master CV changed for every future application, and which application folder got the new copy.
- **Format:** each setting changed, old → new (e.g. `body_size: 10 → 11`).
- Page counts from the render output.
