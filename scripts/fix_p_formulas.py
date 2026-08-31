"""
fix_p_formulas.py
-----------------
Cross-references the P-section of dictionary.json with pages in
1008_PDFsam_Dictionary Book 2.pdf and produces:
  1. p_formulas_report.json  – each candidate word, its current definition,
                               and the raw PDF text for that headword.
  2. A patched dictionary.json with KaTeX formatting applied.

Run from the project root:
    python scripts/fix_p_formulas.py
"""

import sys
import os
import json
import re
import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8")

# ------------------------------------------------------------------ paths ----
PDF_PATH  = r"split_sections/1008_PDFsam_Dictionary Book 2.pdf"
DICT_PATH = "dictionary.json"
REPORT_PATH = "p_formulas_report.json"

# ------------------------------------------------------------------ helpers --

def strip_math_blocks(text):
    """Remove $$ ... $$ blocks so we can inspect the remaining plain text."""
    out = text
    while "$$" in out:
        s = out.find("$$")
        e = out.find("$$", s + 2)
        if e == -1:
            break
        out = out[:s] + out[e + 2:]
    return out


MATH_CHARS = set("=+<>∑∫±√πθαβγλμ^")


def looks_like_needs_katex(definition):
    """Return True if the definition appears to contain raw/un-rendered math."""
    if "$$" in definition:
        # Already has at least one KaTeX block – may still need more, but skip
        # for now; we deal with fully missing ones first.
        plain = strip_math_blocks(definition)
    else:
        plain = definition
    has_math_keyword = any(
        kw in plain.lower()
        for kw in ("formula", "equation", "given by", "expressed as", "defined as", "= ", "≡")
    )
    has_math_char = any(c in plain for c in MATH_CHARS)
    return has_math_keyword or has_math_char


# ------------------------------------------------------------------ PDF text -

def get_pdf_pages_text(pdf_path):
    """Return list of page texts (one string per page)."""
    doc = fitz.open(pdf_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return pages


def find_word_in_pdf(word, pages_text):
    """
    Naive search: look for the headword (uppercase) in each PDF page.
    Return (page_index, raw_snippet) for the first match, or (None, None).
    """
    needle = word.upper()
    for i, text in enumerate(pages_text):
        # Look for the word at the start of a line (typical dict layout)
        for line in text.splitlines():
            if line.strip().startswith(needle):
                # Grab surrounding context (~400 chars)
                idx = text.find(line)
                snippet = text[idx: idx + 600].strip()
                return i, snippet
    # Fallback: plain contains search
    for i, text in enumerate(pages_text):
        if needle in text.upper():
            idx = text.upper().find(needle)
            snippet = text[idx: idx + 600].strip()
            return i, snippet
    return None, None


# ------------------------------------------------------------------ KaTeX fixes

# Simple heuristic patterns for common physics/maths formula fragments
# that the PDF extractor typically mangles.  Each tuple is
#   (compiled_regex, replacement_string_with_katex).
FORMULA_PATTERNS = [
    # "F = ma" style simple equations – wrap in $ $
    # We only touch lines that look like pure formula lines (short, all math)
    # This is done per-entry in apply_katex_fixes().
]


def apply_katex_fixes(word, definition):
    """
    Apply rule-based KaTeX fixes to a definition string.
    Returns the (possibly) patched definition.
    """
    d = definition

    # ----- pattern: "X = Y" where X is a single letter variable and Y is a
    # mathematical expression NOT already inside $...$
    # We use a conservative approach: only wrap clearly mathematical
    # sub-strings that are outside existing $...$ blocks.

    # 1. Fix superscript patterns like "r2" "m2" "v2" "x2" "s2" that look
    #    like r², m², v² etc. when they appear standalone (not inside words).
    d = re.sub(r'(?<!\$)\b([A-Za-z])2\b(?!\$)', r'$\1^2$', d)
    d = re.sub(r'(?<!\$)\b([A-Za-z])3\b(?!\$)', r'$\1^3$', d)

    # 2. Fix "10 -9" / "10-9" / "10 9" style exponents (common in SI units)
    d = re.sub(r'\b10\s*-\s*(\d+)\b', r'$10^{-\1}$', d)
    d = re.sub(r'\b10\s*(\d+)\b(?!\s*nm|\s*Hz|\s*K)', r'$10^{\1}$', d)

    # 3. Fix "x n" subscript-like patterns in series notation like "a n", "b n"
    # (only when surrounded by spaces/punctuation, not inside words)
    # Skip – too risky without context.

    # 4. Greek letters written as words
    greek = {
        r'\bpi\b': 'π',
        r'\balpha\b': 'α',
        r'\bbeta\b': 'β',
        r'\bgamma\b': 'γ',
        r'\bdelta\b': 'δ',
        r'\btheta\b': 'θ',
        r'\blambda\b': 'λ',
        r'\bmu\b': 'μ',
        r'\bomega\b': 'ω',
        r'\bsigma\b': 'σ',
    }
    # (We skip this – too risky to blindly replace English words)

    return d


# ------------------------------------------------------------------ main -----

def main():
    print("Loading dictionary …")
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    p_entries = data.get("P", [])
    print(f"  P-section entries: {len(p_entries)}")

    print("Loading PDF …")
    pages_text = get_pdf_pages_text(PDF_PATH)
    print(f"  PDF pages: {len(pages_text)}")

    print("Scanning for formula candidates …")
    report = []
    fix_count = 0

    for i, entry in enumerate(p_entries):
        word = entry.get("word", "")
        definition = entry.get("definition", "")

        if not definition:
            continue

        if not looks_like_needs_katex(definition):
            continue

        # Find this word in the PDF
        page_idx, snippet = find_word_in_pdf(word, pages_text)

        # Apply conservative KaTeX patches
        new_def = apply_katex_fixes(word, definition)
        changed = new_def != definition

        report.append({
            "word": word,
            "page": page_idx,
            "pdf_snippet": snippet[:500] if snippet else None,
            "original_definition": definition,
            "patched_definition": new_def,
            "changed": changed,
        })

        if changed:
            p_entries[i]["definition"] = new_def
            fix_count += 1

    data["P"] = p_entries

    # Save report
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\nReport saved to {REPORT_PATH}")
    print(f"  Total candidates: {len(report)}")
    print(f"  Entries auto-patched: {fix_count}")

    # Save patched dictionary
    with open(DICT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\ndictionary.json updated.")
    print("\nNOTE: The report contains pdf_snippet for every candidate.")
    print("Please review p_formulas_report.json for entries where the PDF")
    print("shows a formula that is NOT yet rendered with KaTeX in the definition.")


if __name__ == "__main__":
    main()
