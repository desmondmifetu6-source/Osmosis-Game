"""
integrate_ef_batch_9.py
=======================
Section E-F Diagram Integration - Batch 9 (Screenshots 81-90)

  81. Screenshot_8-9-2026_18152_  -> Energy losses in a food chain
  82. Screenshot_8-9-2026_18224_  -> A food web
  83. Screenshot_8-9-2026_18433_  -> Four-stroke petrol engine
  84. Screenshot_8-9-2026_1851_   -> Domestic fowl anatomy
  85. Screenshot_8-9-2026_18528_  -> Apparatus for fractional distillation
  86. Screenshot_8-9-2026_18555_  -> Frame of reference
  87. Screenshot_8-9-2026_18632_  -> Free electrons of an atom/ion/molecule
  88. Screenshot_8-9-2026_18654_  -> A frequency polygon on Cartesian plane
  89. Screenshot_8-9-2026_18726_  -> The Frost diagram (for manganese)
  90. Screenshot_8-9-2026_1878_   -> Friedel-Craft Alkylation & Acylation of Benzene
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_18152_.jpeg",  "dict_food_chain_energy.png"),
    ("Screenshot_8-9-2026_18224_.jpeg",  "dict_food_web.png"),
    ("Screenshot_8-9-2026_18433_.jpeg",  "dict_four_stroke_engine.png"),
    ("Screenshot_8-9-2026_1851_.jpeg",   "dict_domestic_fowl.png"),
    ("Screenshot_8-9-2026_18528_.jpeg",  "dict_fractional_distillation.png"),
    ("Screenshot_8-9-2026_18555_.jpeg",  "dict_frame_of_reference.png"),
    ("Screenshot_8-9-2026_18632_.jpeg",  "dict_free_electrons.png"),
    ("Screenshot_8-9-2026_18654_.jpeg",  "dict_frequency_polygon.png"),
    ("Screenshot_8-9-2026_18726_.jpeg",  "dict_frost_diagram.png"),
    ("Screenshot_8-9-2026_1878_.jpeg",   "dict_friedel_crafts.png"),
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
    # 81 - Food chain energy
    "food chain":                       "diagrams/dict_food_chain_energy.png",
    "energy losses in a food chain":    "diagrams/dict_food_chain_energy.png",
    "trophic efficiency":               "diagrams/dict_food_chain_energy.png",
    "ecological efficiency":            "diagrams/dict_food_chain_energy.png",
    "energy flow":                      "diagrams/dict_food_chain_energy.png",

    # 82 - Food web
    "food web":                         "diagrams/dict_food_web.png",
    "food webs":                        "diagrams/dict_food_web.png",
    "producer":                         "diagrams/dict_food_web.png",
    "consumer":                         "diagrams/dict_food_web.png",

    # 83 - Four stroke engine
    "four-stroke petrol engine":        "diagrams/dict_four_stroke_engine.png",
    "four-stroke engine":               "diagrams/dict_four_stroke_engine.png",
    "internal combustion engine":       "diagrams/dict_four_stroke_engine.png",
    "intake stroke":                    "diagrams/dict_four_stroke_engine.png",
    "compression stroke":               "diagrams/dict_four_stroke_engine.png",
    "power stroke":                     "diagrams/dict_four_stroke_engine.png",
    "expansion stroke":                 "diagrams/dict_four_stroke_engine.png",
    "exhaust stroke":                   "diagrams/dict_four_stroke_engine.png",
    "petrol engine":                    "diagrams/dict_four_stroke_engine.png",
    "piston":                           "diagrams/dict_four_stroke_engine.png",

    # 84 - Domestic fowl
    "fowl":                             "diagrams/dict_domestic_fowl.png",
    "domestic fowl":                    "diagrams/dict_domestic_fowl.png",
    "chicken":                          "diagrams/dict_domestic_fowl.png",
    "bird":                             "diagrams/dict_domestic_fowl.png",
    "beak":                             "diagrams/dict_domestic_fowl.png",
    "wattle":                           "diagrams/dict_domestic_fowl.png",
    "comb":                             "diagrams/dict_domestic_fowl.png",
    "contour feather":                  "diagrams/dict_domestic_fowl.png",

    # 85 - Fractional distillation
    "fractional distillation":          "diagrams/dict_fractional_distillation.png",
    "fractionating column":             "diagrams/dict_fractional_distillation.png",
    "distillation":                     "diagrams/dict_fractional_distillation.png",
    "condenser":                        "diagrams/dict_fractional_distillation.png",
    "distilling flask":                 "diagrams/dict_fractional_distillation.png",
    "fractional distillation apparatus":"diagrams/dict_fractional_distillation.png",

    # 86 - Frame of reference
    "frame of reference":               "diagrams/dict_frame_of_reference.png",
    "reference point":                  "diagrams/dict_frame_of_reference.png",
    "inertial frame":                   "diagrams/dict_frame_of_reference.png",

    # 87 - Free electrons
    "free electron":                    "diagrams/dict_free_electrons.png",
    "free electrons":                   "diagrams/dict_free_electrons.png",
    "delocalized electron":             "diagrams/dict_free_electrons.png",
    "ionization":                       "diagrams/dict_free_electrons.png",
    "valence electron":                 "diagrams/dict_free_electrons.png",

    # 88 - Frequency polygon
    "frequency polygon":                "diagrams/dict_frequency_polygon.png",
    "histogram":                        "diagrams/dict_frequency_polygon.png",
    "frequency distribution":           "diagrams/dict_frequency_polygon.png",

    # 89 - Frost diagram
    "frost diagram":                    "diagrams/dict_frost_diagram.png",
    "frost diagrams":                   "diagrams/dict_frost_diagram.png",
    "oxidation state":                  "diagrams/dict_frost_diagram.png",
    "manganese":                        "diagrams/dict_frost_diagram.png",
    "redox":                            "diagrams/dict_frost_diagram.png",

    # 90 - Friedel-Crafts reaction
    "friedel-crafts reaction":          "diagrams/dict_friedel_crafts.png",
    "friedel-crafts alkylation":        "diagrams/dict_friedel_crafts.png",
    "friedel-crafts acylation":         "diagrams/dict_friedel_crafts.png",
    "friedel-craft alkylation":         "diagrams/dict_friedel_crafts.png",
    "friedel-craft acylation":          "diagrams/dict_friedel_crafts.png",
    "electrophilic aromatic substitution":"diagrams/dict_friedel_crafts.png",
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
print("\nBatch 9 integration complete!")
