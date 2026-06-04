---
name: scan
description: Scan career pages from a country's company list to find matching jobs. Delegates to the job-scanner-agent which orchestrates scanning via career-scanner sub-agents.
disable-model-invocation: true
---

# /scan — Scan Career Pages for Matching Jobs

Scans all companies in a country's company list and finds jobs matching the candidate's profile.

## Usage

```
/scan <country>
```

Where `<country>` is a subfolder name under `generic-cv/` (e.g., `germany`, `saudi`).

## What You Do

### 1. Validate Inputs

1. Check that `candidate.md` exists at the project root. If missing, stop and tell the user to run `/profile create`.
2. Check that `generic-cv/<country>/` exists. If not, list available country folders under `generic-cv/` and ask the user to pick one.
3. Find the markdown file(s) in `generic-cv/<country>/` containing a company table (look for files with a markdown table that has a "Careers Page" column). If multiple files exist, let the user know and process all of them.

> The required column header (`Careers Page`) and the output filename (`matched-jobs.md`) are shared contracts defined in `config/contracts.yaml` → `scan` (`careers_page_column` / `matched_jobs_filename`). The job-scanner-agent relies on the same values.

### 2. Delegate to job-scanner-agent

Invoke the `job-scanner-agent` subagent with this information:

- The country/region name
- The path to the company list markdown file(s) found in step 1
- The path to `candidate.md`

The job-scanner-agent handles everything from here: parsing companies, launching career-scanner sub-agents, collecting results, and writing `matched-jobs.md`.

### 3. Report Results

When the job-scanner-agent finishes, report a summary to the user:
- How many companies were scanned
- How many had matching jobs
- How many were unscannable
- Where the results file was saved

If the run was interrupted and not all companies were scanned, tell the user they can run `/scan <country>` again — it will resume from where it left off (already-scanned companies are skipped).
