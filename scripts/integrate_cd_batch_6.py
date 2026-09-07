import os
import json
import re
import fitz  # PyMuPDF
from PIL import Image

def find_definition_in_pdf(pdf_path, term):
    doc = fitz.open(pdf_path)
    term_pattern = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
    results = []
    
    for page_idx in range(len(doc)):
        text = doc[page_idx].get_text()
        lines = text.split("\n")
        for i, line in enumerate(lines):
            clean_l = line.strip()
            if term_pattern.match(clean_l) or clean_l.lower() == term.lower():
                block = " ".join([l.strip() for l in lines[i:min(i+15, len(lines))] if l.strip()])
                results.append((page_idx + 1, clean_l, block))
    return results

def main():
    dict_path = 'dictionary.json'
    map_path = 'dictionary_diagrams_map.json'
    core_dict_js = 'core_dictionary.js'
    pdf_c_path = r'split_sections/264_PDFsam_Dictionary Book 2.pdf'
    
    with open(dict_path, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    
    existing_keys = {k.lower(): k for k in dictionary.keys()}
    
    # Batch 6 terms & mappings:
    # 51: Screenshot_30-8-2026_215551_.jpeg -> cinnamic acid
    # 52: Screenshot_30-8-2026_21559_.jpeg  -> cholesterol
    # 53: Screenshot_30-8-2026_21560_.jpeg  -> circle / circle parts
    # 54: Screenshot_30-8-2026_215614_.jpeg -> circle theorems
    # 55: Screenshot_30-8-2026_215634_.jpeg -> circular cone / cone
    # 56: Screenshot_30-8-2026_221012_.jpeg -> cosine law / cosine rule
    # 57: Screenshot_30-8-2026_221021_.jpeg -> corymb
    # 58: Screenshot_30-8-2026_221028_.jpeg -> coterminal angles
    # 59: Screenshot_30-8-2026_22103_.jpeg  -> cortisone
    # 60: Screenshot_30-8-2026_221040_.jpeg -> coumarin
    # 61: Screenshot_30-8-2026_221048_.jpeg -> couple / moment of a couple
    # 62: Screenshot_30-8-2026_221056_.jpeg -> crab
    # 63: Screenshot_30-8-2026_221116_.jpeg -> crenation / crenate
    # 64: Screenshot_30-8-2026_221121_.jpeg -> critical angle
    # 65: Screenshot_30-8-2026_221128_.jpeg -> crest / crest of a wave

    terms_to_check = [
        "cinnamic acid", "cholesterol", "circle", "circle theorems",
        "circular cone", "cosine rule", "cosine law", "corymb",
        "coterminal angles", "cortisone", "coumarin", "couple",
        "moment of a couple", "crab", "crenation", "crenate",
        "critical angle", "crest"
    ]
    
    print("=== Checking Batch 6 Terms in dictionary.json ===")
    added_terms = False
    for term in terms_to_check:
        if term.lower() in existing_keys:
            print(f"  FOUND in dictionary.json: {term} -> '{existing_keys[term.lower()]}'")
        else:
            print(f"  MISSING: {term} -> Searching PDF...")
            res = find_definition_in_pdf(pdf_c_path, term)
            if res:
                page_no, head, block = res[0]
                safe_block = block[:120].encode('ascii', 'replace').decode('ascii')
                print(f"    Found on PDF p. {page_no}: {safe_block}...")
                dictionary[term.lower()] = block
                existing_keys[term.lower()] = term.lower()
                added_terms = True
            else:
                print(f"    Warning: '{term}' not directly matched in Section C PDF.")
                # If term has synonym in dict, e.g., cone vs circular cone
                if term == "circular cone" and "cone" in existing_keys:
                    print(f"    Using cone mapping")
                elif term == "cosine law" and "cosine rule" in existing_keys:
                    print(f"    Using cosine rule")
                elif term == "coterminal angles":
                    # Check if 'coterminal' is in PDF
                    res2 = find_definition_in_pdf(pdf_c_path, "coterminal")
                    if res2:
                        page_no, head, block = res2[0]
                        dictionary[term.lower()] = block
                        existing_keys[term.lower()] = term.lower()
                        added_terms = True

    if added_terms:
        print("\n=== Updating dictionary.json & rebuilding core_dictionary.js ===")
        sorted_dict = dict(sorted(dictionary.items(), key=lambda x: x[0].lower()))
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_dict, f, indent=2, ensure_ascii=False)
        
        import clean_and_enrich_formulas
        clean_and_enrich_formulas.process_dictionary(dict_path, dict_path, core_dict_js)
        print("Dictionary rebuilt!")
    else:
        print("No missing terms needed to be added to dictionary.json.")

    # Image mapping definitions:
    # (source_file, target_filename, list_of_terms)
    images_to_process = [
        ("Screenshot_30-8-2026_215551_.jpeg", "dict_cinnamic_acid.png", ["cinnamic acid"]),
        ("Screenshot_30-8-2026_21559_.jpeg", "dict_cholesterol.png", ["cholesterol"]),
        ("Screenshot_30-8-2026_21560_.jpeg", "dict_circle_parts.png", ["circle"]),
        ("Screenshot_30-8-2026_215614_.jpeg", "dict_circle_theorems.png", ["circle theorems"]),
        ("Screenshot_30-8-2026_215634_.jpeg", "dict_circular_cone.png", ["cone", "circular cone"]),
        ("Screenshot_30-8-2026_221012_.jpeg", "dict_cosine_rule.png", ["cosine rule", "cosine law"]),
        ("Screenshot_30-8-2026_221021_.jpeg", "dict_corymb.png", ["corymb"]),
        ("Screenshot_30-8-2026_221028_.jpeg", "dict_coterminal_angles.png", ["coterminal angles"]),
        ("Screenshot_30-8-2026_22103_.jpeg", "dict_cortisone.png", ["cortisone"]),
        ("Screenshot_30-8-2026_221040_.jpeg", "dict_coumarin.png", ["coumarin"]),
        ("Screenshot_30-8-2026_221048_.jpeg", "dict_couple_forces.png", ["couple", "moment of a couple"]),
        ("Screenshot_30-8-2026_221056_.jpeg", "dict_crab.png", ["crab"]),
        ("Screenshot_30-8-2026_221116_.jpeg", "dict_crenation.png", ["crenation", "crenate"]),
        ("Screenshot_30-8-2026_221121_.jpeg", "dict_critical_angle.png", ["critical angle"]),
        ("Screenshot_30-8-2026_221128_.jpeg", "dict_crest.png", ["crest", "crest of a wave"]),
    ]

    print("\n=== Saving Diagram Images (51-65) ===")
    os.makedirs('diagrams', exist_ok=True)
    for src_name, tgt_name, terms in images_to_process:
        src_p = os.path.join('c-d didagrams', src_name)
        tgt_p = os.path.join('diagrams', tgt_name)
        with Image.open(src_p) as img:
            img.save(tgt_p, 'PNG')
        print(f"  Saved {tgt_name}")

    print("\n=== Updating dictionary_diagrams_map.json & core_dictionary_diagrams.js ===")
    with open(map_path, 'r', encoding='utf-8') as f:
        diag_map = json.load(f)

    for src_name, tgt_name, terms in images_to_process:
        for t in terms:
            diag_map[t.lower()] = tgt_name

    sorted_map = dict(sorted(diag_map.items()))
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)

    with open('core_dictionary_diagrams.js', 'w', encoding='utf-8') as f:
        f.write("const DICTIONARY_DIAGRAMS = " + json.dumps(sorted_map, indent=2, ensure_ascii=False) + ";\n")

    print(f"Total mapped terms now: {len(sorted_map)}")
    print("Batch 6 integration complete!")

if __name__ == '__main__':
    main()
