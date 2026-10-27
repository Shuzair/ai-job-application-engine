# Job Application Engine — Netherlands

Personal tool: give it a job posting in the Netherlands, get the CV and a tailored cover letter as docx + pdf. This branch (`netherland`) is for one candidate applying to Dutch jobs only, on Windows with Microsoft Word. There are no other countries, no styles to choose, and no UI.

**One CV for every application.** `/cv` builds a master CV from candidate.md once, to Dutch standards, in `master-cv/`. `/apply` copies it unchanged into each application folder; only the cover letter is written per job.

## Architecture

1. **Content (AI):** subagents write structured YAML following the Netherlands style rules: `cv-data.yaml` once for the master CV, `cl-data.yaml` per application.
2. **Config:** the Netherlands style folders hold the layout and validation limits (`cv-format.yaml` / `cl-format.yaml`) and the data shape (`cv-data-schema.yaml` / `cl-data-schema.yaml`).
3. **Rendering (deterministic code):** `scripts/render.py` turns YAML + config into docx, then exports PDF through Word. No AI involved.

## Project Structure

```
candidate.md                          ← candidate profile (single source of truth, gitignored)
job-applications/input.md             ← fill per application (or paste the JD with /apply)
job-applications/output/              ← one versioned folder per application
master-cv/                            ← the master CV: cv-data.yaml, cv.docx, cv.pdf (gitignored)
config/contracts.yaml                 ← shared strings: style folder names, master CV folder, override filenames, research placeholders
scripts/
  run.py                              ← venv wrapper; forces UTF-8 (the Windows console is cp1252)
  master_cv.py                        ← master CV: status (exists / rendered / stale), copy into a folder, backup
  prepare_folder.py                   ← parses input.md, creates <company>_<role>_v<n>/, writes the input snapshot
  parse_input.py                      ← input.md → JSON (same format for input.md and the snapshot)
  reset_input.py                      ← resets input.md to the blank template
  validate_output.py                  ← checks CV/CL data: schema, limits, JD keyword coverage (CV prose + letter)
  render.py                           ← YAML → docx → pdf, content check, page-count check, opens in Word
  render_cv.py / render_cl.py         ← deterministic docx generators
  render_validate.py                  ← post-render check that every YAML value reached the docx
  validate_schema.py                  ← JSON Schema (YAML) validation
  word.py                             ← Word automation: close an open docx, export PDF + page count, open
  contracts.py                        ← typed loader for config/contracts.yaml
tests/                                ← pytest suite
.claude/skills/cv/                    ← /cv (build the master CV)
.claude/skills/apply/                 ← /apply (orchestrator)
.claude/skills/revise/                ← /revise (targeted edits)
.claude/skills/company-research/      ← research method used by research-agent
.claude/skills/cv-style-netherlands/  ← CV rules (SKILL.md) + cv-format.yaml + cv-data-schema.yaml
.claude/skills/cl-style-netherlands/  ← CL rules (SKILL.md) + cl-format.yaml + cl-data-schema.yaml
.claude/agents/research-agent.md      ← company research (Sonnet; never reads candidate.md)
.claude/agents/cv-agent.md            ← writes the master cv-data.yaml from candidate.md (no job description)
.claude/agents/cl-agent.md            ← writes cl-data.yaml; carries all per-job tailoring
```

## Candidate Profile

`candidate.md` at the project root is required. If it is missing or empty, say so immediately.

Read `candidate.md` before generating any CV or cover letter content. It is the single source of truth. Never fabricate, invent, or inflate any experience, skill, or metric not documented there. When adding to it, keep every detail the user supplies — never condense.

## Netherlands Rules That Override Everything

- Documents are always in **English**. If a posting is written in Dutch, still write in English and tell the user (it usually means Dutch is required).
- Never put nationality, visa, sponsorship or work-permit status in a CV or cover letter (candidate.md → Visa Note). Relocation readiness is fine.
- No photo, no date of birth.

## Input

`job-applications/input.md` sections: Company, Link, Role, Location, Job Description (last — runs to the end of the file, so a pasted posting may contain its own `#` lines).

Required: Role, Job Description. Optional: Company (empty for agency postings → research skipped), Link, Location (a city; defaults to `Netherlands`).

`/apply` also accepts the posting pasted with the command, or a posting URL, and fills `input.md` from it.

## Output Folder

`job-applications/output/<company>_<role>_v<n>/` — lowercase, hyphens, `no-name` when there is no company, version auto-incremented.

- `input.md` — snapshot of the input
- `research.md` — company research, or the skipped placeholder
- `cv-data.yaml`, `cv.docx`, `cv.pdf` (and `cv-format-override.yaml` if the master has one) — copy of the master CV as it was when this application was made
- `cl-data.yaml`, `cover-letter.docx`, `cover-letter.pdf` — the cover letter
- `cl-format-override.yaml` — per-application letter format changes from `/revise` (deep-merged over the style config)

## Master CV

`master-cv/` holds the one CV: `cv-data.yaml`, an optional `cv-format-override.yaml`, `cv.docx`, `cv.pdf`, and `cv-data.previous.yaml` (the data before the last `/cv` rebuild). `/revise cv` edits it here, then copies it into the current application folder; older folders keep what was sent.

```bash
python scripts/run.py scripts/master_cv.py status          # exists, rendered, stale (candidate.md newer than the CV)
python scripts/run.py scripts/master_cv.py copy <folder>   # refuses if missing or not rendered
```

## Rendering

Run every script through `python scripts/run.py scripts/<name>.py` — it uses the project venv, installs `requirements.txt` when it changes, and forces UTF-8 output. Never use bare `python3` or `pip install`.

```bash
python scripts/run.py scripts/validate_output.py <folder> [--type cv|cl|both]
python scripts/run.py scripts/render.py <folder> [--only cv|cl] [--no-pdf] [--no-open]
```

`render.py` fails closed: a schema error, content missing from the docx, or a failed PDF export exits 1 and nothing is reported as generated. It closes the docx in Word first (Word locks open files) and warns when the PDF exceeds `validation.max_pages` (CV 2, letter 1).

Do not hand-edit the docx: it is regenerated from YAML. Use `/revise`.

## Commands

| Command | Purpose |
|---|---|
| `/cv [render]` | Build the master CV from candidate.md → validate → docx + pdf. Run once, and after candidate.md changes |
| `/apply [JD or URL]` | Folder → research → copy master CV → cover letter → validate → docx + pdf → open in Word |
| `/revise [cv\|cl] [folder] feedback` | Content edit (YAML) or format edit (override file), then re-render. CV edits go to the master and are copied into the folder (default: the latest) |

## Tests

```bash
python scripts/run.py -m pytest -q
```
