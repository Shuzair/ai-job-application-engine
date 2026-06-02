#!/usr/bin/env python3
"""Scaffold style files for a new country or region.

Creates cv-style-{identifier}/ and cl-style-{identifier}/ folders under
the skills directory by copying from the best available base style:

  Country identifier:
    1. Region style (cv-style-{region}) if it exists
    2. Default style (cv-style-default)

  Region identifier:
    1. Default style (cv-style-default)

Copies format configs and data schemas, then generates SKILL.md stubs
with correct frontmatter for the new identifier.

Usage:
    python3 scripts/scaffold_style.py --identifier spain --type country --region europe
    python3 scripts/scaffold_style.py --identifier middle-east --type region

Output: JSON to stdout with fields:
    cv_style_dir   — path to created cv-style-{id}/ folder
    cl_style_dir   — path to created cl-style-{id}/ folder
    cv_base        — which base style was used for CV (e.g., "europe", "default")
    cl_base        — which base style was used for CL
    files_created  — list of all created file paths
    error          — error message if something failed, else null
"""

import argparse
import json
import re
import shutil
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Hint & block data
# ---------------------------------------------------------------------------

# Each hint: (substring_to_match, comment_to_inject)
# Matches the FIRST non-comment line containing the substring, then stops.
# The comment replaces any existing inline comment on that line.

_CV_FORMAT_HINTS: tuple[tuple[str, str], ...] = (
    # page
    ("size: A4", "# [CUSTOMIZE: page size — A4 for Europe/Asia/most countries, Letter for US/Canada. Options: A4 (210×297mm), Letter (216×279mm)]"),
    ("top:", "# [CUSTOMIZE: top margin — Suggested range: 1.5–2.5cm. Research local norms (e.g., AFNOR=2cm, DIN 5008=2.7cm)]"),
    ("bottom:", "# [CUSTOMIZE: bottom margin — Suggested range: 1.5–2.5cm. Typically matches top margin]"),
    ("left:", "# [CUSTOMIZE: left margin — Suggested range: 2.0–2.5cm. Some countries have standards (e.g., DIN 5008=2.5cm, AFNOR=2cm min)]"),
    ("right:", "# [CUSTOMIZE: right margin — Suggested range: 1.5–2.0cm. Can be slightly smaller than left]"),
    # header
    ("name_font_size:", "# [CUSTOMIZE: name font size — Suggested range: 14–20pt. Research local CV header sizing conventions]"),
    ("name_color:", "# [CUSTOMIZE: name color — Popular professional choices: \"#2E74B5\" (steel blue), \"#1F3864\" (dark navy), \"#2C3E50\" (charcoal), \"#000000\" (black). Conservative markets prefer darker tones]"),
    ("name_case:", "# [CUSTOMIZE: name case — Options: upper, title, as-is. Research local CV header conventions]"),
    ("name_bold:", "# [CUSTOMIZE: name bold — Options: true, false. True is standard in most markets]"),
    ("show_titles:", "# [CUSTOMIZE: show role titles below name — Options: true, false. True if local CVs include a professional headline]"),
    ("titles_font_size:", "# [CUSTOMIZE: titles font size — Suggested range: 9–11pt. Secondary text, smaller than name]"),
    ("contact_font_size:", "# [CUSTOMIZE: contact info font size — Suggested range: 9–10pt. Standard secondary text]"),
    ("links_font_size:", "# [CUSTOMIZE: links font size — Suggested range: 9–10pt. Same size as contact info typically]"),
    ("show_relocation:", "# [CUSTOMIZE: show relocation notice — Options: true, false. True if relocation statements are common in this market]"),
    ("relocation_font_size:", "# [CUSTOMIZE: relocation font size — Suggested range: 9–10pt. Typically matches contact/links size]"),
    ("relocation_bold:", "# [CUSTOMIZE: relocation bold — Options: true, false. Bold draws attention to availability]"),
    # sections
    ("heading_case:", "# [CUSTOMIZE: section heading case — Options: upper, title, as-is. Research local section heading style]"),
    ("heading_underline:", "# [CUSTOMIZE: heading underline — Options: true (horizontal rule below heading), false. Research if ruled headings are standard]"),
    ("heading_bold:", "# [CUSTOMIZE: heading bold — Options: true, false. True in most markets]"),
    ("heading_size:", "# [CUSTOMIZE: heading font size — Suggested range: 11–14pt. Research local section heading size]"),
    # typography
    ("heading_font:", "# [CUSTOMIZE: heading font — Popular professional fonts: Calibri, Arial, Garamond, Cambria, Helvetica, Times New Roman. Research locally popular fonts]"),
    ("body_font:", "# [CUSTOMIZE: body font — Popular choices: Calibri, Arial, Garamond, Cambria. Should match or pair well with heading font]"),
    ("body_size:", "# [CUSTOMIZE: body font size — Suggested range: 9–12pt. Research local standard (e.g., France=10pt, Denmark=11pt)]"),
    ("line_spacing:", "# [CUSTOMIZE: line spacing multiplier — Suggested range: 1.0–1.15 for CVs. Research local readability norms]"),
    # skills/languages
    ("separator:", "# [CUSTOMIZE: separator between items — Options: \" · \" (middle dot), \" | \" (pipe), \", \" (comma). Research local preference]"),
    # experience
    ("show_company_description:", "# [CUSTOMIZE: company description line — Options: true, false. True in most European markets]"),
    ("max_bullets_per_role:", "# [CUSTOMIZE: max bullets per role — Suggested range: 4–6. Research local CV density expectations]"),
    # colors
    ("primary:", "# [CUSTOMIZE: primary/accent color — Popular: \"#2E74B5\" (steel blue), \"#1F3864\" (dark navy), \"#2C3E50\" (charcoal), \"#34495E\" (dark slate). Conservative markets prefer darker]"),
    # validation
    ("summary_min_words:", "# [CUSTOMIZE: minimum summary words — Suggested range: 30–50. Adjust based on local summary length norms]"),
    ("summary_max_words:", "# [CUSTOMIZE: maximum summary words — Suggested range: 80–120. Research local expectations]"),
    ("max_bullet_words:", "# [CUSTOMIZE: max words per bullet — Suggested range: 15–20. Some markets prefer shorter, others longer]"),
    ("max_bullets_recent:", "# [CUSTOMIZE: max bullets for recent roles — Suggested range: 4–6. Research local expectations for detail level]"),
    ("max_bullets_old:", "# [CUSTOMIZE: max bullets for older roles — Suggested range: 2–4. Older roles should be briefer]"),
    ("max_pages:", "# [CUSTOMIZE: max page count — Options: 1 (US/Canada), 2 (most countries), 3 (some traditional markets). Research local expectations]"),
)

_CL_FORMAT_HINTS: tuple[tuple[str, str], ...] = (
    # page
    ("size: A4", "# [CUSTOMIZE: must match CV — A4 for Europe/Asia, Letter for US/Canada]"),
    ("top:", "# [CUSTOMIZE: top margin — Suggested range: 2.0–2.5cm. Must match CV top margin]"),
    ("bottom:", "# [CUSTOMIZE: bottom margin — Suggested range: 2.0–2.5cm. Must match CV]"),
    ("left:", "# [CUSTOMIZE: left margin — Suggested range: 2.0–2.5cm. Must match CV]"),
    ("right:", "# [CUSTOMIZE: right margin — Suggested range: 1.5–2.0cm. Must match CV]"),
    # header
    ("name_font_size:", "# [CUSTOMIZE: must match CV name_font_size. Suggested range: 14–20pt]"),
    ("name_color:", "# [CUSTOMIZE: must match CV primary color for visual consistency]"),
    ("name_case:", "# [CUSTOMIZE: must match CV name_case. Options: upper, title, as-is]"),
    ("name_bold:", "# [CUSTOMIZE: must match CV name_bold]"),
    ("show_title:", "# [CUSTOMIZE: show role title — must match CV show_titles. Options: true, false]"),
    ("title_font_size:", "# [CUSTOMIZE: must match CV titles_font_size. Suggested range: 9–11pt]"),
    ("contact_font_size:", "# [CUSTOMIZE: must match CV contact_font_size. Suggested range: 9–10pt]"),
    ("links_font_size:", "# [CUSTOMIZE: must match CV links_font_size. Suggested range: 9–10pt]"),
    ("show_relocation:", "# [CUSTOMIZE: must match CV show_relocation]"),
    ("relocation_font_size:", "# [CUSTOMIZE: must match CV relocation_font_size]"),
    ("relocation_bold:", "# [CUSTOMIZE: must match CV relocation_bold]"),
    # date
    ("alignment:", "# [CUSTOMIZE: date alignment — Options: left, right. Research local business letter date placement conventions]"),
    # body
    ("paragraph_spacing_after:", "# [CUSTOMIZE: paragraph spacing — Suggested range: 100–160 twips (≈5–8pt). Research local letter paragraph spacing norms]"),
    # sign_off
    ("closing_text:", "# [CUSTOMIZE: sign-off phrase — Research local language closing + English alternative. Examples: \"Cordialement,\" (FR), \"Med venlig hilsen,\" (DK), \"Mit freundlichen Grüßen,\" (DE)]"),
    # typography
    ("heading_font:", "# [CUSTOMIZE: must match CV heading_font. Popular: Calibri, Arial, Garamond, Cambria]"),
    ("body_font:", "# [CUSTOMIZE: must match CV body_font]"),
    ("body_size:", "# [CUSTOMIZE: must match CV body_size. Suggested range: 9–12pt]"),
    ("line_spacing:", "# [CUSTOMIZE: must match CV line_spacing. Suggested range: 1.0–1.15]"),
    # colors
    ("primary:", "# [CUSTOMIZE: must match CV primary color for visual consistency]"),
    # validation
    ("min_paragraphs:", "# [CUSTOMIZE: min paragraph count — Suggested range: 2–4. Research local cover letter paragraph norms]"),
    ("max_paragraphs:", "# [CUSTOMIZE: max paragraph count — Suggested range: 4–6. Research local norms]"),
    ("min_total_words:", "# [CUSTOMIZE: min word count — Suggested range: 200–300. Research local cover letter length expectations]"),
    ("max_total_words:", "# [CUSTOMIZE: max word count — Suggested range: 350–500. Research local expectations (e.g., Denmark=300-400, France=300-500)]"),
)

# Multi-line comment blocks inserted ABOVE a matched key line.
# Each: (line_match_substring, comment_block_text)
_CV_FORMAT_BLOCKS: tuple[tuple[str, str], ...] = (
    (
        "sections:",
        (
            "# [CUSTOMIZE: SECTIONS — This is a critical section to customize.]\n"
            "# Add or remove sections based on local norms. Common additions:\n"
            "#   interests, volunteer_work, awards, references, self_pr, military_service\n"
            "# Update headings with local-language equivalents as inline comments.\n"
            "# Update section_types for new sections: inline, list, or paragraph.\n"
            "# Examples: interests → inline, volunteer_work → list, self_pr → paragraph"
        ),
    ),
)

_CL_FORMAT_BLOCKS: tuple[tuple[str, str], ...] = (
    (
        "sign_off:",
        (
            "# [CUSTOMIZE: SIGN-OFF — Research local business letter closing conventions.]\n"
            "# Provide the local-language closing phrase AND an English alternative.\n"
            "# The agent should select based on the letter language."
        ),
    ),
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _title_case(identifier: str) -> str:
    """Convert hyphenated identifier to title case for display."""
    return identifier.replace("-", " ").title()


def _resolve_base(
    skills_path: Path, prefix: str, id_type: str, region: str | None
) -> str | None:
    """Determine the best base style to copy from.

    For countries: region style if it exists, else default.
    For regions/new: always default.
    """
    if id_type == "country" and region:
        region_dir = skills_path / f"{prefix}-{region}"
        if region_dir.is_dir():
            return region
    default_dir = skills_path / f"{prefix}-default"
    if default_dir.is_dir():
        return "default"
    return None


def _copy_config_files(src_dir: Path, dst_dir: Path, prefix: str) -> list[str]:
    """Copy format config and data schema from source to destination.

    Returns list of created file paths.
    """
    created = []
    for suffix in ("format.yaml", "data-schema.yaml"):
        filename = f"{prefix}-{suffix}"
        src = src_dir / filename
        dst = dst_dir / filename
        if src.is_file():
            shutil.copy2(src, dst)
            created.append(str(dst))
    return created


def _update_file_header_comment(
    filepath: Path, old_style: str, new_style: str
) -> None:
    """Update the first comment line in a YAML file to reflect the new style name."""
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")
    # Replace old style name in first few comment lines
    old_pattern = re.compile(r"(?<!\w)" + re.escape(old_style) + r"(?!\w)", re.IGNORECASE)
    for i, line in enumerate(lines):
        if not line.startswith("#"):
            break
        if old_pattern.search(line):
            lines[i] = old_pattern.sub(new_style, line)
    filepath.write_text("\n".join(lines), encoding="utf-8")


def _find_yaml_comment(line: str) -> int:
    """Find the index of the inline comment # in a YAML line.

    Handles # inside quoted strings (e.g., color values like "#2E74B5").
    Returns -1 if no inline comment found.
    """
    in_single = False
    in_double = False
    for i, ch in enumerate(line):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return i
    return -1


def _inject_block_comments(filepath: Path, blocks: tuple[tuple[str, str], ...]) -> None:
    """Inject multi-line comment blocks ABOVE matched lines in a YAML file.

    Each block is: (line_match_substring, comment_block_text)
    The comment block is inserted immediately before the first matching line.
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    # Process bottom-up to avoid index shifting
    insertions: list[tuple[int, str]] = []
    for match_sub, block_text in blocks:
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#"):
                continue
            if match_sub in line:
                insertions.append((i, block_text))
                break

    # Sort by line index descending so insertions don't shift earlier indices
    insertions.sort(key=lambda x: x[0], reverse=True)
    for idx, block in insertions:
        block_lines = block.split("\n")
        for j, bl in enumerate(block_lines):
            lines.insert(idx + j, bl)

    filepath.write_text("\n".join(lines), encoding="utf-8")


def _inject_customize_hints(filepath: Path, hints: tuple[tuple[str, str], ...]) -> None:
    """Inject [CUSTOMIZE] hint comments into a copied format YAML file.

    For each hint, finds the first line containing the match substring and
    replaces any existing inline comment with the hint (or appends it).
    Only modifies lines that haven't already been customized (still have
    base-style generic comments or no comment at all).
    """
    text = filepath.read_text(encoding="utf-8")
    lines = text.split("\n")

    for match_sub, hint_comment in hints:
        for i, line in enumerate(lines):
            stripped = line.strip()
            # Skip pure comment lines
            if stripped.startswith("#"):
                continue
            if match_sub in line:
                # Found the first matching line — replace/add comment
                comment_idx = _find_yaml_comment(line)
                if comment_idx >= 0:
                    # Replace existing comment
                    lines[i] = line[:comment_idx].rstrip() + "  " + hint_comment
                else:
                    # No comment — append
                    lines[i] = line.rstrip() + "  " + hint_comment
                break  # first match only

    filepath.write_text("\n".join(lines), encoding="utf-8")


def _generate_cv_skill_md(dst_dir: Path, identifier: str) -> str:
    """Generate a CV SKILL.md stub with correct frontmatter."""
    title = _title_case(identifier)
    content = (
        "---\n"
        f"name: cv-style-{identifier}\n"
        f'description: "{title} CV style. Complete, self-contained CV writing\n'
        f"  rules for {title} job applications. Loaded when style resolution\n"
        f"  matches {identifier}. This is a full style skill — not a partial override.\"\n"
        "user-invocable: false\n"
        "---\n\n"
        f"# {title} CV Style\n\n"
        f"This style covers CV writing rules for {title} job applications. "
        "It does NOT cover visual formatting — that is controlled by the style's "
        "`cv-format.yaml` in this folder.\n\n"
        "Read `candidate.md` before writing any CV content. Every claim, skill, "
        "and metric must be traceable to that file. Never fabricate.\n\n"
        "---\n\n"
        "## Pre-work: Decode the Job Posting First\n\n"
        "Before writing anything, analyze the job posting and extract:\n\n"
        "- The **top 3 technologies** mentioned most prominently\n"
        "- The **core responsibility** from the first 2-3 requirement bullets\n"
        "- **Must-haves vs nice-to-haves**: required/essential vs preferred/bonus\n"
        "- **Cultural signals**: team structure, work style, company culture indicators\n"
        "- Whether the posting mentions relocation support or visa sponsorship\n"
        "- **Language requirements**: local language needed or English-only acceptable\n\n"
        "---\n\n"
        "## Data Collection Philosophy\n\n"
        "These rules define HOW to collect and filter data from candidate.md for each "
        "section. They are fixed across all styles — only the presentation rules "
        "(bucket names, bullet format, tone) vary by country.\n\n"
        "### Skills — Relevance-First Filtering\n\n"
        "1. **Collect**: Read ALL skills from `candidate.md`\n"
        "2. **Match**: Keep skills that appear in the JD (exact or synonym match)\n"
        "3. **Expand**: If the JD mentions a skill the candidate lacks exactly but "
        "has a closely related or similar skill, include that similar skill "
        '(e.g., JD says "Redshift" → candidate has "Snowflake" → include Snowflake)\n'
        "4. **Discard**: Remove all remaining skills that have no relevance to the JD "
        "or company's domain\n"
        "5. **Distribute**: Organize the surviving skills into the category buckets "
        "defined below. If a bucket ends up empty after filtering, omit it entirely\n\n"
        "### Certifications — Strict Relevance Gate\n\n"
        "1. **Collect**: Read ALL certifications from `candidate.md`\n"
        "2. **Filter**: Keep ONLY certifications relevant to the job description — "
        "the technology, domain, or methodology must connect to what the role requires\n"
        "3. **Discard**: Remove all certifications with no relevance to the target role. "
        "Do not include them just to fill space\n\n"
        "### Experience — Maximum Context, Then Rank\n\n"
        "1. **Collect**: Read ALL experience details from `candidate.md` — roles, "
        "projects, technologies, metrics, achievements, context\n"
        "2. **Analyze**: Rank each piece of experience by relevance to the JD. "
        "Prioritize: matching technologies, matching responsibilities, matching scale/domain\n"
        "3. **Shape**: Write bullet points using terminology and keywords from the JD. "
        'If the JD says "data pipelines," use that phrase — not a synonym. '
        "Mirror the JD's technical vocabulary in the bullets\n"
        "4. **Prioritize**: Place the most JD-relevant bullets first within each role. "
        "Cut the least relevant bullets when space is tight\n"
        "5. **Format**: Follow the bullet writing rules defined in the style section below "
        "(word count, action verbs, tone)\n\n"
        "### Summary — Candidate-Meets-JD Synthesis\n\n"
        "1. **Read**: Study the full candidate profile — experience arc, strongest skills, "
        "key achievements, career trajectory\n"
        "2. **Synthesize**: Write an optimal summary that positions the candidate for THIS "
        "specific role. The summary should read as if this candidate is a natural fit for the job\n"
        "3. **Mirror**: Use the job title and key terms from the JD. If the JD says "
        '"Senior Data Engineer," the summary should echo that framing\n'
        "4. **Quantify**: Include the single most impressive metric from candidate.md "
        "that aligns with the role\n"
        "5. **Format**: Follow the structure and tone rules defined in the style section below\n\n"
        "---\n\n"
        "## CV Sections\n\n"
        "Generate these sections in this exact order.\n\n"
        "### 1. Header\n\n"
        "Include: full name, location, email, phone, LinkedIn URL, GitHub (if relevant).\n\n"
        "Add one line about relocation readiness if applying to a different country.\n\n"
        f"[CUSTOMIZE: specify which personal info fields are required/expected/discouraged for {title}"
        " — photo, DOB, nationality, marital status, address format]\n\n"
        "### 2. Professional Summary\n\n"
        "Follow the Summary data collection philosophy above, then format as exactly "
        "4 components in 3-5 lines total:\n\n"
        "1. **Who you are**: Mirror the job title from the posting. State years of "
        "experience and domain.\n"
        "2. **What you do best**: Name 3-5 technologies matching the JD's must-haves.\n"
        "3. **Differentiator**: One quantified achievement most relevant to this role.\n"
        "4. **Availability**: Relocation readiness or availability statement if applicable.\n\n"
        "[CUSTOMIZE: adjust tone — formal/direct/humble, pronoun usage, country-specific phrasing]\n\n"
        "### 3. Skills\n\n"
        "Follow the Skills data collection philosophy above (collect → match → expand → discard → distribute).\n\n"
        "Distribute surviving skills into up to 6 category buckets (omit empty buckets):\n\n"
        f"[CUSTOMIZE: define the bucket names for {title}"
        ' job market — examples: "Programming & Scripting", "Cloud Platforms", '
        '"Databases", "Data Processing", "DevOps & Tools", "Soft Skills". '
        "Adjust to local job-market terminology, separator style, whether proficiency "
        "ratings are used. Maximum 6 buckets]\n\n"
        "### 4. Professional Experience\n\n"
        "Follow the Experience data collection philosophy above (collect all → "
        "rank by JD relevance → shape with JD terminology → prioritize).\n\n"
        "[CUSTOMIZE: specify date format, bullet writing rules, max words per bullet, "
        "max bullets per role (recent vs older), company description norms, tone for "
        "bullets, action verb preferences, rules for combining multiple roles at the "
        "same company]\n\n"
        "### 5. Education\n\n"
        "[CUSTOMIZE: specify local grading system, when to include GPA, degree "
        "equivalence guidance, whether to include thesis/coursework, high school "
        "inclusion rules]\n\n"
        "### 6. Certifications\n\n"
        "Follow the Certifications data collection philosophy above (keep only "
        "JD-relevant, discard the rest).\n\n"
        "[CUSTOMIZE: specify format, country-specific certifications that carry weight, "
        "date display format]\n\n"
        "### 7. Languages\n\n"
        "[CUSTOMIZE: specify proficiency scale (CEFR, JLPT, etc.), format (inline vs "
        "list), when this section is critical]\n\n"
        "---\n\n"
        "## Critical Rules\n\n"
        "- **ATS compliance**: Use standard characters. Avoid tables, columns, graphics, "
        "headers/footers.\n"
        "- **Factual integrity**: Never fabricate experience, skills, or metrics not in "
        "candidate.md.\n"
        "- **Page limit**: Maximum 2 pages. Trim order if exceeding: oldest role bullets "
        "→ weakest project → project context → bullet word count. Never cut certifications, "
        "education, or languages.\n"
        "- Use en-dash for date ranges, middle dot for skill separators.\n\n"
        "[CUSTOMIZE: add country-specific tone summary, cultural sensitivities, legal requirements]\n"
    )
    path = dst_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return str(path)


def _generate_cl_skill_md(dst_dir: Path, identifier: str) -> str:
    """Generate a CL SKILL.md stub with correct frontmatter."""
    title = _title_case(identifier)
    content = (
        "---\n"
        f"name: cl-style-{identifier}\n"
        f'description: "{title} CL style. Complete, self-contained cover letter\n'
        f"  writing rules for {title} job applications. Loaded when style resolution\n"
        f"  matches {identifier}. This is a full style skill — not a partial override.\"\n"
        "user-invocable: false\n"
        "---\n\n"
        f"# {title} Cover Letter Style\n\n"
        f"This style covers cover letter writing rules for {title} job applications. "
        "Visual formatting is controlled by the style's `cl-format.yaml` in this folder.\n\n"
        "Read `candidate.md` before writing. Every claim must be traceable to that file. "
        "Read `research.md` from the application folder for company details.\n\n"
        "---\n\n"
        "## Structure: 4 Paragraphs, 250-400 Words Total\n\n"
        "[CUSTOMIZE: adjust paragraph count and word range based on country norms]\n\n"
        "### Paragraph 1 — Hook (3-4 sentences)\n\n"
        "Open with genuine, specific enthusiasm for the company. Reference something "
        "concrete from research.md. Name the exact position.\n\n"
        "[CUSTOMIZE: country-specific opening conventions]\n\n"
        "### Paragraph 2 — Why I'm a Good Fit (4-6 sentences)\n\n"
        "Connect 2-3 specific achievements from candidate.md to JD requirements. "
        "Use quantified metrics as narrative.\n\n"
        "[CUSTOMIZE: country-specific quantification norms]\n\n"
        "### Paragraph 3 — Why This Company (3-4 sentences)\n\n"
        "Demonstrate knowledge of the company from research.md. Explain why the "
        "candidate wants to work there specifically. Mention relocation readiness "
        "if applicable.\n\n"
        "[CUSTOMIZE: country-specific expectations for this paragraph]\n\n"
        "### Paragraph 4 — Close (2-3 sentences)\n\n"
        "Express enthusiasm for discussing the role further. Thank them for consideration.\n\n"
        "[CUSTOMIZE: adjust enthusiasm level and call-to-action for the culture]\n\n"
        "---\n\n"
        "## Addressing and Sign-off\n\n"
        'Address to "Dear Hiring Team" unless a specific contact name is provided.\n\n'
        "Sign off with \"Kind regards,\" followed by the candidate's full name.\n\n"
        "[CUSTOMIZE: country-specific addressing conventions, formal titles, sign-off "
        "phrases in local language and English]\n\n"
        "---\n\n"
        "## Tone Rules\n\n"
        "Professional, warm, and confident. Balance enthusiasm with substance.\n\n"
        "[CUSTOMIZE: formality level, humility vs confidence balance, words/phrases "
        "to use and avoid, cultural values to reflect]\n\n"
        "---\n\n"
        "## What NOT to Include\n\n"
        "- Visa or sponsorship status (unless country norms dictate otherwise)\n"
        "- Salary expectations (unless asked)\n"
        "- References\n"
        "- Personal information beyond what's in the header\n\n"
        "[CUSTOMIZE: country-specific exclusions and legal considerations]\n\n"
        "---\n\n"
        "## Critical Rules\n\n"
        "- **ATS-safe characters**: Plain text, no special formatting.\n"
        "- **Factual integrity**: Every claim traceable to candidate.md.\n"
        "- **Word count**: Enforce the total word limit strictly.\n"
        "- **Keywords**: Naturally integrate JD keywords without keyword stuffing.\n\n"
        "[CUSTOMIZE: country-specific legal or cultural rules]\n"
    )
    path = dst_dir / "SKILL.md"
    path.write_text(content, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# Main scaffold logic
# ---------------------------------------------------------------------------


def scaffold_style(
    identifier: str,
    id_type: str,
    region: str | None,
    skills_dir: Path,
) -> dict:
    """Scaffold style files for a new country or region.

    Args:
        identifier: Normalized identifier (e.g., "spain", "middle-east").
        id_type: "country", "region", or "new".
        region: Parent region if type is country.
        skills_dir: Path to .claude/skills directory.

    Returns:
        Result dict with created paths and base info.
    """
    cv_dst = skills_dir / f"cv-style-{identifier}"
    cl_dst = skills_dir / f"cl-style-{identifier}"

    # Resolve bases
    cv_base = _resolve_base(skills_dir, "cv-style", id_type, region)
    cl_base = _resolve_base(skills_dir, "cl-style", id_type, region)

    if cv_base is None:
        return {"error": f"Base CV style not found: {identifier}"}
    if cl_base is None:
        return {"error": f"Base CL style not found: {identifier}"}

    cv_src = skills_dir / f"cv-style-{cv_base}"
    cl_src = skills_dir / f"cl-style-{cl_base}"

    # Create destination directories
    cv_dst.mkdir(parents=True, exist_ok=True)
    cl_dst.mkdir(parents=True, exist_ok=True)

    files_created: list[str] = []

    # Copy config files
    files_created.extend(_copy_config_files(cv_src, cv_dst, "cv"))
    files_created.extend(_copy_config_files(cl_src, cl_dst, "cl"))

    # Update header comments in copied files
    cv_title = _title_case(cv_base)
    cl_title = _title_case(cl_base)
    new_title = _title_case(identifier)

    cv_format = cv_dst / "cv-format.yaml"
    cl_format = cl_dst / "cl-format.yaml"

    if cv_format.is_file():
        _update_file_header_comment(cv_format, cv_title, new_title)
    if cl_format.is_file():
        _update_file_header_comment(cl_format, cl_title, new_title)

    # Inject block comments
    if cv_format.is_file():
        _inject_block_comments(cv_format, _CV_FORMAT_BLOCKS)
    if cl_format.is_file():
        _inject_block_comments(cl_format, _CL_FORMAT_BLOCKS)

    # Inject customize hints
    if cv_format.is_file():
        _inject_customize_hints(cv_format, _CV_FORMAT_HINTS)
    if cl_format.is_file():
        _inject_customize_hints(cl_format, _CL_FORMAT_HINTS)

    # Generate SKILL.md stubs
    files_created.append(_generate_cv_skill_md(cv_dst, identifier))
    files_created.append(_generate_cl_skill_md(cl_dst, identifier))

    return {
        "cv_style_dir": str(cv_dst),
        "cl_style_dir": str(cl_dst),
        "cv_base": cv_base,
        "cl_base": cl_base,
        "files_created": files_created,
        "error": None,
    }


def main():
    parser = argparse.ArgumentParser(description="Scaffold style files.")
    parser.add_argument(
        "--identifier",
        required=True,
        help="Normalized style identifier (e.g., 'spain', 'middle-east').",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["country", "region", "new"],
        help="Whether the identifier is a country, region, or new entry.",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="Parent region for country identifiers (e.g., 'europe').",
    )
    args = parser.parse_args()

    # Determine skills directory
    project_root = Path(__file__).resolve().parent.parent
    skills_dir = project_root / ".claude" / "skills"

    result = scaffold_style(args.identifier, args.type, args.region, skills_dir)
    json.dump(result, sys.stdout, indent=2)
    sys.stdout.write("\n")

    if result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
