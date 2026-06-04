---
name: format
description: Finalize CV and cover letter as PDF. Re-renders docx from YAML data and converts to PDF. This is the "publish" step — run it when you're satisfied with the content and formatting after previewing via /apply and /revise.
disable-model-invocation: true
argument-hint: "[folder_name] [style]"
---

User-provided arguments: $ARGUMENTS

# /format — Finalize Documents as PDF

This command renders the final docx and converts to PDF. It is the "publish" step in the workflow — run it after you've previewed and revised the documents using `/apply` and `/revise`.

For formatting changes (fonts, sizes, margins, colors), use `/revise <cv|cl> [folder] "your feedback"` before running `/format`.

**Error handling:** If any step fails, stop and tell the user what went wrong with full error details.

## Step 1: Identify Target Folder

Parse `$ARGUMENTS` to determine the target folder and optional style override.

**If the first argument starts with `generic-cv/`:**
- The target folder is the specified path (e.g., `generic-cv/saudi`)
- A second argument is REQUIRED — the style name (country, region, or `default`). If missing, stop and tell the user:
  > Usage: `/format generic-cv/<country> <style>`
  > Example: `/format generic-cv/saudi europe`

**If the first argument is a folder name (or empty):**
- Look for it in `job-applications/output/$ARGUMENTS/`
- If not found, tell the user and list available folders
- If empty, scan `job-applications/output/` for the most recently modified folder and confirm with the user: "Formatting data from [folder_name] — is that correct?"

## Step 2: Validate Data Files Exist

Check the target folder for:
- `cv-data.yaml` — required
- `cl-data.yaml` — required

If either is missing, stop and tell the user which file is missing. Suggest running `/rerun cv [folder]` or `/rerun cl [folder]` to generate it.

## Step 3: Resolve Format Config and Schema Paths

Each style skill folder contains its own format config and schema. Resolve the correct paths using the style resolver script.

### For `job-applications/output/` folders:

Read `input.md` from the target folder to extract Location and Style fields. Then run:

```bash
python scripts/run.py scripts/parse_input.py --input <target_folder>/input.md
```

Use the parsed `location` and `style` values to resolve the style:

```bash
python scripts/run.py scripts/resolve_style.py --location "<location>" [--style "<style>"]
```

### For `generic-cv/` folders:

Use the explicit style argument provided by the user:

```bash
python scripts/run.py scripts/resolve_style.py --location "default" --style "<user_style_arg>"
```

### Result:

The script outputs JSON with `cv_config`, `cl_config`, `cv_schema`, `cl_schema` paths. Verify all 4 files exist. If any is missing, stop and tell the user which file is missing and in which style folder.

## Step 4: Ensure Python Environment

The wrapper script `scripts/run.py` automatically creates the venv and installs dependencies from `requirements.txt` if needed. No manual install step required.

## Step 5: Run the Rendering Script

Execute the rendering script from the project root:

```bash
python scripts/run.py scripts/render.py --type both \
  --data-dir <target_folder> \
  --cv-config <cv-config-path> \
  --cl-config <cl-config-path> \
  --cv-schema <cv-schema-path> \
  --cl-schema <cl-schema-path> \
  --pdf
```

This script will:
1. Load `cv-data.yaml` and validate it against the resolved CV schema
2. Load the resolved CV format config for formatting settings
3. Generate `cv.docx` using python-docx with deterministic formatting
4. Load `cl-data.yaml` and validate it against the resolved CL schema
5. Load the resolved CL format config for formatting settings
6. Generate `cover-letter.docx`
7. Convert both to PDF (if available)

If schema validation fails, the script prints the specific errors and exits. Report these to the user — they likely indicate a malformed YAML file from the agent.

If PDF conversion fails, the docx files are still generated successfully.

## Step 6: Post-Render Validation

After rendering, run the post-render validator to confirm all YAML content made it into the docx:

```bash
python scripts/run.py scripts/render_validate.py <target_folder>/cv.docx <target_folder>/cv-data.yaml "CV"
python scripts/run.py scripts/render_validate.py <target_folder>/cover-letter.docx <target_folder>/cl-data.yaml "Cover Letter"
```

Include the results in your report.

## Step 7: Report Back

Tell the user:
- Style resolved (e.g., "Using cv-style-europe / cl-style-europe")
- Whether a per-application format override was applied (override filenames `cv-format-override.yaml` / `cl-format-override.yaml` are the shared contract defined in `config/contracts.yaml` → `override_files`)
- Files created (list all generated files with paths)
- Post-render validation results (content checks and stats)
- Whether PDF conversion succeeded or was skipped
- If formatting changes are needed, suggest: "Use `/revise <cv|cl> [folder] \"your feedback\"` to adjust formatting, then re-run `/format`"
