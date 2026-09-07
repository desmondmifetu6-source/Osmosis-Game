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

print("=== STEP 1: Updating dictionary.json with missing terms ===")
with open(dict_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

c_entries = data.get('C', [])

# 1. Insert 'calixarenes' if missing
has_calix = any(item.get('word', '').lower() in ['calixarene', 'calixarenes'] for item in c_entries)
if not has_calix:
    # insert before 'call admission control'
    idx_insert = 0
    for i, item in enumerate(c_entries):
        if item.get('word', '').lower() > 'calixarenes':
            idx_insert = i
            break
    new_calix = {
        "word": "calixarenes",
        "raw_headword": "CALIXARENES (CALIXARENE)",
        "synonyms": ["calixarene", "phenol-derived calixarene"],
        "definition": "Macrocyclic compounds that have molecules with a cuplike structure. The simplest, calix[4]arene has four phenol molecules joined by four –CH2-groups into a ring. Calix[6]arene has six phenol molecules in the ring. Calixarenes have hydrophobic cavities that can play host to smaller molecules or ions in Host-Guest Complexes. Calixarenes are used in commercial applications such as ion selective electrodes, selective membranes and stationary phase in high-performance liquid chromatography (HPLC), which is a technique used to separate, identify, and quantify each component in a mixture."
    }
    c_entries.insert(idx_insert, new_calix)
    print(f"  + Added 'calixarenes' at index {idx_insert}")

# 2. Insert 'cannabinoids' if missing
has_cannab = any(item.get('word', '').lower() in ['cannabinoid', 'cannabinoids'] for item in c_entries)
if not has_cannab:
    # insert before 'cannabis'
    idx_insert = 0
    for i, item in enumerate(c_entries):
        if item.get('word', '').lower() > 'cannabinoids':
            idx_insert = i
            break
    new_cannab = {
        "word": "cannabinoids",
        "raw_headword": "CANNABINOIDS (CANNABINOID)",
        "synonyms": ["cannabinoid", "tetrahydrocannabinol", "thc"],
        "definition": "Structurally related phenolic constituents of the plant Cannabis sativa or generally referring to compounds not necessarily structurally related but which are known to elicit physiological action through interaction with the cannabinoid receptor found in the brain and the spleen of mammals. Tetrahydrocannabinol (THC) is the most notable cannabinoid with the structure in the diagram."
    }
    c_entries.insert(idx_insert, new_cannab)
    print(f"  + Added 'cannabinoids' at index {idx_insert}")

data['C'] = c_entries
with open(dict_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("  dictionary.json updated successfully.")

print("\n=== STEP 2: Rebuilding core_dictionary.js ===")
cleaner.process_dictionary(dict_json_path, dict_json_path, 'core_dictionary.js')
print("  core_dictionary.js rebuilt successfully!")

print("\n=== STEP 3: Processing and Saving Diagram Images ===")
# List of (source_filename, list_of_target_names, optional_crop_box)
# If no crop_box, direct copy
items = [
    ("Screenshot 2026-08-30 212430.png", ["dict_chloroprene.png"], None),
    ("Screenshot 2026-08-30 212906.png", ["dict_caffeine.png"], None),
    ("Screenshot 2026-08-30 213001.png", ["dict_calixarene.png", "dict_calixarenes.png", "dict_phenol_derived_calixarene.png"], None),
    # 4. Multi-figure: Vernier calipers & scale
    ("Screenshot 2026-08-30 213059.png", ["dict_vernier.png", "dict_sliding_callipers.png"], None),
    ("Screenshot 2026-08-30 213237.png", ["dict_calorimeter.png", "dict_simple_calorimeter.png"], None),
    ("Screenshot_30-8-2026_21334_.jpeg", ["dict_calomel_electrode.png", "dict_calomel_half_cell.png"], None),
    ("Screenshot_30-8-2026_214236_.jpeg", ["dict_camphor.png"], None),
    ("Screenshot_30-8-2026_214318_.jpeg", ["dict_cannizzaro_reaction.png"], None),
    ("Screenshot_30-8-2026_214330_.jpeg", ["dict_canine.png", "dict_canines.png", "dict_canine_tooth.png"], None),
    ("Screenshot_30-8-2026_214339_.jpeg", ["dict_cannabinoid.png", "dict_cannabinoids.png", "dict_thc.png"], None),
    ("Screenshot_30-8-2026_214412_.jpeg", ["dict_capillary.png", "dict_vertebrate_capillary.png", "dict_blood_capillary.png"], None),
    ("Screenshot_30-8-2026_214423_.jpeg", ["dict_capacitor.png", "dict_capacitor_symbols.png"], None),
    ("Screenshot_30-8-2026_21442_.jpeg", ["dict_cantilever.png", "dict_cantilever_beam.png"], None),
    ("Screenshot_30-8-2026_214448_.jpeg", ["dict_capitate.png", "dict_capitate_structure.png"], None),
    ("Screenshot_30-8-2026_214458_.jpeg", ["dict_capitulum.png", "dict_capitulum_of_a_flower.png"], None),
    ("Screenshot_30-8-2026_214527_.jpeg", ["dict_carbocation.png", "dict_carbocation_structure.png"], None),
    ("Screenshot_30-8-2026_214537_.jpeg", ["dict_carbon_cycle.png"], None),
    ("Screenshot_30-8-2026_214548_.jpeg", ["dict_carbon_dioxide.png", "dict_co2.png"], None),
    ("Screenshot_30-8-2026_21458_.jpeg", ["dict_captan.png"], None),
    ("Screenshot_30-8-2026_214625_.jpeg", ["dict_cardioid.png"], None)
]

for src_file, targets, _ in items:
    src_path = os.path.join(src_dir, src_file)
    if not os.path.exists(src_path):
        print(f"  WARNING: missing {src_path}")
        continue
    # Open image with PIL to guarantee standard clean PNG format
    with Image.open(src_path) as img:
        for tgt in targets:
            tgt_path = os.path.join(out_dir, tgt)
            img.save(tgt_path, "PNG")
            print(f"  Saved {tgt}")

# Also split Screenshot 2026-08-30 213059.png into Fig 1 (calipers) and Fig 2 (scale)
im_v = Image.open(os.path.join(src_dir, "Screenshot 2026-08-30 213059.png"))
w, h = im_v.size
# Fig 1 is roughly top to 52%
fig1 = im_v.crop((0, 0, w, int(h * 0.54)))
fig1.save(os.path.join(out_dir, "dict_vernier_callipers.png"), "PNG")
fig1.save(os.path.join(out_dir, "dict_callipers.png"), "PNG")
# Fig 2 is roughly 52% to bottom
fig2 = im_v.crop((0, int(h * 0.52), w, h))
fig2.save(os.path.join(out_dir, "dict_vernier_scale.png"), "PNG")
print("  Split vernier callipers and vernier scale successfully.")

print("\n=== STEP 4: Updating dictionary_diagrams_map.json & core_dictionary_diagrams.js ===")
with open(map_json_path, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

new_mappings = {
    "chloroprene": "diagrams/dict_chloroprene.png",
    "caffeine": "diagrams/dict_caffeine.png",
    "calixarene": "diagrams/dict_calixarene.png",
    "calixarenes": "diagrams/dict_calixarenes.png",
    "phenol-derived calixarene": "diagrams/dict_phenol_derived_calixarene.png",
    "vernier": "diagrams/dict_vernier.png",
    "callipers": "diagrams/dict_callipers.png",
    "vernier callipers": "diagrams/dict_vernier_callipers.png",
    "sliding callipers": "diagrams/dict_sliding_callipers.png",
    "vernier scale": "diagrams/dict_vernier_scale.png",
    "calorimeter": "diagrams/dict_calorimeter.png",
    "simple calorimeter": "diagrams/dict_simple_calorimeter.png",
    "calomel electrode": "diagrams/dict_calomel_electrode.png",
    "calomel half cell": "diagrams/dict_calomel_half_cell.png",
    "camphor": "diagrams/dict_camphor.png",
    "cannizzaro reaction": "diagrams/dict_cannizzaro_reaction.png",
    "canine": "diagrams/dict_canine.png",
    "canines": "diagrams/dict_canines.png",
    "canine tooth": "diagrams/dict_canine_tooth.png",
    "cannabinoid": "diagrams/dict_cannabinoid.png",
    "cannabinoids": "diagrams/dict_cannabinoids.png",
    "thc": "diagrams/dict_thc.png",
    "tetrahydrocannabinol": "diagrams/dict_thc.png",
    "capillary": "diagrams/dict_capillary.png",
    "vertebrate capillary": "diagrams/dict_vertebrate_capillary.png",
    "blood capillary": "diagrams/dict_blood_capillary.png",
    "capacitor": "diagrams/dict_capacitor.png",
    "types of capacitor": "diagrams/dict_capacitor_symbols.png",
    "variable capacitor": "diagrams/dict_capacitor.png",
    "cantilever": "diagrams/dict_cantilever.png",
    "cantilever beam": "diagrams/dict_cantilever_beam.png",
    "capitate": "diagrams/dict_capitate.png",
    "capitate structure": "diagrams/dict_capitate_structure.png",
    "capitulum": "diagrams/dict_capitulum.png",
    "capitulum of a flower": "diagrams/dict_capitulum_of_a_flower.png",
    "carbocation": "diagrams/dict_carbocation.png",
    "carbocation structure": "diagrams/dict_carbocation_structure.png",
    "carbon cycle": "diagrams/dict_carbon_cycle.png",
    "carbon dioxide": "diagrams/dict_carbon_dioxide.png",
    "co2": "diagrams/dict_co2.png",
    "captan": "diagrams/dict_captan.png",
    "cardioid": "diagrams/dict_cardioid.png"
}

diag_map.update(new_mappings)

with open(map_json_path, 'w', encoding='utf-8') as f:
    json.dump(diag_map, f, indent=4, ensure_ascii=False)

js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(diag_map, indent=4, ensure_ascii=False) + ";\n"
with open(core_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print("  Saved dictionary_diagrams_map.json and core_dictionary_diagrams.js successfully!")
print(f"Total mapped terms now: {len(diag_map)}")
