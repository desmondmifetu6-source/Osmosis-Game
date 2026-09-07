import os
import json
import re
import fitz
from PIL import Image

_pdf_cache = {}

def get_pdf_pages(pdf_path):
    if pdf_path not in _pdf_cache:
        if not os.path.exists(pdf_path):
            _pdf_cache[pdf_path] = []
            return []
        print(f"  Caching text for {pdf_path}...", flush=True)
        doc = fitz.open(pdf_path)
        pages = []
        for i in range(len(doc)):
            text = doc[i].get_text()
            pages.append((i + 1, text, text.split("\n")))
        _pdf_cache[pdf_path] = pages
    return _pdf_cache[pdf_path]

def find_in_cached_pdf(pdf_path, term):
    pages = get_pdf_pages(pdf_path)
    pat = re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE)
    for pg, text, lines in pages:
        if term.lower() not in text.lower():
            continue
        for i, line in enumerate(lines):
            cl = line.strip()
            if pat.match(cl) or cl.lower() == term.lower():
                block = " ".join(l.strip() for l in lines[i:min(i+15, len(lines))] if l.strip())
                return (pg, block)
    return None

def main():
    dict_path = 'dictionary.json'
    map_path  = 'dictionary_diagrams_map.json'
    core_js   = 'core_dictionary.js'
    diag_js   = 'core_dictionary_diagrams.js'
    pdf_c     = r'split_sections/264_PDFsam_Dictionary Book 2.pdf'
    pdf_d     = r'split_sections/414_PDFsam_Dictionary Book 2.pdf'

    images_to_process = [
        ("Screenshot 2026-08-30 212430.png", "dict_chloroprene.png", ["chloroprene"]),
        ("Screenshot 2026-08-30 212906.png", "dict_caffeine.png", ["caffeine"]),
        ("Screenshot 2026-08-30 213001.png", "dict_calixarene.png", ["calixarene"]),
        ("Screenshot 2026-08-30 213059.png", "dict_vernier_callipers.png", ["vernier callipers", "vernier scale", "vernier"]),
        ("Screenshot 2026-08-30 213237.png", "dict_calorimeter.png", ["calorimeter", "specific heat capacity"]),
        ("Screenshot_30-8-2026_21517_.jpeg", "dict_castor_oil.png", ["castor oil", "ricinus communis"]),
        ("Screenshot_30-8-2026_21549_.jpeg", "dict_chalcone_co2.png", ["chalcone", "carbon dioxide"]),
        ("Screenshot_30-8-2026_22288_.jpeg", "dict_1_4_dioxane.png", ["1,4-dioxane", "dioxane"]),
        ("Screenshot_30-8-2026_222950_.jpeg", "dict_dibenzo_dioxin.png", ["dibenzo-1,4-dioxin", "dioxin", "2,3,7,8-tetrachlorodibenzodioxin"]),
        ("Screenshot_30-8-2026_222959_.jpeg", "dict_diphenylamine.png", ["diphenylamine"]),
        ("Screenshot_30-8-2026_223010_.jpeg", "dict_diphenylmethanone.png", ["diphenylmethanone", "benzophenone"]),
        ("Screenshot_30-8-2026_223044_.jpeg", "dict_dipolar_bond.png", ["dipolar bond"]),
        ("Screenshot_30-8-2026_223050_.jpeg", "dict_dipyridyl.png", ["dipyridyl", "bipyridine"]),
        ("Screenshot_30-8-2026_2230_.jpeg", "dict_cirrus_tendril.png", ["cirrus"]),
        ("Screenshot_30-8-2026_223135_.jpeg", "dict_disjoint_sets.png", ["disjoint sets"]),
        ("Screenshot_30-8-2026_22313_.jpeg", "dict_dc_motor.png", ["dc motor", "direct current motor"]),
        ("Screenshot_30-8-2026_223142_.jpeg", "dict_dispersion_prism.png", ["dispersion", "optical dispersion"]),
        ("Screenshot_30-8-2026_223159_.jpeg", "dict_distal_convoluted_tubule.png", ["distal convoluted tubule"]),
        ("Screenshot_30-8-2026_22318_.jpeg", "dict_citric_acid.png", ["citric acid"]),
        ("Screenshot_30-8-2026_223219_.jpeg", "dict_dodecagon.png", ["dodecagon"]),
        ("Screenshot_30-8-2026_223231_.jpeg", "dict_dodecylbenzene.png", ["dodecylbenzene"]),
        ("Screenshot_30-8-2026_223246_.jpeg", "dict_dopamine.png", ["dopamine"]),
        ("Screenshot_30-8-2026_22328_.jpeg", "dict_claisen_condensation.png", ["claisen condensation"]),
        ("Screenshot_30-8-2026_223349_.jpeg", "dict_doppler_effect.png", ["doppler effect"]),
        ("Screenshot_30-8-2026_223410_.jpeg", "dict_down_feather.png", ["down feather"]),
        ("Screenshot_30-8-2026_22341_.jpeg", "dict_clasping_leaf.png", ["clasping leaf", "amplexicaul"]),
        ("Screenshot_30-8-2026_223423_.jpeg", "dict_drift_speed.png", ["drift speed", "drift velocity"]),
        ("Screenshot_30-8-2026_223437_.jpeg", "dict_dumas_method.png", ["dumas' method", "dumas method"]),
        ("Screenshot_30-8-2026_22357_.jpeg", "dict_clavate_leaf.png", ["clavate", "clavate leaf"]),
        ("Screenshot_30-8-2026_2238_.jpeg", "dict_cisplatin.png", ["cisplatin"]),
        ("Screenshot_30-8-2026_22427_.jpeg", "dict_cluster_cellular.png", ["cluster"]),
        ("Screenshot_30-8-2026_22441_.jpeg", "dict_cochlea.png", ["cochlea"]),
        ("Screenshot_30-8-2026_22449_.jpeg", "dict_cocaine.png", ["cocaine"]),
        ("Screenshot_30-8-2026_2248_.jpeg", "dict_cleft_leaf.png", ["cleft", "cleft leaf"]),
        ("Screenshot_30-8-2026_22512_.jpeg", "dict_codeine.png", ["codeine"]),
        ("Screenshot_30-8-2026_2251_.jpeg", "dict_cockroach.png", ["cockroach", "periplaneta americana"]),
        ("Screenshot_30-8-2026_22537_.jpeg", "dict_colchicine.png", ["colchicine"]),
        ("Screenshot_30-8-2026_22549_.jpeg", "dict_coleorhiza.png", ["coleorhiza"]),
        ("Screenshot_30-8-2026_22619_.jpeg", "dict_component_vector.png", ["component vector", "vector resolution"]),
        ("Screenshot_30-8-2026_22630_.jpeg", "dict_compound_microscope.png", ["compound microscope"]),
        ("Screenshot_30-8-2026_22642_.jpeg", "dict_compound_leaf_types.png", ["compound leaf", "pinnate", "bipinnate"]),
        ("Screenshot_30-8-2026_22658_.jpeg", "dict_compression_rarefaction.png", ["compression", "rarefaction"]),
        ("Screenshot_30-8-2026_2266_.jpeg", "dict_complete_graph.png", ["complete graph"]),
        ("Screenshot_30-8-2026_22716_.jpeg", "dict_concavity.png", ["concavity", "concave function"]),
        ("Screenshot_30-8-2026_22744_.jpeg", "dict_connate_perfoliate.png", ["connate-perfoliate", "connate"]),
        ("Screenshot_30-8-2026_22752_.jpeg", "dict_consecutive_angles.png", ["consecutive angles", "consecutive interior angles"]),
        ("Screenshot_30-8-2026_2279_.jpeg", "dict_concave_polygon.png", ["concave polygon"]),
        ("Screenshot_30-8-2026_22818_.jpeg", "dict_propanone.png", ["propanone", "acetone"]),
        ("Screenshot_30-8-2026_22828_.jpeg", "dict_constructive_interference.png", ["constructive interference"]),
        ("Screenshot_30-8-2026_22845_.jpeg", "dict_contour_feather.png", ["contour feather"]),
        ("Screenshot_30-8-2026_2288_.jpeg", "dict_propanal.png", ["propanal"]),
        ("Screenshot_30-8-2026_22914_.jpeg", "dict_corm_cocoyam.png", ["corm", "cocoyam", "colocasia esculenta"]),
        ("Screenshot_30-8-2026_22923_.jpeg", "dict_corniculate.png", ["corniculate"]),
        ("Screenshot_30-8-2026_22931_.jpeg", "dict_coroniform.png", ["coroniform"]),
        ("Screenshot_30-8-2026_2293_.jpeg", "dict_coordination_isomers.png", ["coordination isomerism", "geometric isomerism"]),
        ("Screenshot_30-8-2026_22942_.jpeg", "dict_corresponding_angles.png", ["corresponding angles"]),
        ("Screenshot_30-8-2026_22951_.jpeg", "dict_cortisol.png", ["cortisol"]),
    ]

    print(f"=== STEP 1: Saving {len(images_to_process)} Diagram Images to diagrams/ ===", flush=True)
    os.makedirs('diagrams', exist_ok=True)
    for src_name, tgt_name, terms in images_to_process:
        sp = os.path.join('c-d didagrams', src_name)
        tp = os.path.join('diagrams', tgt_name)
        if os.path.exists(sp):
            with Image.open(sp) as img:
                img.save(tp, 'PNG')
            print(f"  Saved {tgt_name}", flush=True)

    print("\n=== STEP 2: Checking dictionary.json for Missing Terms ===", flush=True)
    with open(dict_path, 'r', encoding='utf-8') as f:
        dictionary = json.load(f)

    existing_words = set()
    for letter, items in dictionary.items():
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict) and item.get('word'):
                    existing_words.add(item['word'].lower().strip())
                    for syn in item.get('synonyms', []):
                        existing_words.add(syn.lower().strip())

    terms_to_check = []
    for _, _, terms in images_to_process:
        for t in terms:
            if t.lower() not in terms_to_check:
                terms_to_check.append(t.lower())

    added_count = 0
    for term in terms_to_check:
        if term in existing_words:
            print(f"  FOUND: {term}", flush=True)
        else:
            print(f"  MISSING: {term} -> Searching PDF...", flush=True)
            res = find_in_cached_pdf(pdf_c, term)
            if not res:
                res = find_in_cached_pdf(pdf_d, term)
            if res:
                pg, block = res
                first_char = term[0].upper() if term[0].isalpha() else '1'
                if first_char not in dictionary:
                    dictionary[first_char] = []

                synonyms = []
                m = re.match(r'^[A-Za-z0-9\s,\-\.]+\s*\(([^)]+)\)', block[:120])
                if m:
                    syn_str = m.group(1)
                    synonyms = [s.strip().lower() for s in syn_str.split(';') if s.strip()]

                entry = {
                    "word": term,
                    "raw_headword": term.upper(),
                    "synonyms": synonyms,
                    "definition": block.strip()
                }
                dictionary[first_char].append(entry)
                existing_words.add(term)
                added_count += 1
                safe_s = block[:60].encode('ascii', 'replace').decode('ascii')
                print(f"    Added '{term}' p.{pg}: {safe_s}...", flush=True)
            else:
                print(f"    Not found in PDF directly.", flush=True)

    if added_count > 0:
        print(f"\nAdded {added_count} new entries to dictionary.json.", flush=True)
        for letter in dictionary:
            if isinstance(dictionary[letter], list):
                dictionary[letter].sort(key=lambda x: x.get('word', '').lower() if isinstance(x, dict) else str(x).lower())
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, indent=2, ensure_ascii=False)

    print("\n=== STEP 3: Updating dictionary_diagrams_map.json ===", flush=True)
    with open(map_path, 'r', encoding='utf-8') as f:
        diag_map = json.load(f)

    for _, tgt_name, terms in images_to_process:
        val = f"diagrams/{tgt_name}"
        for t in terms:
            diag_map[t.lower().strip()] = val

    sorted_map = dict(sorted(diag_map.items()))
    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)
    print(f"Total entries in dictionary_diagrams_map.json: {len(sorted_map)}", flush=True)

    print("\n=== STEP 4: Regenerating core_dictionary_diagrams.js ===", flush=True)
    json_str = json.dumps(sorted_map, indent=2, ensure_ascii=False)
    js_content = f"""// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)

const DictionaryDiagrams = {json_str};

if (typeof window !== 'undefined') {{
  window.DictionaryDiagrams = DictionaryDiagrams;
  window.DICTIONARY_DIAGRAMS = DictionaryDiagrams;
}}
if (typeof module !== 'undefined') {{
  module.exports = DictionaryDiagrams;
}}
"""
    with open(diag_js, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Saved {diag_js}", flush=True)

    print("\n=== STEP 5: Rebuilding core_dictionary.js index ===", flush=True)
    import sys
    sys.path.append('scripts')
    import clean_and_enrich_formulas
    clean_and_enrich_formulas.process_dictionary(dict_path, dict_path, core_js)
    print("\n=== COMPLETE! ===", flush=True)

if __name__ == '__main__':
    main()
