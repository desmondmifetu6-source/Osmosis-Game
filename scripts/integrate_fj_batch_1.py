"""
integrate_fj_batch_1.py
=======================
Integration of F-J Diagrams - Batch 1 (Screenshots 1 to 30)
"""

import os
import shutil
import json

SCREENSHOT_DIR = "f-j diagrams"
DIAGRAMS_DIR = "diagrams"

copies = [
    ("Screenshot_11-9-2026_153052_.jpeg", "dict_galeate.png"),
    ("Screenshot_11-9-2026_15309_.jpeg",  "dict_galactose.png"),
    ("Screenshot_11-9-2026_153112_.jpeg", "dict_galilean_telescope.png"),
    ("Screenshot_11-9-2026_153129_.jpeg", "dict_moving_coil_galvanometer.png"),
    ("Screenshot_11-9-2026_15312_.jpeg",  "dict_gallic_acid.png"),
    ("Screenshot_11-9-2026_153145_.jpeg", "dict_gamma_aminobutyric_acid.png"),
    ("Screenshot_11-9-2026_153158_.jpeg", "dict_gas_engine.png"),
    ("Screenshot_11-9-2026_153243_.jpeg", "dict_argand_diagram_gaussian.png"),
    ("Screenshot_11-9-2026_153255_.jpeg", "dict_geiger_counter.png"),
    ("Screenshot_11-9-2026_15326_.jpeg",  "dict_gas_thermometer.png"),
    ("Screenshot_11-9-2026_153334_.jpeg", "dict_ac_generator.png"),
    ("Screenshot_11-9-2026_153348_.jpeg", "dict_geoboard.png"),
    ("Screenshot_11-9-2026_15335_.jpeg",  "dict_gem_dimethyl_group.png"),
    ("Screenshot_11-9-2026_15340_.jpeg",  "dict_geraniol.png"),
    ("Screenshot_11-9-2026_153411_.jpeg", "dict_gibbous_calyx.png"),
    ("Screenshot_11-9-2026_153420_.jpeg", "dict_gibberellins.png"),
    ("Screenshot_11-9-2026_153436_.jpeg", "dict_gladiate_leaf.png"),
    ("Screenshot_11-9-2026_153452_.jpeg", "dict_glucuronic_acid.png"),
    ("Screenshot_11-9-2026_153458_.jpeg", "dict_glutathione.png"),
    ("Screenshot_11-9-2026_153518_.jpeg", "dict_glycosidic_bonds.png"),
    ("Screenshot_11-9-2026_153527_.jpeg", "dict_gnomon_magic_square.png"),
    ("Screenshot_11-9-2026_153546_.jpeg", "dict_gradient.png"),
    ("Screenshot_11-9-2026_153554_.jpeg", "dict_graduate_involucre.png"),
    ("Screenshot_11-9-2026_15357_.jpeg",  "dict_propane_1_2_3_triol.png"),
    ("Screenshot_11-9-2026_153612_.jpeg", "dict_graphene.png"),
    ("Screenshot_11-9-2026_15361_.jpeg",  "dict_grafting.png"),
    ("Screenshot_11-9-2026_153624_.jpeg", "dict_structure_of_graphite.png"),
    ("Screenshot_11-9-2026_153631_.jpeg", "dict_grasshopper.png"),
    ("Screenshot_11-9-2026_153641_.jpeg", "dict_gravitation.png"),
]

print("== Step 1: Copying screenshots to diagrams/ ==")
for src_name, dst_name in copies:
    src = os.path.join(SCREENSHOT_DIR, src_name)
    dst = os.path.join(DIAGRAMS_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  [WARN] NOT FOUND: {src}")
        continue
    shutil.copy2(src, dst)
    print(f"  [OK] {src_name} -> {dst_name}")

NEW_MAPPINGS = {
    # 1. Galeate
    "galeate": "diagrams/dict_galeate.png",
    "galeate corolla": "diagrams/dict_galeate.png",

    # 2. Galactose
    "galactose": "diagrams/dict_galactose.png",

    # 3. Galilean telescope
    "galilean telescope": "diagrams/dict_galilean_telescope.png",

    # 4. Moving coil galvanometer
    "moving coil galvanometer": "diagrams/dict_moving_coil_galvanometer.png",
    "galvanometer": "diagrams/dict_moving_coil_galvanometer.png",

    # 5. Gallic Acid
    "gallic acid": "diagrams/dict_gallic_acid.png",
    "3,4,5-trihydroxybenzoic acid": "diagrams/dict_gallic_acid.png",

    # 6. Gamma-Aminobutyric Acid
    "gamma-aminobutyric acid": "diagrams/dict_gamma_aminobutyric_acid.png",
    "gaba": "diagrams/dict_gamma_aminobutyric_acid.png",

    # 7. Gas engine
    "gas engine": "diagrams/dict_gas_engine.png",

    # 9. Argand diagram / Gaussian plane
    "argand diagram": "diagrams/dict_argand_diagram_gaussian.png",
    "gaussian plane": "diagrams/dict_argand_diagram_gaussian.png",
    "complex plane": "diagrams/dict_argand_diagram_gaussian.png",

    # 10. Geiger counter
    "geiger counter": "diagrams/dict_geiger_counter.png",
    "geiger-muller counter": "diagrams/dict_geiger_counter.png",
    "gm counter": "diagrams/dict_geiger_counter.png",

    # 11. Gas thermometer
    "gas thermometer": "diagrams/dict_gas_thermometer.png",
    "constant volume gas thermometer": "diagrams/dict_gas_thermometer.png",

    # 12. AC generator
    "ac generator": "diagrams/dict_ac_generator.png",
    "alternator": "diagrams/dict_ac_generator.png",
    "dynamo": "diagrams/dict_ac_generator.png",

    # 13. Geoboard
    "geoboard": "diagrams/dict_geoboard.png",

    # 14. Gem-dimethyl Group
    "gem-dimethyl group": "diagrams/dict_gem_dimethyl_group.png",
    "geminal": "diagrams/dict_gem_dimethyl_group.png",

    # 15. Geraniol
    "geraniol": "diagrams/dict_geraniol.png",

    # 16. Gibbous calyx
    "gibbous calyx": "diagrams/dict_gibbous_calyx.png",
    "gibbous": "diagrams/dict_gibbous_calyx.png",

    # 17. Gibberellins
    "gibberellins": "diagrams/dict_gibberellins.png",
    "gibberellin": "diagrams/dict_gibberellins.png",
    "gibberellic acid": "diagrams/dict_gibberellins.png",

    # 18. Gladiate leaf
    "gladiate leaf": "diagrams/dict_gladiate_leaf.png",
    "gladiate": "diagrams/dict_gladiate_leaf.png",

    # 19. Glucuronic Acid
    "glucuronic acid": "diagrams/dict_glucuronic_acid.png",

    # 20. Glutathione
    "glutathione": "diagrams/dict_glutathione.png",

    # 21. Glycosidic Bonds
    "glycosidic bonds": "diagrams/dict_glycosidic_bonds.png",
    "glycosidic bond": "diagrams/dict_glycosidic_bonds.png",
    "glycoside linkage": "diagrams/dict_glycosidic_bonds.png",

    # 22. Gnomon magic square
    "gnomon magic square": "diagrams/dict_gnomon_magic_square.png",
    "gnomon": "diagrams/dict_gnomon_magic_square.png",

    # 23. Gradient
    "gradient": "diagrams/dict_gradient.png",
    "slope": "diagrams/dict_gradient.png",

    # 24. Graduate Involucre
    "graduate involucre": "diagrams/dict_graduate_involucre.png",
    "gradate involucre": "diagrams/dict_graduate_involucre.png",
    "involucre": "diagrams/dict_graduate_involucre.png",

    # 25. Propane-1,2,3-triol
    "propane-1,2,3-triol": "diagrams/dict_propane_1_2_3_triol.png",
    "glycerol": "diagrams/dict_propane_1_2_3_triol.png",
    "glycerin": "diagrams/dict_propane_1_2_3_triol.png",

    # 26. Graphene
    "graphene": "diagrams/dict_graphene.png",

    # 27. Grafting
    "grafting": "diagrams/dict_grafting.png",
    "scion": "diagrams/dict_grafting.png",

    # 28. Structure of graphite
    "graphite": "diagrams/dict_structure_of_graphite.png",
    "structure of graphite": "diagrams/dict_structure_of_graphite.png",

    # 29. Grasshopper
    "grasshopper": "diagrams/dict_grasshopper.png",
    "lateral view of a grasshopper": "diagrams/dict_grasshopper.png",

    # 30. Gravitation
    "gravitation": "diagrams/dict_gravitation.png",
    "newton's law of gravitation": "diagrams/dict_gravitation.png",
    "universal gravitation": "diagrams/dict_gravitation.png",
}

MAP_FILE = "dictionary_diagrams_map.json"
print(f"\n== Step 2: Updating {MAP_FILE} ==")

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

added = 0
for term, path in NEW_MAPPINGS.items():
    if term not in diagram_map:
        diagram_map[term] = path
        print(f"  + Added:   \"{term}\"")
        added += 1
    else:
        print(f"  ~ Updated: \"{term}\" -> {path}")
        diagram_map[term] = path
        added += 1

diagram_map_sorted = dict(sorted(diagram_map.items()))
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(diagram_map_sorted, f, indent=2, ensure_ascii=False)

print(f"\n  [OK] {MAP_FILE} saved. Updated/Added: {added}")

print("\n== Step 3: Rebuilding core_dictionary_diagrams.js ==")
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

print("  [OK] core_dictionary_diagrams.js rebuilt successfully.")
print(f"Total mapped entries in dictionary: {len(diagram_map_sorted)}")
