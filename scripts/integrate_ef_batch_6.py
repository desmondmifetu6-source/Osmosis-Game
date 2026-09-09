"""
integrate_ef_batch_6.py
=======================
Section E-F Diagram Integration - Batch 6 (Screenshots 51-60)

  51. Screenshot_8-9-2026_135311_  -> Drawing of a mammalian (human) excretory system
  52. Screenshot_8-9-2026_135329_  -> Excurrent leaf
  53. Screenshot_8-9-2026_135439_  -> Reaction profile diagram for exothermic reaction
  54. Screenshot_8-9-2026_135517_  -> An explanate flower
  55. Screenshot_8-9-2026_135628_  -> Exterior angles of triangle, transversal, polygon
  56. Screenshot_8-9-2026_13572_   -> External work done on expansion
  57. Screenshot_8-9-2026_135752_  -> Extrinsic semiconductor (p-type and n-type)
  58. Screenshot_8-9-2026_135813_  -> Longitudinal section of a mammalian eye
  59. Screenshot_8-9-2026_175251_  -> Face-centred cube (FCC)
  60. Screenshot_8-9-2026_17532_   -> Addition/subtraction & multiplication/division fact triangle
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_135311_.jpeg",  "dict_excretory_system.png"),
    ("Screenshot_8-9-2026_135329_.jpeg",  "dict_excurrent_leaf.png"),
    ("Screenshot_8-9-2026_135439_.jpeg",  "dict_exothermic_reaction.png"),
    ("Screenshot_8-9-2026_135517_.jpeg",  "dict_explanate_flower.png"),
    ("Screenshot_8-9-2026_135628_.jpeg",  "dict_exterior_angles.png"),
    ("Screenshot_8-9-2026_13572_.jpeg",   "dict_external_work_expansion.png"),
    ("Screenshot_8-9-2026_135752_.jpeg",  "dict_extrinsic_semiconductor.png"),
    ("Screenshot_8-9-2026_135813_.jpeg",  "dict_mammalian_eye.png"),
    ("Screenshot_8-9-2026_175251_.jpeg",  "dict_face_centred_cube.png"),
    ("Screenshot_8-9-2026_17532_.jpeg",   "dict_fact_triangle.png"),
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
    # 51 - Mammalian Excretory System
    "excretory system":                 "diagrams/dict_excretory_system.png",
    "mammalian excretory system":       "diagrams/dict_excretory_system.png",
    "human excretory system":           "diagrams/dict_excretory_system.png",
    "kidney":                           "diagrams/dict_excretory_system.png",
    "ureter":                           "diagrams/dict_excretory_system.png",
    "renal artery":                     "diagrams/dict_excretory_system.png",
    "renal vein":                       "diagrams/dict_excretory_system.png",
    "urethra":                          "diagrams/dict_excretory_system.png",
    "urinary bladder":                  "diagrams/dict_excretory_system.png",
    "sphincter muscle":                 "diagrams/dict_excretory_system.png",

    # 52 - Excurrent leaf
    "excurrent leaf":                   "diagrams/dict_excurrent_leaf.png",
    "excurrent":                        "diagrams/dict_excurrent_leaf.png",

    # 53 - Exothermic reaction profile
    "exothermic reaction":              "diagrams/dict_exothermic_reaction.png",
    "reaction profile":                 "diagrams/dict_exothermic_reaction.png",
    "reaction profile diagram":         "diagrams/dict_exothermic_reaction.png",
    "exothermic":                       "diagrams/dict_exothermic_reaction.png",
    "activation energy":                "diagrams/dict_exothermic_reaction.png",

    # 54 - Explanate flower
    "explanate flower":                 "diagrams/dict_explanate_flower.png",
    "explanate":                        "diagrams/dict_explanate_flower.png",

    # 55 - Exterior angles
    "exterior angle":                   "diagrams/dict_exterior_angles.png",
    "exterior angles":                  "diagrams/dict_exterior_angles.png",
    "exterior angles of a triangle":    "diagrams/dict_exterior_angles.png",
    "exterior angles of a polygon":     "diagrams/dict_exterior_angles.png",

    # 56 - External work done on expansion
    "external work done on expansion":  "diagrams/dict_external_work_expansion.png",
    "work done on expansion":           "diagrams/dict_external_work_expansion.png",
    "expansion work":                   "diagrams/dict_external_work_expansion.png",

    # 57 - Extrinsic semiconductor
    "extrinsic semiconductor":          "diagrams/dict_extrinsic_semiconductor.png",
    "p-type semiconductor":             "diagrams/dict_extrinsic_semiconductor.png",
    "n-type semiconductor":             "diagrams/dict_extrinsic_semiconductor.png",

    # 58 - Mammalian eye
    "mammalian eye":                    "diagrams/dict_mammalian_eye.png",
    "eye":                              "diagrams/dict_mammalian_eye.png",
    "cornea":                           "diagrams/dict_mammalian_eye.png",
    "iris":                             "diagrams/dict_mammalian_eye.png",
    "pupil":                            "diagrams/dict_mammalian_eye.png",
    "retina":                           "diagrams/dict_mammalian_eye.png",
    "vitreous humour":                  "diagrams/dict_mammalian_eye.png",
    "aqueous humor":                    "diagrams/dict_mammalian_eye.png",
    "blind spot":                       "diagrams/dict_mammalian_eye.png",
    "yellow spot":                      "diagrams/dict_mammalian_eye.png",
    "optic nerve":                      "diagrams/dict_mammalian_eye.png",
    "choroid":                          "diagrams/dict_mammalian_eye.png",
    "conjunctiva":                      "diagrams/dict_mammalian_eye.png",

    # 59 - Face-centred cube
    "face-centred cube":                "diagrams/dict_face_centred_cube.png",
    "face-centred cubic":               "diagrams/dict_face_centred_cube.png",
    "face-centered cubic":              "diagrams/dict_face_centred_cube.png",
    "fcc":                              "diagrams/dict_face_centred_cube.png",
    "face-centred cubic lattice":       "diagrams/dict_face_centred_cube.png",

    # 60 - Fact triangle
    "fact triangle":                    "diagrams/dict_fact_triangle.png",
    "fact family":                      "diagrams/dict_fact_triangle.png",
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
print("\nBatch 6 integration complete!")
