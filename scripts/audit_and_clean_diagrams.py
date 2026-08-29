"""
audit_and_clean_diagrams.py
===========================
Audits dictionary diagrams against:
1. Exact file existence
2. Image validity (size, extreme aspect ratio, corruption)
3. Term cleanliness (no OCR scraps, no bracket leftovers, no stray punctuation)
4. Valid presence in the core STEM dictionary

Regenerates:
- dictionary_diagrams_map.json
- core_dictionary_diagrams.js
"""

import os
import json
import re
import sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

MAP_JSON = "dictionary_diagrams_map.json"
DIAG_JS = "core_dictionary_diagrams.js"
DIAGRAMS_DIR = "diagrams"

def clean_and_rebuild():
    if not os.path.exists(MAP_JSON):
        print(f"Error: {MAP_JSON} not found.")
        return

    with open(MAP_JSON, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    with open("dictionary.json", "r", encoding="utf-8") as f:
        dict_data = json.load(f)
    dict_words = set()
    for letter_entries in dict_data.values():
        for item in letter_entries:
            if item.get("word"):
                dict_words.add(item["word"])
    dict_words_lower = {w.lower().strip(): w for w in dict_words}

    print(f"Starting audit on {len(diag_map)} mapped diagram entries...")
    print(f"Dictionary contains {len(dict_words)} words.")

    cleaned_map = {}
    removed_entries = []

    for term, rel_path in diag_map.items():
        clean_t = term.lower().strip()
        base_t = re.sub(r'\(.*?\)', '', clean_t).strip()
        reasons = []

        # Check file existence
        full_path = os.path.join(os.path.dirname(__file__), "..", rel_path) if not os.path.isabs(rel_path) else rel_path
        if not os.path.exists(full_path) and not os.path.exists(rel_path):
            reasons.append("file_missing")
            removed_entries.append((term, rel_path, reasons))
            continue

        actual_path = rel_path if os.path.exists(rel_path) else full_path

        # Check key hygiene
        if clean_t.startswith("(") and clean_t.endswith(")") and len(clean_t) < 8:
            reasons.append("parenthetical_abbreviation_fragment")
        if clean_t.endswith(";") or clean_t.endswith("]") or clean_t.startswith("[") or "\ufffd" in clean_t:
            reasons.append("malformed_characters_or_brackets")
        if re.match(r'^\d+[\,\-]', clean_t) and not (clean_t in dict_words_lower):
            reasons.append("unmatched_numeric_prefix_fragment")
        if len(clean_t) <= 2:
            reasons.append("too_short_ocr_fragment")

        # Check known false positives (words without diagrams in book)
        KNOWN_FALSE = {'abfarad', 'acid', 'cookie', 'cone', 'concave up'}
        if clean_t in KNOWN_FALSE or base_t in KNOWN_FALSE:
            reasons.append("known_false_positive_no_diagram_in_book")

        # Check image validity
        try:
            with Image.open(actual_path) as img:
                w, h = img.size
                aspect = w / h if h > 0 else 0
                if aspect > 5.5 or (aspect < 0.18 and aspect > 0):
                    reasons.append(f"extreme_aspect_ratio_{aspect:.2f}")
                if w < 40 or h < 40:
                    reasons.append(f"tiny_image_{w}x{h}")
        except Exception as e:
            reasons.append(f"image_open_error_{e}")

        # Check matching against dictionary words
        is_in_dict = (clean_t in dict_words_lower) or (base_t in dict_words_lower)
        if not is_in_dict:
            reasons.append("not_in_dictionary")

        if reasons:
            removed_entries.append((term, rel_path, reasons))
        else:
            # Map canonical clean key
            cleaned_map[clean_t] = rel_path
            # Also provide base word mapping if term has alias in parens e.g. "abdomen (abdominal cavity)" -> "abdomen"
            if base_t and base_t != clean_t and base_t in dict_words_lower:
                if base_t not in cleaned_map:
                    cleaned_map[base_t] = rel_path

    print("\n--- AUDIT RESULTS ---")
    print(f"Total entries processed: {len(diag_map)}")
    print(f"Entries retained (clean, verified): {len(cleaned_map)}")
    print(f"Entries purged (false / malformed / distorted): {len(removed_entries)}")

    # Sort dictionary map alphabetically
    sorted_map = dict(sorted(cleaned_map.items()))

    # Write cleaned dictionary_diagrams_map.json
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    print(f"Saved cleaned {MAP_JSON}")

    # Write core_dictionary_diagrams.js
    with open(DIAG_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")
    print(f"Regenerated {DIAG_JS}")

if __name__ == "__main__":
    clean_and_rebuild()
