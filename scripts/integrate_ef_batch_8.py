"""
integrate_ef_batch_8.py
=======================
Section E-F Diagram Integration - Batch 8 (Screenshots 71-80)

  71. Screenshot_8-9-2026_175729_  -> Filtration apparatus
  72. Screenshot_8-9-2026_175748_  -> Fischer projection of (2R) and (2S)-2-butanol
  73. Screenshot_8-9-2026_175835_  -> Bony fish anatomy (Tilapia and gills)
  74. Screenshot_8-9-2026_175854_  -> Flabellate structure
  75. Screenshot_8-9-2026_175915_  -> Flavone, flavonol, anthocyanine backbones
  76. Screenshot_8-9-2026_175924_  -> Fleming's Left-Hand Rule
  77. Screenshot_8-9-2026_175933_  -> Fleming's Right-Hand Rule
  78. Screenshot_8-9-2026_18010_   -> Anatomy of a flower (longitudinal section & complete flower)
  79. Screenshot_8-9-2026_18033_   -> Chemical Structure of Fluorescein
  80. Screenshot_8-9-2026_18116_   -> Focal length (converging/diverging lenses & mirrors)
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_175729_.jpeg",  "dict_filtration.png"),
    ("Screenshot_8-9-2026_175748_.jpeg",  "dict_fischer_projection.png"),
    ("Screenshot_8-9-2026_175835_.jpeg",  "dict_bony_fish.png"),
    ("Screenshot_8-9-2026_175854_.jpeg",  "dict_flabellate_structure.png"),
    ("Screenshot_8-9-2026_175915_.jpeg",  "dict_flavonoids.png"),
    ("Screenshot_8-9-2026_175924_.jpeg",  "dict_flemings_left_hand_rule.png"),
    ("Screenshot_8-9-2026_175933_.jpeg",  "dict_flemings_right_hand_rule.png"),
    ("Screenshot_8-9-2026_18010_.jpeg",   "dict_flower_anatomy.png"),
    ("Screenshot_8-9-2026_18033_.jpeg",   "dict_fluorescein.png"),
    ("Screenshot_8-9-2026_18116_.jpeg",   "dict_focal_length.png"),
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
    # 71 - Filtration
    "filtration":                       "diagrams/dict_filtration.png",
    "filter paper":                     "diagrams/dict_filtration.png",
    "residue":                          "diagrams/dict_filtration.png",
    "filtrate":                         "diagrams/dict_filtration.png",
    "filter funnel":                    "diagrams/dict_filtration.png",

    # 72 - Fischer projection
    "fischer projection":               "diagrams/dict_fischer_projection.png",
    "fischer projections":              "diagrams/dict_fischer_projection.png",
    "2-butanol":                        "diagrams/dict_fischer_projection.png",
    "enantiomer":                       "diagrams/dict_fischer_projection.png",
    "stereoisomer":                     "diagrams/dict_fischer_projection.png",

    # 73 - Bony fish anatomy
    "bony fish":                        "diagrams/dict_bony_fish.png",
    "fish":                             "diagrams/dict_bony_fish.png",
    "tilapia":                          "diagrams/dict_bony_fish.png",
    "operculum":                        "diagrams/dict_bony_fish.png",
    "gills":                            "diagrams/dict_bony_fish.png",
    "gill filaments":                   "diagrams/dict_bony_fish.png",
    "gill rakers":                      "diagrams/dict_bony_fish.png",
    "lateral line":                     "diagrams/dict_bony_fish.png",
    "pectoral fin":                     "diagrams/dict_bony_fish.png",
    "pelvic fin":                       "diagrams/dict_bony_fish.png",
    "dorsal fin":                       "diagrams/dict_bony_fish.png",
    "caudal fin":                       "diagrams/dict_bony_fish.png",
    "anal fin":                         "diagrams/dict_bony_fish.png",

    # 74 - Flabellate structure
    "flabellate structure":             "diagrams/dict_flabellate_structure.png",
    "flabellate":                       "diagrams/dict_flabellate_structure.png",
    "flabellate leaf":                  "diagrams/dict_flabellate_structure.png",
    "fan-shaped":                       "diagrams/dict_flabellate_structure.png",

    # 75 - Flavonoids
    "flavone":                          "diagrams/dict_flavonoids.png",
    "flavonol":                         "diagrams/dict_flavonoids.png",
    "anthocyanin":                      "diagrams/dict_flavonoids.png",
    "anthocyanine":                     "diagrams/dict_flavonoids.png",
    "flavonoid":                        "diagrams/dict_flavonoids.png",
    "flavonoids":                       "diagrams/dict_flavonoids.png",

    # 76 - Fleming's Left-Hand Rule
    "fleming's left-hand rule":         "diagrams/dict_flemings_left_hand_rule.png",
    "flemings left hand rule":          "diagrams/dict_flemings_left_hand_rule.png",
    "left-hand rule":                   "diagrams/dict_flemings_left_hand_rule.png",

    # 77 - Fleming's Right-Hand Rule
    "fleming's right-hand rule":        "diagrams/dict_flemings_right_hand_rule.png",
    "flemings right hand rule":         "diagrams/dict_flemings_right_hand_rule.png",
    "right-hand rule":                  "diagrams/dict_flemings_right_hand_rule.png",

    # 78 - Flower anatomy
    "flower":                           "diagrams/dict_flower_anatomy.png",
    "complete flower":                  "diagrams/dict_flower_anatomy.png",
    "pistil":                           "diagrams/dict_flower_anatomy.png",
    "carpel":                           "diagrams/dict_flower_anatomy.png",
    "gynoecium":                        "diagrams/dict_flower_anatomy.png",
    "androecium":                       "diagrams/dict_flower_anatomy.png",
    "stamen":                           "diagrams/dict_flower_anatomy.png",
    "anther":                           "diagrams/dict_flower_anatomy.png",
    "filament":                         "diagrams/dict_flower_anatomy.png",
    "petal":                            "diagrams/dict_flower_anatomy.png",
    "sepal":                            "diagrams/dict_flower_anatomy.png",
    "receptacle":                       "diagrams/dict_flower_anatomy.png",
    "pedicel":                          "diagrams/dict_flower_anatomy.png",

    # 79 - Fluorescein
    "fluorescein":                      "diagrams/dict_fluorescein.png",
    "chemical structure of fluorescein":"diagrams/dict_fluorescein.png",
    "fluorophore":                      "diagrams/dict_fluorescein.png",

    # 80 - Focal length
    "focal length":                     "diagrams/dict_focal_length.png",
    "converging lens":                  "diagrams/dict_focal_length.png",
    "diverging lens":                   "diagrams/dict_focal_length.png",
    "converging mirror":                "diagrams/dict_focal_length.png",
    "diverging mirror":                 "diagrams/dict_focal_length.png",
    "convex lens":                      "diagrams/dict_focal_length.png",
    "concave lens":                     "diagrams/dict_focal_length.png",
    "concave mirror":                   "diagrams/dict_focal_length.png",
    "convex mirror":                    "diagrams/dict_focal_length.png",
    "principal focus":                  "diagrams/dict_focal_length.png",
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
print("\nBatch 8 integration complete!")
