import os
import json
import re
import sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

def audit():
    with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    with open("core_dictionary.js", "r", encoding="utf-8") as f:
        core_dict_content = f.read()

    dict_words = set(re.findall(r'word:\s*"([^"]+)"', core_dict_content))
    dict_words_lower = {w.lower().strip(): w for w in dict_words}

    print(f"Total entries in diag_map: {len(diag_map)}")
    print(f"Total words in dictionary: {len(dict_words)}")

    to_remove = []
    to_keep = []

    for term, path in diag_map.items():
        reasons = []
        clean_t = term.lower().strip()
        base_t = re.sub(r'\(.*?\)', '', clean_t).strip()

        # Check 1: File existence
        if not os.path.exists(path):
            reasons.append("file_not_found")

        # Check 2: Key validity (malformed fragments, trailing punctuation, brackets, weird chars)
        if clean_t.startswith("(") and clean_t.endswith(")") and len(clean_t) < 8:
            reasons.append("parenthetical_abbreviation_fragment")
        if clean_t.endswith(";") or clean_t.endswith("]") or clean_t.startswith("[") or "\ufffd" in clean_t:
            reasons.append("malformed_characters_or_brackets")
        if re.match(r'^\d+[\,\-]', clean_t) and not (clean_t in dict_words_lower):
            reasons.append("unmatched_numeric_prefix_fragment")
        if len(clean_t) <= 2:
            reasons.append("too_short_ocr_fragment")

        # Check 3: Image properties
        if os.path.exists(path):
            try:
                with Image.open(path) as img:
                    w, h = img.size
                    aspect = w / h if h > 0 else 0
                    if aspect > 5.5 or (aspect < 0.18 and aspect > 0):
                        reasons.append(f"extreme_aspect_ratio_{aspect:.2f}")
                    if w < 50 or h < 50:
                        reasons.append(f"tiny_image_{w}x{h}")
            except Exception as e:
                reasons.append(f"image_open_error_{e}")

        # Check 4: Must match a real word or base word in dictionary
        is_in_dict = (clean_t in dict_words_lower) or (base_t in dict_words_lower)
        if not is_in_dict:
            reasons.append("not_in_dictionary")

        if reasons:
            to_remove.append((term, path, reasons))
        else:
            to_keep.append((term, path))

    print(f"\n--- AUDIT SUMMARY ---")
    print(f"Entries to KEEP (clean, verified, valid image & dictionary term): {len(to_keep)}")
    print(f"Entries flagged for REMOVAL: {len(to_remove)}")
    print("\nSample Flagged Entries:")
    for t, p, r in to_remove[:30]:
        print(f"  ❌ '{t}' ({p}) -> {', '.join(r)}")

    print("\nSample Valid Kept Entries:")
    for t, p in to_keep[:15]:
        print(f"  ✅ '{t}' ({p})")

if __name__ == "__main__":
    audit()
