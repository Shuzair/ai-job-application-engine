# Job Application Engine — Netherlands

Tailored CV and cover letter for a job in the Netherlands, from one job posting. Personal use: one candidate, Dutch jobs only, Windows + Microsoft Word.

## Use it

1. Keep `candidate.md` (project root) complete and current — every document is built from it.
2. In Claude Code, run `/apply` with the posting pasted after it, or a posting URL, or fill `job-applications/input.md` and run `/apply` on its own.
3. Review the CV and cover letter that open in Word. The PDFs are next to them in `job-applications/output/<company>_<role>_v<n>/`.
4. Change anything with `/revise`, e.g. `/revise make the summary more technical` or `/revise cl shorten the opening`. The PDFs are re-exported each time.

## What it does

- Researches the company (skipped for agency postings with no company name).
- Extracts the posting's keywords from the posting alone (`jd-keywords.yaml`), then maps your profile three ways: job → you (do you have each keyword, how strongly), you → job (your achievements ranked for this employer, including what the posting only implies) and company → you (verified company facts that connect to your background).
- Every mapped claim quotes `candidate.md` word for word and carries an evidence strength (shipped, built, tooling, certified, learning, planned). The validator checks every quote exists, that everything you have made it into the CV, and that nothing you lack — or know only from tooling, a certificate or a plan — is listed as a skill.
- Writes each section to Dutch norms for data and analytics engineer roles, with the emphasis set by the role (analytics vs data engineer) and seniority (medior / senior).
- Uses one fixed layout for every application (`scripts/nl_template.py`), built for an international data / analytics engineer: A4, Calibri, one column, summary → technical skills → experience → projects → education → certifications → languages → interests. Only the text changes per job.
- Never puts nationality, visa or sponsorship in the documents; relocation readiness only.
- Flags a posting written in Dutch, which usually means Dutch is required.
- Checks the data against the schema and the style limits, checks every value reached the docx, and checks the PDF page count.

## Requirements

- Windows with Microsoft Word (PDF export and opening documents)
- Python 3.10+; `python scripts/run.py` creates `venv/` and installs `requirements.txt` on first use

## Tests

```bash
python scripts/run.py -m pytest -q
```

See `CLAUDE.md` for how the pieces fit together.
