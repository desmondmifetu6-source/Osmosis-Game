import os
import sys
import json
import re
import fitz  # PyMuPDF
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
    dict_path   = 'dictionary.json'
    map_path    = 'dictionary_diagrams_map.json'
    core_js     = 'core_dictionary.js'
    pdf_c       = r'split_sections/264_PDFsam_Dictionary Book 2.pdf'

    with open(dict_path, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)
    existing = {k.lower(): k for k in dictionary.keys()}

    # Vision inspection results:
    # 66  Screenshot_30-8-2026_221148_.jpeg -> Flower of a Crotalaria (standard petal, wing petal, sepals)
    # 67  Screenshot_30-8-2026_22115_.jpeg  -> Chemical structure of Creatine
    # 68  Screenshot_30-8-2026_221254_.jpeg -> Crown Ethers (18-crown-6-ether)
    # 69  Screenshot_30-8-2026_221317_.jpeg -> Cube (3D, length labelled)
    # 70  Screenshot_30-8-2026_22131_.jpeg  -> Cruciform flower shape
    # 71  Screenshot_30-8-2026_221326_.jpeg -> Cubic function graph (y=x^3)
    # 72  Screenshot_30-8-2026_221339_.jpeg -> Cuboid
    # 73  Screenshot_30-8-2026_221348_.jpeg -> Curine & Tubocurarine structures
    # 74  Screenshot_30-8-2026_221357_.jpeg -> Curve on the Cartesian plane
    # 75  Screenshot_30-8-2026_221414_.jpeg -> Curved surface of a sphere
    # 76  Screenshot_30-8-2026_221428_.jpeg -> Cusp of a leaf
    # 77  Screenshot_30-8-2026_221438_.jpeg -> Cyanuric acid chemical structure
    # 78  Screenshot_30-8-2026_221444_.jpeg -> Cyathium inflorescence
    # 79  Screenshot_30-8-2026_221456_.jpeg -> Cyclic Adenosine Monophosphate (cAMP)
    # 80  Screenshot_30-8-2026_221521_.jpeg -> Cyclic polygon
    # 81  Screenshot_30-8-2026_221539_.jpeg -> Cyclic polygon & cyclic quadrilateral examples
    # 82  Screenshot_30-8-2026_221546_.jpeg -> Cyclohexadiene-1,4-dione (benzoquinone/quinone) structure
    # 83  Screenshot_30-8-2026_221552_.jpeg -> Cycloid drawn on Cartesian plane
    # 84  Screenshot_30-8-2026_22159_.jpeg  -> Cyclamate chemical structure
    # 85  Screenshot_30-8-2026_221613_.jpeg -> Cyclotron (magnetic field perpendicular to plane)

    terms_to_check = [
        "crotalaria", "creatine", "crown ethers", "crown ether",
        "cube", "cruciform", "cubic function",
        "cuboid", "curine", "tubocurarine",
        "curve", "curved surface", "cusp",
        "cyanuric acid", "cyathium",
        "cyclic adenosine monophosphate", "camp",
        "cyclic polygon", "cyclic quadrilateral",
        "cyclohexadiene", "benzoquinone", "quinone",
        "cycloid", "cyclamate", "cyclotron"
    ]

    print("=== Checking Batch 7 Terms in dictionary.json ===")
    added = False
    for term in terms_to_check:
        if term.lower() in existing:
            print(f"  FOUND: {term}")
        else:
            print(f"  MISSING: {term} -> Searching PDF...")
            res = find_in_pdf(pdf_c, term)
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
        ("Screenshot_30-8-2026_221148_.jpeg", "dict_crotalaria.png",          ["crotalaria"]),
        ("Screenshot_30-8-2026_22115_.jpeg",  "dict_creatine.png",            ["creatine"]),
        ("Screenshot_30-8-2026_221254_.jpeg", "dict_crown_ether.png",         ["crown ethers", "crown ether"]),
        ("Screenshot_30-8-2026_221317_.jpeg", "dict_cube.png",                ["cube"]),
        ("Screenshot_30-8-2026_22131_.jpeg",  "dict_cruciform.png",           ["cruciform"]),
        ("Screenshot_30-8-2026_221326_.jpeg", "dict_cubic_function.png",      ["cubic function"]),
        ("Screenshot_30-8-2026_221339_.jpeg", "dict_cuboid.png",              ["cuboid"]),
        ("Screenshot_30-8-2026_221348_.jpeg", "dict_curine.png",              ["curine", "tubocurarine"]),
        ("Screenshot_30-8-2026_221357_.jpeg", "dict_curve_cartesian.png",     ["curve"]),
        ("Screenshot_30-8-2026_221414_.jpeg", "dict_curved_surface_sphere.png", ["curved surface"]),
        ("Screenshot_30-8-2026_221428_.jpeg", "dict_cusp_leaf.png",           ["cusp"]),
        ("Screenshot_30-8-2026_221438_.jpeg", "dict_cyanuric_acid.png",       ["cyanuric acid"]),
        ("Screenshot_30-8-2026_221444_.jpeg", "dict_cyathium.png",            ["cyathium"]),
        ("Screenshot_30-8-2026_221456_.jpeg", "dict_camp.png",                ["cyclic adenosine monophosphate", "camp"]),
        ("Screenshot_30-8-2026_221521_.jpeg", "dict_cyclic_polygon.png",      ["cyclic polygon"]),
        ("Screenshot_30-8-2026_221539_.jpeg", "dict_cyclic_quadrilateral.png",["cyclic quadrilateral"]),
        ("Screenshot_30-8-2026_221546_.jpeg", "dict_benzoquinone.png",        ["cyclohexadiene", "benzoquinone", "quinone"]),
        ("Screenshot_30-8-2026_221552_.jpeg", "dict_cycloid.png",             ["cycloid"]),
        ("Screenshot_30-8-2026_22159_.jpeg",  "dict_cyclamate.png",           ["cyclamate"]),
        ("Screenshot_30-8-2026_221613_.jpeg", "dict_cyclotron.png",           ["cyclotron"]),
    ]

    print("\n=== Saving Diagram Images (66-85) ===")
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
    print("Batch 7 integration complete!")

if __name__ == '__main__':
    main()
