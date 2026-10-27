# Job Application Engine — Redesign (v4, decisions locked)

*As of 2026-09-26 · Agreed design and final plan · Supersedes v3 (2026-09-24), v2 (2026-09-23) and v1 (2026-09-22)*

---

## 0. Status and change log

| Version | Date | What it was |
| --- | --- | --- |
| v1 | 2026-09-22 | First synthesis of the discussion. |
| v2 | 2026-09-23 | Rebuilt on five research passes and five independent design critiques; answered your eight points of feedback with verdicts; listed 13 open decisions. |
| v3 | 2026-09-24 | All decisions taken. Perspective (local / foreign) becomes a hard matching axis; domain (employer sector) becomes an optional matching axis; the legacy folders are archived rather than migrated; personal data lives in a tracked `local/` folder with ignored contents; the "default" template is replaced by a schema-enforced blank. Phases now carry "done when" criteria. |
| **v4** | **2026-09-26** | **Human-friendliness review applied.** Ten new decisions (16–25): an always-available `_generic` skill so the first run needs no research; plain words wherever the person reads, ids only in files; unknown values ask instead of blocking; the profile is collected progressively in plain language; `/revise` infers its mode and says so; `/apply` takes a URL or a pasted posting and never wipes `input.md`; scripts never surface a traceback; progress and time are shown; Windows encoding is fixed first. The audit table gains four crashes reproduced on Windows and retracts one claim. Phases re-sequenced so the person feels the gains in phases 0–1. |

Appendix A keeps the honest record of how we got here — including the points where I recommended one thing and you decided another, and why the result is still sound. Appendix A.2 records the v4 review of 2026-09-26.

---

## 1. Decisions — final

| # | Decision | Decided | One-line rationale |
| --- | --- | --- | --- |
| 1 | Matching axes | **geo** (required), **perspective** (derived, hard), **role** (required, from a tree), **domain** (optional, default `any`), **work_model** (optional, default `any`) | People search role first, sector second; "data engineer at a bank" is decidable when domain means the employer's sector. |
| 2 | Local vs foreign | **Separate skills per perspective.** A skill is written for a local applicant or a foreign one. Cross-perspective skills are never offered as fallbacks. Fine-grained branches (permit / sponsorship × in-country / abroad) live inside each. A skill may declare `perspective: any` where research finds no difference. | Research focus: "how a foreigner gets hired in Germany" is one coherent question with its own sources. Safety comes from the hard-axis rule. |
| 3 | Seniority | A mandatory researched block per skill (native ladder, canonical map, IC/management track, lexicon, nullable bands, experience clock) and **one shared detector** with a weighted rule. | Grade code decides alone; else title and scope must agree; years only breaks a tie; profile default breaks a remaining tie; else ask. |
| 4 | Residence | **Citizenship or permanent residence** of the target → perspective. **Current residence** → presence. **Work history** → local experience. History is a compulsory yes/no gate with details only on yes. | No recruiter source uses years-resident; UK law forbids inferring right to work from it. |
| 5 | Group-level skills | Allowed (`germany--foreign--data--any--any`); offered as a **visible** fallback for leaf roles; the choice is persisted. Never applied silently. | Prevents the exact-hit rate collapsing to zero under full specification. |
| 6 | Personal data | `local/` inside the repo: folder tracked with `.gitkeep`, contents gitignored. `job-applications/` stays where it is (same pattern already), path configurable. | Proper structure, no accidental commits, second person can use the repo. |
| 7 | Drift | Report only — but a **new** skill must acknowledge or fix its own disagreements with same-geo siblings before it is `ready`. | Accuracy over duplication; unexplained drift must at least be visible. |
| 8 | Employer type | Conditioning input from research front-matter, with a per-skill default. Phase 2. | Gulf government vs MNC; Mittelstand vs startup — today left to the AI's judgement. |
| 9 | First two skills | `germany--foreign--data-engineer--any--any` and `uk--foreign--registered-nurse--any--any` | Private-sector tech without grade codes vs NHS bands with them; both from the foreign perspective, which is the harder case and your own. A local-perspective skill follows in phase 6 as the tooling test. |
| 10 | Legacy 30 folders | Moved to `archive/legacy-styles/` at cutover (out of `.claude/skills/`). **No migration.** Referenced by `/skill create` as undated hints when researching that geo. | They will not fit the new shape; their research is still useful by hand. |
| 11 | Page fit | Render → count pages → trim in the skill's declared order. No converter available → recorded warning, never an AI estimate. | Page fit is a property of the rendered document. |
| 12 | Templates | `styles/_blank` (every required key, every value `TODO`) enforced by `config/rules.schema.yaml` and conformance. `cv-style-default` retired as a source. | Your goal — every skill has the same shape — is enforced harder by a schema than by copying; values come only from research. |
| 13 | Unsourced figures | Dropped unless sourced (e.g. "82% of German recruiters expect a photo"). | Generated prose must not carry folklore as rationale. |
| 14 | Meaning of domain | **The employer's sector** (finance, healthcare, automotive…), not the job family. The job family is the middle level of the role tree and is derived, never asked. | Confirmed 2026-09-24. |
| 15 | Perspective rule | Citizen **or permanent resident** of the target country (or of any country in a target region) → `local`; everyone else → `foreign`. Shown in the decision table; overridable per application. | Confirmed 2026-09-24. US green-card holders, Singapore PRs and UK ILR holders are treated as locals by law and recruiters alike. |
| 16 | First run | **`styles/_generic/`: an always-available, market-neutral skill** (reserved id, outside axis-space, `perspective: any`), seeded from today's default styles. The resolver never returns "none": exact → nearest same-perspective (visible) → `_generic` (visible banner). Never a scaffold source. | A fresh clone with a profile must produce documents before any research; "create a skill" is an offer, never a gate. |
| 17 | Plain words | Everything the person reads — decision table, offers, questions, reports — is plain language ("Germany · foreign applicant · data engineer"). Skill ids, axis names and hashes live in files and appear at most as a secondary line nobody has to type. | Ids are maintainer names. |
| 18 | Unknown values | An unknown geo, role or domain, or a residence without a recorded authorisation, is a **T1 question** with up to three suggestions and an "add as new" option — never a BLOCK. Answers persist as aliases (`local/aliases.yaml`) or profile facts. BLOCK is reserved for a missing or corrupt file. | Principle 8 demands a next step; a question with suggestions is one, a wall is not. |
| 19 | Progressive profile | Compulsory blocks are compulsory **per target country** and asked in plain language; code writes the codes. "I don't know" is accepted for permit flags and stored as `unknown` with one warning. A new geo at `/apply` asks only the missing questions, inside the one batched message, and saves the answers. | The derivations need facts; the person need not know ISO 3166 or permit taxonomy. |
| 20 | `/revise` mode | Optional. When omitted, a bounded classifier (T2) picks `content` or `format`; the report states the choice and its reason; one word flips it; abstain → ask. `--set` and `decision` imply their mode. | A mandatory flag trades one bug for a token everyone must remember. |
| 21 | `/apply` entry | `/apply <url>`, `/apply` with the posting pasted, or the `input.md` file. Fields are extracted (T2, every value a verified substring) and shown in the decision table; low confidence joins the batched question. `input.md` is **never wiped**; a repeated posting (`jd_sha256`) is offered as a new version. | The file is one door, not the only one; a silent wipe is a surprise. |
| 22 | No tracebacks | Every script returns `{ok, error: {code, message, next_step}}`; the wrapper converts uncaught exceptions into the same shape with a log path; skills print `message` and `next_step` verbatim from `config/messages.yaml`. Phase 0. | Verified 2026-09-26: four scripts die with a Python traceback on Windows before any message is shown. |
| 23 | Windows first | `scripts/run.py` forces UTF-8 for every child process; a test runs every script under a cp1252 stdout with non-ASCII input. First item of phase 0. | The owner's machine is Windows; the first experience must not be an encoding error. |
| 24 | Progress and time | Before each agent step `/apply` prints one line with an estimate from recorded durations in `state.json`; `/apply check` shows the decision table and the plan without running agents. | Minutes of silence read as a hang. |
| 25 | Sequence | User-facing wins land in phases 0–1: Windows, structured errors, persistence, `current` pointer, no confirmation round trips, inferred `/revise` mode, decision table, progress. Taxonomies, conformance tiers, drift reports and audit trails follow; `decisions.jsonl` detail sits behind `--audit`. | The person feels phases 0, 1 and 7; the rest is maintainer tooling. |

---

## 2. Product vision

Any person, in any field, at any seniority, produces a CV and cover letter tailored to any country, region, or work model, in English.

- A person creates a profile once: **facts** (citizenships, where they live, work authorisations with expiry, qualifications with dates, languages, target countries, roles and optionally sectors) and **narrative** (experience, projects, stories).
- Per application they hand over the posting — a URL, the pasted text, or a small structured form (company, link, role title, country, city, work model, optional domain, job description). Nothing else is asked unless a derivation is genuinely ambiguous.
- Code derives the person's perspective for that country, resolves the skill for {country, perspective, role, domain, work model}, derives eligibility and presence, detects the posting's seniority from the skill's own lexicon, and records every decision with evidence.
- If no exact skill exists, the person sees the nearest ones with what differs — never one written from the other perspective — or chooses to research a new one. The choice is remembered. If nothing fits, the generic skill is used with a visible banner; applying never waits on research.
- Skills are researched **as whole points**, from one applicant perspective, each describing every seniority level and every eligibility branch relevant to that perspective, with per-rule sources.
- The AI writes content within a contract that code validates; everything else is code.
- The first run works: a fresh clone with a profile produces a CV and cover letter through the `_generic` skill before anyone researches anything. Research improves the result; it never gates it.
- Nothing is a wall: an unknown value is a question with suggestions, an inferred choice is stated and reversible with one word, and the person never types an identifier.

---

## 3. What exists today

Three layers: AI agents write YAML content; per-style YAML configs control visuals and data shape; Python scripts render docx and PDF.

A "style" today is one country or region, a full copy of three files with no inheritance:

| File | Owns | Read by |
| --- | --- | --- |
| `SKILL.md` | writing rules, tone, sections (prose) | cv-agent, cl-agent |
| `cv-format.yaml` | page, fonts, colours, section order, photo, validation limits | render_cv.py, validate_output.py |
| `cv-data-schema.yaml` | shape of cv-data.yaml | render.py, validate_output.py, cv-agent |

15 CV styles and 15 cover-letter styles (~90 files), every one a Claude Code skill under `.claude/skills/` and therefore announced in every session. Resolution: explicit `Style:` → country → region via `config/style-resolution.yaml` → default. Commands: `/profile`, `/apply`, `/revise`, `/rerun`, `/format`, `/scan`, `/style`.

Verified on the owner's Windows machine on 2026-09-26: the console encoding is cp1252; Word is installed and docx2pdf converts in about 7 s per document; LibreOffice is not installed; 14 tests pass and none touch the renderer.

---

## 4. Validated audit findings

Confirmed against the code. The redesign removes each class, not each instance.

| Theme | What is wrong | Evidence |
| --- | --- | --- |
| Rules stated twice, and they disagree | The europe guide allows 4 bullets on a previous role; the validator caps it at 3. Germany and denmark say a photo is expected; their configs set `enabled: false`. `max_pages` is declared in 15 configs and read by nothing. Three skills instruct "match the language of the posting", contradicting English-only. | `validate_output.py:96`, `cv-style-europe/SKILL.md:121`, `cv-style-germany/cv-format.yaml:28`, `cv-style-germany/SKILL.md:26,201` |
| Renderer ignores what schemas declare | 8 schemas declare nationality, visa_status, work_permit etc.; the renderer emits none. Dubai marks two of them *required*. Sections a style asks for (dubai Projects, Interests) vanish if absent from `sections.order`. | `render_cv.py:524-558`, `render_cv.py:562`, `cv-style-dubai/cv-format.yaml:40-45` |
| Structured sections mangled | Dict values are stringified; a usa project with bullets renders a Python list literal. | `render_cv.py:398`, `cv-style-usa/cv-data-schema.yaml:114-134` |
| Gates fail open | "Generated" printed for a PDF that may not exist. Missing config → default style, exit 0. Missing schema path → validation skipped, `valid: true`. Post-render check cannot see table cells, so every photo style fails it on correct output. | `render.py:64,91`, `resolve_style.py:134-191`, `validate_output.py:71,247`, `render_validate.py:131` |
| Input re-parsed from prose | Snapshot re-parse scrapes bold labels out of the JD body; `/format`, `/revise`, `/rerun` re-derive the style from it → the final PDF can use a different style than the draft. Any line starting `# ` inside the JD truncates it. Research-skipped state is detected by grepping placeholder strings. | `parse_input.py:74,101`, `format/SKILL.md:47-57`, `config/contracts.yaml:21-29` |
| Location parsing | "City, Region, Country" → garbage ISO codes and default style. Two countries → *last* (docs say first). `Hybrid (DE-NL)`, the docs' own example → default. | `prepare_folder.py:87-93`, `resolve_style.py:63-78` |
| Style-creation tooling | A region created without countries writes a YAML null that crashes the resolver on every later `/apply`. Fuzzy match with no override: `nepal` → "did you mean malta?", no way forward. | `update_style_resolution.py:218`, `validate_style_input.py:76`, `style/SKILL.md:27` |
| Dead code and features | `/scan` orchestrator lists a tool `SubAgent` that does not exist. `/format generic-cv/` has no producer. The only validator functions the tests cover are unreachable from `/apply`. `audit-check` is loaded as if it were a country. | `job-scanner-agent.md:4`, `format/SKILL.md:22-39`, `validate_output.py:266-270` |
| Permissions and privacy | Blanket `Bash` globs for python3, pip install and curl. `.gitignore` protects only `*.jpg`. The research agent holds `candidate.md` while fetching external URLs. | `.claude/settings.json:16-18`, `.gitignore:60`, `apply/SKILL.md:96` |
| Windows | POSIX continuations and curl-grep fallbacks in prose. `python3` in the permission globs and `run.sh`. `open_docx.py` force-closes any open `cv.docx` from any application. | `apply/SKILL.md:120`, `career-scanner-agent.md:58`, `open_docx.py:57` |
| Tests | 14 tests. Rendering layer 0%. `scaffold_style.py` 0%. No CI, no lockfile. | `tests/` |
| Windows encoding | Four scripts crash with `UnicodeEncodeError` before any message reaches the person: the resolver on every region-lookup location ("London, UK", "Remote (EU)") because the trace contains an arrow; `render.py` on any schema error because the line starts with ✗; `render_validate.py` on every run (✓/✗); `parse_input.py` — and `prepare_folder.py` by the same line — on a JD containing an emoji or an arrow (`ensure_ascii=False`). Console encoding is cp1252. | `resolve_style.py:184,229`, `render.py:49`, `render_validate.py:141`, `parse_input.py:189`, `prepare_folder.py:197` |
| Supplied data never reaches the page | The Germany skill instructs the agent to include date of birth, nationality and work permit; nine schemas accept those fields; the renderer prints only name, titles, location, phone, email, links, relocation and photo. | `cv-style-germany/SKILL.md:75-81`, `render_cv.py` header block |
| Confirmation round trips and guessed intent | `/format`, `/revise` and `/rerun` without a folder each ask "is that correct?"; `/rerun` ships a swapped-argument detector. `/revise` classifies by keyword list: "reorder skills to put Python first" contains "order" and becomes a format edit; "change my title to …" contains "title" and does the same. | `format/SKILL.md:31`, `rerun/SKILL.md:20-28`, `revise/SKILL.md:36,77` |

**Verification (2026-09-26, Windows 11, Python 3.12).** Reproduced by running the code: the four encoding crashes; "Germany, Netherlands" → Netherlands; "Munich, Bavaria, Germany" → default style and folder `mu-ba-de`; "Hybrid (DE-NL)" → default; a `# ` line inside the JD truncates it with `valid: true`; a `**Location:**` label inside the JD overrides the real location on snapshot re-parse; a USA project with bullets renders as `['Designed the schema', 'Wrote 200 tests']`; the post-render check fails Name and Email on a correct photo CV; 14 tests pass, none touch the renderer. PDF conversion through Word succeeded (about 7 s per document; LibreOffice absent). Not re-tested: the region-null crash in `update_style_resolution.py`. **Retracted:** `nepal` returns type `new` with no correction — the "did you mean malta?" dead end did not reproduce.

---

## 5. Design principles

1. **Accuracy over duplication.** A skill is researched as a whole for its exact point. Two skills both saying "Germany expects a photo" is fine. *Unverified copied text* is not — every rule carries sources and a verification date.
2. **One folder, everything in it — for rules.** A person opens a skill and sees every rule that will apply, with rationale and sources. Shared config holds only **identifiers** (taxonomies) and **world facts** (free-movement zones, dated). A rule says what a CV should do; a fact says what the world is.
3. **Skills are points, not layers.** Geo, perspective, role and domain interact; they are researched together and never composed at runtime.
4. **Axes describe the posting and the applicant's standing in that market; conditioning inputs describe the applicant's details or the JD.** Test for any future fact: open-ended value set no one skill can cover → axis; closed set one researcher can describe exhaustively in one session → conditioning, and conformance requires every value described.
5. **Perspective is hard.** A skill written for locals is never offered to a foreign applicant, or vice versa. `any` is a deliberate research finding ("this market does not distinguish"), not a default.
6. **Rules are stated once, as data.** Whatever the AI reads and whatever code checks come from the same `rules.yaml`. Prose is generated.
7. **AI proposes, code decides.** Every AI output passes a code gate; every routing decision is code; every AI decision that affects routing is recorded with extracted evidence and can be overridden.
8. **Gates fail closed.** A wrong or missing input is an error with a next step, never a silent fallback.
9. **Resolve once, persist, never re-derive.** `/apply` writes the decision record; every later command reads only that.
10. **Context cost is constant in the number of skills.** The AI never enumerates skills.
11. **Shape from the schema, values from research.** Every skill has the identical structure because the schema enforces it, not because a template was copied.
12. **English only** for now. Language is a reserved axis name; a conformance rule forbids output-language instructions in generated prose.
13. **Very modular.** Each file has exactly one kind of author: researcher (`rules`, `theme`, `sources`), renderer developer (`layouts/`), maintainer (`config/`), code (`plan.json`, `input.json`, generated `SKILL.md`, `index.yaml`).
14. **Effort is a cost.** Every question, flag, identifier or confirmation the person must handle counts against the design. Prefer an inferred default stated aloud over a flag, a question with suggestions over a block, and plain words over ids.
15. **The first run works.** A fresh clone with a profile produces documents before any research. Missing knowledge degrades the result visibly; it never blocks it.

---

## 6. System boundary: deterministic core, bounded AI edge

Determinism cannot come from sampling settings (Anthropic states temperature 0 was never deterministic; current models reject the knobs; the cause is server-side batching). It comes from shrinking what the model decides, persisting every AI result once, and gating every AI output with code. Every decision point is assigned a tier:

- **T0 — code.** Same inputs, same output.
- **T1 — code; ask the user if undecided.** The answer is persisted.
- **T2 — bounded AI.** Schema'd output; code validates what the decoder cannot (word caps, tiers, provenance); at most two retries with the validator's exact errors fed back; then fail closed. Evidence is extracted text that code verifies. Never re-invoked downstream on the same question.

| # | Decision | Today | Target | Recorded as |
| --- | --- | --- | --- | --- |
| 1 | Parse company / link / role / country / city / work model / domain / JD | free text, prose re-parse | **T0** structured form; or **T2** extraction from a URL or pasted posting, every value a verified substring, shown in the decision table; low confidence → batched question; `jd.txt` raw | `posting.*` + `source`, `jd_sha256` |
| 2 | Geo | comma counting | **T0** validated against `geo.yaml`; unknown → **T1** question with up to three suggestions, answer saved as an alias | `axes.geo` |
| 3 | Perspective | none | **T0** citizen or PR of target → local, else foreign; region: any member country | `axes.perspective` + derived_from |
| 4 | Work model | none | **T0** form field, else JD regex table, else `onsite` | `axes.work_model` + evidence |
| 5 | Role | none | **T0** title matched against the person's target roles for that geo; several or unknown → **T1** question with suggestions or "add as new under <group>" | `axes.role` + source |
| 6 | Domain | none | **T0** form field → research front-matter → profile target (if exactly one) → `any`; unknown value → **T1** question | `axes.domain` + source |
| 7 | Document kind | none | **T0** from skill manifest | `document.kind` |
| 8 | Skill | cascade, re-run per command | **T0** resolver; no exact hit → **T1** ranked nearest (same perspective only) → `_generic` with a visible banner; never "none" | `skill.match` |
| 9 | Seniority | AI (v1) | **T1** weighted code voters; ambiguous → AI extraction proposal (T2) → user confirms | `seniority.*` with spans |
| 10 | Work authorisation, presence | prose in profile | **T0** from profile facts + dated zones table; residence without a recorded authorisation → **T1** question saved to the profile | `origin.*` |
| 11 | Employer type | writer's judgement | **T2** research front-matter; per-skill default | `employer.*` |
| 12 | Run research? | AI reads intent | **T0** company non-empty and no flag | `research.mode` |
| 13 | Research content | AI | **T2** schema'd front-matter; body treated as untrusted input | `research.sha256` |
| 14 | JD language | AI (three skills) | **T0** stopword ratio; warn if not English | `jd_language` |
| 15 | JD signal list | AI, ephemeral | **T2** `jd-signals.yaml`; every quote a verified substring of `jd.txt` | file hash |
| 16 | Section inclusion | AI | **T0** required / optional per level from `plan.json` | validator |
| 17 | Photo | AI | **T0** `rules.photo.expected` AND `profile.photo_path` exists | warning if expected and missing |
| 18 | CV text | AI | **T2** schema + level limits + provenance anchors + signal ids; ≤2 retries | attempts, hashes |
| 19 | CL text | AI | **T2** same + overlap check vs CV | same |
| 20 | Legal-status header line | AI prose | **T0** template over profile facts | `plan.header_lines` |
| 21 | Trim to page limit | AI estimate | **T0** render → pages → `rules.trim_order`; no converter → warning | `trim_applied` |
| 22 | Render docx / pdf | code | **T0**; fail closed on missing PDF | `render-manifest.json` |
| 23 | Post-render check | misses tables | **T0** every text node incl. tables; checks bullets | checks |
| 24 | `/revise` content vs format | AI keywords | **T0** when given or implied (`--set`, `decision`); else **T2** classifier, choice and reason stated, one word flips it; abstain → ask | `revisions[].mode` + `inferred` |
| 25 | `/revise` NL → format patch | AI | **T2** validated against layout token ranges; or **T0** `--set k=v` | patch |
| 26 | `/revise` content edit | AI, unbounded | **T2** plan-then-edit; changes outside the plan rejected | plan, diff |
| 27 | Target folder default | mtime scan | **T0** `job-applications/current` pointer | — |
| 28 | Research skipped? | grep placeholder | **T0** `state.json` | `research.status` |
| 29 | Stale CL after CV rerun | prose warning | **T0** input-hash comparison | `artifacts[].inputs` |
| 30 | Skill scaffold source | cascade from default | **T0** nearest same-region **same-perspective** skill, else `_blank` | `scaffolded_from` |
| 31 | Skill research edits | AI | **T2** `rules.yaml` schema + per-rule sources + conformance | `research_date`, sources |
| 32 | SKILL.md text | hand-written | **T0** generated (full, and filtered per application) | hash |
| 33 | Progress and duration | none | **T0** one line before each agent step with the median of the last five recorded durations | `state.durations` |
| 34 | Repeated posting | none | **T0** `jd_sha256` match against existing folders → offer `v<n+1>` or stop | `posting.repeat_of` |
| 35 | Script failure | traceback | **T0** wrapper converts any uncaught exception into `{ok: false, error: {code, message, next_step, log}}` | `state.failed` |

Eight T2 steps remain (1 when the posting is fetched or pasted, 11, 13, 15, 18, 19, 24 when the mode is omitted, 26; plus 31 at authoring time). Every T2 output is shown to the person and reversible with one word. Everything else is code or code-with-question.

**Recording.** Each application folder carries `input.json` (decision record), `state.json` (state machine plus artefact hashes), and `decisions.jsonl` (append-only: step, model id, prompt template hash, schema hash, input hashes, output pointer, evidence quotes, human action). Hashes and pointers, not copies of candidate text. `decisions.jsonl` is written only with `--audit` or `audit: true` in `config/local.yaml`; the default report shows no hash or model id.

**Reproducibility.** `input.json.engine` records the git commit, scripts hash, Python and dependency versions, layout version. Re-rendering months later = check out that commit, `render.py --folder <dir>`, compare `render-manifest.json`. Re-*generating* prose is a new version folder.

**Honest limits.** Seniority is near-deterministic where a grade code exists and probabilistic in private-sector tech. The design exposes confidence and a user gate rather than promising determinism everywhere. Regenerated prose will differ; the design says so.

---

## 7. Model: a skill is a point in axis-space

A skill covers one combination of geo, perspective, role, domain and work model, researched together as a whole, for one applicant perspective.

Why not orthogonal layers merged at runtime: real interactions would be lost. Grandes-écoles prestige matters for French engineering, not French nursing. The German *Arbeitszeugnis* culture shapes every German CV. Degree recognition is mandatory only for regulated professions in Germany and Canada. And the foreign applicant's question ("how do I get hired here as an outsider") has different sources and different answers from the local's.

Cost: duplication across skills sharing a geo, and one research session per point. Both accepted. Skills are created on demand; one person needs roughly 4–12 (2–3 roles × 2–4 geos, one perspective per geo), typically ~6. Scaffolding from the nearest same-perspective skill and research-vs-confirm modes (section 21) bound the marginal cost without composing anything at runtime. Until a point has a skill, `_generic` serves it (decision 16), so the first application never waits on research.

---

## 8. Axes and conditioning inputs

**Matching axes** select the skill. **Conditioning inputs** select branches inside it.

| Kind | Name | Values | `any` allowed on skill | Source at `/apply` |
| --- | --- | --- | --- | --- |
| axis, hard | `geo` | country id or region id (`germany`, `europe`, `worldwide`) | no | form field, validated |
| axis, hard | `perspective` | `local`, `foreign` | yes — only as a research finding that the market does not distinguish | derived: citizen or PR of target → local |
| axis | `role` | tree id, leaf or group (`data-engineer`, `data`) | no | form title matched to profile targets |
| axis (optional) | `domain` | employer sector id (`finance`, `healthcare`, `automotive`, `e-commerce`, `energy`, `telecom`, `manufacturing`, `education`, `media`, `logistics`, `consulting`, `defence`, `non-profit`, …) | yes (default) | form field → research → profile → `any` |
| axis (weak) | `work_model` | `onsite`, `hybrid`, `remote` | yes (default) | form field or JD regex |
| property | `document.kind` | `cv`, `resume`, `academic-cv` | — | skill manifest |
| conditioning | `seniority` | canonical `entry`, `mid`, `senior`, `executive` + `track: ic \| management` + native label | — | detector over skill lexicon |
| conditioning | `work_authorization` | `citizen`, `permanent-resident`, `treaty-mobility`, `permit-held`, `needs-sponsorship` | — | derived from profile facts |
| conditioning | `presence` | `in-country`, `abroad` | — | derived from current residence |
| conditioning | `employer_type` | `government`, `mnc`, `local-private`, `startup`, `ngo`, `academic`, `unknown` | — | research front-matter; skill default |
| context | `local_experience_years`, `degree_countries`, `experience_countries`, `relocation_date`, `jd_language` | facts | — | derived; passed to writer and templates |
| reserved | `language` | — | — | not built |

**Domain vs employer type.** Domain is *what the business does* (finance, healthcare). Employer type is *what kind of organisation* (government, MNC, startup). A fintech startup: domain finance, type startup. A public hospital: domain healthcare, type government. Domain is chosen by the applicant as a target and selects a skill; employer type is discovered per application by research and selects a branch.

**Perspective vs work authorisation.** Perspective is the coarse question "is this my home market" — decided by citizenship or permanent residence. Work authorisation is the fine question "what paperwork stands between me and starting" — an EU citizen in Germany is `foreign` perspective with `treaty-mobility` authorisation (no visa line, but degree-recognition and language rules may apply). A local skill needs branches for {citizen, permanent-resident}; a foreign skill for {treaty-mobility, permit-held, needs-sponsorship}; an `any` skill for all five.

**Skill id** = `{geo}--{perspective}--{role}--{domain}--{work_model}` with every axis explicit; the folder name must equal the id computed from the manifest. Examples: `germany--foreign--data-engineer--any--any`, `germany--foreign--data-engineer--finance--any`, `uk--foreign--registered-nurse--any--any`, `canada--any--data-engineer--any--any`, `worldwide--any--data-engineer--any--remote`.

**Reserved ids.** `_blank` (the schema-enforced template) and `_generic` (the always-available, market-neutral fallback) start with an underscore, sit outside axis-space and take no part in distance. `_generic` declares `perspective: any`, is offered last and always visibly, and is never a scaffold source.

---

## 9. Taxonomies

`config/taxonomy/roles.yaml` is a tree used for validating role values and computing fallback distance. The **group** level is the job family (what v1 called "domain"); it is derived from the leaf and never asked.

```yaml
families:
  technology:
    software: [backend-engineer, frontend-engineer, fullstack-engineer, mobile-engineer, devops-engineer, qa-engineer]
    data:     [data-engineer, analytics-engineer, data-analyst, data-scientist, ml-engineer]
  commercial:
    sales:     [sales-engineer, account-executive, sales-manager]
    marketing: [marketing-manager, content-marketer, growth-marketer]
  healthcare:
    nursing:   [registered-nurse, icu-nurse, nurse-practitioner]
aliases: {"software engineer": software, "data engineering": data-engineer}
strip_tokens: ["(m/w/d)", "(f/m/x)", "(w/m/d)"]
rules: {unknown_role: ask}           # T1 question: three nearest leaves, or 'add <role> under <group>'; the answer is saved as an alias
```

`config/taxonomy/domains.yaml` is a flat list of employer sectors with aliases (`fintech: finance`, `banking: finance`, `pharma: healthcare`, `public: government-services`…) and `unknown_domain: ask` with the same question shape.

`config/taxonomy/geo.yaml` replaces `style-resolution.yaml`: canonical country ids, regions, aliases (`dubai → uae`, `united-kingdom → uk`), default document kind per geo. `audit-check` is removed.

`config/zones.yaml` is a **dated** fact table of free-movement blocs with a source per row, limited to unambiguous law: EU/EEA/CH, UK–Ireland Common Travel Area, Australia–New Zealand Trans-Tasman. GCC is deliberately absent (work rights there are permit-based for the population this tool serves).

Matching prefers exact, then offers an ancestor (group-level skill) as a visible fallback confirmed once — never descends automatically. Distance: role leaf ↔ its group 10, siblings 20, cousins 40, different family never; domain same 0, to `any` 5, different 15 (offered with a note); work_model same 0, to `any` 3, different 5; geo same 0, country → its region 40, sibling country 60, different region never; **perspective different → never**. When nothing remains, `_generic` is offered with a banner; the resolver never returns none. Aliases learned from answers live in `local/aliases.yaml`, shadow the shared alias tables, and are promoted to `config/taxonomy/` by hand.

---

## 10. Candidate profile

Two files, one author kind each. `local/profile.yaml` holds **facts** code reads; `local/candidate.md` holds **narrative** the writer reads. Personal Details, Target and Languages move out of `candidate.md` in the same change (one-time script with backup).

```yaml
schema_version: 1
identity:
  name: "…"
  legal_name_as_in_passport: "…"        # Gulf and Japan require exact match
  email: …; phone: …; links: {linkedin: …, github: …}
citizenships: [PK]                        # *compulsory*; ISO 3166-1 alpha-2
residence:
  current: {country: DE, city: Berlin, since: 2023-09}            # *compulsory*
  lived_abroad_recently: true            # *compulsory* yes/no: ≥6 months in another country in the last 10 years
  history: [{country: PK, city: Lahore, from: 2018-01, to: 2023-08}]   # only if yes
work_authorizations:                     # *compulsory* for every target country not covered by citizenship or a zone
  - {country: DE, type: eu-blue-card, status: valid, valid_until: 2027-05, employer_bound: true, transferable: false, permanent: false}
qualifications:                          # feeds the experience clock (PQE, post-registration years)
  - {name: "BSc Computer Science", body: "…", awarded: 2018-06, country: PK}
languages:                               # *compulsory*; English required
  - {language: en, level: C1, certificate: "IELTS 7.5, 2024"}
  - {language: de, level: B1}
targets:                                 # *compulsory*; ≥1
  - {geo: germany, roles: [data-engineer, analytics-engineer], domains: [finance], seniority_default: senior}
  - {geo: netherlands, roles: [data-engineer], seniority_default: senior, relocation: {available_from: 2026-11}}
photo_path: assets/photo.jpg             # optional; must exist if set
experience_ids: {exp-1: "Senior Data Engineer @ Afiniti", …}   # stable anchors for provenance
preferences: {skill_choices: {}}         # persisted fallback decisions keyed by axis tuple
```

`domains` on a target is optional. `perspective`, `citizen` and `treaty-mobility` are **derived**, never asked. The research agent never receives this file.

**Progressive collection (decision 19).** `/profile` asks in plain language and writes the codes: "Which passports do you hold?" → `citizenships: [PK]` through `geo.yaml` aliases; "Do you hold a permit or visa for Germany? Which one, until when, and is it tied to your employer?" → one `work_authorizations` entry. Blocks are compulsory only for the countries in `targets`. A new geo at `/apply` asks just the missing questions inside the one batched message and saves the answers. "I don't know" is accepted for `transferable`, `employer_bound` and `valid_until` and stored as `unknown`; the templates omit that clause and the report warns once where the market expects it.

**Why each compulsory field, shown verbatim by `/profile` from `config/profile-questions.yaml`:**

- *Citizenships:* "Decides whether a country is your home market and whether you can work there without a permit. Gulf and Dutch CVs print nationality; UK, Canadian and US CVs must not. We need it to decide, not to display."
- *Current residence:* "Decides whether your CV needs a relocation or availability line and which address format applies. In the Gulf, in-country candidates with transferable permits are shortlisted first; in the US an out-of-area address costs interviews unless replaced by a dated relocation line."
- *Lived abroad recently:* "If you have worked in a target country before, that is local experience employers there value. Answer no if it does not apply."
- *Work authorisation per target country:* "Recruiters in the UK, Australia and the Gulf read visa type and expiry in the header; silence is read as a complication. In Canada and the US it belongs on the application form and must stay off the CV. Without this we cannot choose the right header for {geo}."
- *Qualification dates:* "UK law counts years since qualification, not since your first job; nursing counts post-registration years."
- *Languages:* "Most markets expect language levels; some check that the local language is stated."
- *Target roles and optional sectors per country:* "Rules differ by role and country together; a sector (finance, healthcare) can narrow them further. Naming yours once lets us pick the right skill without asking on every application."
- *Seniority default:* computed from experience dates and shown for confirmation; used only as a tiebreak.

---

## 11. Seniority

**What the research established.** No standard ladder exists across companies even within US software; levels are defined by scope and impact, only the entry rung by years. Where a formal system exists it is a **grade code** bound to a **sector**: NHS Agenda-for-Change bands (set by a 16-factor job evaluation; about half of UK nurses stay at Band 5 for a whole career), UK civil-service grades, US federal GS (one year at the next-lower grade), German TVöD, UK law PQE. Years-of-experience requirements have near-zero validity for performance (81-sample meta-analysis, ρ = .06) and are inflated in postings (61% of US "entry-level" ads require 3+ years). Every formal levelling scheme is multi-factor and scope-led, and every one separates individual-contributor from management tracks. "Associate" alone spans entry to senior depending on industry and country.

**Design.**

1. **Lexicon is per-skill data; the detector is one shared script.** The lexicon is a mandatory research topic.
2. **Native ladder + canonical enum + track.** Code keys on `entry | mid | senior | executive`. Each skill carries its market's native ladder as ordered labels, a native→canonical map checked by conformance, and a track flag. `input.json` records all three. The CV mirrors the native label; the validator reads `levels[canonical]`.
3. **Weighted rule.** Grade code decides alone; else title and scope must agree; years break a tie only; the profile default breaks a remaining tie; else ask.
4. **Bands are nullable** with a rationale.
5. **Experience clock** per skill: `career | since_qualification | in_specialty`.
6. **Confidence exposed**: `high | medium`; `decided_by: grade | vote | tiebreak | user | ai-proposed`.

**Skill block (UK nursing excerpt):**

```yaml
seniority:
  native_ladder: [Band 5, Band 6, Band 7, Band 8a, Band 8b, Band 8c, Band 8d, Band 9]
  native_to_canonical: {Band 5: entry, Band 6: mid, Band 7: senior, Band 8a: senior, Band 8b: executive, Band 8c: executive, Band 8d: executive, Band 9: executive}
  tracks: {ic: [Band 5, Band 6, Band 7], management: [Band 8a, Band 8b, Band 8c, Band 8d, Band 9]}
  experience_clock: since_qualification
  lexicon:
    grade_codes: {pattern: "\\bband\\s*(5|6|7|8[abcd]|9)\\b", map: native}      # decisive when present
    title_markers: {entry: [staff nurse, newly qualified], mid: [junior sister, specialist nurse], senior: [senior sister, advanced nurse practitioner, ward manager], executive: [matron, nurse consultant, head of nursing]}
    scope_markers: {mid: [supervise, mentor students], senior: [lead a shift, manage a team, prescribe], executive: [budget, service redesign, directorate]}
    scope_min_hits: 2
    years_bands: null
    years_rationale: "Band is set by job evaluation, not years; RCN: about half of nurses remain Band 5 for their whole career."
  levels:
    entry:     {cv: {max_pages: 2, summary_style: summary, bullet_tiers: [4, 3, 2], emphasize: [placements, competencies]}, cl: {max_words: 350, paragraphs: [3, 4]}}
    mid:       {cv: {max_pages: 2, summary_style: summary, bullet_tiers: [5, 4, 3], emphasize: [specialty, autonomy]},    cl: {max_words: 350, paragraphs: [3, 4]}}
    senior:    {cv: {max_pages: 2, summary_style: summary, bullet_tiers: [6, 4, 3], emphasize: [leadership, prescribing]}, cl: {max_words: 400, paragraphs: [3, 5]}}
    executive: {cv: {max_pages: 2, summary_style: narrative, bullet_tiers: [6, 4, 2], emphasize: [service, budget, org]}, cl: {max_words: 450, paragraphs: [4, 5]}}
  sources: [s7, s8, s12]
```

**Detector (`scripts/detect_seniority.py`), shared code:**

```
features = extract(jd_title, jd_text)   # normalised title, grade-code matches, years phrases (max lower bound), scope hits per level, all with spans
if grade code matched and in lexicon           → level = map[code]; confidence high; decided_by grade
elif grade code matched but not in lexicon     → ASK (fail closed; lexicon gap recorded)
title = longest-phrase vote or abstain;  scope = argmax hits if ≥ min_hits and margin ≥ 1 else abstain;  years = band(max lower bound) if bands not null else abstain
if title and scope agree                       → level; confidence high; decided_by vote
elif exactly one of title/scope voted (v):
    if years == v                              → v; medium; vote
    elif profile.targets[geo].seniority_default == v → v; medium; tiebreak
    else                                       → ASK, preselect v
elif title and scope disagree                  → ASK, show both with spans
else:
    proposal = AI({level, quotes[]}); every quote must be a literal substring of jd.txt; never auto-accepted → ASK, preselect if valid
track = management if management scope markers ≥ min_hits else ic
sanity: candidate years (per experience_clock) more than one band off → WARNING only
record: level, native_label, track, confidence, decided_by, evidence spans, (model id and prompt hash if AI used)
```

A golden JD corpus per skill (expected level and voter outcomes) is part of conformance. Region-level skills carry a blended, lower-confidence lexicon and are not exempt.

---

## 12. Perspective, eligibility and origin

**What the research established.** Three market patterns exist:

| Pattern | Markets (cited) | What the CV does |
| --- | --- | --- |
| **A** — eligibility line for non-locals only | UK (visa type, expiry, restriction in header), Australia (subclass and expiry; citizens and PRs also state work rights), Germany (residence permit if held; ZAB comparability often requested, esp. public sector) | locals write nothing about status; non-citizens add one line |
| **B** — same fields for everyone, different values | UAE, Saudi Arabia, Qatar (nationality from *all* applicants; visa/Iqama/QID with transferability for expats), Netherlands and Germany (nationality, DOB standard for all), Japan (rirekisho has no nationality field for anyone), Singapore (status line for all) | structure does not branch; values differ |
| **C** — status excluded for everyone | US (authorisation is a yes/no form question; visa status off the résumé; disclosure, if any, in the cover letter), Canada (immigration status on the newcomer portal's exclusion list) | the generator must **not** insert status or nationality |

"Local" is not one fact. Recruiters resolve: can you start without paperwork (authorisation, transferability, expiry); when and at what cost (presence); do you know this market (where past work was done). Law and recruiters treat permanent residents as locals (US green card, Singapore PR, UK ILR), and never infer status from length of residence.

**Design under decision 2.**

**Perspective is the coarse split and a hard axis.** A skill is researched from one audience's standpoint:

- `local` — for citizens and permanent residents. Its eligibility topic asks "what do locals state, if anything" (Pattern A/C: usually nothing; Pattern B: nationality with the local value).
- `foreign` — for everyone else. Its eligibility topic asks "how does a foreign applicant present in this market": disclosure location, permit lines, degree recognition, language prominence, relocation wording, foreign-employer descriptors.
- `any` — declared when research finds the market does not distinguish (Pattern C markets, fully remote worldwide). Requires all five authorisation branches, trivially.

**Derivation (`scripts/derive_origin.py`), code only, runs before skill resolution:**

```
countries = [target] if country else region.member_countries
perspective:
  if any(c in citizenships for c in countries)                              → local
  elif any(valid authorisation with permanent=true for c in countries)      → local
  elif target is worldwide                                                  → any
  else                                                                      → foreign
work_authorization (for the specific target country):
  citizen                                                                   if in citizenships
  permanent-resident                                                        if a valid permanent authorisation exists
  permit-held (type, valid_until, transferable, employer_bound carried)     if a valid non-permanent authorisation exists
  treaty-mobility                                                           if zones.yaml grants work-without-permit for a citizenship (dated; EU/EEA/CH, CTA, TTTA only)
  ASK "You live in {target}. What lets you work there?" — options: the five values above; the answer is saved to profile.yaml   if residence.current == target   # residence never implies right to work
  needs-sponsorship                                                         otherwise
presence = in-country if residence.current.country == target else abroad     (relocation.available_from carried)
local_experience_years = months of experience entries with country == target
warnings: needs-sponsorship and JD matches no-sponsorship phrases; abroad with no available_from where the skill prints one
```

The derived perspective appears in the decision table and can be overridden per application ("treat me as local"); the override is recorded.

**Inside each skill: fine branches keyed on `work_authorization × presence`, scoped to the perspective.** Nationality is a skill-level base rule (`personal_data.nationality: required | optional | forbidden`), rendered from the profile fact. Header lines are **templates over facts**, rendered by code; the writer never composes legal-status text. Every block has a cover-letter side. Privacy rules are validator rules: never render passport, visa grant, Emirates ID, Iqama, SIN, BRP or share-code numbers.

**Foreign-perspective skill, Germany (excerpt):**

```yaml
personal_data:
  nationality: {value: optional, kind: enforced, rationale: "Standard personal-details item; Bundesagentur lists DOB, place of birth, address.", sources: [s2]}
eligibility_disclosure:
  sensitivity: high
  pattern: A
  rationale: "Non-EU applicants without a permit are screened out early unless Blue Card or Chancenkarte eligibility is explicit; ZAB comparability often requested, especially in the public sector."
  sources: [s3, s4, s5]
  cv:
    location: header
    branches:                            # must cover every foreign-perspective value: treaty-mobility, permit-held, needs-sponsorship
      - {work_authorization: treaty-mobility,   presence: in-country, line: null}
      - {work_authorization: treaty-mobility,   presence: abroad,     line: null, relocation_line: true}
      - {work_authorization: permit-held,       presence: in-country, line: "{permit_type} — valid until {valid_until}"}
      - {work_authorization: permit-held,       presence: abroad,     line: "{permit_type} — valid until {valid_until}", relocation_line: true}
      - {work_authorization: needs-sponsorship, presence: any,        line: "Eligible for EU Blue Card — available from {available_from}", note: "State the eligibility route and an availability window."}
  cover_letter: {location: none}
foreign_credentials:
  recognition_note: {value: optional, kind: guidance, applies_when: degree_country != target, rationale: "ZAB Statement of Comparability requested by many employers; mandatory only for regulated professions.", sources: [s6]}
foreign_experience_context:
  employer_descriptor: {value: required, template: "{name} ({industry}, {size_or_rank}, {country})", max_words: 12, sources: [s7]}
```

**Local-perspective skill, Germany** would carry branches for `citizen` and `permanent-resident` × presence (typically `line: null`; a citizen abroad gets `relocation_line: true`), and the same `personal_data.nationality: optional` rule.

**A US skill** (`usa--any--…`): `pattern: C`, `cv.location: never`, `cover_letter.location: paragraph` with a template, `nationality: forbidden`; the validator fails closed if either appears.

Conformance: `sensitivity` and `pattern` mandatory; branches cover every authorisation value relevant to the perspective; templates reference only known fact fields; Pattern B/C skills may declare empty branch tables *with* pattern and sources, so researchers are not pushed to invent differences.

---

## 13. Employer type

Recurs in every research strand: UAE government requires nationality from everyone while MNCs with anti-bias policies want photo/DOB/nationality omitted; the German skill's own rationale says "include for Mittelstand, omit for startups"; grade systems are bound to sector. Today this is left to the writer's judgement from prose.

`research.md` gets front-matter: `employer: {domain: finance, type: startup, evidence: "…"}` — `domain` from the sector list (used for axis resolution when the form field is empty), `type` from the closed set. Skills may branch `by_employer_type` inside eligibility and personal-data blocks; conformance requires a default. When unknown, the skill's default applies and the report says so.

---

## 14. Anatomy of one skill folder

```
styles/germany--foreign--data-engineer--any--any/
  manifest.yaml       id, axes, document.kind, layout, version, content_hash, research_date, status, provenance, scaffolded_from, research.topics, changelog
  rules.yaml          every content rule; all seniority levels; eligibility branches for this perspective; sections; each decision rule = {value, kind, rationale, scope, sources, verified}
  theme.yaml          numbers only; validated against the layout's token schema
  sources.yaml        id → {url, title, tier, published, accessed, excerpt}
  research-log.md     append-only per topic; includes what was taken from archive/legacy-styles as undated hints
  SKILL.md            GENERATED (full, all levels and branches) — never hand-edited
  example/            cv-data.yaml, cl-data.yaml for the smoke render
```

There is **no hand-written `schema.yaml`**: the data shape is compiled from `rules.sections` plus the global entry-type registry in the layout module.

```yaml
id: germany--foreign--data-engineer--any--any
axes: {geo: germany, perspective: foreign, role: data-engineer, domain: any, work_model: any}
derived: {region: europe, family: technology, group: data}
document: {kind: cv}
layout: single-column@1
version: 1
content_hash: sha256:…
created: 2026-10-06
research_date: 2026-10-06
provenance: researched                 # researched | manual
status: ready                          # draft | ready | deprecated
scaffolded_from: {id: _blank}
research:
  topics:
    seniority:      {mode: research, status: researched, date: 2026-10-06, sources: [s1, s2, s7], minutes: 9}
    eligibility:    {mode: research, status: researched, date: 2026-10-06, sources: [s3, s4, s5], minutes: 8}
    sections:       {mode: research, …}
    personal_data:  {mode: research, …}
    format_norms:   {mode: research, …}
    tone_bullets:   {mode: research, …}
covers: [cv, cover-letter]
changelog:
  - {version: 1, date: 2026-10-06, by: manual, summary: "hand-built from _blank as the first proof skill"}
```

`styles/_generic/` has the same anatomy: `id: _generic`, `axes: {geo: worldwide, perspective: any, role: any, domain: any, work_model: any}` (the reserved id is the only one allowed `any` on geo and role), `provenance: manual`, `status: ready`, seeded from today's `cv-style-default` and `cl-style-default`. Its rationales are market-neutral and its rules are `guidance` unless a source supports `enforced`; it passes conformance and the smoke render like any other skill.

---

## 15. Rules as data, prose generated

`rules.yaml` is the single source. Two SKILL.md files are generated from it: a **full** one in the skill folder (every level and branch — for humans and the conformance byte-equality check) and a **filtered** one written into each application's `style/` at `/apply` containing only the resolved level, branches and shared rules. The writer reads the filtered one, so it cannot follow the wrong level because the wrong level is not in front of it (and the context shrinks from 6–9k to 2.5–4k tokens).

**Every decision rule has one shape:**

```yaml
personal_data:
  photo:
    value: expected                    # required | expected | optional | discouraged | forbidden
    kind: enforced                     # enforced (code reads it) | guidance | signal
    rationale: "Bewerbungsfoto still expected by most German employers despite AGG (2006); US-style tech firms indifferent."
    scope: "all levels; Mittelstand and corporates"
    sources: [s1, s3]
    verified: 2026-10-06               # conformance rejects missing
    inherited_from: null               # set when scaffolded and confirmed
    divergence_note: null              # acknowledges an intentional difference from same-geo siblings
    contested: false
```

**Accurate, operationally:** traceable to ≥1 `sources.yaml` entry with tier, URL, published date (or `unknown`), accessed date and a ≤300-char excerpt; geo-specific (and role-specific for role-owned topics); verified in this pass; rationale states norm, scope and exceptions; stated once; passes conformance. **Tiers:** 1 official/legal/standards; 2 institutional market actors in the geo; 3 expert commentary; 4 anecdotal. `enforced` needs ≥1 tier-≤2 or ≥2 agreeing tier-3; `guidance` ≥1 tier-≤3; `signal` any tier, never enforced. `config/source-tiers.yaml` maps known domains to tiers; unknown defaults to 3; the AI cannot self-label.

---

## 16. Theme, layout, and the compile step

| Concern | File | Author | Examples |
| --- | --- | --- | --- |
| **What appears** | `rules.yaml` | researcher | sections and their **order**, headings, photo *expected*, nationality rule, bullet limits per level, tone, date format |
| **How it looks (numbers)** | `theme.yaml` | researcher | page size, margins, two font roles, sizes, line spacing, colour roles, separators, heading case, photo *size* |
| **Structure** | `layouts/single-column/` | renderer developer | slots, entry-type registry, header fields it can draw, photo *positions*, token schema |

```yaml
# layouts/single-column/layout.yaml
name: single-column
version: 1
slots:
  header: {fields: [name, headline, location, phone, email, linkedin, github, nationality, status_line, relocation_line, date_of_birth, photo], photo_positions: [none, top-right, top-left]}
  main:   {section_types: [entry-list, string-list, inline, paragraph, key-value, key-value-comment, publication, numbered, reversed-numbered]}
  letter: {slots: [recipient, date, subject, opening, body, closing, signature, enclosure]}
theme_tokens:
  required: [page.size, page.margins.{top,bottom,left,right}, typography.{heading_font,body_font,body_size,line_spacing}, header.name_font_size, sections.heading_size, colors.{primary,body,link}]
  optional: {header.alignment: center, header.name_case: as-is, sections.heading_case: as-is, sections.heading_underline: false, skills.separator: " | ", photo.width_cm: 3.5, photo.height_cm: 4.5, photo.position: top-right}
  ranges:   {typography.body_size: [9, 12], typography.line_spacing: [1.0, 1.5], page.margins.*: [1.0, 3.0]}
```

The entry-type registry is **global** and lives here, including publication, numbered and key-value-with-comment types that v1's five could not render. Unknown token in a theme → conformance failure. Photo: *expected* is a rule, *size* is theme, *position* a layout parameter — "one shape" is one layout with `photo.position`. Renderer implementation: define named Word styles from the theme once; the layout references style names.

**Compile step.** `scripts/compile_plan.py` reads the application's copied `style/` plus `input.json` (level, work_authorization, presence, employer_type) and any `format-override.yaml`, and writes `style/plan.json`: the fully resolved, branch-free set of everything the validator and renderer need. They read **only** `plan.json`. Branch selection happens exactly once. `plan.json` stamps source hashes; render refuses a mismatched plan.

---

## 17. The application folder

```
job-applications/output/<location>_<company>_<role>_v<n>/
  jd.txt  input.json  state.json  decisions.jsonl  input.md (generated view)
  style/   copied skill + plan.json + filtered SKILL.md
  profile/ snapshot hashes
  research.md (front-matter: employer domain/type, sources)   jd-signals.yaml
  cv-data.yaml  cl-data.yaml  (with provenance anchors)
  cv-format-override.yaml  cl-format-override.yaml  revision-plan.yaml
  render-manifest.json   cv.docx  cv.pdf  cover-letter.docx  cover-letter.pdf
```

**`input.json` (excerpt):**

```json
{"schema_version": 1, "created_at": "2026-10-06T10:01:02Z",
 "engine": {"git_commit": "…", "scripts_sha256": "…", "python": "3.12.10", "python_docx": "1.1.2", "layout": "single-column@1"},
 "posting": {"company": "…", "role_title_raw": "Senior Data Engineer (m/w/d)", "country": "germany", "city": "Berlin", "work_model": "hybrid", "domain": "", "jd_sha256": "…", "jd_language": {"detected": "en", "score": 0.93}},
 "axes": {"geo": "germany", "perspective": "foreign", "role": "data-engineer", "domain": "finance", "work_model": "hybrid",
          "source": {"geo": "input", "perspective": "derived: not a citizen or PR of DE", "role": "profile.targets[0]", "domain": "research", "work_model": "jd:'2 days on-site' @1180"}},
 "skill": {"id": "germany--foreign--data-engineer--any--any", "version": 1, "content_hash": "…", "research_date": "2026-10-06", "age_days_at_apply": 0,
           "match": {"kind": "exact", "wildcards_used": ["domain", "work_model"]}},
 "seniority": {"level": "senior", "native_label": "Senior", "track": "ic", "confidence": "high", "decided_by": "vote", "evidence": {"…": "…"}},
 "origin": {"work_authorization": "permit-held", "presence": "in-country", "permit": {"type": "eu-blue-card", "valid_until": "2027-05", "transferable": false}, "zones_as_of": "2026-09-01"},
 "employer": {"domain": "finance", "type": "mnc", "source": "research"},
 "research": {"mode": "run"},
 "overrides": []}
```

**State machine** (`state.json`, single writer `scripts/state.py`): `created → resolved → researched | research_skipped → signals_extracted → cv_drafted → cl_drafted → draft_rendered → published`, with `needs_user(question)` and `failed(step)`. Every command declares allowed from-states; `/format` on a non-rendered or stale folder is an error. `artifacts[name] = {sha256, produced_by, inputs}`; staleness is a hash comparison. `state.json` also records `durations[step]`; `/apply` prints the median of the last five before each agent step (decision 24). The source `job-applications/input.md` is never reset by code; a run whose `jd_sha256` matches an existing folder is offered as `v<n+1>` or stopped (decision 21).

---

## 18. Skill registry and resolution

Zero style skills under `.claude/skills/` — only process skills (`apply`, `format`, `revise`, `rerun`, `profile`, `skill`). Styles live in `styles/<id>/` as data.

`scripts/resolve_skill.py` is the **only** reader of the registry. It builds the axes→path map from manifests at runtime (never stale), validates axis values against the taxonomies, and returns JSON: an exact hit (all axes equal or the skill declares `any`; prefer fewest wildcards), or up to three ranked candidates **from the same perspective** with per-axis differences, then `_generic` with a banner — "No skill covers Nepal · foreign applicant · data engineer yet. Using the generic skill: no country norms applied. Say *research nepal* to create one (about 25 minutes)." The resolver never returns none, and every offer prints plain words with the id as a secondary line. `styles/index.yaml` is a generated, committed snapshot; a test asserts it equals a rebuild. The AI never reads either; `/apply` passes the resolved path to the writer agent.

An accepted fallback is persisted in `profile.preferences.skill_choices` keyed by the axis tuple, reused visibly ("using X, your choice on <date>; say *reconsider* to change"), re-asked only when a strictly closer skill appears. Draft skills are offered only with explicit confirmation.

Context cost per writer run ≈ 12–19k tokens, independent of skill count: instructions ~3k + filtered SKILL.md 2.5–4k + compiled schema ~1.3k + narrative 3–6k + JD 0.8–2k + research 1–2k + values ~0.3k.

---

## 19. Application flow (`/apply`)

**Entry (decision 21).** Three doors, one result: `/apply https://…` fetches the posting; `/apply` followed by the pasted posting; or `/apply` alone reads `job-applications/input.md`. From a URL or pasted text, code extracts company, link, role title, country, city, work model and domain (T2, every value a verified substring of `jd.txt`) and shows them in the decision table with `source: extracted`; a low-confidence field joins the one batched question. The file form stays for people who prefer it:

```
# Company        [optional]
# Link           [optional]
# Role           [job title exactly as listed]
# Country        [free text; validated against geo.yaml aliases — unknown → one question with suggestions]
# City           [optional]
# Work model     [remote | hybrid | onsite | blank = detect from JD]
# Domain         [optional: employer sector, e.g. finance, healthcare — blank = from research or profile, else any]
# Skill          [optional exact skill id override]
# Job Description
```

`input.md` is never reset. A posting whose `jd_sha256` matches an existing folder is offered as `v<n+1>` or stopped.

**Order:** parse → derive perspective, authorisation, presence → research (if company; yields employer domain/type) → resolve domain → resolve skill → detect seniority → compile plan → signals → CV → CL → render. `resolve_application.py` returns `decisions{}` (value, source, evidence), `questions[]` and `gates[]`; `/apply` prints gates verbatim from `config/messages.yaml`, asks all open questions in **one** batched message, re-runs with answers, persists. Profile facts learned this way are saved to `profile.yaml`; application facts to `input.json`. Before each agent step `/apply` prints one line — `Research · about 2 min (median of your last 5 runs)`. `/apply check` is the dry run: the decision table and the plan, no agents.

**Report header** (plain words; ids only as secondary lines):

```
Decisions (change any with /revise decision <field> <value>):
  country      Germany                          from the posting
  applicant    foreign applicant                not a citizen or permanent resident of Germany
  role         data engineer                    matches your target role for Germany
  sector       finance                          research: "Series-C payments platform"
  work model   hybrid                           posting: "2 days on-site per week"
  skill        Germany · foreign applicant · data engineer   exact match · sector and work model covered as "any" · researched today
               id germany--foreign--data-engineer--any--any
  level        senior, individual contributor   title "Senior" · scope: mentor, own, architect · 5+ years   confidence high
  status       permit held, in Germany          profile: EU Blue Card, valid to 2027-05
  employer     multinational                    research
Time: research ~2 min · CV ~3 min · cover letter ~2 min (median of your last 5 runs)
Warnings: none
```

When `_generic` is used, the skill line becomes a banner:

```
  skill        Generic (no country norms)       no skill covers Nepal · foreign applicant · data engineer yet — say "research nepal" to create one (~25 min)
```

**Bounded AI contract** for CV and CL: the agent receives the filtered SKILL.md, compiled schema, level and branch values, `jd-signals.yaml`, narrative, research. Every bullet and paragraph carries `src` (into `experience_ids`/narrative anchors) and `signals`. `validate_output.py` checks schema, level limits from `plan.json`, anchor resolution, signal ids, forbidden fields, privacy identifiers, CL/CV overlap. Failures fed back verbatim; ≤2 retries; then `failed(step)`.

**Trim to fit:** render → PDF → count pages (Word via `docx2pdf` on Windows; LibreOffice elsewhere) → apply `rules.trim_order` until it fits; record `trim_applied`. No converter → recorded warning.

**`/revise` grammar:** `/revise <cv|cl> [content|format] [--folder NAME] [--set KEY=VALUE …] ["instruction"]`. Mode optional (decision 20): `--set` implies `format`; otherwise a bounded classifier picks one and the report says so — `Treating this as a content edit (you mentioned the summary). Say "format" if you meant the look.` — and that one word re-runs with the other mode; if the classifier abstains, it asks. A golden set ("reorder skills to put Python first" → content; "make the font bigger" → format; "change my title to Senior Data Engineer" → content) is part of the evals. `format --set` is pure code; `format` with instruction → AI patch validated against token ranges, diff shown; `content` → AI declares JSON pointers first, code rejects changes outside the plan. `/revise decision <field> <value>` overrides a recorded decision (e.g. perspective) and re-resolves.

---

## 20. Skill creation and lifecycle (`/skill create`)

**Prompting.** `geo` and `role` are asked, each with a one-line why and three examples, validated; fuzzy match offers "Did you mean X? [yes] [no, add '<value>' as new under <group>]". `domain` is asked as optional ("blank = applies to every sector; give one only if you are targeting a specific industry"). `work_model` is shown with default and provenance. **`perspective` defaults from the creator's own profile for that geo** — "your profile makes you a foreign applicant in Germany; building the foreign-perspective skill. Change to local or any?" — since one person only needs one perspective per country. `document.kind` is derived and shown. Before research, a confirmation card: the id, each axis with value and source, the nearest same-perspective skill with per-axis differences, the research plan with estimated time and provenance, "proceed?". The card speaks plain words — `Germany · foreign applicant · data engineer` — with the id as a secondary line; the person never types one. `/apply` offers this command, with the time estimate, whenever `_generic` was used.

**Scaffolding.** From the nearest skill **in the same region and the same perspective**; otherwise from `styles/_blank`. There is no cross-perspective scaffolding — the research is different. Every copied rule is stamped `verified: false, inherited_from`; conformance refuses `ready` while any remains. `cv-style-default` is not a source, and neither is `_generic`.

**Legacy reference.** The research plan lists `archive/legacy-styles/cv-style-<geo>/` and `cl-style-<geo>/` (if present) as undated tier-3 hints to read for that geo's format norms, section names and local terminology — never as sources for enforced rules.

**Research plan** from `config/research-topics.yaml`: mode `research` if the topic is mandatory, or the source is `_blank`, or its owner axes intersect the changed axes; else `confirm` (re-open cited sources, record `accessed`, answer the role-specific sub-question). **Always research:** seniority for this geo + role; eligibility disclosure **for this perspective**; sections; personal data; format norms. The researcher agent receives **only** the axes and the plan.

**Conformance (`skill_conform.py`):** folder == derived id; axes in taxonomies; `rules.yaml` valid against `config/rules.schema.yaml`; every evidence-required path has sources meeting the tier rule; no `verified: false`, `TODO` or `[CUSTOMIZE]`; mandatory topics researched this pass; seniority block complete; eligibility block has `sensitivity`, `pattern`, and branches covering every authorisation value relevant to the perspective; every section has a heading and a registry type; theme validates against the layout tokens with no extras; dead-key check against the consumed-paths list the renderer and validator publish; CL fields tagged `must_match_cv` equal CV values; generated SKILL.md byte-equals regeneration; no output-language instruction; golden JD corpus passes; smoke render of `example/` passes including table cells; index row matches manifest; no unsourced numeric claim in any rationale.

**Versioning and staleness.** `version` (integer; index build refuses a content change without a bump), `content_hash`, `research_date`, `status`. Staleness computed, warned at 365 days (180 for fast-moving topics), shown in the offer and recorded per application. `/skill refresh <id>` re-runs mandatory topics in research mode, the rest in confirm mode, bumps the version.

**Drift report** (`skill_drift.py`, exit 0 always): groups ready skills by geo **and perspective**; lists geo-owned rule paths that disagree, with rationales; `divergence_note` acknowledges a genuine interaction. Runs in the suite as a report and at the end of `/skill create`, where the new skill must acknowledge or fix its own disagreements before `ready`.

---

## 21. Scale and context cost

| | Single user | Shared repo, this design | Shared repo if origin were fine-grained axes |
| --- | --- | --- | --- |
| Possible points | — | ~40 geos × 2 perspectives × ~30 roles ≈ 2,400 (fewer where `perspective: any`) | × 5 authorisation values ≈ 6,000 |
| Realised on demand | 4–12 (~6) | 200–600 | 600–1,600 |
| Cross-user reuse | — | everyone sharing a perspective in that market | only when authorisation status matches |
| Update cost when a geo's norms shift | 1–3 skills | up to 2N in that geo | 5N |

Research cost per new skill is bounded by same-perspective scaffolding: sharing a geo and perspective with the source researches ~4 role topics + 2 always-topics and confirms ~7; from `_blank`, all ~13. Time estimates come from `manifest.research.topics[].minutes` across existing skills, shown as a range with provenance. First-run cost is zero research: `_generic` serves every point until a skill exists.

**Second person without forking.** Engine (`scripts/`, `layouts/`, `styles/`, `config/`, `tests/`) is the repo. The person is `local/` (tracked folder, ignored contents): `profile.yaml`, `candidate.md`, `styles-local/`. `job-applications/output/` already follows the same pattern and stays; its path is configurable in `config/local.yaml`. The index covers `styles/` and `styles-local/`; local shadows shared for the same id with a printed provenance line. CI rejects any content under `local/`.

---

## 22. Testing

1. **Conformance** over every `styles/*/` — pure Python, ~20 ms each; every PR.
2. **Golden-text renders per layout** — a kitchen-sink fixture per layout exercising every entry type, a photo, a project with bullets, a bullet with a colon; compare extracted docx text. PDF only here.
3. **Smoke render per skill** — `example/` data; post-render check including table cells; no golden files. Changed skills on PRs; all nightly.
4. **Table-driven tests** for the deterministic parts: perspective and origin derivation over (citizenships, residence, authorisations, target) tuples — Irish citizen in London → local, citizen; German citizen arrived UK 2022 → foreign, needs-sponsorship; NZ citizen in Sydney → foreign, treaty-mobility (indefinite); Indian citizen with transferable UAE visa → foreign, permit-held; US green-card holder in Berlin applying to New York → local, permanent-resident, abroad; Italian in Berlin applying to Germany → foreign, treaty-mobility; seniority golden JD corpus per skill; `zones.yaml` has a source and effective date per row; the matcher is total and never returns a cross-perspective candidate.
5. **Phase 0 experiment:** canonicalise the docx zip and test for equal sha256 across renders. Outcome decides whether docx goldens are hashes or extracted text.
6. **Windows and error-shape tests:** every script runs under a cp1252 stdout with non-ASCII input and exits cleanly; every script, given a missing or corrupt input, exits non-zero with a `{ok: false, error: {code, message, next_step}}` body and never a traceback; `config/messages.yaml` covers every error code (completeness test).
7. **Contract tests between schema, rules and renderer:** every header field and section a schema or `rules.sections` declares is consumed by the renderer (consumed-paths list) or the check fails; a structured item with a list value renders as bullets, never as a list literal.
8. **Evals for the two bounded classifiers:** the `/revise` mode golden set, and posting extraction over ten real postings (company, role, country, work model), including one with an emoji and one with a `# ` heading inside the description.

---

## 23. Final plan

Each phase leaves the repo working and ends with the full suite green. Phase 0 starts on your word.

| Phase | What | Done when | Depends on |
| --- | --- | --- | --- |
| **0** | **Windows, no dead ends, safety net.** (1) `scripts/run.py` forces UTF-8 for every child process; every script's output is UTF-8-safe; a test runs each script under a cp1252 stdout with non-ASCII input. (2) Structured errors: every script returns `{ok, error: {code, message, next_step}}`, the wrapper wraps uncaught exceptions with a log path, `config/messages.yaml` exists with a completeness test, and the skills print messages verbatim. (3) Fail-closed gates: PDF must exist; missing config/schema/style are errors; the post-render check reads table cells and checks bullets. (4) The renderer honours today's schemas: every header field a legacy schema declares renders or leaves the schema; list values inside structured items render as bullets; every schema-declared section is in `sections.order` (test). (5) Reconcile the legacy prose/validator disagreements (Europe bullets, Germany and Denmark photo comments) and remove output-language instructions from three skills. (6) Hygiene: drop blanket `Bash` globs; `.gitignore` every image type plus the future `local/` contents; `python` not `python3`; pin dependencies; create `local/` with `.gitkeep`. (7) Docs: README and CLAUDE.md drop `/scan` and `generic-cv/`, the `/scan` skill is disabled with a message, and the PDF section names Word on Windows and LibreOffice elsewhere. (8) `config/taxonomy/geo.yaml` (dubai→uae, uk aliases, no audit-check); golden-text render tests and a conformance test over today's code; docx canonicalisation experiment. | Every script passes the cp1252 test; every failure path exits non-zero with a structured message (test); a Germany CV with date of birth and nationality renders them; a USA project renders bullets; README's commands and tree match the repo; experiment result recorded in this document. | — |
| **1** | **Persist, structure, and the daily flow.** `/apply` from a URL, pasted text or `input.md`, with substring-verified extraction; `jd.txt`, `input.json`, `state.json` with the state machine and step durations; `input.md` never reset; repeat detection by `jd_sha256`; materialised `style/` per application; `job-applications/current` pointer and no confirmation round trips; `/format`, `/revise`, `/rerun` read only the folder and refuse a hash mismatch with a next step; `/revise` with optional mode, stated inference and `--set`; decision table in plain words for what exists at this phase (country, style, research mode, folder); progress lines with recorded durations; `/apply check`; open questions batched into one message. | Re-running `/format` on an existing folder cannot change its style; a pasted JD containing an emoji and a `# ` line runs to a rendered draft with zero questions; no command asks "is that correct?"; a folder without `input.json` is refused with the F1 message. | 0 |
| **2** | **Profile and derivations.** `profile.yaml` schema; `/profile` rework with per-target compulsory blocks, plain-language questions, why-texts and code-written codes, `unknown` accepted for permit flags; one-time migration of Personal Details, Target and Languages out of `candidate.md`; `config/zones.yaml`; `derive_origin.py` (perspective, work_authorization, presence; a residence without authorisation asks) and `detect_seniority.py` with table-driven tests; research front-matter with employer domain and type; `config/taxonomy/roles.yaml` and `domains.yaml` with `unknown: ask` and `local/aliases.yaml`. | The derivation test table passes; `/profile audit` fails closed on a missing compulsory block for a target country only; a new target at `/apply` asks just the missing questions; the research agent no longer receives `candidate.md`. | 1 |
| **3** | **Rules as data and the layout contract.** `config/rules.schema.yaml` (seniority block, perspective-scoped eligibility block, per-rule sources, kinds, tiers); `theme.yaml`; `layouts/single-column/layout.yaml` with token schema and entry-type registry; `compile_plan.py`; SKILL.md generator (full and filtered); dead-key check; `skill_conform.py`; `styles/_blank`; **`styles/_generic`** built from `_blank` and seeded from today's default styles, market-neutral, `status: ready`. **Hand-build the two proof skills** from `_blank`: `germany--foreign--data-engineer--any--any`, `uk--foreign--registered-nurse--any--any`. | Both proof skills and `_generic` pass conformance, the proof skills including their golden JD corpora; a deliberately broken skill (missing branch, unsourced enforced rule, dead theme key) fails; `_generic` renders the kitchen-sink fixture. | 2 |
| **4** | **Registry and cutover.** `styles/` outside `.claude/skills/`; manifests; `resolve_skill.py` with the hard-perspective rule, the distance table and `_generic` last — it never returns none; offers in plain words with the id as a secondary line; generated `index.yaml` with CI check; `cv-writer` process skill reading a path; persisted fallback choices. **Move the 30 legacy folders to `archive/legacy-styles/`**; remove the old resolver. | No style skill appears in the session skill list; an application resolves by dictionary lookup; a fresh clone with only a profile completes `/apply` for any geo through `_generic` with the banner; a cross-perspective candidate never appears in a fallback offer (test). | 3 |
| **5** | **Generic renderer.** Registry types incl. publication / numbered / key-value-comment; header fields from `plan.json`; status-line templates from facts; named Word styles; trim-to-fit with page count; `render_validate` over all text nodes; layout goldens. | Both proof skills render the kitchen-sink fixture and their `example/` data; the UK nurse fixture with a photo passes the post-render check; a locale header field declared in rules appears in the docx. | 3 |
| **6** | **`/skill create` and lifecycle.** Prompted axes with perspective defaulted from the creator's profile; the plain-language confirmation card with the id as a secondary line; same-region same-perspective scaffolding or `_blank`; legacy folder referenced as hints; research/confirm modes; `sources.yaml` tiers; versioning and staleness; drift report with acknowledgement; `/skill refresh`; researcher isolated from candidate data; the offer from `/apply` after a `_generic` run. **Build the third skill with the tool:** a local-perspective skill for the creator's home country and primary role — the local-perspective and tooling test. | The third skill passes conformance without hand edits; the drift report runs at creation and the skill acknowledges or fixes its disagreements. | 4, 5 |
| **7** | **`/apply` integration, remainder.** `resolve_application.py` with the full decision table (perspective, role, sector, level, status, employer); `jd-signals.yaml` with substring verification; provenance anchors; bounded retry; `decisions.jsonl` behind `--audit`; `/revise decision`. | An end-to-end `/apply` on a real posting produces a CV whose every bullet resolves to a profile anchor, with zero questions asked in the common case; the default report contains no hash or model id. | 6 |
| **8** | **Retire and document.** Remove `/style`; decide `/scan` (fix the tool name or delete); rewrite README and CLAUDE.md to match; this document becomes `docs/design.md`. | README's commands and folder tree match the repo exactly. | 7 |

---

## 24. Deferred and out of scope

- **Language axis.** Name reserved; a conformance rule forbids output-language instructions meanwhile.
- **Multiple candidates.** Single-person profile; the per-geo authorisation map moves under a candidate id if needed.
- **`/scan`.** Broken (`SubAgent` tool) and a prompt-injection surface. Removed from the docs and disabled with a message in phase 0; fixed or deleted in phase 8.
- **Audit trail depth.** `decisions.jsonl` (model ids, prompt-template hashes, engine stamps) is written only with `--audit` or `audit: true` in `config/local.yaml`; the default report never shows it.
- **Pay range as a seniority signal.** Legally present only in some US states and, from June 2026, EU postings; optional per-skill table later.
- **New Zealand eligibility guidance** could not be verified; research before an NZ skill.
- **Long-term permit-holder as local.** Decided: legal status (citizen/PR) decides perspective; a person may override per application. Revisit only if a researched skill shows a market treats long-term residents differently from other permit holders.

---

## Appendix A. How we got here

### A.1 The v2 review (2026-09-23)

The v2 review answered your eight points of feedback with verdicts. This is the record, including the points where I recommended one thing and you decided another.

| Point | v2 verdict | Final |
| --- | --- | --- |
| 1. Seniority needs its own researched skill | Adopt the observation (market-specific, strongly evidenced); change the container — a mandatory block inside each point skill plus one shared detector. | As v2. |
| 2. Different skills for local and foreign applicants | I recommended branches inside one skill: the difference is 1–3 header lines, Gulf markets use the same fields for everyone, Canada/Japan/NL have no difference, and fallback across the two would be fail-open. | **You decided perspective is a skill-level axis** for research focus. Made safe by three mechanisms: perspective is a hard axis (never cross-offered); the fine branches stay inside each skill; `any` is available where research finds no difference. Cost accepted under accuracy over duplication. |
| 3. As deterministic as possible | Adopt and go further; be honest about the ceiling. | As v2. |
| 4. Index instead of loading skills | Adopt; the AI does not read the index either. | As v2. |
| 5. Theme numbers in the skill, structure separate | Adopt; three-way split; section order stays a rule; one layout with a photo parameter. | As v2. |
| 6. Origin and residence in the profile, compulsory | Adopt; facts not categories; machine-readable file; residence history a cheap gate. | As v2, with your clarification that residence links to perspective — resolved as citizenship/PR → perspective, current residence → presence. |
| 7. Domain compulsory; each combination its own skill | Adopt compulsory role; I proposed one tree axis and retiring "domain". | **You clarified domain means the employer's sector**, optional, role first. Adopted as an optional axis; the job family is derived from the role tree. |
| 8. Tell me where I am wrong | Honoured. | Honoured. |

**Where v1 was wrong:** it contradicted itself on where seniority lives; its global years-bands and title lists were contradicted cell by cell; its four-value origin enum conflated authorisation with presence; its justification "origin does not change the market" was wrong (the NHS band *is* the posting; Nitaqat makes nationality market-level); its equal-weight vote let years outvote a title; its per-skill schema was the source of the "renderer ignores schema" class; its "explicit location grammar" was a smaller bug surface, not zero; it carried the unsourced 82% figure; its origin block was CV-only.

### A.2 The v4 review (2026-09-26)

A human-friendliness review of v3 against the running code, on the owner's Windows machine. Every recommendation was adopted; no v3 decision was reversed. Decision 2 (perspective as a hard axis) stands — its friendliness cost, a smaller fallback set, is what `_generic` offsets.

| Finding | v3 | v4 |
| --- | --- | --- |
| Four scripts crash on Windows before any message | not known | decision 23; first item of phase 0 |
| A fresh user needs researched skills before the first CV | `_blank` only; default retired; resolver may return "none" | decision 16: `_generic`, never none |
| Skill ids in the person's face | ids in the decision table and offers | decision 17: plain words, id secondary |
| BLOCK on unknown geo, role, domain, or an unrecorded authorisation | `unknown_role: fail`; BLOCK with suggestions | decision 18: T1 questions, answers persisted |
| Compulsory profile facts as codes | compulsory blocks with why-texts | decision 19: per target, plain language, `unknown` accepted |
| Mandatory `/revise` mode | mode mandatory | decision 20: inferred, stated, one word flips |
| `input.md` the only door, silently wiped | structured form; today's reset kept | decision 21: URL, paste or file; never wiped; repeat detection |
| Tracebacks as errors | messages in phase 7 | decision 22: structured errors in phase 0 |
| Minutes of silence | — | decision 24: progress and duration |
| The person feels phases 0, 1 and 7 | user-facing pieces in phase 7 | decision 25: re-sequenced |
| Header fields declared by nine schemas never render | audit row, fixed in phase 5 | phase 0 item (4); consumed-paths test |
| "nepal → did you mean malta?" | audit row | retracted; not reproduced |

---

## Appendix B. Sources

Load-bearing citations behind sections 11–16. All pages were opened, not quoted from snippets.

**Seniority semantics.** Levels.fyi, *Standard SWE Level Framework* — <https://www.levels.fyi/blog/swe-level-framework.html> · Dropbox Engineering Career Framework — <https://dropbox.github.io/dbx-career-framework/> · GOV.UK DDaT Capability Framework, software developer — <https://ddat-capability-framework.service.gov.uk/role/software-developer> · SFIA — <https://sfia-online.org/en/about-sfia/how-sfia-works> · NHS Agenda for Change job matching (RDaSH) — <https://www.rdash.nhs.uk/policies/nhs-agenda-for-change-job-matching-and-evaluation-procedure/> · RCN on Band 6 — <https://www.rcn.org.uk/About-us/Our-Influencing-work/Position-statements/rcn-position-on-nursing-being-a-band-6-profession> · OPM GS qualification policies — <https://www.opm.gov/policy-data-oversight/classification-qualifications/general-schedule-qualification-policies/> · TVöD Stufen — <https://www.oeffentlichen-dienst.de/tvoed/bund/stufen.html> · Institute for Government, civil service grades — <https://www.instituteforgovernment.org.uk/explainer/civil-service-grades> · Van Iddekinge et al., prehire experience meta-analysis — <https://digitalcommons.unf.edu/unf_faculty_publications/785/> · SHRM on entry-level requirements — <https://www.shrm.org/topics-tools/news/talent-acquisition/entry-level-experience-requirements-hurting-hiring> · Mercer IPE — <https://www.mercer.com/solutions/talent-and-rewards/job-architecture/job-evaluation-ipe/> · jobriver.de, lise.de on German Junior/Senior — <https://jobriver.de/ratgeber/junior-mid-level-oder-senior-karrierestufen-in-der-it-erklart>, <https://www.lise.de/insights/artikel/ab-wann-senior-developer/> · LinkedIn seniority field — <https://www.linkedin.com/help/recruiter/answer/a415043/>.

**Foreign vs local applicants.** Duke — <https://careerhub.students.duke.edu/resources/u-s-job-internship-search-strategy-for-international-students/> · Purdue OWL — <https://owl.purdue.edu/owl/job_search_writing/preparing_an_application/tips_and_terms.html> · UH Bauer — <https://careercenter.bauer.uh.edu/resources-for-international-students/> · EEOC — <https://www.eeoc.gov/pre-employment-inquiries-and-citizenship> · DOJ IER FAQ — <https://www.justice.gov/crt/iers-frequently-asked-questions-faqs> · UK National Careers Service — <https://nationalcareers.service.gov.uk/careers-advice/cv-sections> · Manchester careers, visa — <https://www.careers.manchester.ac.uk/international/ukworkafterstudy/talkingtoemployersaboutyourvisa/> · GOV.UK recruiting from outside the UK — <https://www.gov.uk/guidance/recruiting-people-from-outside-the-uk> · Settlement.Org — <https://settlement.org/ontario/employment/find-a-job/resume/what-do-i-include-in-my-canadian-resume-what-do-i-exclude/> · OHRC application forms — <https://www.ohrc.on.ca/en/iv-human-rights-issues-all-stages-employment/4-designing-application-forms> · RMIT résumé guide — <https://www.rmit.edu.au/content/dam/rmit/rmit-images/students/Life-and-work-opportunities/Jobs-and-career-advice/Careers-Resume-2018.pdf> · CVShark, work rights — <https://cvshark.com.au/guides/work-rights-on-australian-resume> · GulfTalent — <https://www.gulftalent.com/resources/dubai-jobs-guide/building-your-profile> · Labeeb (private; government) — <https://www.labeeb.ae/best-cv-format-for-dubai-a-complete-guide-for-job-seekers>, <https://labeeb.ae/should-you-include-photo-nationality-visa-status-on-a-uae-government-cv/> · ProHireWrite, Saudi — <https://prohirewrite.com/en/nationality-on-saudi-resume/> · Qatar Living — <https://www.qatarliving.com/en/article/writing-first-cv-qatar-job-market> · Make-it-in RLP — <https://make-it-in.rlp.de/en/for-skilled-workers/searching-and-applying-for-jobs/tips-on-job-applications-in-germany> · Bundesagentur ZAV — <https://www.arbeitsagentur.de/vor-ort/zav/working-and-living-in-germany/iss-en/issue-01-2026/application-cv> · ZAB — <https://zab.kmk.org/en/statement-comparability> · Anerkennung in Deutschland — <https://www.anerkennung-in-deutschland.de/html/en/pro/assessment-higher-education-qualifications.php> · The Hague International Centre — <https://www.thehagueinternationalcentre.nl/how-to-write-a-cv-in-the-netherlands> · MHLW rirekisho — <https://kouseisaiyou.mhlw.go.jp/assets/pdf/methods/04.pdf> · TAFEP — <https://www.tal.sg/tafep/getting-started/fair/tripartite-guidelines>.

**What makes someone "local".** Home Office Code of Practice — <https://www.gov.uk/government/publications/right-to-work-checks-code-of-practice-on-avoiding-discrimination/code-of-practice-for-employers-avoiding-unlawful-discrimination-while-preventing-illegal-working-6-april-2022-accessible-version> · GOV.UK sponsor licence — <https://www.gov.uk/uk-visa-sponsorship-employers> · Common Travel Area — <https://www.gov.uk/government/publications/common-travel-area-guidance> · Your Europe, work permits — <https://europa.eu/youreurope/citizens/work/work-abroad/work-permits/index_en.htm> · Directive 2003/109 Art. 15 — <https://www.legislation.gov.uk/eudr/2003/109/article/15> · u.ae work permits — <https://u.ae/en/information-and-services/jobs/Sector-of-employment/employment-in-the-private-sector/work-permits> · NZ MFAT on SCV 444 — <https://www.mfat.govt.nz/en/countries-and-regions/australia-and-pacific/australia/new-zealand-high-commission-to-australia/living-in-australia/moving-to-australia/immigration-status-visa-residency-and-citizenship> · MOM Fair Consideration Framework — <https://www.mom.gov.sg/employment-practices/fair-consideration-framework> · NBER digest of Oreopoulos — <https://www.nber.org/digest/sep09/why-do-skilled-immigrants-struggle-labor-market> · OHRC, "Canadian experience" — <https://www.ohrc.on.ca/en/policy-removing-canadian-experience-barrier> · SHRM, local applicants — <https://www.shrm.org/topics-tools/news/hr-magazine/ask-hr-expert-can-advertise-local-applicants>.

**Deterministic LLM pipelines.** Anthropic glossary — <https://platform.claude.com/docs/en/about-claude/glossary> · Messages API — <https://platform.claude.com/docs/en/api/messages> · Thinking Machines, *Defeating Nondeterminism* — <https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/> · Anthropic structured outputs — <https://platform.claude.com/docs/en/build-with-claude/structured-outputs> · Anthropic citations — <https://platform.claude.com/docs/en/build-with-claude/citations> · *Building Effective Agents* — <https://www.anthropic.com/engineering/building-effective-agents> · *Equipping Agents with Skills* — <https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills> · 12-Factor Agents — <https://github.com/humanlayer/12-factor-agents> · Instructor re-ask — <https://python.useinstructor.com/concepts/reask_validation/> · Pydantic AI retries — <https://pydantic.dev/docs/ai/core-concepts/retries/> · Guardrails on_fail — <https://www.guardrailsai.com/docs/concepts/validator_on_fail_actions> · AWS Step Functions + Bedrock — <https://aws.amazon.com/blogs/compute/validating-multi-agent-decisions-with-step-functions-and-bedrock-agentcore/> · CaMeL — <https://arxiv.org/abs/2503.18813> · Temporal determinism — <https://docs.temporal.io/workflow-definition> · OpenTelemetry GenAI — <https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md> · EU AI Act Art. 12 — <https://artificialintelligenceact.eu/article/12/> · Microsoft HAX — <https://www.microsoft.com/en-us/haxtoolkit/guideline/support-efficient-correction/> · LangChain HITL — <https://docs.langchain.com/oss/python/langchain/human-in-the-loop> · Reproducible Builds — <https://reproducible-builds.org/docs/definition/> · DVC repro — <https://doc.dvc.org/command-reference/repro> · Stripe idempotency — <https://docs.stripe.com/api/idempotent_requests>.

**Theme vs layout in CV generators.** JSON Resume — <https://jsonresume.org/theme-development> · RenderCV — <https://docs.rendercv.com/user_guide/yaml_input_structure/design/>, <https://docs.rendercv.com/user_guide/yaml_input_structure/cv/> · Reactive Resume — <https://rxresu.me/schema.json>, <https://docs.rxresu.me/guides/using-custom-styles> · Awesome-CV — <https://raw.githubusercontent.com/posquit0/Awesome-CV/master/awesome-cv.cls> · moderncv — <https://raw.githubusercontent.com/moderncv/moderncv/master/moderncvstyleclassic.sty> · Typst modern-cv — <https://raw.githubusercontent.com/DeveloperPaul123/modern-cv/main/lib.typ> · OpenResume — <https://raw.githubusercontent.com/xitanggg/open-resume/main/src/app/lib/redux/settingsSlice.ts> · OOXML theme part — <https://learn.microsoft.com/en-us/previous-versions/office/developer/office-2007/cc964302(v=office.12)>.
