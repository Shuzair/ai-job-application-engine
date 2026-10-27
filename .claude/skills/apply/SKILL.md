---
name: apply
description: Apply for a job in the Netherlands. Takes a job description pasted with the command, a posting URL, or job-applications/input.md; creates a versioned output folder, researches the company, attaches the master CV unchanged, writes a tailored cover letter, and renders docx + pdf.
disable-model-invocation: true
argument-hint: "[pasted job description or posting URL — optional]"
---

User-provided arguments: $ARGUMENTS

# /apply — Netherlands Job Application

You are the orchestrator. Every application uses the Netherlands style (`cv-style-netherlands`, `cl-style-netherlands`); there is no style choice to make.

**The CV is the same for every application.** It is the master CV in `master-cv/` (built by `/cv`), copied unchanged into the application folder. Only the cover letter is written for this job.

**Error handling:** If a step fails, stop, say which step failed with the error details, and ask whether to retry or abort. Do not continue past a failure.

## Step 1: Check the Master CV

`candidate.md` must exist at the project root. If it doesn't, stop and say so — it is the single source of truth for every document.

```bash
python scripts/run.py scripts/master_cv.py status
```

- `exists` false: there is no master CV yet. Run the `/cv` steps (`.claude/skills/cv/SKILL.md`) first, then continue here.
- `rendered` false: the master's data changed since it was rendered. Render it: `python scripts/run.py scripts/render.py master-cv --only cv --no-open`.
- `stale` true: candidate.md changed after the master CV was built. Continue, and say so in the report: the CV may be missing recent changes; `/cv` rebuilds it.

## Step 2: Get the Job Description

- **Pasted job description in `$ARGUMENTS`:** write it into `job-applications/input.md` using the template headers — `# Company`, `# Link`, `# Role`, `# Location`, `# Job Description`. Take Company, Role and Location (city) from the posting; put the full posting text, unedited, under `# Job Description` (last section).
- **Posting URL in `$ARGUMENTS`:** fetch it with WebFetch, then fill `input.md` the same way, with the URL under `# Link`. If the page has no usable job description (login wall, JS-only page), ask the user to paste the text instead.
- **No arguments:** use `job-applications/input.md` as the user filled it.

If the posting is clearly for a job outside the Netherlands, say so and ask before continuing.

## Step 3: Create the Folder

```bash
python scripts/run.py scripts/prepare_folder.py --input job-applications/input.md --output-dir job-applications/output
```

Outputs JSON: `folder_path`, `folder_name`, `parsed` (company, link, role, location, job_description, date). The folder is named `<company>_<role>_v<n>` and gets an `input.md` snapshot. If `valid` is `false`, show `errors` and stop.

## Step 4: Company Research

**Skip research if** Company is empty (agency posting) or the user asked to skip it. Then write `research.md` in the folder — the title (`Not Available`) and first sentence are a shared contract (`config/contracts.yaml` → `research_placeholders`), use them verbatim:

```markdown
# Company Research: Not Available

Research was skipped for this application. Either the company was not specified (HR agency posting) or research was explicitly skipped.

The cover letter is tailored based on the job description and candidate profile only.
```

**Otherwise** delegate to `research-agent` with: the company name, the link, and the full path where it writes `research.md`. Do not pass `candidate.md`. When it returns, check that `research.md` exists.

## Step 5: Attach the Master CV

```bash
python scripts/run.py scripts/master_cv.py copy <folder_path>
```

Copies `cv-data.yaml`, `cv.docx`, `cv.pdf` (and the master's format override, if any) into the folder. The CV is never edited per application.

## Step 6: Cover Letter Agent

Delegate to `cl-agent` with:
- Full path to `candidate.md`
- Full path to the application folder (now has the master CV's `cv-data.yaml`)
- Whether research was skipped (if so: open with the role and a JD requirement, not the company's product or mission)
- The letter date: `parsed.date` from Step 3

Check that `cl-data.yaml` exists.

## Step 7: Validate

```bash
python scripts/run.py scripts/validate_output.py <folder_path> --type cl
```

Outputs JSON with `errors`, `limits`, `warnings`:
- **errors** (schema, name mismatch): fix the YAML yourself if the fix is mechanical (a wrong key, a misplaced field); otherwise stop and show them.
- **limits**: fix any *over* limit yourself with the smallest edit that brings it in — tighten or cut the weakest sentence. Never add facts. Leave *under* limits as they are and report them.
- **warnings**: a `[keywords]` warning names skills the job asks for that the candidate has but neither the CV prose nor the letter mentions — work the most important one into the letter if it fits the word limit, otherwise report it. Report other warnings.

Re-run the validator after any fix.

## Step 8: Render

```bash
python scripts/run.py scripts/render.py <folder_path> --only cl
```

Writes `cover-letter.docx` and `cover-letter.pdf`, checks the content made it into the docx, reports the page count, and opens it in Word. If it exits with `ERROR`, stop and show the message. If it prints a page-limit `WARNING`, trim the letter, then render again. Then open the CV too:

```bash
python scripts/run.py scripts/word.py open <folder_path>/cv.docx
```

## Step 9: Report Back

1. **Folder:** full path
2. **Research:** done or skipped; if done, a 2–3 line company summary, and whether the company is a recognised IND sponsor (from research.md)
3. **CV:** the master CV, attached unchanged (say if it is stale — candidate.md changed after it was built)
4. **Cover letter:** achievements highlighted, the job's must-haves it covers that the CV doesn't show, company details used (or JD-focused only), word count
5. **Gaps:** JD requirements the candidate can't match
6. **Checks:** limits fixed or left, warnings, page counts
7. **Language:** if the posting is written in Dutch, say so — it usually means Dutch is required; the documents are in English
8. **Next:** "Review the letter in Word. Use `/revise cl` for letter changes; `/revise cv` changes the master CV for every future application."

Finally, reset the input file — only after everything above succeeded:

```bash
python scripts/run.py scripts/reset_input.py --input job-applications/input.md
```
