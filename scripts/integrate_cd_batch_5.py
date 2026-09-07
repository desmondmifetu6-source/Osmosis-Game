import os
import json
from PIL import Image
import clean_and_enrich_formulas as cleaner
import fitz

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\c-d didagrams"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"
map_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
core_js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"
dict_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary.json"
pdf_path = r"c:\Users\Desmond\Desktop\final_osmosis\split_sections\264_PDFsam_Dictionary Book 2.pdf"

with open(dict_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

c_entries = data.get('C', [])
existing_words = {e['word'].lower().strip() for e in c_entries}
for e in c_entries:
    for s in e.get('synonyms', []):
        existing_words.add(s.lower().strip())

batch_terms_check = [
    ("chalcone", "CHALCONE"),
    ("chelate", "CHELATE"),
    ("chlor-alkali cell", "CHLOR-ALKALI CELL"),
    ("chlorine", "CHLORINE"),
    ("chloroplast", "CHLOROPLAST"),
    ("chromatic number", "CHROMATIC NUMBER"),
    ("ciliate", "CILIATE"),
    ("cincinnus", "CINCINNUS")
]

print("=== Checking Batch 5 Terms in dictionary.json ===")
doc = fitz.open(pdf_path)

for term, headword in batch_terms_check:
    if term in existing_words:
        print(f"  FOUND in dictionary.json: {term}")
    else:
        print(f"  MISSING: {term} -> Searching PDF...")
        found_def = None
        for page_idx, page in enumerate(doc):
            text = page.get_text()
            if headword in text:
                lines = text.splitlines()
                for l_idx, line in enumerate(lines):
                    if line.strip().startswith(headword):
                        def_lines = [line.split(":", 1)[-1].strip() if ":" in line else line.strip()]
                        for next_l in lines[l_idx+1:]:
                            if next_l.strip().isupper() and ":" in next_l:
                                break
                            def_lines.append(next_l.strip())
                        found_def = " ".join(def_lines).strip()
                        print(f"    Found on page {page_idx+1}: {found_def[:80]}...")
                        break
                if found_def:
                    break
        if found_def:
            idx_insert = 0
            for i, item in enumerate(c_entries):
                if item.get('word', '').lower() > term:
                    idx_insert = i
                    break
            new_entry = {
                "word": term,
                "raw_headword": headword,
                "synonyms": [],
                "definition": found_def
            }
            c_entries.insert(idx_insert, new_entry)
            existing_words.add(term)
            print(f"    Inserted '{term}' into Section C at index {idx_insert}")

data['C'] = c_entries
with open(dict_json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\n=== Rebuilding core_dictionary.js ===")
cleaner.process_dictionary(dict_json_path, dict_json_path, 'core_dictionary.js')
print("core_dictionary.js rebuilt successfully!")

print("\n=== Saving Diagram Images (41-50) ===")
items = [
    ("Screenshot_30-8-2026_21531_.jpeg", ["dict_chalcone.png"]),
    ("Screenshot_30-8-2026_215327_.jpeg", ["dict_chelate.png", "dict_chelation.png"]),
    ("Screenshot_30-8-2026_215352_.jpeg", ["dict_chemical_compound.png", "dict_chemical_bonding.png"]),
    ("Screenshot_30-8-2026_215439_.jpeg", ["dict_chlor_alkali_cell.png", "dict_chlor_alkali_process.png"]),
    ("Screenshot_30-8-2026_215447_.jpeg", ["dict_chlorine_preparation.png"]),
    ("Screenshot_30-8-2026_215457_.jpeg", ["dict_chloroplast.png", "dict_granum.png"]),
    ("Screenshot_30-8-2026_215520_.jpeg", ["dict_chromatic_number.png"]),
    ("Screenshot_30-8-2026_215532_.jpeg", ["dict_ciliate_leaf.png", "dict_ciliate.png"]),
    ("Screenshot_30-8-2026_215540_.jpeg", ["dict_cincinnus.png", "dict_cincinnus_inflorescence.png"])
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

print("\n=== Updating dictionary_diagrams_map.json & core_dictionary_diagrams.js ===")
with open(map_json_path, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

new_mappings = {
    "chalcone": "diagrams/dict_chalcone.png",
    "chelate": "diagrams/dict_chelate.png",
    "chelation": "diagrams/dict_chelation.png",
    "chemical compound": "diagrams/dict_chemical_compound.png",
    "chemical bonding": "diagrams/dict_chemical_bonding.png",
    "bonding of atoms in a chemical compound": "diagrams/dict_chemical_compound.png",
    "chlor-alkali cell": "diagrams/dict_chlor_alkali_cell.png",
    "chlor-alkali process": "diagrams/dict_chlor_alkali_process.png",
    "diaphragm of chlor-alkali cell": "diagrams/dict_chlor_alkali_cell.png",
    "chlorine": "diagrams/dict_chlorine_preparation.png",
    "preparation of chlorine": "diagrams/dict_chlorine_preparation.png",
    "chloroplast": "diagrams/dict_chloroplast.png",
    "structure of a chloroplast": "diagrams/dict_chloroplast.png",
    "granum": "diagrams/dict_granum.png",
    "chromatic number": "diagrams/dict_chromatic_number.png",
    "ciliate": "diagrams/dict_ciliate.png",
    "ciliate leaf": "diagrams/dict_ciliate_leaf.png",
    "cincinnus": "diagrams/dict_cincinnus.png",
    "cincinnus inflorescence": "diagrams/dict_cincinnus_inflorescence.png"
}

diag_map.update(new_mappings)

with open(map_json_path, 'w', encoding='utf-8') as f:
    json.dump(diag_map, f, indent=4, ensure_ascii=False)

js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(diag_map, indent=4, ensure_ascii=False) + ";\n"
with open(core_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Total mapped terms now: {len(diag_map)}")
print("Batch 5 integration complete!")
