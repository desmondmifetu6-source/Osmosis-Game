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

    # Vision inspection results (images 86–105):
    # 86  Screenshot_30-8-2026_221633_.jpeg -> Chemical structure of Cyclonite (RDX explosive)
    # 87  Screenshot_30-8-2026_221642_.jpeg -> Structure of Cyclopentadiene
    # 88  Screenshot_30-8-2026_22164_.jpeg  -> Structure of Cyclopropane
    # 89  Screenshot_30-8-2026_221655_.jpeg -> Cylinder (radius, height)
    # 90  Screenshot_30-8-2026_221713_.jpeg -> Cylindrical coordinates of a right-angled triangle
    # 91  Screenshot_30-8-2026_22173_.jpeg  -> Chemical structure of Cysteine (amino acid)
    # 92  Screenshot_30-8-2026_221757_.jpeg -> Chemical structure of 1,2-Diaminoethane (Ethylenediamine)
    # 93  Screenshot_30-8-2026_221813_.jpeg -> Chemical structure of 1,6-Diaminohexane (Hexamethylenediamine)
    # 94  Screenshot_30-8-2026_221824_.jpeg -> Chemical structure of 1,2-Dibromoethane
    # 95  Screenshot_30-8-2026_221830_.jpeg -> Chemical structure of 1,2-Dihydroxybenzene
    # 96  Screenshot_30-8-2026_221842_.jpeg -> The Daniell Cell (electrochemistry, zinc anode, copper cathode, salt bridge)
    # 97  Screenshot_30-8-2026_221849_.jpeg -> Various degrees of Damping (critically, over, under)
    # 98  Screenshot_30-8-2026_22185_.jpeg  -> Chemical structure of 1,3-Dihydroxybenzene
    # 99  Screenshot_30-8-2026_221915_.jpeg -> Chemical structure of DDT (Dichlorodiphenyltrichloroethane)
    # 100 Screenshot_30-8-2026_222015_.jpeg -> Chemical structure of Decanedioic Acid
    # 101 Screenshot_30-8-2026_22201_.jpeg  -> Trans-decalin & Cis-decalin structures
    # 102 Screenshot_30-8-2026_222112_.jpeg -> Decarboxylation reaction mechanism
    # 103 Screenshot_30-8-2026_222118_.jpeg -> Radioactive decay curve (half-life T1/2)
    # 104 Screenshot_30-8-2026_222130_.jpeg -> Decompound leaves
    # 105 Screenshot_30-8-2026_222138_.jpeg -> Decurrent leaves

    terms_to_check = [
        "cyclonite", "cyclopentadiene", "cyclopropane",
        "cylinder", "cylindrical coordinates",
        "cysteine", "ethylenediamine", "1,2-diaminoethane",
        "hexamethylenediamine", "1,6-diaminohexane",
        "1,2-dibromoethane", "dibromoethane",
        "1,2-dihydroxybenzene", "catechol",
        "daniell cell", "damping",
        "1,3-dihydroxybenzene", "resorcinol",
        "ddt", "dichlorodiphenyltrichloroethane",
        "decanedioic acid", "sebacic acid",
        "decalin", "trans-decalin", "cis-decalin",
        "decarboxylation",
        "radioactive decay", "decay curve",
        "decompound leaf", "decompound",
        "decurrent leaf", "decurrent"
    ]

    print("=== Checking Batch 8 Terms in dictionary.json ===")
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
        ("Screenshot_30-8-2026_221633_.jpeg", "dict_cyclonite.png",                ["cyclonite"]),
        ("Screenshot_30-8-2026_221642_.jpeg", "dict_cyclopentadiene.png",           ["cyclopentadiene"]),
        ("Screenshot_30-8-2026_22164_.jpeg",  "dict_cyclopropane.png",              ["cyclopropane"]),
        ("Screenshot_30-8-2026_221655_.jpeg", "dict_cylinder.png",                  ["cylinder"]),
        ("Screenshot_30-8-2026_221713_.jpeg", "dict_cylindrical_coordinates.png",   ["cylindrical coordinates"]),
        ("Screenshot_30-8-2026_22173_.jpeg",  "dict_cysteine.png",                  ["cysteine"]),
        ("Screenshot_30-8-2026_221757_.jpeg", "dict_ethylenediamine.png",           ["ethylenediamine", "1,2-diaminoethane"]),
        ("Screenshot_30-8-2026_221813_.jpeg", "dict_hexamethylenediamine.png",      ["hexamethylenediamine", "1,6-diaminohexane"]),
        ("Screenshot_30-8-2026_221824_.jpeg", "dict_dibromoethane.png",             ["1,2-dibromoethane", "dibromoethane"]),
        ("Screenshot_30-8-2026_221830_.jpeg", "dict_catechol.png",                  ["1,2-dihydroxybenzene", "catechol"]),
        ("Screenshot_30-8-2026_221842_.jpeg", "dict_daniell_cell.png",              ["daniell cell"]),
        ("Screenshot_30-8-2026_221849_.jpeg", "dict_damping.png",                   ["damping"]),
        ("Screenshot_30-8-2026_22185_.jpeg",  "dict_resorcinol.png",                ["1,3-dihydroxybenzene", "resorcinol"]),
        ("Screenshot_30-8-2026_221915_.jpeg", "dict_ddt.png",                       ["ddt", "dichlorodiphenyltrichloroethane"]),
        ("Screenshot_30-8-2026_222015_.jpeg", "dict_decanedioic_acid.png",          ["decanedioic acid", "sebacic acid"]),
        ("Screenshot_30-8-2026_22201_.jpeg",  "dict_decalin.png",                   ["decalin", "trans-decalin", "cis-decalin"]),
        ("Screenshot_30-8-2026_222112_.jpeg", "dict_decarboxylation.png",           ["decarboxylation"]),
        ("Screenshot_30-8-2026_222118_.jpeg", "dict_decay_curve.png",               ["radioactive decay", "decay curve"]),
        ("Screenshot_30-8-2026_222130_.jpeg", "dict_decompound_leaf.png",           ["decompound", "decompound leaf"]),
        ("Screenshot_30-8-2026_222138_.jpeg", "dict_decurrent_leaf.png",            ["decurrent", "decurrent leaf"]),
    ]

    print("\n=== Saving Diagram Images (86-105) ===")
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
    print("Batch 8 integration complete!")

if __name__ == '__main__':
    main()
