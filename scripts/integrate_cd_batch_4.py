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
    ("catkin", "CATKIN"),
    ("cell cycle", "CELL CYCLE"),
    ("centipede", "CENTIPEDE"),
    ("cervical vertebra", "CERVICAL VERTEBRA"),
    ("cervix", "CERVIX"),
    ("ceva's theorem", "CEVA'S THEOREM"),
    ("chalaza", "CHALAZA"),
    ("centromere", "CENTROMERE"),
    ("charles' law", "CHARLES' LAW")
]

print("=== Checking Batch 4 Terms in dictionary.json ===")
doc = fitz.open(pdf_path)

for term, headword in batch_terms_check:
    if term in existing_words:
        print(f"  FOUND in dictionary.json: {term}")
    else:
        print(f"  MISSING: {term} -> Searching PDF...")
        # Search PDF
        found_def = None
        for page_idx, page in enumerate(doc):
            text = page.get_text()
            if headword in text:
                # locate paragraph
                lines = text.splitlines()
                for l_idx, line in enumerate(lines):
                    if line.strip().startswith(headword):
                        # capture definition until next ALL CAPS header or blank line
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
            # insert into c_entries alphabetically
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

print("\n=== Saving Diagram Images (31-40) ===")
items = [
    ("Screenshot_30-8-2026_21485_.jpeg", ["dict_catkin.png"]),
    ("Screenshot_30-8-2026_214912_.jpeg", ["dict_cell_cycle.png", "dict_cell_division_cycle.png"]),
    ("Screenshot_30-8-2026_215148_.jpeg", ["dict_centipede.png", "dict_external_features_of_a_centipede.png"]),
    ("Screenshot_30-8-2026_215218_.jpeg", ["dict_cervical_vertebra.png", "dict_cervical_vertebrae.png"]),
    ("Screenshot_30-8-2026_215229_.jpeg", ["dict_cervix.png", "dict_cervix_of_female_reproductive_system.png"]),
    ("Screenshot_30-8-2026_215244_.jpeg", ["dict_cevas_theorem.png"]),
    ("Screenshot_30-8-2026_215254_.jpeg", ["dict_chalaza.png", "dict_anatropous_ovule.png"]),
    ("Screenshot_30-8-2026_21527_.jpeg", ["dict_centromere.png", "dict_sister_chromatids.png", "dict_centromere_of_homologous_chromosome.png"]),
    ("Screenshot_30-8-2026_215317_.jpeg", ["dict_charles_law.png", "dict_graphical_illustration_of_charles_law.png"])
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
    "catkin": "diagrams/dict_catkin.png",
    "cell cycle": "diagrams/dict_cell_cycle.png",
    "cell division cycle": "diagrams/dict_cell_division_cycle.png",
    "centipede": "diagrams/dict_centipede.png",
    "external features of a centipede": "diagrams/dict_centipede.png",
    "cervical vertebra": "diagrams/dict_cervical_vertebra.png",
    "cervical vertebrae": "diagrams/dict_cervical_vertebra.png",
    "cervix": "diagrams/dict_cervix.png",
    "cervix of the female reproductive system": "diagrams/dict_cervix.png",
    "cervix of female reproductive system": "diagrams/dict_cervix.png",
    "ceva's theorem": "diagrams/dict_cevas_theorem.png",
    "cevas theorem": "diagrams/dict_cevas_theorem.png",
    "chalaza": "diagrams/dict_chalaza.png",
    "anatropous ovule": "diagrams/dict_chalaza.png",
    "centromere": "diagrams/dict_centromere.png",
    "sister chromatids": "diagrams/dict_sister_chromatids.png",
    "centromere of homologous chromosome": "diagrams/dict_centromere.png",
    "charles' law": "diagrams/dict_charles_law.png",
    "charles law": "diagrams/dict_charles_law.png",
    "graphical illustration of charles' law": "diagrams/dict_charles_law.png"
}

diag_map.update(new_mappings)

with open(map_json_path, 'w', encoding='utf-8') as f:
    json.dump(diag_map, f, indent=4, ensure_ascii=False)

js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(diag_map, indent=4, ensure_ascii=False) + ";\n"
with open(core_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Total mapped terms now: {len(diag_map)}")
print("Batch 4 integration complete!")
