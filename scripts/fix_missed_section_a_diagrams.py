import os
import shutil
import json

MISSED_DIR = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams\missed diagrams from sectino a"
DIAGRAMS_DIR = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"

MAPPINGS = [
    {
        "src": "Screenshot_1-9-2026_134118_.jpeg",
        "dest_files": ["dict_abacus.png"],
        "keys": ["abacus"]
    },
    {
        "src": "Screenshot_1-9-2026_134131_.jpeg",
        "dest_files": ["dict_abaxial.png"],
        "keys": ["abaxial"]
    },
    {
        "src": "Screenshot_1-9-2026_134141_.jpeg",
        "dest_files": ["dict_abbe_prism.png"],
        "keys": ["abbe prism"]
    },
    {
        "src": "Screenshot_1-9-2026_134149_.jpeg",
        "dest_files": ["dict_abbe_refractometer.png"],
        "keys": ["abbe refractometer", "abbe type critical angle refractometer"]
    },
    {
        "src": "Screenshot_1-9-2026_134158_.jpeg",
        "dest_files": ["dict_abdomen.png", "dict_abdomen_abdominal_cavity.png"],
        "keys": ["abdomen", "abdomen (abdominal cavity)", "abdominal cavity"]
    },
    {
        "src": "Screenshot_1-9-2026_13416_.jpeg",
        "dest_files": ["dict_valine.png", "dict_2_amino_3_methylbutanoic_acid.png"],
        "keys": ["valine", "2-amino-3-methylbutanoic acid", "val"]
    }
]

print("Step 1: Copying physical diagram assets...")
for item in MAPPINGS:
    src_path = os.path.join(MISSED_DIR, item["src"])
    if not os.path.exists(src_path):
        print(f"ERROR: Source file missing: {src_path}")
        continue
    
    for dest_name in item["dest_files"]:
        dest_path = os.path.join(DIAGRAMS_DIR, dest_name)
        shutil.copy2(src_path, dest_path)
        print(f"Copied {item['src']} -> {dest_name}")

print("\nStep 2: Updating dictionary_diagrams_map.json (Source of Truth)...")
map_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
with open(map_path, "r", encoding="utf-8") as f:
    diag_map = json.load(f)

for item in MAPPINGS:
    primary_dest = f"diagrams/{item['dest_files'][0]}"
    for key in item["keys"]:
        norm_key = key.lower().strip()
        diag_map[norm_key] = primary_dest
        print(f"Mapped '{norm_key}' -> {primary_dest}")

sorted_map = dict(sorted(diag_map.items()))
with open(map_path, "w", encoding="utf-8") as f:
    json.dump(sorted_map, f, indent=4, ensure_ascii=False)

print("\nStep 3: Regenerating core_dictionary_diagrams.js bundle...")
js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"
js_content = f"// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nconst DictionaryDiagrams = {json.dumps(sorted_map, indent=4, ensure_ascii=False)};\n"
with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("\nStep 4: Empirical Integrity Verification...")
missing_count = 0
for k, v in sorted_map.items():
    full_path = os.path.join(r"c:\Users\Desmond\Desktop\final_osmosis", v)
    if not os.path.exists(full_path):
        print(f"WARNING: File missing for key '{k}': {v}")
        missing_count += 1

if missing_count == 0:
    print("SUCCESS! 100% of diagram mappings exist physically on disk!")
else:
    print(f"FOUND {missing_count} MISSING FILES.")
