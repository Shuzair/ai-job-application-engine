---
name: rerun
description: Re-run a specific agent (cv, cl, or research) on an existing application folder without re-running the full /apply workflow. Use when a draft needs regeneration but the other outputs are fine.
disable-model-invocation: true
argument-hint: "<agent> [folder_name]"
arguments: agent folder
---

Re-run agent: **$agent**
Target folder: **$folder**

# /rerun — Re-run a Single Agent

## Step 1: Parse and Validate Arguments

Two arguments are expected:
- `$agent` — which agent to re-run: `cv`, `cl`, or `research`
- `$folder` — the application folder name inside `job-applications/output/`

**Argument order validation:** The first argument MUST be one of `cv`, `cl`, or `research`. If the first argument looks like a folder name (e.g., contains hyphens and underscores, or ends with `_v1`, `_v2`, etc.) and the second argument is a valid agent name, the user likely swapped the order. In that case, tell them:
> It looks like you swapped the arguments. Try: `/rerun $second_arg $first_arg`

If `$agent` is not one of `cv`, `cl`, or `research`, stop and tell the user:
> Usage: `/rerun <cv|cl|research> [folder_name]`

If `$folder` is empty:
- Scan `job-applications/output/` for the most recently modified folder
- Confirm with the user: "Re-running **$agent** agent on **[folder_name]** — is that correct?"

If the folder doesn't exist under `job-applications/output/`, stop and list available folders.

## Step 2: Validate Prerequisites

Check that the required files exist in the target folder before delegating.

**For `research`:**
- `input.md` must exist in the folder
- Read `input.md` to extract Company and Link — if both are empty, stop and tell the user research cannot run without a company name

**For `cv`:**
- `input.md` must exist
- `research.md` must exist (even the placeholder version)
- `candidate.md` must exist at the project root

**For `cl`:**
- `input.md` must exist
- `research.md` must exist
- `cv-data.yaml` must exist (the cover letter depends on it for consistency)
- `candidate.md` must exist at the project root

If any prerequisite is missing, stop and tell the user which file is missing and why it's needed.

## Step 3: Determine Context

Parse the folder's `input.md` and resolve the style using scripts:

```bash
python scripts/run.py scripts/parse_input.py --input <folder_path>/input.md
python scripts/run.py scripts/resolve_style.py --location "<location>" [--style "<style>"]
```

Store the parsed input values and resolved style paths. Also check whether research was skipped (check if `research.md` contains the skipped-research placeholder). The exact detection strings — `"Research was skipped for this application."` and the title `"Not Available"` — are the shared contract defined in `config/contracts.yaml` → `research_placeholders` (`skipped` / `skipped_title`). They are written by `/apply`; if they change, change them in `config/contracts.yaml` and keep this detector in sync.

## Step 4: Delegate to Agent

### If `$agent` is `research`:

Delegate to the `research-agent` subagent. Pass:
- The company name and link from `input.md`
- The full path where it should write `research.md`
- The full path to `candidate.md` at the project root (so the research agent can note tech stack overlaps in its "Relevance to Candidate" section)

**Verify:** After the agent returns, check that `research.md` exists and was updated. If it doesn't, stop and report the failure.

**Cascade:** After research completes successfully, check if `cv-data.yaml` or `cl-data.yaml` already exist in the folder. If either exists, they are now stale — they were generated from the old research. Use the style already resolved in Step 3, then automatically re-run both agents in sequence:

1. **Re-run cv-agent** — pass candidate.md, application folder, and the `cv_style_skill` value from Step 3. Verify `cv-data.yaml` is updated.
2. **Re-run cl-agent** — pass candidate.md, application folder, and the `cl_style_skill` value from Step 3. Verify `cl-data.yaml` is updated.

If only `cv-data.yaml` exists (no `cl-data.yaml`), re-run only the cv-agent. Report which agents were cascaded in Step 5.

### If `$agent` is `cv`:

Use the `cv_style_skill` value from Step 3 (e.g., `cv-style-europe`).

Delegate to the `cv-agent` subagent. Pass:
- Full path to `candidate.md` (project root)
- Full path to the application folder
- The `cv_style_skill` value as the CV style skill name to load

**If research was skipped:** Tell the cv-agent explicitly that there is no company research available. The CV should be tailored purely based on the job description and the candidate's profile.

**Verify:** After the agent returns, check that `cv-data.yaml` exists in the folder. If it doesn't, stop and report the failure.

**Stale cover letter warning:** If `cl-data.yaml` exists in the folder, it was built on the previous CV and may now be inconsistent. After reporting the CV rerun results, warn the user:
> The cover letter (`cl-data.yaml`) was generated from the previous CV data and may now be inconsistent. Consider running `/rerun cl [folder]` or `/revise cl [folder] "align with updated CV"` to update it.

### If `$agent` is `cl`:

Use the `cl_style_skill` value from Step 3 (e.g., `cl-style-europe`).

Delegate to the `cl-agent` subagent. Pass:
- Full path to `candidate.md` (project root)
- Full path to the application folder
- The `cl_style_skill` value as the CL style skill name to load

**If research was skipped:** Tell the cl-agent explicitly that there is no company research available. The cover letter should focus on the role requirements and the candidate's fit, not company-specific details.

**Verify:** After the agent returns, check that `cl-data.yaml` exists in the folder. If it doesn't, stop and report the failure.

## Step 5: Report Back

Tell the user:
1. Which agent was re-run and on which folder
2. If `$agent` was `research` and drafts were cascaded, list which agents were re-run automatically and why
3. The agent's tailoring report (technologies prioritized, achievements highlighted, etc.)
4. The updated file path(s)
5. Remind them to run `/format [folder_name]` if drafts are finalized
