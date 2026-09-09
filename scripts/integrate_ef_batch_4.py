"""
integrate_ef_batch_4.py
=======================
Section E-F Diagram Integration - Batch 4 (Screenshots 31-40)

  31. Screenshot_8-9-2026_12390_    -> Energy band
  32. Screenshot_8-9-2026_123956_   -> Enolate tautomers
  33. Screenshot_8-9-2026_124052_   -> Ensiform leaf
  34. Screenshot_8-9-2026_124229_   -> Entire Leaf
  35. Screenshot_8-9-2026_124344_   -> Enzyme / Enzyme-substrate complex
  36. Screenshot_8-9-2026_124425_   -> Epicycle
  37. Screenshot_8-9-2026_124452_   -> Epicycloid on Cartesian plane
  38. Screenshot_8-9-2026_124631_   -> Epiphyte
  39. Screenshot_8-9-2026_133720_   -> Chemical structure of Epoxide
  40. Screenshot_8-9-2026_13375_    -> Structure of Epoxyethane
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_12390_.jpeg",   "dict_energy_band.png"),
    ("Screenshot_8-9-2026_123956_.jpeg",  "dict_enolate.png"),
    ("Screenshot_8-9-2026_124052_.jpeg",  "dict_ensiform_leaf.png"),
    ("Screenshot_8-9-2026_124229_.jpeg",  "dict_entire_leaf.png"),
    ("Screenshot_8-9-2026_124344_.jpeg",  "dict_enzyme_action.png"),
    ("Screenshot_8-9-2026_124425_.jpeg",  "dict_epicycle.png"),
    ("Screenshot_8-9-2026_124452_.jpeg",  "dict_epicycloid.png"),
    ("Screenshot_8-9-2026_124631_.jpeg",  "dict_epiphyte.png"),
    ("Screenshot_8-9-2026_133720_.jpeg",  "dict_epoxide.png"),
    ("Screenshot_8-9-2026_13375_.jpeg",   "dict_epoxyethane.png"),
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
    # 31 - Energy band
    "energy band":                      "diagrams/dict_energy_band.png",
    "conduction band":                  "diagrams/dict_energy_band.png",
    "valence band":                     "diagrams/dict_energy_band.png",
    "forbidden band":                   "diagrams/dict_energy_band.png",

    # 32 - Enolate tautomers
    "enolate":                          "diagrams/dict_enolate.png",
    "enol":                             "diagrams/dict_enolate.png",
    "tautomer":                         "diagrams/dict_enolate.png",
    "enolate tautomers":                "diagrams/dict_enolate.png",

    # 33 - Ensiform leaf
    "ensiform leaf":                    "diagrams/dict_ensiform_leaf.png",
    "ensiform":                         "diagrams/dict_ensiform_leaf.png",

    # 34 - Entire leaf
    "entire leaf":                      "diagrams/dict_entire_leaf.png",
    "entire":                           "diagrams/dict_entire_leaf.png",

    # 35 - Enzyme action
    "enzyme":                           "diagrams/dict_enzyme_action.png",
    "enzyme-substrate complex":         "diagrams/dict_enzyme_action.png",
    "enzyme substrate complex":         "diagrams/dict_enzyme_action.png",
    "active site":                      "diagrams/dict_enzyme_action.png",
    "substrate":                        "diagrams/dict_enzyme_action.png",
    "enzyme action":                    "diagrams/dict_enzyme_action.png",

    # 36 - Epicycle
    "epicycle":                         "diagrams/dict_epicycle.png",

    # 37 - Epicycloid
    "epicycloid":                       "diagrams/dict_epicycloid.png",

    # 38 - Epiphyte
    "epiphyte":                         "diagrams/dict_epiphyte.png",
    "epiphytic fern":                   "diagrams/dict_epiphyte.png",

    # 39 - Epoxide
    "epoxide":                          "diagrams/dict_epoxide.png",
    "chemical structure of epoxide":    "diagrams/dict_epoxide.png",

    # 40 - Epoxyethane
    "epoxyethane":                      "diagrams/dict_epoxyethane.png",
    "structure of epoxyethane":         "diagrams/dict_epoxyethane.png",
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
print("\nBatch 4 integration complete!")
