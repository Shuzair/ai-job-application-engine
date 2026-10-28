# Research: how CVs for data roles are screened (for the recruiter review)

Notes for designing the recruiter-review agent. Each finding names its source; the source's type says how much weight it gets. Full texts are not stored here.

**Weight:** study or survey with a stated method > hiring manager writing from their own screening > recruitment agency advice > vendor/course blog.

## Sources read

| # | Source | Type | Date |
|---|---|---|---|
| S7 | Gergely Orosz, "How to write an effective developer resume: Advice from a hiring manager", Stack Overflow Blog. Hiring manager (Uber Amsterdam, Skyscanner, Skype); interviewed ~24 recruiters and hiring managers at Google, Facebook, Microsoft, Transferwise for *The Tech Resume Inside Out*. | Hiring manager + interviews | Nov 2020 |
| S8 | Chris Garzon, "The Real Reason Your Data Engineering Resume Gets Rejected", Data Engineer Academy. Former data engineer at Amazon and Lyft; founder of a course company (sells coaching in the article). | Hiring manager, commercial | Feb 2026 |
| S9 | "How Much is Too Much Bragging on A Resume?", Association for Psychological Science, summarising Waung, McAuslan, DiMambro & Miegoc (2016), *Journal of Business and Psychology* 32(6), 727–746 — 60 real resumes analysed plus a mock-hiring experiment. | Peer-reviewed study (summary) | Nov 2017 |
| S10 | "Recruiters Don't Read, They Skim: 62% Admit Rejecting CVs Quickly", Kickresume Resume Trends Survey. Online survey, Dec 2025, 1,004 respondents worldwide, only 12% HR-related; Europe 28%. Quotes HR expert Marta Říhová. | Vendor survey | Feb 2026 |
| S11 | "Preparing a good CV", Undutchables (Dutch recruitment agency for internationals). | Dutch agency advice | undated |

## Findings

### 1. Two reads: a short scan decides whether there is a second read
- A quick scan of a few seconds for location, years of experience, languages and technologies, position names, company names, anything that stands out; only if it matches is there a second, top-to-bottom read (S7).
- Hiring-manager scan order for data engineers: current/most recent role and organisation → technologies in the skills section → evidence of having built systems similar to theirs (S8).
- 62% of HR respondents have rejected a candidate without fully reading the CV; 76% say they spend at least 30 s on a CV; early rejection is on "clearly defined requirements… usually visible immediately" (a required technology, a degree, seniority). "Within 30 seconds yes/no on key criteria… within one to three minutes I decide on a prescreen." (S10)
- → **Review check:** within the first third of page 1, can a reader see: the role name, years of experience, the posting's top must-have technologies, and one system similar to theirs?

### 2. The three questions a data hiring manager asks (S8)
1. Can this person solve our specific data problems?
2. Have they built systems similar to what we need?
3. Will they thrive in our technical environment (stack, scale, way of working)?
- → **Review check:** each question gets a yes/partly/no with the CV line that answers it.

### 3. Specific beats general
- Most CVs list responsibilities or "hand-wavy" work; stand out with numbers, active language that shows what *you* did, and the technologies used, woven into the bullet (S7).
- Pair every technical bullet with a business-oriented result; give scale ("ingested 3 billion rows daily from 17 sources", not "built ETL pipelines") (S8).
- Red flags: responsibilities instead of results; tools listed with no context of how they were used; company-internal acronyms and jargon — one to two technical terms per bullet with a plain-language outcome; irrelevant or outdated skills (S8).
- Short, plain sentences starting with a verb (S11).
- → **Review check:** flag bullets with no result or scale, bullets that read as duties, internal acronyms a Dutch reader would have to look up, and stacks of more than ~3 technical terms in one bullet.

### 4. Relevant first, tailored
- The CV's goal is the recruiter call, not the full career story; put what matches this position first, cut older and less relevant detail (S7).
- With work experience, readers weigh: current company and title → technologies → education (less over time) → extracurricular → certifications (generalist tech employers rarely care unless industry-recognised; agencies and traditional companies give some weight) → personal projects (less with experience) → interests (a conversation starter) (S7).
- In most of Europe two pages are common for experienced people; everything relevant must still be on page 1 (S7). Two pages are acceptable with relevant experience; no irrelevant information (S11).
- → **Review check:** is the most relevant role and the strongest match on page 1? Is anything on the CV irrelevant to this posting?

### 5. Technologies: crisp and believable
- Have a technologies section on page 1, but don't rate your level — a listed technology is assumed to be known well (S7). So listing something known only lightly is a credibility risk.
- Positions hiring for specific technologies want to see meaningful work with them, i.e. in the bullets (S7, S8).
- → **Review check:** every technology the posting cares about that the CV lists also appears in a bullet; nothing listed looks thin.

### 6. Confidence, not bragging
- Impression management is very common in resumes and cover letters. A medium amount of self-promotion improved perceived job and organisational fit; the highest intensity was seen as manipulative/disingenuous and ranked lower (S9).
- 58% of respondents keep their CV strictly formal (S10).
- → **Review check:** flag superlatives, self-ratings ("expert", "exceptional"), claims of sole credit for team results, and claims whose scope outruns the evidence. Do not flag plain, confident statements of fact.

### 7. Format and Dutch norms
- Single column; dates, title and company clearly separated; location and technologies easy to find (S7). Clear headings, spacing, simple layout, no spelling errors (S11).
- In the Netherlands a photo is not customary (S11). Nationality and date of birth are "appreciated but not obligatory" (S11) — the project rule stays: never include them (CLAUDE.md).
- Gaps in the employment record make employers "assume the worst"; give a reason (S11).
- References are customary to offer but not required (S11). Employers check references for accuracy (S11).
- → **Review check:** unexplained gaps between roles.

### 8. ATS: disputed
- S8 says many companies filter with an ATS before a human reads. S7 (interviews with recruiters at major tech companies) says automatic "robot rejection" does not happen at tech companies; a human reads the CV.
- → **Design consequence:** the review judges the CV as a human reader; keyword presence is already checked by code (validate_output.py). The review must not push keyword stuffing.

### 9. Cover letters
- A coin toss: large companies often ignore them; smaller firms and start-ups read them. Keep it short, don't repeat the CV, add why you fit (S7).

## Numbers to treat with care
- "7.4 seconds" (Ladders 2018 eye-tracking, cited second-hand in S8), "80% rejected in under 10 seconds" and "92% of hiring managers prioritise quantifiable results" (S8, uncited) — not used as rules.
- S10's sample is mostly non-HR; its recruiter figures rest on ~120 people.

## Still to read
Dutch-specific screening and the analytics-engineer hiring view are thin so far:
- Ladders eye-tracking study (primary)
- Jobseeker NL, "HR-trends 2026" (Dutch HR survey, 1,013 respondents)
- Leiden International Centre, recruiter insights for internationals
- Undutchables, "Writing a strong CV, part 1"
- dbt Labs, "How to hire an analytics engineer" and "How to find a role in analytics engineering"
