---
name: revise
description: Make targeted edits to an existing CV or cover letter draft based on user feedback without regenerating from scratch. Use when the user wants to adjust specific parts of a draft — e.g., "make the summary more technical", "change paragraph 2", "add more bullets to the Afiniti role".
disable-model-invocation: true
argument-hint: "<cv|cl> [folder_name] \"feedback\""
---

User-provided arguments: $ARGUMENTS

# /revise — Targeted Draft Revision

Make targeted edits to an existing draft based on user feedback. Unlike `/rerun`, this does NOT regenerate from scratch — it modifies the existing draft while preserving everything the user hasn't asked to change.

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

## Step 5: Apply Revisions

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

## Step 6: Write Updated Data

Overwrite the existing data file (`cv-data.yaml` or `cl-data.yaml`) with the revised version. Ensure the output is valid YAML.

## Step 7: Report Back

Tell the user:
1. What was changed (list specific sections/paragraphs modified)
2. What was preserved (confirm untouched sections)
3. If revising the cover letter, note the updated word count
4. Remind them to re-run `/format [folder]` if they want updated docx/pdf files
