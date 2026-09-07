import os
import shutil
import json
from PIL import Image
import clean_and_enrich_formulas as cleaner

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\c-d didagrams"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"
map_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
core_js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"
dict_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary.json"

print("=== STEP 1: Updating dictionary.json with missing terms for Batch 3 ===")
with open(dict_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Add 'castor oil' in C
c_entries = data.get('C', [])
has_castor = any(item.get('word', '').lower() in ['castor oil', 'castor tree'] for item in c_entries)
if not has_castor:
    idx_insert = 0
    for i, item in enumerate(c_entries):
        if item.get('word', '').lower() > 'castor oil':
            idx_insert = i
            break
    new_castor = {
        "word": "castor oil",
        "raw_headword": "CASTOR OIL (RICINUS COMMUNIS; CASTOR TREE)",
        "synonyms": ["ricinus communis", "castor tree", "castor oil plant", "castor nut"],
        "definition": "A pale-yellowish oil extracted from the seed of the castor-oil plant (Ricinus communis). It contains a mixture of glycerides of fatty acids, the predominant acid being ricinoleic acid, C17H32(OH)COOH. It is used as a drying oil in paints and varnishes and medically as a laxative."
    }
    c_entries.insert(idx_insert, new_castor)
    print(f"  + Added 'castor oil' to Section C at index {idx_insert}")
data['C'] = c_entries

# 2. Add 'plant cell' in P
p_entries = data.get('P', [])
has_plant_cell = any(item.get('word', '').lower() in ['plant cell'] for item in p_entries)
if not has_plant_cell:
    idx_insert = 0
    for i, item in enumerate(p_entries):
        if item.get('word', '').lower() > 'plant cell':
            idx_insert = i
            break
    new_plant_cell = {
        "word": "plant cell",
        "raw_headword": "PLANT CELL",
        "synonyms": ["typical plant cell"],
        "definition": "The structural and functional unit of plants, typically eukaryotic with a rigid cellulose cell wall outside the cell membrane, plastids such as chloroplasts for photosynthesis, and a large central vacuole containing cell sap."
    }
    p_entries.insert(idx_insert, new_plant_cell)
    print(f"  + Added 'plant cell' to Section P at index {idx_insert}")
data['P'] = p_entries

with open(dict_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  dictionary.json updated successfully.")

print("\n=== STEP 2: Rebuilding core_dictionary.js ===")
cleaner.process_dictionary(dict_json_path, dict_json_path, 'core_dictionary.js')
print("  core_dictionary.js rebuilt successfully!")

print("\n=== STEP 3: Saving Diagram Images for Batch 3 (21-30) ===")
items = [
    ("Screenshot_30-8-2026_214640_.jpeg", ["dict_carnot_cycle.png"]),
    ("Screenshot_30-8-2026_214654_.jpeg", ["dict_carrot.png", "dict_taproot_system_of_carrot.png", "dict_taproot.png"]),
    ("Screenshot_30-8-2026_214718_.jpeg", ["dict_cashew.png", "dict_cashew_tree.png", "dict_cashew_nut.png"]),
    ("Screenshot_30-8-2026_214729_.jpeg", ["dict_cassegrain_arrangement.png", "dict_cassegrain_telescope.png"]),
    ("Screenshot_30-8-2026_214741_.jpeg", ["dict_castor_oil.png", "dict_castor_tree.png", "dict_ricinus_communis.png"]),
    ("Screenshot_30-8-2026_214756_.jpeg", ["dict_cathode_ray_tube.png", "dict_crt.png", "dict_cathode_ray.png"]),
    ("Screenshot_30-8-2026_21478_.jpeg", ["dict_cartesian_coordinates.png", "dict_rectangular_coordinates.png"]),
    ("Screenshot_30-8-2026_214813_.jpeg", ["dict_caudate_leaf.png", "dict_caudate.png"]),
    ("Screenshot_30-8-2026_214848_.jpeg", ["dict_animal_cell.png", "dict_typical_animal_cell.png"]),
    ("Screenshot_30-8-2026_214858_.jpeg", ["dict_plant_cell.png", "dict_typical_plant_cell.png"])
]

for src_file, targets in items:
    src_path = os.path.join(src_dir, src_file)
    if not os.path.exists(src_path):
        print(f"  WARNING: missing {src_path}")
        continue
    with Image.open(src_path) as img:
        for tgt in targets:
            tgt_path = os.path.join(out_dir, tgt)
            img.save(tgt_path, "PNG")
            print(f"  Saved {tgt}")

print("\n=== STEP 4: Updating dictionary_diagrams_map.json & core_dictionary_diagrams.js ===")
with open(map_json_path, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

new_mappings = {
    "carnot cycle": "diagrams/dict_carnot_cycle.png",
    "carrot": "diagrams/dict_carrot.png",
    "taproot system of carrot": "diagrams/dict_taproot_system_of_carrot.png",
    "taproot": "diagrams/dict_taproot.png",
    "cashew": "diagrams/dict_cashew.png",
    "cashew tree": "diagrams/dict_cashew_tree.png",
    "cashew nut": "diagrams/dict_cashew_nut.png",
    "cassegrain arrangement": "diagrams/dict_cassegrain_arrangement.png",
    "cassegrain telescope": "diagrams/dict_cassegrain_telescope.png",
    "castor oil": "diagrams/dict_castor_oil.png",
    "castor tree": "diagrams/dict_castor_tree.png",
    "ricinus communis": "diagrams/dict_ricinus_communis.png",
    "cathode ray tube": "diagrams/dict_cathode_ray_tube.png",
    "crt": "diagrams/dict_crt.png",
    "cathode ray": "diagrams/dict_cathode_ray.png",
    "cartesian coordinates": "diagrams/dict_cartesian_coordinates.png",
    "rectangular coordinates": "diagrams/dict_rectangular_coordinates.png",
    "caudate": "diagrams/dict_caudate.png",
    "caudate leaf": "diagrams/dict_caudate_leaf.png",
    "animal cell": "diagrams/dict_animal_cell.png",
    "typical animal cell": "diagrams/dict_typical_animal_cell.png",
    "plant cell": "diagrams/dict_plant_cell.png",
    "typical plant cell": "diagrams/dict_typical_plant_cell.png",
    "cell": "diagrams/dict_animal_cell.png"
}

diag_map.update(new_mappings)

with open(map_json_path, 'w', encoding='utf-8') as f:
    json.dump(diag_map, f, indent=4, ensure_ascii=False)

js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(diag_map, indent=4, ensure_ascii=False) + ";\n"
with open(core_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Total mapped terms now: {len(diag_map)}")
print("Batch 3 integration complete!")
