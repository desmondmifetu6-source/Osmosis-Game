import os, json, re
import fitz
from PIL import Image

def find_in_pdf(pdf_path, term):
    doc = fitz.open(pdf_path)
    pat = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
    for pg in range(len(doc)):
        text = doc[pg].get_text()
        lines = text.split("\n")
        for i, line in enumerate(lines):
            cl = line.strip()
            if pat.match(cl) or cl.lower() == term.lower():
                block = " ".join(l.strip() for l in lines[i:min(i+15, len(lines))] if l.strip())
                return (pg+1, block)
    return None

def main():
    dict_path = 'dictionary.json'
    map_path  = 'dictionary_diagrams_map.json'
    core_js   = 'core_dictionary.js'
    pdf_c     = r'split_sections/264_PDFsam_Dictionary Book 2.pdf'
    pdf_d     = r'split_sections/414_PDFsam_Dictionary Book 2.pdf'

    with open(dict_path, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    existing = {k.lower(): k for k in dictionary.keys()}

    # Vision inspection results (images 106-135):
    # 106 Screenshot_30-8-2026_22213_.jpeg  -> Decagon (regular polygon)
    # 107 Screenshot_30-8-2026_222150_.jpeg -> Decussate leaves
    # 108 Screenshot_30-8-2026_222214_.jpeg -> Delocalization (resonance arrow diagram)
    # 109 Screenshot_30-8-2026_222225_.jpeg -> Resonance and electron delocalization in benzene
    # 110 Screenshot_30-8-2026_22223_.jpeg  -> Dehiscence (line of dehiscence on pod)
    # 111 Screenshot_30-8-2026_222257_.jpeg -> Deltahedron
    # 112 Screenshot_30-8-2026_222323_.jpeg -> Demodulator for AM signal (simplified)
    # 113 Screenshot_30-8-2026_222342_.jpeg -> Densities of some common substances (table)
    # 114 Screenshot_30-8-2026_222354_.jpeg -> Dentate leaf (dentation)
    # 115 Screenshot_30-8-2026_22237_.jpeg  -> Deltoid leaf
    # 116 Screenshot_30-8-2026_222423_.jpeg -> Dewar Structure (of benzene)
    # 117 Screenshot_30-8-2026_222435_.jpeg -> Diagonal (cuboid + quadrilateral)
    # 118 Screenshot_30-8-2026_22243_.jpeg  -> Circulatory system of man or mammal
    # 119 Screenshot_30-8-2026_222449_.jpeg -> Structure of diamond (giant covalent solid)
    # 120 Screenshot_30-8-2026_22244_.jpeg  -> Chemical structure of Deoxyribose
    # 121 Screenshot_30-8-2026_22250_.jpeg  -> Chemical structure of Diazepam
    # 122 Screenshot_30-8-2026_222524_.jpeg -> Chemical structure of DDT (duplicate diagram)
    # 123 Screenshot_30-8-2026_22254_.jpeg  -> Circumscribed circle / Circumcircle
    # 124 Screenshot_30-8-2026_222555_.jpeg -> Diels-Alder Reaction
    # 125 Screenshot_30-8-2026_22259_.jpeg  -> Dichasium cyme (inflorescence)
    # 126 Screenshot_30-8-2026_22261_.jpeg  -> Diesel cycle (P-V diagram)
    # 127 Screenshot_30-8-2026_222623_.jpeg -> Diffraction (narrow slit, broad slit)
    # 128 Screenshot_30-8-2026_222637_.jpeg -> Diffraction Grating
    # 129 Screenshot_30-8-2026_222647_.jpeg -> Diffused Reflection
    # 130 Screenshot_30-8-2026_22270_.jpeg  -> Digitate leaf
    # 131 Screenshot_30-8-2026_222711_.jpeg -> Chemical structure of Dihydroxysuccinic Acid (tartaric acid)
    # 132 Screenshot_30-8-2026_222727_.jpeg -> Chemical structure of Dimethyl Sulphoxide (DMSO)
    # 133 Screenshot_30-8-2026_222738_.jpeg -> Chemical structure of Dimethylformamide (DMF)
    # 134 Screenshot_30-8-2026_222746_.jpeg -> Chemical structure of Dimethylglyoxime
    # 135 Screenshot_30-8-2026_22282_.jpeg  -> Diode (p-n junction with symbol)

    terms_to_check = [
        "decagon", "decussate", "delocalization",
        "benzene resonance", "dehiscence",
        "deltahedron", "demodulator", "am demodulation",
        "density table", "dentate leaf", "dentate",
        "deltoid leaf", "deltoid",
        "dewar structure", "dewar benzene",
        "diagonal",
        "circulatory system",
        "diamond structure", "diamond",
        "deoxyribose",
        "diazepam",
        "circumscribed circle", "circumcircle",
        "diels-alder", "diels alder reaction",
        "dichasium", "dichasium cyme",
        "diesel cycle",
        "diffraction", "diffraction grating",
        "diffused reflection", "diffuse reflection",
        "digitate leaf", "digitate",
        "dihydroxysuccinic acid", "tartaric acid",
        "dimethyl sulphoxide", "dmso",
        "dimethylformamide", "dmf",
        "dimethylglyoxime",
        "diode"
    ]

    print("=== Checking Batch 9 Terms in dictionary.json ===")
    added = False
    for term in terms_to_check:
        if term.lower() in existing:
            print(f"  FOUND: {term}")
        else:
            print(f"  MISSING: {term} -> Searching PDF C...")
            res = find_in_pdf(pdf_c, term)
            if not res:
                res = find_in_pdf(pdf_d, term)
            if res:
                pg, block = res
                safe = block[:100].encode('ascii','replace').decode('ascii')
                print(f"    Found p.{pg}: {safe}...")
                dictionary[term.lower()] = block
                existing[term.lower()] = term.lower()
                added = True
            else:
                print(f"    Not found in PDF directly.")

    if added:
        print("\n=== Rebuilding dictionary & core_dictionary.js ===")
        sorted_d = dict(sorted(dictionary.items(), key=lambda x: x[0].lower()))
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(sorted_d, f, indent=2, ensure_ascii=False)
        import clean_and_enrich_formulas
        clean_and_enrich_formulas.process_dictionary(dict_path, dict_path, core_js)
        print("Rebuilt!")
    else:
        print("No new terms added.")

    images_to_process = [
        ("Screenshot_30-8-2026_22213_.jpeg",  "dict_decagon.png",                ["decagon"]),
        ("Screenshot_30-8-2026_222150_.jpeg", "dict_decussate.png",              ["decussate"]),
        ("Screenshot_30-8-2026_222214_.jpeg", "dict_delocalization.png",         ["delocalization"]),
        ("Screenshot_30-8-2026_222225_.jpeg", "dict_benzene_resonance.png",      ["benzene resonance"]),
        ("Screenshot_30-8-2026_22223_.jpeg",  "dict_dehiscence.png",             ["dehiscence"]),
        ("Screenshot_30-8-2026_222257_.jpeg", "dict_deltahedron.png",            ["deltahedron"]),
        ("Screenshot_30-8-2026_222323_.jpeg", "dict_demodulator.png",            ["demodulator", "am demodulation"]),
        ("Screenshot_30-8-2026_222342_.jpeg", "dict_density_table.png",          ["density table"]),
        ("Screenshot_30-8-2026_222354_.jpeg", "dict_dentate.png",                ["dentate", "dentate leaf"]),
        ("Screenshot_30-8-2026_22237_.jpeg",  "dict_deltoid_leaf.png",           ["deltoid", "deltoid leaf"]),
        ("Screenshot_30-8-2026_222423_.jpeg", "dict_dewar_structure.png",        ["dewar structure", "dewar benzene"]),
        ("Screenshot_30-8-2026_222435_.jpeg", "dict_diagonal.png",               ["diagonal"]),
        ("Screenshot_30-8-2026_22243_.jpeg",  "dict_circulatory_system.png",     ["circulatory system"]),
        ("Screenshot_30-8-2026_222449_.jpeg", "dict_diamond.png",                ["diamond", "diamond structure"]),
        ("Screenshot_30-8-2026_22244_.jpeg",  "dict_deoxyribose.png",            ["deoxyribose"]),
        ("Screenshot_30-8-2026_22250_.jpeg",  "dict_diazepam.png",               ["diazepam"]),
        ("Screenshot_30-8-2026_22254_.jpeg",  "dict_circumcircle.png",           ["circumcircle", "circumscribed circle"]),
        ("Screenshot_30-8-2026_222555_.jpeg", "dict_diels_alder.png",            ["diels-alder", "diels alder reaction"]),
        ("Screenshot_30-8-2026_22259_.jpeg",  "dict_dichasium.png",              ["dichasium", "dichasium cyme"]),
        ("Screenshot_30-8-2026_22261_.jpeg",  "dict_diesel_cycle.png",           ["diesel cycle"]),
        ("Screenshot_30-8-2026_222623_.jpeg", "dict_diffraction.png",            ["diffraction"]),
        ("Screenshot_30-8-2026_222637_.jpeg", "dict_diffraction_grating.png",    ["diffraction grating"]),
        ("Screenshot_30-8-2026_222647_.jpeg", "dict_diffuse_reflection.png",     ["diffused reflection", "diffuse reflection"]),
        ("Screenshot_30-8-2026_22270_.jpeg",  "dict_digitate_leaf.png",          ["digitate", "digitate leaf"]),
        ("Screenshot_30-8-2026_222711_.jpeg", "dict_tartaric_acid.png",          ["dihydroxysuccinic acid", "tartaric acid"]),
        ("Screenshot_30-8-2026_222727_.jpeg", "dict_dmso.png",                   ["dimethyl sulphoxide", "dmso"]),
        ("Screenshot_30-8-2026_222738_.jpeg", "dict_dimethylformamide.png",      ["dimethylformamide", "dmf"]),
        ("Screenshot_30-8-2026_222746_.jpeg", "dict_dimethylglyoxime.png",       ["dimethylglyoxime"]),
        ("Screenshot_30-8-2026_22282_.jpeg",  "dict_diode.png",                  ["diode"]),
    ]

    print("\n=== Saving Diagram Images (106-135) ===")
    os.makedirs('diagrams', exist_ok=True)
    for src, tgt, terms in images_to_process:
        sp = os.path.join('c-d didagrams', src)
        tp = os.path.join('diagrams', tgt)
        with Image.open(sp) as img:
            img.save(tp, 'PNG')
        print(f"  Saved {tgt}")

    print("\n=== Updating dictionary_diagrams_map.json ===")
    with open(map_path, 'r', encoding='utf-8') as f:
        diag_map = json.load(f)
    for src, tgt, terms in images_to_process:
        for t in terms:
            diag_map[t.lower()] = tgt
    sorted_map = dict(sorted(diag_map.items()))
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)
    with open('core_dictionary_diagrams.js', 'w', encoding='utf-8') as f:
        f.write("const DICTIONARY_DIAGRAMS = " + json.dumps(sorted_map, indent=2, ensure_ascii=False) + ";\n")
    print(f"Total mapped terms now: {len(sorted_map)}")
    print("Batch 9 integration complete!")

if __name__ == '__main__':
    main()
