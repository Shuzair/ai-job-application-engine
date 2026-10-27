# Job Application Engine — Netherlands

Tailored CV and cover letter for a job in the Netherlands, from one job posting. Personal use: one candidate, Dutch jobs only, Windows + Microsoft Word.

## Use it

1. Keep `candidate.md` (project root) complete and current — every document is built from it.
2. In Claude Code, run `/apply` with the posting pasted after it, or a posting URL, or fill `job-applications/input.md` and run `/apply` on its own.
3. Review the CV and cover letter that open in Word. The PDFs are next to them in `job-applications/output/<company>_<role>_v<n>/`.
4. Change anything with `/revise`, e.g. `/revise make the summary more technical` or `/revise cl shorten the opening`. The PDFs are re-exported each time.

## What it does

- Researches the company (skipped for agency postings with no company name).
- Writes the CV and cover letter in English to Dutch norms: direct, factual, quantified; CV max 2 pages, letter max 1 page and 250–350 words.
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
