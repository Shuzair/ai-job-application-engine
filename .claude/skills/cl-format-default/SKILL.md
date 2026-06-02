---
name: cl-format-default
description: "DEPRECATED — superseded by per-style cl-format.yaml files in each style skill folder (e.g. cl-style-default/cl-format.yaml). Legacy cover letter layout reference kept for historical context only. Do NOT use this skill for rendering."
user-invocable: false
---

# Cover Letter Format — Default (DEPRECATED)

> **This skill is deprecated.** Visual formatting is now controlled by per-style `cl-format.yaml` files in each style skill folder (e.g., `.claude/skills/cl-style-default/cl-format.yaml`) and rendered deterministically by `scripts/render_cl.py`. Do not use this skill — it is kept for historical reference only.

This skill previously defined the visual layout for generating cover letter documents (docx and pdf). The style skills define what content to write — this skill defined how it looked on the page.

## Page Setup

- Page size: A4 (210mm x 297mm)
- Margins: 1 inch (2.54cm) all sides
- Single column layout

## Header

Identical to the CV header — same layout, same styling:
- **Name**: large bold text, blue color (#2E74B5), centered
- **Title line**: regular weight, centered (e.g., "Data Engineer")
- **Contact line**: phone | email, centered
- **Links line**: linkedin | github, centered, blue hyperlinks
- **Relocation line**: "Open to Relocation" centered, bold
- Horizontal rule below the header block

This creates visual consistency between CV and cover letter as a matched set.

## Date

- Left-aligned
- Format: "Month DD, YYYY" (e.g., "Feb 26, 2026")
- Placed below the header with spacing above and below

## Salutation

- "Dear Hiring Team," (or specific name if provided)
- Left-aligned, regular weight

## Body

- 4 paragraphs of plain text
- No bullets, no bold, no formatting within the body
- Standard paragraph spacing between each paragraph
- Left-aligned, justified or left-aligned (no center)

## Sign-off

```
Kind regards,

**[Full Name from candidate.md]**
[Job Title from candidate.md]
[Email from candidate.md]
[Phone from candidate.md]
```

- "Kind regards," on its own line
- Name: bold, blue (#2E74B5)
- Title: use the candidate's most recent job title from `candidate.md` (under Professional Experience, the first/current role)
- Email, phone on separate lines below, regular weight
- Pull all values from `candidate.md` — do not hardcode

## Typography

- Font: same as CV (Calibri, Arial, or similar clean sans-serif)
- Body text: 11pt
- Name in header: 18-20pt (matching CV)
- Line spacing: 1.15
- Colors: black text body, blue (#2E74B5) for name and hyperlinks only

## General Rules

- Maximum 1 page — hard limit
- No decorative elements beyond the horizontal rule under header
- The cover letter should visually match the CV — same header, same font, same color
- Hyperlinks in blue, underlined