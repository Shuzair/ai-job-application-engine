---
name: cv-format-default
description: "DEPRECATED — superseded by per-style cv-format.yaml files in each style skill folder (e.g. cv-style-default/cv-format.yaml). Legacy CV layout reference kept for historical context only. Do NOT use this skill for rendering."
user-invocable: false
---

# CV Format — Default (DEPRECATED)

> **This skill is deprecated.** Visual formatting is now controlled by per-style `cv-format.yaml` files in each style skill folder (e.g., `.claude/skills/cv-style-default/cv-format.yaml`) and rendered deterministically by `scripts/render_cv.py`. Do not use this skill — it is kept for historical reference only.

This skill previously defined the visual layout for generating CV documents (docx and pdf). The style skills define what content to write — this skill defined how it looked on the page.

## Page Setup

- Page size: A4 (210mm x 297mm)
- Margins: 1 inch (2.54cm) all sides
- Single column layout, no sidebars

## Header

Center-aligned block:
- **Name**: large bold text, blue color (#2E74B5), all caps or title case
- **Title line**: regular weight, centered below name. Multiple titles are joined with ` · ` (e.g., "Analytics Engineer · Data Engineer")
- **Contact line**: phone | email, centered, smaller font
- **Links line**: linkedin.com/in/handle | github.com/handle, centered, blue hyperlinks
- **Relocation line**: "Open to Relocation" centered, bold

## Section Headings

- Text: UPPERCASE, bold
- Horizontal rule directly below the heading text
- Consistent spacing above each section heading

## Section Order

Follow this exact order:
1. Professional Summary
2. Skills
3. Professional Experience
4. Education
5. Certifications
6. Languages

## Professional Summary

- Plain paragraph text, no bullets
- 3-5 lines

## Skills

Format each category on its own line:
```
**Category:** Skill · Skill · Skill · Skill
```
- Category name bold, followed by colon
- Skills separated by middle dots (·) only — never pipes
- No bullet points, no indentation
- If cv-draft.md uses pipes (|) as separators, convert them to · during docx generation

## Professional Experience

Each role as a block:
```
**Job Title**                                         Date Range
Company (HQ: City, Country) — Candidate Location (Work Model)
*Brief company description in italics*

- Bullet point 1
- Bullet point 2
```
- Job title: bold, left-aligned
- Date range: right-aligned on same line
- Company line: regular weight, includes HQ location, candidate location, and work model (Hybrid/Remote/On-site)
- Company description: italic, one line
- Bullets: standard bullet points, regular weight

## Education

Each entry:
```
**Degree Name (Status if applicable)**                    Date Range
University Name
GPA: x.x/4.0 (if included)
```
- Degree: bold, left-aligned
- Date: right-aligned
- University on next line, regular weight
- GPA optional, on next line if included

## Certifications

Each certification as a block:
```
**Certification Name**                                    Date Range
Issuing Body | Credential ID: xxx | Verify: [link]
```
- Name: bold, left-aligned
- Date: right-aligned on same line
- Details line below: regular weight, includes verify link as hyperlink

## Languages

Single line:
```
**Language:** Level · **Language:** Level
```

The cv-agent produces `English: C1 · Urdu: Native`. Bold the language name (including colon) in the docx. Separate entries with middle dots (·).

## Typography

- Font: clean sans-serif (Calibri, Arial, or similar)
- Body text: 10-11pt
- Name in header: 18-20pt
- Section headings: 12pt
- Line spacing: 1.15
- Colors: black text body, blue (#2E74B5) for name and hyperlinks only

## General Rules

- No photos
- No decorative elements, borders, or graphics beyond horizontal rules
- Hyperlinks in blue, underlined
- Consistent alignment throughout — left-aligned body, right-aligned dates
- Maximum 2 pages

## Page Count Enforcement

After generating cv.docx, estimate the page count. If the document exceeds 2 pages:

1. Reduce body font from 11pt → 10pt
2. Reduce line spacing from 1.15 → 1.05
3. Reduce spacing before section headings by 20%
4. If still over 2 pages, warn the user: "CV exceeds 2 pages — consider asking the cv-agent to trim bullets via /rerun cv"

Do NOT silently truncate content. Surface the issue to the user.