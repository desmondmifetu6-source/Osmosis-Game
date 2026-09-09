"""
integrate_ef_batch_10.py
========================
Section E-F Diagram Integration - Batch 10 (Screenshots 91-94)
FINAL DIAGRAM BATCH!

  91. Screenshot_8-9-2026_18830_  -> Chemical structure of Fumaric Acid
  92. Screenshot_8-9-2026_1884_   -> Side view of a frustum
  93. Screenshot_8-9-2026_18850_  -> Funiculus of an ovule
  94. Screenshot_8-9-2026_1898_   -> Funnelform flower
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_18830_.jpeg",  "dict_fumaric_acid.png"),
    ("Screenshot_8-9-2026_1884_.jpeg",   "dict_frustum.png"),
    ("Screenshot_8-9-2026_18850_.jpeg",  "dict_funiculus.png"),
    ("Screenshot_8-9-2026_1898_.jpeg",   "dict_funnelform_flower.png"),
]

print("-- Step 1: Copying screenshots -> diagrams/ --")
for src_name, dst_name in copies:
    src = os.path.join(SCREENSHOT_DIR, src_name)
    dst = os.path.join(DIAGRAMS_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  WARNING: {src} not found")
        continue
    shutil.copy2(src, dst)
    print(f"  OK  {src_name}  ->  {dst_name}")

NEW_MAPPINGS = {
    # 91 - Fumaric acid
    "fumaric acid":                     "diagrams/dict_fumaric_acid.png",
    "chemical structure of fumaric acid":"diagrams/dict_fumaric_acid.png",
    "trans-butenedioic acid":           "diagrams/dict_fumaric_acid.png",

    # 92 - Frustum
    "frustum":                          "diagrams/dict_frustum.png",
    "frustum of a cone":                "diagrams/dict_frustum.png",
    "slant height":                     "diagrams/dict_frustum.png",
    "truncated cone":                   "diagrams/dict_frustum.png",

    # 93 - Funiculus
    "funiculus":                        "diagrams/dict_funiculus.png",
    "funicule":                         "diagrams/dict_funiculus.png",
    "anatropous ovule":                 "diagrams/dict_funiculus.png",
    "ovule stalk":                      "diagrams/dict_funiculus.png",

    # 94 - Funnelform flower
    "funnelform flower":                "diagrams/dict_funnelform_flower.png",
    "funnelform":                       "diagrams/dict_funnelform_flower.png",
    "infundibuliform":                  "diagrams/dict_funnelform_flower.png",
}

MAP_FILE = "dictionary_diagrams_map.json"
print(f"\n-- Step 2: Updating {MAP_FILE} --")

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

added = skipped = 0
for term, path in NEW_MAPPINGS.items():
    if term not in diagram_map:
        diagram_map[term] = path
        print(f"  + Added:   \"{term}\"")
        added += 1
    else:
        print(f"  ~ Skipped: \"{term}\" (exists -> {diagram_map[term]})")
        skipped += 1

diagram_map_sorted = dict(sorted(diagram_map.items()))
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(diagram_map_sorted, f, indent=2, ensure_ascii=False)
print(f"\n  OK {MAP_FILE} saved. Added: {added}, Skipped: {skipped}")

print("\n-- Step 3: Rebuilding core_dictionary_diagrams.js --")
js_lines = ["const DictionaryDiagrams = {"]
items = list(diagram_map_sorted.items())
for i, (term, path) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    js_lines.append(f'  "{term}": "{path}"{comma}')
js_lines += ["};", "",
    "if (typeof window !== 'undefined') {",
    "  window.DictionaryDiagrams = DictionaryDiagrams;",
    "}",
    "if (typeof module !== 'undefined') {",
    "  module.exports = DictionaryDiagrams;",
    "}"]

with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
    f.write("\n".join(js_lines) + "\n")

print("  OK core_dictionary_diagrams.js rebuilt.")
print("\nBatch 10 (FINAL BATCH) integration complete!")
