"""Validate a generated docx against its source YAML data.

Post-render validation: checks that content from the YAML data file
actually made it into the generated docx document.

Usage:
    python3 validate.py <docx_path> <yaml_path> <label>

Example:
    python3 validate.py folder/cv.docx folder/cv-data.yaml "CV"
    python3 validate.py folder/cover-letter.docx folder/cl-data.yaml "Cover Letter"
"""

import sys

try:
    from docx import Document
except ImportError:
    print("Error: python-docx is not installed. Run: pip install python-docx", file=sys.stderr)
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("Error: PyYAML is not installed. Run: pip install PyYAML", file=sys.stderr)
    sys.exit(1)


def _extract_content_values(data, label):
    """Extract key content strings from YAML data to verify in the docx.

    Returns a list of (check_name, expected_text) tuples.
    Only extracts values (content), not keys.
    """
    checks = []

    if label == "CV":
        # Header
        header = data.get("header", {})
        if header.get("name"):
            checks.append(("Name", header["name"]))
        if header.get("email"):
            checks.append(("Email", header["email"]))

        # Summary (first 50 chars)
        summary = data.get("summary", "")
        if summary:
            preview = summary.strip()[:60].rsplit(" ", 1)[0]
            checks.append(("Summary start", preview))

        # Experience company names and titles
        for role in data.get("experience", []):
            checks.append((f"Role: {role['title']}", role["title"]))
            checks.append((f"Company: {role['company']}", role["company"]))

        # Project names (supports both object {name: ...} and plain string formats)
        for proj in data.get("projects", []):
            if isinstance(proj, dict):
                checks.append((f"Project: {proj['name']}", proj["name"]))
            elif isinstance(proj, str):
                preview = proj[:50]
                checks.append((f"Project entry", preview))

        # Education institutions
        for edu in data.get("education", []):
            checks.append((f"Education: {edu['institution']}", edu["institution"]))

        # Certifications
        for cert in data.get("certifications", []):
            checks.append((f"Cert: {cert['name']}", cert["name"]))

        # Custom sections (any top-level key not in the known set)
        known_keys = {"header", "summary", "skills", "experience", "projects",
                      "education", "certifications", "languages"}
        for key, value in data.items():
            if key in known_keys:
                continue
            if isinstance(value, str) and len(value) > 10:
                # Single-string section (e.g., self_pr, objective)
                preview = value.strip()[:60].rsplit(" ", 1)[0]
                checks.append((f"{key.title()}", preview))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, str) and len(item) > 10:
                        preview = item.strip()[:60].rsplit(" ", 1)[0]
                        checks.append((f"{key.title()} item {i+1}", preview))
                    elif isinstance(item, dict):
                        # Structured item — check the first non-empty string value
                        for v in item.values():
                            if isinstance(v, str) and len(v) > 3:
                                checks.append((f"{key.title()} item {i+1}", v))
                                break

    elif label == "Cover Letter":
        # Header
        header = data.get("header", {})
        if header.get("name"):
            checks.append(("Name", header["name"]))

        # Salutation
        if data.get("salutation"):
            checks.append(("Salutation", data["salutation"]))

        # Each paragraph (first 50 chars)
        for i, para in enumerate(data.get("paragraphs", []), 1):
            preview = para.strip()[:60].rsplit(" ", 1)[0]
            checks.append((f"Paragraph {i} start", preview))

        # Sign-off
        sign_off = data.get("sign_off", {})
        if sign_off.get("closing"):
            checks.append(("Closing", sign_off["closing"]))
        if sign_off.get("name"):
            checks.append(("Sign-off name", sign_off["name"]))

    return checks


def validate(docx_path, yaml_path, label):
    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    doc = Document(docx_path)

    # p.text misses hyperlink runs (raw XML w:hyperlink nodes bypass python-docx).
    # Extract text from every w:t element inside each paragraph to capture them.
    from docx.oxml.ns import qn as _qn
    def _para_full_text(para):
        return "".join(node.text or "" for node in para._p.iter() if node.tag == _qn("w:t"))

    docx_text = "\n".join(_para_full_text(p) for p in doc.paragraphs)

    checks = _extract_content_values(data, label)

    print(f"\n{label} — Content Check:")
    passed = 0
    failed = 0
    for check_name, expected in checks:
        # Case-insensitive search for the content value
        found = expected.lower() in docx_text.lower()
        status = "✓" if found else "✗"
        if found:
            passed += 1
        else:
            failed += 1
        print(f"  {status} {check_name}")

    print(f"\n  Result: {passed}/{passed + failed} content checks passed")

    # Stats on the docx output
    words = len(docx_text.split())
    chars_with_spaces = len(docx_text)
    chars_no_spaces = len(docx_text.replace(" ", "").replace("\n", ""))
    print(f"\n{label} — Stats:")
    print(f"  Words:                    {words}")
    print(f"  Characters (with spaces): {chars_with_spaces}")
    print(f"  Characters (no spaces):   {chars_no_spaces}")

    if failed > 0:
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 validate.py <docx_path> <yaml_path> <label>", file=sys.stderr)
        sys.exit(1)
    success = validate(sys.argv[1], sys.argv[2], sys.argv[3])
    sys.exit(0 if success else 1)
