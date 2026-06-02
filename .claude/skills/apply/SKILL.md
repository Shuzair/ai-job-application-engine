---
name: apply
description: Generate a tailored CV and cover letter for a job application. Reads input.md, creates a versioned output folder, optionally researches the company, and delegates to subagents for CV and cover letter generation.
disable-model-invocation: true
---

# /apply — Generate Job Application

You are the orchestrator. You read the input, set up the folder, and delegate work to three subagents in sequence.

**Error handling:** If any agent fails, reports an error, or returns without completing its task, stop the workflow immediately. Tell the user which step failed, include the error details, and ask how to proceed (retry, skip, or abort). Do not continue to the next step after a failure.

## Step 1: Read and Validate Input

First, check that `candidate.md` exists at the project root. If it doesn't, stop and tell the user:
> `candidate.md` not found. This file is required — it contains your professional profile and is the single source of truth for all CV and cover letter generation.
>
> To create it, run `/profile` and say "create". This will walk you through a guided interview to build your profile section by section. You can also use "improve", "audit", or "add" to manage an existing profile.

Run the input parser script:

```bash
python scripts/run.py scripts/parse_input.py --input job-applications/input.md
```

This outputs JSON with: company, link, role, location, style, job_description, date, valid, errors.

If `valid` is `false`, stop and show the errors to the user. The script handles placeholder detection and required field validation automatically.

Store the parsed values for use in subsequent steps.

## Step 2: Create Folder and Save Input Snapshot

Run the folder preparation script:

```bash
python scripts/run.py scripts/prepare_folder.py --input job-applications/input.md --output-dir job-applications/output
```

This outputs JSON with: folder_path, folder_name, version. It creates the folder, derives the versioned name following the naming rules, and writes the input.md snapshot automatically.

Store `folder_path` and `folder_name` for subsequent steps.

## Step 3: Resolve Style

Run the style resolver script using the parsed location and style values from Step 1:

```bash
python scripts/run.py scripts/resolve_style.py --location "<location>" [--style "<style>"]
```

This outputs JSON with: cv_style, cl_style, cv_config, cl_config, cv_schema, cl_schema, and resolution trace.

Store all paths for use when delegating to agents and for the /format step.

## Step 4: Reset input.md (deferred)

**Do NOT reset yet.** Mark this step as pending. The actual reset happens in Step 9 (Report Back) — only after all agents have completed successfully. When the time comes, run:

```bash
python scripts/run.py scripts/reset_input.py --input job-applications/input.md
```

## Step 5: Determine Research Mode

Decide whether to run company research based on two signals:

**Skip research if ANY of these are true:**
- Company field in input.md is empty
- Link field in input.md is empty AND no company name is recognizable from the JD
- The user explicitly said to skip research (e.g., "apply without research", "skip research", "no research")

**Run research if ALL of these are true:**
- Company field is filled
- The user did not request skipping research

If skipping research, create a minimal `research.md` in the folder:

```markdown
# Company Research: Not Available

Research was skipped for this application. Either the company was not specified (HR agency posting) or research was explicitly skipped.

The CV and cover letter are tailored based on the job description and candidate profile only.
```

Then proceed directly to Step 7.

If running research, proceed to Step 6.

## Step 6: Delegate to Research Agent

Delegate to the `research-agent` subagent using the Agent tool. Pass the following in the prompt:
- The company name and link from the input
- The full path where it should write `research.md` (the application folder)
- The full path to `candidate.md` at the project root (so the research agent can note tech stack overlaps in its "Relevance to Candidate" section)

Wait for the agent to complete and report back.

**Verify:** Check that `research.md` exists in the application folder. If it doesn't, stop and tell the user the research agent failed to produce output.

## Step 7: Delegate to CV Agent

Use the `cv_style_skill` value from Step 3 (e.g., `cv-style-europe`, `cv-style-denmark`, `cv-style-default`).

Delegate to the `cv-agent` subagent using the Agent tool. Pass the following in the prompt:
- Full path to `candidate.md` (project root)
- Full path to the application folder (contains `input.md` and `research.md`)
- The `cv_style_skill` value as the CV style skill name to load

**If research was skipped:** Tell the cv-agent explicitly that there is no company research available. The CV should be tailored purely based on the job description and the candidate's profile. Do not attempt to align experience with company-specific context — focus on matching JD requirements, technologies, and role responsibilities.

Wait for the agent to complete and report back.

**Verify:** Check that `cv-data.yaml` exists in the application folder. If it doesn't, stop and tell the user the CV agent failed to produce output.

**Validate content:** Run the output validator to check the CV data against the style's schema and rules:

```bash
python scripts/run.py scripts/validate_output.py --type cv \
  --data-dir <folder_path> \
  --cv-config <cv_config_path> \
  --cv-schema <cv_schema_path>
```

If the result contains schema validation errors, stop and tell the user — the CV agent produced structurally invalid output. Include the specific errors. Do not proceed to Step 8 until fixed.

Warnings (word count, bullet count) are informational — report them in Step 9 but do not block on them.

## Step 8: Delegate to CL Agent

Use the `cl_style_skill` value from Step 3 (e.g., `cl-style-europe`, `cl-style-denmark`, `cl-style-default`).

Delegate to the `cl-agent` subagent using the Agent tool. Pass the following in the prompt:
- Full path to `candidate.md` (project root)
- Full path to the application folder (now contains `input.md`, `research.md`, and `cv-data.yaml`)
- The `cl_style_skill` value as the CL style skill name to load

**If research was skipped:** Tell the cl-agent explicitly that there is no company research available. The cover letter should focus on the role requirements and the candidate's fit, not company-specific details. The opening paragraph should reference the role and JD requirements rather than the company's product or mission.

Wait for the agent to complete and report back.

**Verify:** Check that `cl-data.yaml` exists in the application folder. If it doesn't, stop and tell the user the cover letter agent failed to produce output.

**Validate content:** Run the output validator to check the CL data against the style's schema and rules:

```bash
python scripts/run.py scripts/validate_output.py --type cl \
  --data-dir <folder_path> \
  --cl-config <cl_config_path> \
  --cl-schema <cl_schema_path>
```

If the result contains schema validation errors, stop and tell the user — the CL agent produced structurally invalid output. Include the specific errors.

Warnings (word count, paragraph count) are informational — report them in Step 9 but do not block on them.

## Step 9: Render Draft Documents

After all agents have completed successfully and validation has passed, render the docx files (without PDF — that happens later via `/format`):

```bash
python scripts/run.py scripts/render.py --type both \
  --data-dir <folder_path> \
  --cv-config <cv_config> \
  --cl-config <cl_config> \
  --cv-schema <cv_schema> \
  --cl-schema <cl_schema>
```

Then open both docx files for the user to preview:

```bash
open <folder_path>/cv.docx
open <folder_path>/cover-letter.docx
```

## Step 10: Report Back

Tell the user:

1. **Folder created:** full path to the application folder
2. **Research status:** whether research was done or skipped, and if done, a 2-3 line company summary
3. **CV tailoring decisions** (from cv-agent's report):
   - Technologies prioritized
   - Projects selected
   - JD requirements that couldn't be matched
4. **CL tailoring decisions** (from cl-agent's report):
   - Achievements highlighted
   - Company details used (or note that cover letter is JD-focused only)
   - Word count
5. **Documents rendered:** `cv.docx` and `cover-letter.docx` have been opened for preview
6. **Format settings used** — read the resolved `cv-format.yaml` and `cl-format.yaml` and print this exact template:

```
--- Format Settings (<cv_style>) ---
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

Replace each `<placeholder>` with the actual value from the config files. Use the `cv_style` name (e.g., `europe`, `germany`, `default`) in the header.

7. **Next steps:** "Review the documents in Word. Use `/revise` to adjust content or formatting, then `/format` to finalize as PDF."
8. **Now execute the deferred Step 4:** Run `python scripts/run.py scripts/reset_input.py --input job-applications/input.md` to overwrite it with the blank template. This is the last action — only runs after all agents succeeded.
