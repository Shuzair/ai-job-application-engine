# Job Application Engine

A Claude Code-powered workflow for generating tailored CVs and cover letters with deterministic document rendering.

## Architecture

The system uses a three-layer architecture:

1. **Content Layer (AI-driven):** Agents generate structured YAML data files following style skills for tone, bullet rules, and regional norms.
2. **Config Layer (per-style):** Each style skill folder contains its own format config and data schema. These control all visual/layout settings and data validation per country/region/default.
3. **Rendering Layer (deterministic code):** Python scripts read YAML data + style-specific config and produce identical docx/pdf output every time.

## Prerequisites

| Dependency | Required | Purpose |
|---|---|---|
| [Python 3](https://www.python.org/downloads/) | Yes | Runs all rendering, validation, and utility scripts |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Yes | Powers the AI agents and slash commands that generate CV/CL content |
| [LibreOffice](https://www.libreoffice.org/) | No | Converts `.docx` to `.pdf` during `/format`. Without it, only `.docx` files are produced |

Python dependencies (`python-docx`, `PyYAML`, `jsonschema`, `docx2pdf`) are installed automatically by `scripts/run.py` into a local `venv/` — no manual `pip install` needed.

## Setup

1. Install Python 3 and Claude Code (VS Code extension or CLI)
2. Clone this repo and open it in VS Code with Claude Code
3. Run `/profile create` to build your `candidate.md` through a guided interview
4. You're ready to go — fill `job-applications/input.md` and run `/apply`

## Workflow: Job Application

1. Fill `job-applications/input.md` with company and JD details (Company and Link are optional — leave empty for HR agency postings)
2. Run `/apply` — creates versioned folder, optionally researches company, delegates to agents for structured YAML data. **Note:** `input.md` is automatically reset to a blank template after each run.
3. Review the generated `cv-data.yaml` and `cl-data.yaml` (structured YAML — easy to review and edit)
4. For targeted edits without regeneration, run `/revise cv "make the summary more technical"` or `/revise cl "tone down the opening"`
5. If a data file needs full regeneration, run `/rerun cv [folder]` or `/rerun cl [folder]`
6. Run `/format [folder_name]` — auto-resolves the style from input.md, reads the style's format config and schema, renders cv.docx, cv.pdf, cover-letter.docx, cover-letter.pdf
7. To adjust formatting (fonts, colors, margins, etc.), edit the style's format config (e.g., `.claude/skills/cv-style-europe/cv-format.yaml`) and re-run `/format`

To skip company research explicitly: tell Claude "apply without research" or "skip research".

## Workflow: Career Page Scanning

1. Place a markdown file with a company table (including a "Careers Page" column) in `generic-cv/<country>/`
2. Run `/scan <country>` — the job-scanner-agent parses the company list and delegates to career-scanner sub-agents
3. Each career page is scanned using a cascade: HTTP fetch → ATS API detection → keyword filtering → curl fallback
4. Jobs matching 60%+ of your candidate profile are collected into `generic-cv/<country>/matched-jobs.md`
5. To resume an interrupted scan, run `/scan <country>` again — already-scanned companies are skipped

## Commands

| Command | What it does |
|---|---|
| `/apply` | Reads input.md, creates versioned folder, optionally researches company, delegates to agents for YAML data |
| `/rerun <agent> [folder]` | Re-runs a single agent (`cv`, `cl`, or `research`) on an existing folder. When re-running `research`, automatically cascades to update dependent data files. |
| `/format [folder] [style]` | Runs deterministic rendering: resolves style → validates YAML → reads style-specific config → generates docx/pdf. Style arg required for generic-cv/ folders |
| `/revise <cv\|cl> [folder] "feedback"` | Makes targeted edits to YAML data without full regeneration |
| `/profile create` | Build `candidate.md` from scratch through a guided interview |
| `/profile improve` | Rewrite and fill gaps in an existing `candidate.md` |
| `/profile audit` | Read-only quality review with a scored report |
| `/profile add` | Append new experience, project, or certification to `candidate.md` |
| `/scan <country>` | Scans career pages from `generic-cv/<country>/` company list, finds matching jobs, saves to `matched-jobs.md` |
| `/style <country\|region>` | Scaffolds 6 template files from the best base style (region→default cascade), researches local CV/CL norms online, then edits each file with country-specific customizations. Handles misspelled input via fuzzy matching |

## Rendering Pipeline

The `/format` command resolves the style (same cascade as style resolution), then runs `scripts/render.py` with explicit paths to the style-specific format config and schema:
1. Validates YAML data against the style's schema (e.g., `.claude/skills/cv-style-europe/cv-data-schema.yaml`)
2. Reads format config from the style's folder (e.g., `.claude/skills/cv-style-europe/cv-format.yaml`)
3. Produces `.docx` files deterministically using `python-docx`
4. Converts to `.pdf` via LibreOffice CLI (if available)

For custom sections defined by a style (e.g., `interests`, `awards`), add the section name to `sections.order` in the style's `cv-format.yaml` and set its layout in `sections.section_types` (`inline`, `list`, or `paragraph`). Structured object sections (e.g., `references`) and single-string sections (e.g., `self_pr`) are also handled automatically.

For styles that require a candidate photo, enable `header.photo` in the format config and include `photo_path` in the CV data.

## Format Configuration

All visual/layout decisions are controlled by per-style format configs — no AI interpretation:

- `.claude/skills/cv-style-{name}/cv-format.yaml` — page size, margins, fonts, colors, section order, heading style, spacing
- `.claude/skills/cl-style-{name}/cl-format.yaml` — same but for cover letters (designed to visually match the CV)

Each style has its own complete format config. No inheritance — each is a full copy. Edit the style's config to change fonts, colors, section ordering, etc. Re-run `/format` to see changes.

## Project Structure

```
├── CLAUDE.md                             ← project rules (Claude reads automatically)
├── candidate.md                          ← your profile (swap per person)
├── requirements.txt                      ← Python dependencies
├── config/
│   └── style-resolution.yaml             ← country→region mapping for style skill selection
├── scripts/
│   ├── render.py                         ← CLI entry point for rendering
│   ├── render_cv.py                      ← deterministic CV docx generator
│   ├── render_cl.py                      ← deterministic cover letter docx generator
│   ├── validate_schema.py                ← YAML schema validation utility
│   ├── parse_input.py                    ← parses input.md into structured JSON
│   ├── resolve_style.py                  ← resolves CV/CL style via 4-step cascade
│   ├── prepare_folder.py                 ← creates versioned output folder + writes snapshot
│   ├── reset_input.py                    ← resets input.md to blank template
│   ├── validate_output.py                ← validates CV/CL data against style rules
│   ├── validate_style_input.py           ← validates /style identifier (normalize, fuzzy spell-correct)
│   ├── scaffold_style.py                 ← scaffolds style template files from best available base
│   ├── update_style_resolution.py        ← adds country/region to style-resolution.yaml
│   ├── run.py                            ← cross-platform venv wrapper for Python scripts
│   └── run.sh                            ← legacy wrapper (delegates to run.py)
├── .claude/
│   ├── settings.json                     ← permission settings
│   ├── agents/
│   │   ├── research-agent.md             ← company research subagent
│   │   ├── cv-agent.md                   ← CV data generation (outputs YAML)
│   │   ├── cl-agent.md                   ← cover letter data generation (outputs YAML)
│   │   ├── job-scanner-agent.md          ← orchestrator: scans all companies in a country list
│   │   └── career-scanner-agent.md       ← sub-agent: scans one company's career page for matches
│   └── skills/
│       ├── apply/SKILL.md                ← /apply command (orchestrator)
│       ├── format/SKILL.md               ← /format command (runs render script)
│       ├── rerun/SKILL.md                ← /rerun command (re-run single agent)
│       ├── revise/SKILL.md               ← /revise command (targeted data edits)
│       ├── profile/SKILL.md              ← /profile command (manage candidate.md)
│       ├── cv-style-default/             ← Default CV style
│       │   ├── SKILL.md                  ← content/writing rules
│       │   ├── cv-format.yaml            ← visual formatting config
│       │   └── cv-data-schema.yaml       ← data validation schema
│       ├── cl-style-default/             ← Default CL style
│       │   ├── SKILL.md                  ← content/writing rules
│       │   ├── cl-format.yaml            ← visual formatting config
│       │   └── cl-data-schema.yaml       ← data validation schema
│       ├── cv-style-europe/              ← European CV style
│       │   ├── SKILL.md                  ← content/writing rules
│       │   ├── cv-format.yaml            ← visual formatting config
│       │   └── cv-data-schema.yaml       ← data validation schema
│       ├── cl-style-europe/              ← European CL style
│       │   ├── SKILL.md                  ← content/writing rules
│       │   ├── cl-format.yaml            ← visual formatting config
│       │   └── cl-data-schema.yaml       ← data validation schema
│       ├── cv-format-default/SKILL.md    ← (legacy — superseded)
│       ├── cl-format-default/SKILL.md    ← (legacy — superseded)
│       ├── company-research/SKILL.md     ← company research workflow
│       ├── scan/SKILL.md                 ← /scan command (career page scanning)
│       ├── style/SKILL.md                ← /style command (create new country/region styles)
│       └── format/scripts/validate.py    ← post-render content checker
├── job-applications/
│   ├── input.md                          ← fill this per application
│   └── output/                           ← versioned folders per application
└── generic-cv/                           ← company lists by country + scan results
    └── <country>/                        ← markdown table of companies + matched-jobs.md output
```

## Folder Naming Convention

Each application folder follows: `[location]_[company]_[position]_v[n]`

Examples:
- germany_cargo-one_senior-data-engineer_v1
- de-nl_seedtag_data-engineer_v1
- remote(eu)_company_analytics-engineer_v1
- hybrid(germany)_company_senior-de_v1
- remote(eu)_no-name_data-engineer_v1

If the company is not specified in input.md (HR agency posting), `no-name` is used as the company segment.

## Adding New Styles

Each style is a complete, self-contained object — content rules, visual formatting, and data validation. Only one CV style and one CL style is loaded per application. No inheritance between styles.

Style resolution order: explicit `Style` field in `input.md` → country-specific skill → region fallback (via `config/style-resolution.yaml`) → default.

Run `/style <country|region>` to automatically scaffold, research, and generate all style files. The `/style` command:
1. Validates input with fuzzy spell-correction (`validate_style_input.py`)
2. Scaffolds 6 template files from the best available base — country copies from region style if it exists, otherwise from default; region always copies from default (`scaffold_style.py`)
3. Researches local norms topic-by-topic and edits scaffolded files with `[CUSTOMIZE]` markers as guides
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

Claude Code auto-discovers skills from `.claude/skills/` — no other config changes needed.