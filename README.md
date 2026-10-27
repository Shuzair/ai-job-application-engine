# Job Application Engine — Netherlands

CV and tailored cover letter for a job in the Netherlands, from one job posting. Personal use: one candidate, Dutch jobs only, Windows + Microsoft Word.

The CV is the same for every application: built once from `candidate.md` to Dutch standards. The cover letter is written for each job.

## Use it

1. Keep `candidate.md` (project root) complete and current — every document is built from it.
2. Run `/cv` once to build the master CV (`master-cv/cv.docx`, `master-cv/cv.pdf`). Review it in Word. Run `/cv` again after `candidate.md` changes.
3. For each job, run `/apply` with the posting pasted after it, or a posting URL, or fill `job-applications/input.md` and run `/apply` on its own.
4. Review the cover letter that opens in Word. The CV and both PDFs are next to it in `job-applications/output/<company>_<role>_v<n>/`.
5. Change anything with `/revise`, e.g. `/revise cv make the summary more technical` (changes the master CV for every future application) or `/revise cl shorten the opening`. The PDFs are re-exported each time.

## What it does

- Researches the company (skipped for agency postings with no company name).
- Attaches the master CV unchanged; the cover letter covers what this job asks for that the CV doesn't show, and the report lists requirements you can't match.
- Writes in English to Dutch norms: direct, factual, quantified; A4, CV max 2 pages, letter max 1 page and 250–350 words.
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
