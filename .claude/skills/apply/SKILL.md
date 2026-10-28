---
name: apply
description: Generate a tailored CV and cover letter for a job in the Netherlands. Takes a job description pasted with the command, a posting URL, or job-applications/input.md; creates a versioned output folder, researches the company and extracts the posting's keywords, maps the candidate's profile against the job and the company, writes the CV and cover letter data with subagents, and renders docx + pdf.
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

## Step 3: Company Research and Keywords (wave 1)

Steps 3a and 3b are independent: start both agents in the same message so they run in parallel, then wait for both.

### 3a: Company Research

**Skip research if** Company is empty (agency posting) or the user asked to skip it. Then write `research.md` in the folder — the title (`Not Available`) and first sentence are a shared contract (`config/contracts.yaml` → `research_placeholders`), use them verbatim:

```markdown
# Company Research: Not Available

Research was skipped for this application. Either the company was not specified (HR agency posting) or research was explicitly skipped.

The CV and cover letter are tailored based on the job description and candidate profile only.
```

**Otherwise** delegate to `research-agent` with: the company name, the link, and the full path where it writes `research.md`. Do not pass `candidate.md`. When it returns, check that `research.md` exists.

### 3b: JD Keywords

Delegate to `keyword-agent` with the full path to the application folder. Do not pass `candidate.md` — the keyword list is built from the posting alone.

It writes `jd-keywords.yaml`: the role (title, family, seniority, whether Dutch is required) and the ranked keywords. When it returns, check it:

```bash
python scripts/run.py scripts/validate_output.py <folder_path> --type keywords
```

If it reports errors, send them back to `keyword-agent` once to fix; if they remain, stop and show them.

## Step 4: Profile Mappings (wave 2)

Needs `jd-keywords.yaml` and `research.md`. Start all three agents in the same message so they run in parallel, then wait for all three. Pass each the full path to the application folder and to `candidate.md`.

| Agent | Writes | Question |
|---|---|---|
| `jd-to-profile-agent` | `jd-to-profile.yaml` | For each keyword: does the candidate have it, how strongly, where is the proof? |
| `profile-to-jd-agent` | `profile-to-jd.yaml` | Which achievements would this employer value most, including ones the posting does not name? |
| `company-to-profile-agent` | `company-to-profile.yaml` | Which verified company facts connect to the candidate's background? (Empty is valid; with skipped research it writes an empty file.) |

Every claim in these files carries an evidence strength (shipped / built / tooling / certified / learning / planned) and an exact quote from candidate.md. When all three return, check them together:

```bash
python scripts/run.py scripts/validate_output.py <folder_path> --type mappings
```

The validator checks each schema, that `jd-to-profile.yaml` maps every keyword exactly once, and that every quote exists word for word in candidate.md (research quotes in research.md). If it reports errors, send each agent the errors about its own file once to fix; if they remain, stop and show them.

Then read the three files yourself and look for **conflicts** — e.g. jd-to-profile marks dbt `shipped` while profile-to-jd's dbt highlight is `tooling`. Resolve each toward the **weaker** strength (edit the stronger entry's `strength` and `place` to match; drop `skills` from `place` below `built`), and list what you changed in the report.

## Step 5: CV Agent

Delegate to `cv-agent` with:
- Full path to `candidate.md`
- Full path to the application folder (has `input.md`, `research.md`, `jd-keywords.yaml` and the three mapping files)
- Whether research was skipped (if so: tailor to the JD and profile only, no company-specific framing)

Check that `cv-data.yaml` exists.

## Step 6: Cover Letter Agent

Delegate to `cl-agent` with:
- Full path to `candidate.md`
- Full path to the application folder (now also has `cv-data.yaml`)
- Whether research was skipped (if so: open with the role and a JD requirement, not the company's product or mission)
- The letter date: `parsed.date` from Step 2

Check that `cl-data.yaml` exists.

## Step 7: Validate

```bash
python scripts/run.py scripts/validate_output.py <folder_path>
```

Outputs JSON with `errors`, `limits`, `warnings`:
- **errors** (schema, name mismatch, a gap or weak-evidence keyword listed as a skill): fix the YAML yourself if the fix is mechanical (a wrong key, a misplaced field, removing a skill the candidate lacks or knows too weakly — show it in a bullet worded as jd-to-profile.yaml says); otherwise stop and show them.
- **limits**: fix any *over* limit yourself with the smallest edit that brings it in — cut the least JD-relevant bullet, tighten a long bullet or summary. Never add facts. Leave *under* limits as they are and report them.
- **warnings**: `[keywords]` warnings name must-have keywords the candidate has that the CV does not show. Fix each yourself when candidate.md backs it (jd-to-profile.yaml → `evidence`): add it to the skills section, or work it into an existing bullet without breaking the word limit. Report any you leave and why. Report other warnings.

Re-run the validator after any fix.

## Step 8: Render

```bash
python scripts/run.py scripts/render.py <folder_path>
```

Writes `cv.docx`, `cover-letter.docx`, `cv.pdf`, `cover-letter.pdf`, checks the content made it into each docx, reports page counts, and opens both docx files in Word. If it exits with `ERROR`, stop and show the message. If it prints a page-limit `WARNING`, trim the CV (style trim order: oldest role bullets → interests → project detail → bullet length) or the letter, then render again.

## Step 9: Report Back

1. **Folder:** full path
2. **Research:** done or skipped; if done, a 2–3 line company summary, and whether the company is a recognised IND sponsor (from research.md)
3. **Keywords:** role family and seniority, the top must-haves, analogues used, and must-have gaps (`match: "no"`) — the user should know what the posting asks for that the CV cannot claim
4. **Mappings:** must-haves with weak evidence (strength below `built`) and how they are worded; the top 3 highlights from profile-to-jd.yaml and any implied need it found; the company links (or none); conflicts you resolved
5. **CV:** what leads the summary and skills, projects selected
6. **Cover letter:** achievements highlighted, company details used (or JD-focused only), word count
7. **Checks:** limits fixed or left, warnings, page counts
8. **Language:** if the posting is written in Dutch or `dutch_required` is `yes` in jd-keywords.yaml, say so — the documents are in English
9. **Next:** "Review in Word. Use `/revise` for changes — PDFs are re-exported each time."

Finally, reset the input file — only after everything above succeeded:

```bash
python scripts/run.py scripts/reset_input.py --input job-applications/input.md
```
