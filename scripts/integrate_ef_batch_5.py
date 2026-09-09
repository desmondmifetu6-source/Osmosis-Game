"""
integrate_ef_batch_5.py
=======================
Section E-F Diagram Integration - Batch 5 (Screenshots 41-50)

  41. Screenshot_8-9-2026_133811_  -> Equiangular polygon
  42. Screenshot_8-9-2026_133838_  -> Equilateral Triangle
  43. Screenshot_8-9-2026_133937_  -> Equipotential surface (point charge & uniform field)
  44. Screenshot_8-9-2026_134030_  -> Chemical structure of Ergotamine
  45. Screenshot_8-9-2026_134057_  -> An erose leaf
  46. Screenshot_8-9-2026_134122_  -> Chemical structure of Ergosterol
  47. Screenshot_8-9-2026_134247_  -> Chemical Structure of Paraldehyde
  48. Screenshot_8-9-2026_134640_  -> Euglena
  49. Screenshot_8-9-2026_134747_  -> Eustachian tube of the human ear
  50. Screenshot_8-9-2026_135022_  -> XOR gate & truth table
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_133811_.jpeg",  "dict_equiangular_polygon.png"),
    ("Screenshot_8-9-2026_133838_.jpeg",  "dict_equilateral_triangle.png"),
    ("Screenshot_8-9-2026_133937_.jpeg",  "dict_equipotential_surface.png"),
    ("Screenshot_8-9-2026_134030_.jpeg",  "dict_ergotamine.png"),
    ("Screenshot_8-9-2026_134057_.jpeg",  "dict_erose_leaf.png"),
    ("Screenshot_8-9-2026_134122_.jpeg",  "dict_ergosterol.png"),
    ("Screenshot_8-9-2026_134247_.jpeg",  "dict_paraldehyde.png"),
    ("Screenshot_8-9-2026_134640_.jpeg",  "dict_euglena.png"),
    ("Screenshot_8-9-2026_134747_.jpeg",  "dict_eustachian_tube.png"),
    ("Screenshot_8-9-2026_135022_.jpeg",  "dict_xor_gate.png"),
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
    # 41 - Equiangular polygon
    "equiangular polygon":              "diagrams/dict_equiangular_polygon.png",
    "equiangular":                      "diagrams/dict_equiangular_polygon.png",

    # 42 - Equilateral triangle
    "equilateral triangle":             "diagrams/dict_equilateral_triangle.png",
    "equilateral":                      "diagrams/dict_equilateral_triangle.png",

    # 43 - Equipotential surface
    "equipotential surface":            "diagrams/dict_equipotential_surface.png",
    "equipotential":                    "diagrams/dict_equipotential_surface.png",
    "field line":                       "diagrams/dict_equipotential_surface.png",
    "uniform field":                    "diagrams/dict_equipotential_surface.png",
    "point charge":                     "diagrams/dict_equipotential_surface.png",

    # 44 - Ergotamine
    "ergotamine":                       "diagrams/dict_ergotamine.png",
    "chemical structure of ergotamine": "diagrams/dict_ergotamine.png",

    # 45 - Erose leaf
    "erose leaf":                       "diagrams/dict_erose_leaf.png",
    "erose":                            "diagrams/dict_erose_leaf.png",

    # 46 - Ergosterol
    "ergosterol":                       "diagrams/dict_ergosterol.png",
    "chemical structure of ergosterol": "diagrams/dict_ergosterol.png",

    # 47 - Paraldehyde
    "paraldehyde":                      "diagrams/dict_paraldehyde.png",
    "chemical structure of paraldehyde":"diagrams/dict_paraldehyde.png",

    # 48 - Euglena
    "euglena":                          "diagrams/dict_euglena.png",
    "flagellum":                        "diagrams/dict_euglena.png",
    "eyespot":                          "diagrams/dict_euglena.png",
    "contractile vacuole":              "diagrams/dict_euglena.png",
    "gullet":                           "diagrams/dict_euglena.png",

    # 49 - Eustachian tube
    "eustachian tube":                  "diagrams/dict_eustachian_tube.png",
    "vestibule":                        "diagrams/dict_eustachian_tube.png",
    "tympanic membrane":                "diagrams/dict_eustachian_tube.png",
    "eardrum":                          "diagrams/dict_eustachian_tube.png",
    "auditory canal":                   "diagrams/dict_eustachian_tube.png",
    "auricle":                          "diagrams/dict_eustachian_tube.png",

    # 50 - XOR gate
    "xor gate":                         "diagrams/dict_xor_gate.png",
    "exclusive or":                     "diagrams/dict_xor_gate.png",
    "xor":                              "diagrams/dict_xor_gate.png",
    "logic gate":                       "diagrams/dict_xor_gate.png",
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
print("\nBatch 5 integration complete!")
