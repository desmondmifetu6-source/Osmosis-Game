"""
integrate_ef_batch_7.py
=======================
Section E-F Diagram Integration - Batch 7 (Screenshots 61-70)

  61. Screenshot_8-9-2026_175330_  -> Factor Tree of 18
  62. Screenshot_8-9-2026_175342_  -> Falcate leaf
  63. Screenshot_8-9-2026_175418_  -> Flight feather (quill)
  64. Screenshot_8-9-2026_175522_  -> Fermi levels in Conductor, Semiconductor, Insulator
  65. Screenshot_8-9-2026_175544_  -> Chemical Structure of Ferrocene
  66. Screenshot_8-9-2026_17558_   -> Fern anatomy
  67. Screenshot_8-9-2026_175643_  -> Fibre-optic cable
  68. Screenshot_8-9-2026_17569_   -> Feynman diagram showing time/space, photons, electrons
  69. Screenshot_8-9-2026_175718_  -> Filter pump (water aspirator)
  70. Screenshot_8-9-2026_17571_   -> Field-Emission Microscope (FEM)
"""

import json, shutil, os, sys
sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_175330_.jpeg",  "dict_factor_tree.png"),
    ("Screenshot_8-9-2026_175342_.jpeg",  "dict_falcate_leaf.png"),
    ("Screenshot_8-9-2026_175418_.jpeg",  "dict_flight_feather.png"),
    ("Screenshot_8-9-2026_175522_.jpeg",  "dict_fermi_level.png"),
    ("Screenshot_8-9-2026_175544_.jpeg",  "dict_ferrocene.png"),
    ("Screenshot_8-9-2026_17558_.jpeg",   "dict_fern.png"),
    ("Screenshot_8-9-2026_175643_.jpeg",  "dict_fibre_optic_cable.png"),
    ("Screenshot_8-9-2026_17569_.jpeg",   "dict_feynman_diagram.png"),
    ("Screenshot_8-9-2026_175718_.jpeg",  "dict_filter_pump.png"),
    ("Screenshot_8-9-2026_17571_.jpeg",   "dict_field_emission_microscope.png"),
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
    # 61 - Factor tree
    "factor tree":                      "diagrams/dict_factor_tree.png",
    "prime factorization":              "diagrams/dict_factor_tree.png",

    # 62 - Falcate leaf
    "falcate leaf":                     "diagrams/dict_falcate_leaf.png",
    "falcate":                          "diagrams/dict_falcate_leaf.png",

    # 63 - Flight feather
    "flight feather":                   "diagrams/dict_flight_feather.png",
    "feather":                          "diagrams/dict_flight_feather.png",
    "quill":                            "diagrams/dict_flight_feather.png",
    "calamus":                          "diagrams/dict_flight_feather.png",
    "rachis":                           "diagrams/dict_flight_feather.png",
    "aftershaft":                       "diagrams/dict_flight_feather.png",
    "barbule":                          "diagrams/dict_flight_feather.png",
    "vane":                             "diagrams/dict_flight_feather.png",

    # 64 - Fermi level
    "fermi level":                      "diagrams/dict_fermi_level.png",
    "fermi-dirac distribution":         "diagrams/dict_fermi_level.png",
    "fermi energy":                     "diagrams/dict_fermi_level.png",
    "fermi level in conductor":         "diagrams/dict_fermi_level.png",
    "fermi level in semiconductor":     "diagrams/dict_fermi_level.png",
    "fermi level in insulator":         "diagrams/dict_fermi_level.png",

    # 65 - Ferrocene
    "ferrocene":                        "diagrams/dict_ferrocene.png",
    "chemical structure of ferrocene":  "diagrams/dict_ferrocene.png",
    "metallocene":                      "diagrams/dict_ferrocene.png",
    "sandwich compound":                "diagrams/dict_ferrocene.png",

    # 66 - Fern
    "fern":                             "diagrams/dict_fern.png",
    "frond":                            "diagrams/dict_fern.png",
    "pteridophyte":                     "diagrams/dict_fern.png",
    "adventitious roots":               "diagrams/dict_fern.png",

    # 67 - Fibre-optic cable
    "fibre-optic cable":                "diagrams/dict_fibre_optic_cable.png",
    "fiber-optic cable":                "diagrams/dict_fibre_optic_cable.png",
    "optical fibre":                    "diagrams/dict_fibre_optic_cable.png",
    "optical fiber":                    "diagrams/dict_fibre_optic_cable.png",
    "cladding":                         "diagrams/dict_fibre_optic_cable.png",

    # 68 - Feynman diagram
    "feynman diagram":                  "diagrams/dict_feynman_diagram.png",
    "feynman diagrams":                 "diagrams/dict_feynman_diagram.png",
    "quantum electrodynamics":          "diagrams/dict_feynman_diagram.png",
    "electron-positron annihilation":   "diagrams/dict_feynman_diagram.png",
    "virtual particle":                 "diagrams/dict_feynman_diagram.png",

    # 69 - Filter pump
    "filter pump":                      "diagrams/dict_filter_pump.png",
    "aspirator":                        "diagrams/dict_filter_pump.png",
    "water aspirator":                  "diagrams/dict_filter_pump.png",
    "suction pump":                     "diagrams/dict_filter_pump.png",

    # 70 - Field-Emission Microscope
    "field-emission microscope":        "diagrams/dict_field_emission_microscope.png",
    "fem":                              "diagrams/dict_field_emission_microscope.png",
    "field emission microscopy":        "diagrams/dict_field_emission_microscope.png",
    "field emission":                   "diagrams/dict_field_emission_microscope.png",
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
print("\nBatch 7 integration complete!")
