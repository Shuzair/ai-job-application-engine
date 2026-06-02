# Job Application Engine

Automates tailored CV and cover letter generation for European job applications.

## Architecture

The system uses a three-layer architecture:

1. **Content Layer (AI-driven):** Agents generate structured YAML data files (`cv-data.yaml`, `cl-data.yaml`) following style skills for tone, bullet rules, and regional norms.
2. **Config Layer (per-style):** Each style skill folder contains its own format config (`cv-format.yaml` / `cl-format.yaml`) and data schema (`cv-data-schema.yaml` / `cl-data-schema.yaml`). These control all visual/layout settings and data validation per country/region/default.
3. **Rendering Layer (deterministic code):** Python scripts (`scripts/render.py`) read YAML data + style-specific config and produce identical docx/pdf output every time. No AI involved in rendering.

## Project Structure

```
candidate.md                          ← candidate profile (single source of truth)
job-applications/input.md             ← fill per application
job-applications/output/              ← versioned folders per application
config/
  style-resolution.yaml               ← country→region mapping for style skill selection
scripts/
  render.py                           ← CLI entry point for rendering
  render_cv.py                        ← deterministic CV docx generator
  render_cl.py                        ← deterministic cover letter docx generator
  validate_schema.py                  ← YAML schema validation utility
  parse_input.py                      ← parses input.md into structured JSON (both main and snapshot formats)
  resolve_style.py                    ← resolves CV/CL style via 4-step cascade (deterministic)
  prepare_folder.py                   ← creates versioned output folder + writes input snapshot
  reset_input.py                      ← resets input.md to blank template
  validate_output.py                  ← validates CV/CL data against style-specific rules (word counts, bullets, etc.)
  run.py                              ← cross-platform venv wrapper for Python scripts
  run.sh                              ← legacy wrapper (delegates to run.py)
requirements.txt                      ← Python dependencies
.claude/skills/apply/                 ← /apply skill (orchestrator)
.claude/skills/format/                ← /format skill (runs rendering script)
.claude/agents/research-agent.md      ← company research subagent
.claude/agents/cv-agent.md            ← CV data generation subagent (outputs YAML)
.claude/agents/cl-agent.md            ← cover letter data generation subagent (outputs YAML)
.claude/agents/job-scanner-agent.md   ← orchestrator: scans all companies in a country list
.claude/agents/career-scanner-agent.md ← sub-agent: scans one company's career page for matching jobs
.claude/skills/cv-style-default/       ← default CV style (SKILL.md + cv-format.yaml + cv-data-schema.yaml)
.claude/skills/cl-style-default/       ← default CL style (SKILL.md + cl-format.yaml + cl-data-schema.yaml)
.claude/skills/cv-style-europe/       ← European CV style (SKILL.md + cv-format.yaml + cv-data-schema.yaml)
.claude/skills/cl-style-europe/       ← European CL style (SKILL.md + cl-format.yaml + cl-data-schema.yaml)
.claude/skills/cv-format-default/     ← (legacy — superseded)
.claude/skills/cl-format-default/     ← (legacy — superseded)
.claude/skills/company-research/      ← company research workflow
.claude/skills/format/scripts/        ← post-render validation script
.claude/skills/rerun/                 ← /rerun skill (re-run single agent)
.claude/skills/profile/               ← /profile skill (manage candidate.md)
.claude/skills/revise/                ← /revise skill (targeted data edits)
.claude/skills/scan/                  ← /scan skill (scan career pages for matching jobs)
.claude/skills/style/                 ← /style skill (create new country/region styles)
generic-cv/                           ← company lists by country + scan results
generic-cv/<country>/                 ← markdown table of companies + matched-jobs.md output
```

## Candidate Profile

`candidate.md` at the project root is required for this project to function. If it is missing or empty, tell the user immediately and suggest running `/profile create` to build it.

Read `candidate.md` before generating any CV or cover letter content. This file is the single source of truth. Never fabricate, invent, or inflate any experience, skill, or metric not documented there.

## Input

`job-applications/input.md` has these section headers: Company, Link, Role, Location, Style, Job Description.

Required fields: Role, Location, Job Description. Optional fields: Company, Link, Style (empty when posting is from an HR agency or company is unknown, or when automatic style resolution should apply).

The `/apply` command reads this file as its starting point.

## Folder Naming

Each application gets a versioned folder under `job-applications/output/`.

Format: `[location]_[company]_[position]_v[n]`

All lowercase, hyphens for spaces. If Company is not specified in input.md, use `no-name` as the company segment.

Location rules:
- Single country: `germany`
- Multiple countries: `de-nl-be`
- Remote with region: `remote(eu)`, `remote(worldwide)`
- Remote with country: `remote(germany)`
- On-site + remote mix: `hybrid(germany)`, `hybrid(de-nl)`
- Version: auto-increment from v1. Check existing folders with same prefix.

## Output Folder Contents

Each folder created by `/apply` contains:
- `input.md` — snapshot of input at time of run
- `research.md` — company research (or placeholder if research was skipped)
- `cv-data.yaml` — structured CV data (content produced by AI agent)
- `cl-data.yaml` — structured cover letter data (content produced by AI agent)
- `cv.docx`, `cover-letter.docx` — rendered draft documents (auto-generated by `/apply`)

After `/revise` with format edits, the folder may also contain:
- `cv-format-override.yaml` — per-application CV format overrides (deep-merged on top of base style config)
- `cl-format-override.yaml` — per-application CL format overrides

After `/format` runs, the folder also contains:
- `cv.pdf`, `cover-letter.pdf`

## Rendering Pipeline

All Python scripts must be run via `python scripts/run.py` which ensures the project venv is used and dependencies are installed. On Mac/Linux, `./scripts/run.sh` also works (legacy wrapper). Never use bare `python3` or `pip install` directly.

The rendering pipeline runs `scripts/render.py` with explicit paths to the style-specific format config and schema:
1. Validates YAML data files against the style's schema (e.g., `.claude/skills/cv-style-europe/cv-data-schema.yaml`)
2. Reads format config from the style's folder (e.g., `.claude/skills/cv-style-europe/cv-format.yaml`)
3. If a per-application override file exists (`cv-format-override.yaml` / `cl-format-override.yaml` in the data folder), deep-merges it on top of the base config
4. Produces docx files deterministically using python-docx
5. Converts to PDF via LibreOffice (if `--pdf` flag is passed)

`/apply` auto-renders docx (no PDF). `/format` re-renders docx and converts to PDF (the "publish" step).

To adjust formatting per-application, use `/revise <cv|cl> [folder] "your formatting feedback"` — this creates override files scoped to that application. To adjust the global style defaults, edit the style's format config directly or use `/style`.

For custom sections defined by a style (e.g., `interests`, `awards`), add the section name to `sections.order` in the style's `cv-format.yaml` and optionally set its layout in `sections.section_types` (`inline`, `list`, or `paragraph`). The renderer handles these generically without code changes. Structured object sections (e.g., `references` with name/company/contact fields) and single-string sections (e.g., `self_pr`) are also handled automatically.

For styles that require a candidate photo (e.g., Germany, Japan), enable the `header.photo` block in `cv-format.yaml` and include `photo_path` in the CV data. The renderer places the photo in the top-right corner using a table-based layout.

## Utility Scripts

These scripts handle deterministic operations that must be consistent across all commands. **Always use these scripts instead of implementing the logic manually.**

| Script | Purpose | Interface |
|---|---|---|
| `parse_input.py` | Parse input.md (main or snapshot format) into JSON | `--input <path>` → JSON to stdout |
| `resolve_style.py` | Resolve CV/CL style via 4-step cascade | `--location <loc> [--style <override>]` → JSON to stdout |
| `prepare_folder.py` | Create versioned output folder + write snapshot | `--input <path> --output-dir <path>` → JSON to stdout |
| `reset_input.py` | Reset input.md to blank template | `--input <path>` |
| `validate_output.py` | Validate CV/CL data against style rules | `--type cv\|cl\|both --data-dir <path> --cv-config <path> --cl-config <path>` → JSON to stdout |
| `open_docx.py` | Cross-platform open/reload docx in Word (close+reopen if already open) | `<path> [<path2> ...]` |
| `validate_style_input.py` | Validate /style identifier (normalize, fuzzy spell-correct, classify, check existing) | `--identifier <name>` → JSON to stdout |
| `scaffold_style.py` | Scaffold style template files from best available base (region→default cascade) | `--identifier <name> --type country\|region\|new [--region <region>]` → JSON to stdout |
| `update_style_resolution.py` | Add country/region to style-resolution.yaml programmatically | `--identifier <name> --type country\|region\|new [--region <region>] [--countries "a,b"] [--alias "k:v"]` → JSON to stdout |

All scripts run via `python scripts/run.py scripts/<name>.py` and are importable as Python modules.

## Style Resolution

Each style skill folder is a **complete, self-contained** object containing content rules (SKILL.md), visual formatting (cv-format.yaml / cl-format.yaml), data validation (cv-data-schema.yaml / cl-data-schema.yaml), and output validation limits (validation block in format.yaml). Only one CV style and one CL style is loaded per application. No inheritance between styles — each is a full copy.

**Use the script for resolution — do NOT implement the cascade manually:**

```bash
python scripts/run.py scripts/resolve_style.py --location "<location>" [--style "<override>"]
```

This outputs JSON with `cv_style`, `cl_style`, `cv_style_skill`, `cl_style_skill`, and all config/schema paths.

### Resolution Algorithm

Resolve the style using the first match (highest priority first):

1. **Explicit override:** If the `Style` field in `input.md` is filled, use that value directly as the style identifier (e.g., `germany` → load `cv-style-germany` / `cl-style-germany`)
2. **Country-specific:** Extract the country from the `Location` field. Normalize it (lowercase, spaces to hyphens). If `cv-style-{country}` exists in `.claude/skills/`, use it
3. **Region fallback:** Look up the country in `config/style-resolution.yaml` to find its region. If `cv-style-{region}` exists, use it
4. **Default:** Use `cv-style-default`

Same logic applies to CL styles (`cl-style-{identifier}`).

### Location Parsing Rules

- **Single country:** "Berlin, Germany" → extract `germany`
- **Multiple countries:** "Germany, Netherlands, Belgium" → use the **first** country (`germany`)
- **Remote with region:** "Remote (EU)" → resolve `eu` alias via `config/style-resolution.yaml` → `europe`
- **Remote with country:** "Remote (Germany)" → extract `germany`
- **Remote worldwide:** "Remote (Worldwide)" → use `default`
- **Hybrid:** "Hybrid (Germany)" → extract `germany`

### Naming Convention

- CV styles: `cv-style-{identifier}` (e.g., `cv-style-germany`, `cv-style-europe`, `cv-style-default`)
- CL styles: `cl-style-{identifier}` (e.g., `cl-style-germany`, `cl-style-europe`, `cl-style-default`)

Style skills are placed in `.claude/skills/{name}/SKILL.md` and auto-discovered by Claude Code.

### Creating New Styles

Run `/style <country|region>` to automatically scaffold, research, and generate all style files. The `/style` command:
1. Validates input with fuzzy spell-correction (`validate_style_input.py`)
2. Scaffolds 6 template files from the best available base — country copies from region style if it exists, otherwise from default; region always copies from default (`scaffold_style.py`)
3. Researches local norms topic-by-topic (A–G) and edits scaffolded files with `[CUSTOMIZE]` markers as guides
4. Updates `config/style-resolution.yaml` programmatically (`update_style_resolution.py`)

Or scaffold manually:
```bash
python scripts/run.py scripts/scaffold_style.py --identifier <name> --type country --region <region>
```

Each style folder needs 3 files: `SKILL.md` (content rules), format config (`cv-format.yaml`/`cl-format.yaml`), and data schema (`cv-data-schema.yaml`/`cl-data-schema.yaml`). Each file must be complete and self-contained — no inheritance from other styles.

If adding a new country manually, update `config/style-resolution.yaml` via:
```bash
python scripts/run.py scripts/update_style_resolution.py --identifier <name> --type country --region <region>
```

## Commands

| Command | Purpose |
|---|---|
| `/apply` | Reads input.md, creates folder, researches company, generates YAML data, auto-renders docx, opens in Word, prints format settings |
| `/rerun <agent> [folder]` | Re-runs a single agent (`cv`, `cl`, or `research`) on an existing folder |
| `/format [folder] [style]` | Finalizes documents as PDF — re-renders docx and converts to PDF. The "publish" step |
| `/revise <cv\|cl> [folder] "feedback"` | Edits content (YAML data) or formatting (per-application override), auto-re-renders docx, opens in Word |
| `/profile` | Create, improve, audit, or add to candidate.md. Use keywords: Create, Improve, Audit, Add |
| `/scan <country>` | Scans career pages from `generic-cv/<country>/` company list, finds matching jobs, saves to `matched-jobs.md` |
| `/style <country\|region>` | Scaffolds 6 template files from the best base style (region→default cascade), researches local CV/CL norms online, then edits each file with country-specific customizations. Handles misspelled input via fuzzy matching |