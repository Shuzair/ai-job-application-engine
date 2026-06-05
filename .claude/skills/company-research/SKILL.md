---
name: company-research
description: Research a company for job applications. Use this skill whenever you need to gather information about a company — for CV tailoring, cover letter writing, interview prep, or any context where understanding a company's product, tech stack, culture, and recent news is needed. Triggers on phrases like "research this company", "what does this company do", "find out about", or when the /apply command needs company context.
user-invocable: false
---

# Company Research

Research a company and produce a structured brief. Use web search to gather current information. Be explicit about what was found vs what is inferred.

## Inputs

You need two things:
- **Company name** — from the user or from `job-applications/input.md`
- **Company link** — a URL to start from (optional but helpful)

## Research Process

### Step 1: Visit the company link

If a URL is provided, fetch it first. Look for: what the company does, their product, their mission statement, their about page.

### Step 2: Search for company overview

Search: `[company name]` and `[company name] about`

Extract: what they do, who their customers are, what industry they operate in, company size, headquarters location, funding stage.

### Step 3: Search for tech stack and engineering culture

Search: `[company name] engineering blog`, `[company name] tech stack`, `[company name] engineering jobs`

Extract: what technologies they use, how their engineering team is structured, any public blog posts or talks about their architecture. This is critical for CV tailoring — tech stack overlap between the candidate and the company directly drives which experience bullets to prioritize.

### Step 4: Search for recent news

Search: `[company name] news [current year]`, `[company name] funding`

Extract: recent funding rounds, product launches, leadership changes, acquisitions, partnerships. Anything from the last 6-12 months. This feeds the cover letter's "why this company" paragraph.

### Step 5: Search for culture and values

Search: `[company name] culture`, `[company name] glassdoor`, `[company name] values`

Extract: work culture signals, remote/hybrid policies, diversity initiatives, company values. Look for signals that help tailor tone — flat hierarchy (Nordic style), process-oriented (German style), results-driven (Dutch style).

## Output Format

> The "nothing found" placeholder strings below (no tech stack / no recent news / no engineering culture) are a shared contract defined in `config/contracts.yaml` → `research_placeholders`. Use them verbatim; if they change, change them there.

Write the research to a file called `research.md` with this structure:

```markdown
# Company Research: [Company Name]

**Website:** [URL]
**Industry:** [industry]
**Size:** [employee count if found]
**HQ:** [location]
**Funding/Stage:** [if found]

## What They Do

[1-2 paragraphs describing their core product/service and customers]

## Tech Stack

[List technologies found. Note which ones overlap with the candidate's stack.]

If no tech stack information was found, state that explicitly: "No public tech stack information found."

## Recent News

- [Recent development 1]
- [Recent development 2]
- [Recent development 3]

If nothing recent was found, state: "No recent news found in search results."

## Engineering Culture

[What you found about how they work — team structure, engineering practices, blog posts, conference talks]

If nothing was found, state: "No public engineering culture information found."

## Mission & Values

[From their website or about page]

## Relevance to Candidate

[Brief note on why this is a good fit — tech stack overlap, similar challenges, mission alignment. Reference specific overlaps with candidate.md if you've read it.]
```

## Important Rules

- Never invent information. If a search returns nothing for a section, say so explicitly.
- Clearly distinguish between facts found in search results and your own inferences.
- Prioritize primary sources (company website, official blog, press releases) over secondary sources (news aggregators, review sites).
- Keep it scannable — this file will be reviewed quickly before CV/CL generation.
- The "Relevance to Candidate" section is the bridge between research and tailoring. Make it actionable.