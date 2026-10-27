---
name: cv
description: Build the master CV — one Netherlands-standard CV from candidate.md, sent unchanged with every application. Run once, and again after candidate.md changes. Writes master-cv/ (cv-data.yaml, cv.docx, cv.pdf).
disable-model-invocation: true
argument-hint: "[render — re-render the existing master without rebuilding it]"
---

User-provided arguments: $ARGUMENTS

# /cv — Build the Master CV

The master CV is the one CV that goes with every application. It is built from `candidate.md` alone, never from a job description; `/apply` copies it into each application folder and tailors only the cover letter. It lives in `master-cv/` (`config/contracts.yaml` → `master_cv.dir`).

**Error handling:** If a step fails, stop and say which step failed with the error details. Do not continue past a failure.

If `$ARGUMENTS` is `render`, skip to Step 4.

## Step 1: Check

`candidate.md` must exist at the project root. If it doesn't, stop and say so.

```bash
python scripts/run.py scripts/master_cv.py status
```

If `exists` is true, the master is about to be rebuilt from scratch: any `/revise` edits made to it are replaced. Keep the current data so nothing is lost:

```bash
python scripts/run.py scripts/master_cv.py backup
```

This saves `master-cv/cv-data.previous.yaml`.

## Step 2: CV Agent

Delegate to `cv-agent` with:
- Full path to `candidate.md`
- Output folder: the full path of `master-cv/` at the project root

Check that `master-cv/cv-data.yaml` exists (and, if Step 1 made a backup, that it is newer than the backup).

## Step 3: Validate

```bash
python scripts/run.py scripts/validate_output.py master-cv --type cv
```

Outputs JSON with `errors`, `limits`, `warnings`:
- **errors** (schema): fix the YAML yourself if the fix is mechanical (a wrong key, a misplaced field); otherwise stop and show them.
- **limits**: fix any *over* limit with the smallest edit that brings it in — cut the weakest bullet, tighten a long bullet or the summary. Never add facts. Leave *under* limits as they are and report them.

Re-run the validator after any fix.

## Step 4: Render

```bash
python scripts/run.py scripts/render.py master-cv --only cv
```

Writes `master-cv/cv.docx` and `master-cv/cv.pdf`, checks the content made it into the docx, reports the page count and opens the docx in Word. If it exits with `ERROR`, stop and show the message. If it prints a page-limit `WARNING`, trim (style trim order: oldest role bullets → interests → project detail → bullet length) and render again.

## Step 5: Report Back

1. **Target profile:** lead role, core stack, signature results used (from the agent)
2. **Selected:** projects and certifications, and anything strong left out for space
3. **Checks:** limits fixed or left, page count
4. **Next:** "Review `master-cv/cv.docx` in Word. Use `/revise cv` for changes. Every `/apply` from now on attaches this CV unchanged."
