"""
integrate_ef_batch_3.py
=======================
Section E-F Diagram Integration - Batch 3 (Screenshots 21-30)

  21. Screenshot_8-9-2026_113637_  -> Emarginate leaf
  22. Screenshot_8-9-2026_12313_   -> Eight Curve (lemniscate)
  23. Screenshot_8-9-2026_123244_  -> DUPLICATE of #16 (skip)
  24. Screenshot_8-9-2026_123345_  -> Embryo sac
  25. Screenshot_8-9-2026_123414_  -> Emergent Ray (refraction)
  26. Screenshot_8-9-2026_12352_   -> Emmetropia (Normal vision)
  27. Screenshot_8-9-2026_123547_  -> Enation on a leaf
  28. Screenshot_8-9-2026_123653_  -> The endocrine glands
  29. Screenshot_8-9-2026_123755_  -> Examples of endoparasite (Roundworm & Tapeworm)
  30. Screenshot_8-9-2026_123842_  -> Reaction profile diagram for endothermic reaction
"""

import json
import shutil
import os
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_113637_.jpeg",  "dict_emarginate_leaf.png"),
    ("Screenshot_8-9-2026_12313_.jpeg",   "dict_eight_curve.png"),
    # 23 is duplicate of 16 - skip
    ("Screenshot_8-9-2026_123345_.jpeg",  "dict_embryo_sac.png"),
    ("Screenshot_8-9-2026_123414_.jpeg",  "dict_emergent_ray.png"),
    ("Screenshot_8-9-2026_12352_.jpeg",   "dict_emmetropia.png"),
    ("Screenshot_8-9-2026_123547_.jpeg",  "dict_enation.png"),
    ("Screenshot_8-9-2026_123653_.jpeg",  "dict_endocrine_glands.png"),
    ("Screenshot_8-9-2026_123755_.jpeg",  "dict_endoparasite.png"),
    ("Screenshot_8-9-2026_123842_.jpeg",  "dict_endothermic_reaction.png"),
]

print("-- Step 1: Copying screenshots -> diagrams/ --")
for src_name, dst_name in copies:
    src = os.path.join(SCREENSHOT_DIR, src_name)
    dst = os.path.join(DIAGRAMS_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  WARNING: SOURCE NOT FOUND: {src}")
        continue
    shutil.copy2(src, dst)
    print(f"  OK  {src_name}  ->  {dst_name}")

NEW_MAPPINGS = {
    # 21 - Emarginate leaf
    "emarginate":               "diagrams/dict_emarginate_leaf.png",
    "emarginate leaf":          "diagrams/dict_emarginate_leaf.png",

    # 22 - Eight Curve / Lemniscate
    "eight curve":              "diagrams/dict_eight_curve.png",
    "lemniscate":               "diagrams/dict_eight_curve.png",

    # 24 - Embryo sac
    "embryo sac":               "diagrams/dict_embryo_sac.png",
    "ovule":                    "diagrams/dict_embryo_sac.png",

    # 25 - Emergent Ray
    "emergent ray":             "diagrams/dict_emergent_ray.png",
    "lateral shift":            "diagrams/dict_emergent_ray.png",

    # 26 - Emmetropia
    "emmetropia":               "diagrams/dict_emmetropia.png",
    "normal vision":            "diagrams/dict_emmetropia.png",

    # 27 - Enation
    "enation":                  "diagrams/dict_enation.png",

    # 28 - Endocrine glands
    "endocrine glands":         "diagrams/dict_endocrine_glands.png",
    "endocrine system":         "diagrams/dict_endocrine_glands.png",
    "hypothalamus":             "diagrams/dict_endocrine_glands.png",
    "pituitary gland":          "diagrams/dict_endocrine_glands.png",
    "thyroid gland":            "diagrams/dict_endocrine_glands.png",
    "parathyroid gland":        "diagrams/dict_endocrine_glands.png",
    "adrenal gland":            "diagrams/dict_endocrine_glands.png",
    "para-thyroid gland":       "diagrams/dict_endocrine_glands.png",

    # 29 - Endoparasite (Roundworm & Tapeworm)
    "endoparasite":             "diagrams/dict_endoparasite.png",
    "roundworm":                "diagrams/dict_endoparasite.png",
    "tapeworm":                 "diagrams/dict_endoparasite.png",
    "proglottid":               "diagrams/dict_endoparasite.png",

    # 30 - Endothermic reaction profile
    "endothermic reaction":     "diagrams/dict_endothermic_reaction.png",
    "reaction profile":         "diagrams/dict_endothermic_reaction.png",
    "activation energy":        "diagrams/dict_endothermic_reaction.png",
    "enthalpy change":          "diagrams/dict_endothermic_reaction.png",
    "reaction coordinate":      "diagrams/dict_endothermic_reaction.png",
}

MAP_FILE = "dictionary_diagrams_map.json"
print(f"\n-- Step 2: Updating {MAP_FILE} --")

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

added = 0
skipped = 0
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
js_lines.append("};")
js_lines.append("")
js_lines.append("if (typeof window !== 'undefined') {")
js_lines.append("  window.DictionaryDiagrams = DictionaryDiagrams;")
js_lines.append("}")
js_lines.append("if (typeof module !== 'undefined') {")
js_lines.append("  module.exports = DictionaryDiagrams;")
js_lines.append("}")

with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
    f.write("\n".join(js_lines) + "\n")

print("  OK core_dictionary_diagrams.js rebuilt successfully.")
print("\nBatch 3 integration complete!")
