---
name: apply
description: Generate a tailored CV and cover letter for a job in the Netherlands. Takes a job description pasted with the command, a posting URL, or job-applications/input.md; creates a versioned output folder, researches the company, writes the CV and cover letter data with subagents, and renders docx + pdf.
disable-model-invocation: true
argument-hint: "[pasted job description or posting URL — optional]"
---

User-provided arguments: $ARGUMENTS

# /apply — Netherlands Job Application

You are the orchestrator. Every application uses the Netherlands style (`cv-style-netherlands`, `cl-style-netherlands`); there is no style choice to make.

**Error handling:** If a step fails, stop, say which step failed with the error details, and ask whether to retry or abort. Do not continue past a failure.

## Step 1: Get the Job Description

`candidate.md` must exist at the project root. If it doesn't, stop and say so — it is the single source of truth for every document.

- **Pasted job description in `$ARGUMENTS`:** write it into `job-applications/input.md` using the template headers — `# Company`, `# Link`, `# Role`, `# Location`, `# Job Description`. Take Company, Role and Location (city) from the posting; put the full posting text, unedited, under `# Job Description` (last section).
- **Posting URL in `$ARGUMENTS`:** fetch it with WebFetch, then fill `input.md` the same way, with the URL under `# Link`. If the page has no usable job description (login wall, JS-only page), ask the user to paste the text instead.
- **No arguments:** use `job-applications/input.md` as the user filled it.

If the posting is clearly for a job outside the Netherlands, say so and ask before continuing.

## Step 2: Create the Folder

```bash
python scripts/run.py scripts/prepare_folder.py --input job-applications/input.md --output-dir job-applications/output
```

Outputs JSON: `folder_path`, `folder_name`, `parsed` (company, link, role, location, job_description, date). The folder is named `<company>_<role>_v<n>` and gets an `input.md` snapshot. If `valid` is `false`, show `errors` and stop.

## Step 3: Company Research

**Skip research if** Company is empty (agency posting) or the user asked to skip it. Then write `research.md` in the folder — the title (`Not Available`) and first sentence are a shared contract (`config/contracts.yaml` → `research_placeholders`), use them verbatim:

```markdown
# Company Research: Not Available

Research was skipped for this application. Either the company was not specified (HR agency posting) or research was explicitly skipped.

The CV and cover letter are tailored based on the job description and candidate profile only.
```

**Otherwise** delegate to `research-agent` with: the company name, the link, and the full path where it writes `research.md`. Do not pass `candidate.md`. When it returns, check that `research.md` exists.

## Step 4: CV Agent

Delegate to `cv-agent` with:
- Full path to `candidate.md`
- Full path to the application folder
- Whether research was skipped (if so: tailor to the JD and profile only, no company-specific framing)

Check that `cv-data.yaml` exists.

## Step 5: Cover Letter Agent

Delegate to `cl-agent` with:
- Full path to `candidate.md`
- Full path to the application folder (now has `cv-data.yaml`)
- Whether research was skipped (if so: open with the role and a JD requirement, not the company's product or mission)
- The letter date: `parsed.date` from Step 2

Check that `cl-data.yaml` exists.

## Step 6: Validate

```bash
python scripts/run.py scripts/validate_output.py <folder_path>
```

Outputs JSON with `errors`, `limits`, `warnings`:
- **errors** (schema, name mismatch): fix the YAML yourself if the fix is mechanical (a wrong key, a misplaced field); otherwise stop and show them.
- **limits**: fix any *over* limit yourself with the smallest edit that brings it in — cut the least JD-relevant bullet, tighten a long bullet or summary. Never add facts. Leave *under* limits as they are and report them.
- **warnings**: report them.

Re-run the validator after any fix.

## Step 7: Render

```bash
python scripts/run.py scripts/render.py <folder_path>
```

Writes `cv.docx`, `cover-letter.docx`, `cv.pdf`, `cover-letter.pdf`, checks the content made it into each docx, reports page counts, and opens both docx files in Word. If it exits with `ERROR`, stop and show the message. If it prints a page-limit `WARNING`, trim the CV (style trim order: oldest role bullets → interests → project detail → bullet length) or the letter, then render again.

## Step 8: Report Back

1. **Folder:** full path
2. **Research:** done or skipped; if done, a 2–3 line company summary, and whether the company is a recognised IND sponsor (from research.md)
3. **CV:** technologies prioritised, projects selected, JD requirements that couldn't be matched
4. **Cover letter:** achievements highlighted, company details used (or JD-focused only), word count
5. **Checks:** limits fixed or left, warnings, page counts
6. **Language:** if the posting is written in Dutch, say so — it usually means Dutch is required; the documents are in English
7. **Next:** "Review in Word. Use `/revise` for changes — PDFs are re-exported each time."

Finally, reset the input file — only after everything above succeeded:

```bash
python scripts/run.py scripts/reset_input.py --input job-applications/input.md
```
