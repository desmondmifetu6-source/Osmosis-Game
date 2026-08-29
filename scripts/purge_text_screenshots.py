import json, os, re
from PIL import Image

def run_purge():
    MAP_FILE = "dictionary_diagrams_map.json"
    JS_FILE = "core_dictionary_diagrams.js"
    
    if not os.path.exists(MAP_FILE):
        print(f"Error: {MAP_FILE} not found.")
        return

    with open(MAP_FILE, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    # Blacklist of known text screenshot words / false diagram words
    TEXT_SCREENSHOT_TERMS = {
        'pit', 's i prefix', 'si prefix', 'abfarad', 'acid', 'cookie', 'cone', 'concave up'
    }

    text_screenshots = []
    cleaned_map = {}

    for term, img_path in diag_map.items():
        clean_t = term.lower().strip()
        base_t = re.sub(r'\(.*?\)', '', clean_t).strip()
        
        # Check blacklist
        if clean_t in TEXT_SCREENSHOT_TERMS or base_t in TEXT_SCREENSHOT_TERMS:
            text_screenshots.append((term, img_path, "Known text-screenshot / no diagram in book"))
            continue
            
        # Check image dimensions on disk
        if os.path.exists(img_path):
            try:
                with Image.open(img_path) as im:
                    w, h = im.size
                    aspect = h / w if w > 0 else 0
                    if aspect > 2.2 and h > 400:
                        text_screenshots.append((term, img_path, f"Tall text column screenshot ({w}x{h}, aspect {aspect:.2f})"))
                        continue
            except Exception as e:
                pass
                
        cleaned_map[term] = img_path

    print(f"Starting with {len(diag_map)} terms.")
    print(f"Identified {len(text_screenshots)} fake text-screenshots / false diagrams:")
    for t, p, r in text_screenshots:
        print(f"  [PURGED] {t:30} -> {r} ({p})")

    print(f"Remaining genuine, authentic diagrams: {len(cleaned_map)}")

    # Save cleaned map
    with open(MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_map, f, ensure_ascii=False, indent=4)

    # Regenerate core_dictionary_diagrams.js
    lines = [
        "// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)",
        "",
        "const DictionaryDiagrams = {"
    ]
    sorted_keys = sorted(cleaned_map.keys())
    for i, k in enumerate(sorted_keys):
        comma = "," if i < len(sorted_keys) - 1 else ""
        escaped_k = json.dumps(k)
        escaped_v = json.dumps(cleaned_map[k])
        lines.append(f"    {escaped_k}: {escaped_v}{comma}")
    lines.append("};")
    lines.append("")
    lines.append("if (typeof window !== 'undefined') {")
    lines.append("    window.DictionaryDiagrams = DictionaryDiagrams;")
    lines.append("}")
    lines.append("")
    lines.append("if (typeof module !== 'undefined' && module.exports) {")
    lines.append("    module.exports = DictionaryDiagrams;")
    lines.append("}")
    lines.append("")

    with open(JS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Updated {JS_FILE} successfully with {len(cleaned_map)} clean diagrams.")

if __name__ == "__main__":
    run_purge()
