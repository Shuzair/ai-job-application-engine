# Job Application Engine — Netherlands

Personal tool: give it a job posting in the Netherlands, get a tailored CV and cover letter as docx + pdf. This branch (`netherland`) is for one candidate applying to Dutch jobs only, on Windows with Microsoft Word. There are no other countries, no styles to choose, and no UI.

## Architecture

1. **Keywords (AI):** `keyword-agent` reads the posting first, then `candidate.md`, and writes `jd-keywords.yaml`: the role (title, analytics/data engineer family, junior/medior/senior) and the ranked keywords, each marked as something the candidate has (with evidence), has an analogue for, or lacks. The CV and the cover letter are both written from this one list.
2. **Content (AI):** subagents write the text for each job as structured YAML (`cv-data.yaml`, `cl-data.yaml`) following the Netherlands style rules, section by section from the keywords and the profile. The shape is fixed by `cv-data-schema.yaml` / `cl-data-schema.yaml`.
3. **Fixed layout (deterministic code):** `scripts/nl_template.py` is the one Netherlands layout for an international data / analytics engineer: A4, Calibri 11 pt, one column, fixed section order (summary, technical skills, experience, projects, education, certifications, languages, interests) and six fixed skill categories. Not configurable per application; to change the look of every document, change its constants.
4. **Rendering:** `scripts/render.py` validates the YAML, renders it through the template, checks every value reached the docx, then exports PDF through Word. No AI involved.

## Project Structure

```
candidate.md                          ← candidate profile (single source of truth, gitignored)
job-applications/input.md             ← fill per application (or paste the JD with /apply)
job-applications/output/              ← one versioned folder per application
config/contracts.yaml                 ← shared strings: style folder names, keyword file, research placeholders
scripts/
  run.py                              ← venv wrapper; forces UTF-8 (the Windows console is cp1252)
  prepare_folder.py                   ← parses input.md, creates <company>_<role>_v<n>/, writes the input snapshot
  parse_input.py                      ← input.md → JSON (same format for input.md and the snapshot)
  reset_input.py                      ← resets input.md to the blank template
  validate_output.py                  ← checks CV/CL data: schema, limits (CV_LIMITS / CL_LIMITS), keyword coverage against jd-keywords.yaml
  render.py                           ← YAML → docx → pdf, content check, page-count check, opens in Word
  nl_template.py                      ← the fixed layout for the CV and the cover letter
  render_validate.py                  ← post-render check that every YAML value reached the docx
  validate_schema.py                  ← JSON Schema (YAML) validation
  word.py                             ← Word automation: close an open docx, export PDF + page count, open
  contracts.py                        ← typed loader for config/contracts.yaml
tests/                                ← pytest suite
.claude/skills/apply/                 ← /apply (orchestrator)
.claude/skills/revise/                ← /revise (targeted edits)
.claude/skills/company-research/      ← research method used by research-agent
.claude/skills/jd-keywords/           ← keyword extraction method (SKILL.md) + jd-keywords-schema.yaml
.claude/skills/cv-style-netherlands/  ← CV writing rules (SKILL.md) + cv-data-schema.yaml
.claude/skills/cl-style-netherlands/  ← CL writing rules (SKILL.md) + cl-data-schema.yaml
.claude/agents/research-agent.md      ← company research (Sonnet; never reads candidate.md)
.claude/agents/keyword-agent.md       ← writes jd-keywords.yaml (Sonnet; runs in parallel with research)
.claude/agents/cv-agent.md            ← writes cv-data.yaml
.claude/agents/cl-agent.md            ← writes cl-data.yaml
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
- `jd-keywords.yaml` — the posting's ranked keywords mapped to the candidate
- `cv-data.yaml`, `cl-data.yaml` — content
- `cv.docx`, `cv.pdf`, `cover-letter.docx`, `cover-letter.pdf` — rendered

## Rendering

Run every script through `python scripts/run.py scripts/<name>.py` — it uses the project venv, installs `requirements.txt` when it changes, and forces UTF-8 output. Never use bare `python3` or `pip install`.

```bash
python scripts/run.py scripts/validate_output.py <folder> [--type cv|cl|both|keywords]
python scripts/run.py scripts/render.py <folder> [--only cv|cl] [--no-pdf] [--no-open]
```

`validate_output.py` rejects a keyword marked as a gap (`match: "no"`) listed as a CV skill, and warns about any must-have keyword the candidate has that the CV does not show.

`render.py` fails closed: a schema error, content missing from the docx, or a failed PDF export exits 1 and nothing is reported as generated. It closes the docx in Word first (Word locks open files) and warns when the PDF exceeds the page limit (CV 2, letter 1).

Do not hand-edit the docx: it is regenerated from YAML. Use `/revise`.

## Commands

| Command | Purpose |
|---|---|
| `/apply [JD or URL]` | Folder → research + keywords (parallel) → CV → cover letter → validate → docx + pdf → open in Word |
| `/revise [cv\|cl] [folder] feedback` | Text edit (YAML), then re-render docx + pdf. The layout is fixed. Folder defaults to the latest |

## Tests

```bash
python scripts/run.py -m pytest -q
```
