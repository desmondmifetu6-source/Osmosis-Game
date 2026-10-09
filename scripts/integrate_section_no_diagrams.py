"""
integrate_section_no_diagrams.py
================================
Precision cropping, high-resolution generation, and dual-map integration
for all 60 user-captured screenshots in 'n-o diagrams/' (September 28 captures).

Replaces bad vector-extracted images with pristine, complete-label captures.
Updates:
  - diagrams/dict_*.png
  - dictionary_diagrams_map.json
  - core_dictionary_diagrams.js
  - DIAGRAM_BATCH_MAPPING_GUIDE.md
"""
import os
import json
from PIL import Image

def clean_crop(img, box=None):
    """
    Crops an image. If box is None, trims extreme borders if needed.
    box format: (left, top, right, bottom) in pixels or relative (0.0 - 1.0).
    """
    w, h = img.size
    if box:
        left, top, right, bottom = box
        if isinstance(left, float):
            box = (int(left * w), int(top * h), int(right * w), int(bottom * h))
        return img.crop(box)
    return img

def main():
    src_dir = "n-o diagrams"
    out_dir = "diagrams"
    map_json_path = "dictionary_diagrams_map.json"
    diag_js_path = "core_dictionary_diagrams.js"
    guide_path = "DIAGRAM_BATCH_MAPPING_GUIDE.md"

    os.makedirs(out_dir, exist_ok=True)

    # Specification list:
    # Each entry: (source_filename, [(target_filename, crop_box_or_None, [mapped_terms], caption_desc)])
    specifications = [
        # 1: Paracetamol
        ("Screenshot_28-9-2026_172012_.jpeg", [
            ("dict_paracetamol.png", None, ["paracetamol", "acetaminophen", "4-acetamidophenol"], "Chemical Structure of Paracetamol")
        ]),
        # 2: 1-Naphthol & 2-Naphthol
        ("Screenshot_28-9-2026_172019_.jpeg", [
            ("dict_naphthol.png", None, ["naphthol", "1-naphthol", "2-naphthol", "naphthols"], "1-Naphthol and 2-Naphthol")
        ]),
        # 3: Naphthalene
        ("Screenshot_28-9-2026_172027_.jpeg", [
            ("dict_naphthalene.png", None, ["naphthalene", "chemical formula of naphthalene"], "Chemical formula of Naphthalene")
        ]),
        # 4: Nephroid leaf
        ("Screenshot_28-9-2026_172123_.jpeg", [
            ("dict_nephroid.png", None, ["nephroid", "nephroid leaf"], "Nephroid leaf")
        ]),
        # 5: Nephron
        ("Screenshot_28-9-2026_172133_.jpeg", [
            ("dict_nephron.png", None, ["nephron", "renal tubule", "bowman's capsule", "glomerulus"], "Nephron (labelled anatomy)")
        ]),
        # 6: Nephron (alternate clean capture)
        ("Screenshot_28-9-2026_172143_.jpeg", [
            ("dict_nephron_structure.png", None, ["nephron structure", "loop of henle"], "Nephron structure and tubules")
        ]),
        # 7: Human nervous system
        ("Screenshot_28-9-2026_172155_.jpeg", [
            ("dict_nervous_system.png", None, ["nervous system", "human nervous system", "central nervous system", "spinal cord"], "Human nervous system")
        ]),
        # 8: Net force
        ("Screenshot_28-9-2026_172226_.jpeg", [
            ("dict_net_force.png", None, ["net force", "resultant force"], "Net force of forces acting on an object")
        ]),
        # 9: von Neumann Architecture
        ("Screenshot_28-9-2026_172245_.jpeg", [
            ("dict_von_neumann_architecture.png", None, ["von neumann architecture", "computer architecture", "neumann", "von neumann"], "von Neumann's Computer Architecture")
        ]),
        # 10: Newton's Law of Cooling
        ("Screenshot_28-9-2026_172328_.jpeg", [
            ("dict_newtons_law_of_cooling.png", None, ["newton's law of cooling", "newtons law of cooling", "law of cooling"], "Newton's Law of Cooling (Temperature vs Time)")
        ]),
        # 11: Niacin
        ("Screenshot_28-9-2026_172349_.jpeg", [
            ("dict_niacin.png", None, ["niacin", "nicotinic acid", "vitamin b3"], "Chemical structure of Niacin")
        ]),
        # 12: Neutral points
        ("Screenshot_28-9-2026_17236_.jpeg", [
            ("dict_neutral_points.png", None, ["neutral point", "neutral points", "magnetic neutral points"], "Neutral points (magnetic field lines)")
        ]),
        # 13: Ninhydrin
        ("Screenshot_28-9-2026_172419_.jpeg", [
            ("dict_ninhydrin.png", None, ["ninhydrin", "2,2-dihydroxyindane-1,3-dione"], "Chemical Structure of Ninhydrin")
        ]),
        # 14: Nitrogen cycle
        ("Screenshot_28-9-2026_172445_.jpeg", [
            ("dict_nitrogen_cycle.png", None, ["nitrogen cycle", "nitrogen fixation", "nitrification"], "The nitrogen cycle")
        ]),
        # 15: Nicotine
        ("Screenshot_28-9-2026_17244_.jpeg", [
            ("dict_nicotine.png", None, ["nicotine"], "Chemical Structure of Nicotine")
        ]),
        # 16: Noradrenaline
        ("Screenshot_28-9-2026_172543_.jpeg", [
            ("dict_noradrenaline.png", None, ["noradrenaline", "norepinephrine"], "Chemical Structure of Noradrenaline")
        ]),
        # 17: Decibel scale / Noise pollution
        ("Screenshot_28-9-2026_17254_.jpeg", [
            ("dict_decibel_scale_noise.png", None, ["noise", "noise pollution", "decibel", "decibel scale"], "Decibel scale of sounds (Noise pollution)")
        ]),
        # 18: Normal Curve
        ("Screenshot_28-9-2026_17266_.jpeg", [
            ("dict_normal_curve.png", None, ["normal curve", "normal distribution", "gaussian distribution", "bell curve"], "Normal Curve (Scores vs Frequency)")
        ]),
        # 19: NOT truth table
        ("Screenshot_28-9-2026_172751_.jpeg", [
            ("dict_not_truth_table.png", None, ["not", "not operation", "inverter table"], "A truth table describing the operation of NOT")
        ]),
        # 20: Nucellus
        ("Screenshot_28-9-2026_172813_.jpeg", [
            ("dict_nucellus.png", None, ["nucellus", "megasporocyte", "integument", "micropyle"], "Nucellus (botanical ovule cross-section)")
        ]),
        # 21: NOT gate symbol
        ("Screenshot_28-9-2026_17282_.jpeg", [
            ("dict_not_gate.png", None, ["not gate", "inverter", "not circuit"], "Not gate symbol and truth table")
        ]),
        # 22: Nuclear reactor
        ("Screenshot_28-9-2026_172840_.jpeg", [
            ("dict_nuclear_reactor.png", None, ["nuclear reactor", "moderator", "control rods", "fuel rods"], "Nuclear reactor (labelled cross-section)")
        ]),
        # 23: 3-oxobutanoic Acid
        ("Screenshot_28-9-2026_172916_.jpeg", [
            ("dict_3_oxobutanoic_acid.png", None, ["3-oxobutanoic acid", "acetoacetic acid", "oxoacid"], "Chemical Structure of 3-oxobutanoic Acid")
        ]),
        # 24: Number line
        ("Screenshot_28-9-2026_17291_.jpeg", [
            ("dict_number_line.png", None, ["number line", "real line"], "Number line")
        ]),
        # 25: Obcordate leaf & Obcordate fruit (split)
        ("Screenshot_28-9-2026_172940_.jpeg", [
            ("dict_obcordate_leaf.png", (0.0, 0.0, 1.0, 0.50), ["obcordate", "obcordate leaf"], "Obcordate leaf"),
            ("dict_obcordate_fruit.png", (0.0, 0.50, 1.0, 1.0), ["obcordate fruit"], "Obcordate fruit")
        ]),
        # 26: Obdeltoid leaf
        ("Screenshot_28-9-2026_172949_.jpeg", [
            ("dict_obdeltoid.png", None, ["obdeltoid", "obdeltoid leaf"], "Obdeltoid leaf")
        ]),
        # 27: Oblique leaf base
        ("Screenshot_28-9-2026_173055_.jpeg", [
            ("dict_oblique_leaf_base.png", None, ["oblique leaf base", "oblique leaf"], "Oblique leaf base")
        ]),
        # 28: Oblanceolate leaf
        ("Screenshot_28-9-2026_173134_.jpeg", [
            ("dict_oblanceolate.png", None, ["oblanceolate", "oblancelate", "oblanceolate leaf"], "Oblanceolate leaf")
        ]),
        # 29: Oblique Triangle
        ("Screenshot_28-9-2026_17313_.jpeg", [
            ("dict_oblique_triangle.png", None, ["oblique triangle", "oblique"], "Oblique Triangle")
        ]),
        # 30: Obovate leaf
        ("Screenshot_28-9-2026_173215_.jpeg", [
            ("dict_obovate.png", None, ["obovate", "obovate leaf"], "Obovate leaf")
        ]),
        # 31: Obtuse leaf
        ("Screenshot_28-9-2026_173226_.jpeg", [
            ("dict_obtuse_leaf.png", None, ["obtuse leaf", "obtuse apex"], "Obtuse leaf")
        ]),
        # 32: Ocreate structure (Ochrea)
        ("Screenshot_28-9-2026_173239_.jpeg", [
            ("dict_ocrea.png", None, ["ocrea", "ochrea", "ocreate structure"], "Ocreate structure (ocrea / ochrea)")
        ]),
        # 33: Oblong Leaf
        ("Screenshot_28-9-2026_17323_.jpeg", [
            ("dict_oblong_leaf.png", None, ["oblong", "oblong leaf"], "Oblong Leaf")
        ]),
        # 34: Oestrogens (Oestradiol, Oestrone, Oestriol)
        ("Screenshot_28-9-2026_17330_.jpeg", [
            ("dict_oestrogen.png", None, ["oestrogen", "estrogen", "oestradiol", "estradiol", "oestrone", "estrone", "oestriol"], "Oestrogen structures (Oestradiol, Oestrone, Oestriol)")
        ]),
        # 35: Ogive
        ("Screenshot_28-9-2026_173712_.jpeg", [
            ("dict_ogive.png", None, ["ogive", "cumulative frequency curve", "cumulative frequency"], "Ogive (cumulative frequency curve)")
        ]),
        # 36: Okro pod
        ("Screenshot_28-9-2026_173812_.jpeg", [
            ("dict_okro.png", None, ["okro", "okra", "lady's finger", "gumbo"], "Okro pod (cross-section & vertical splits)")
        ]),
        # 37: Olecranon Process
        ("Screenshot_28-9-2026_173824_.jpeg", [
            ("dict_olecranon_process.png", None, ["olecranon process", "olecranon", "ulna"], "Olecranon Process (elbow joint anatomy)")
        ]),
        # 38: Omasum of a cow
        ("Screenshot_28-9-2026_173839_.jpeg", [
            ("dict_omasum.png", None, ["omasum", "manyplies", "psalterium", "ruminant stomach"], "Omasum of a cow (ruminant digestive tract)")
        ]),
        # 39: Operational amplifiers (Non-inverting & Inverting)
        ("Screenshot_28-9-2026_173926_.jpeg", [
            ("dict_operational_amplifier.png", None, ["operational amplifier", "op-amp", "non-inverting amplifier", "inverting amplifier"], "Operational amplifiers (inverting & non-inverting)")
        ]),
        # 40: Onion bulb section
        ("Screenshot_28-9-2026_17393_.jpeg", [
            ("dict_onion.png", None, ["onion", "tunicated bulb", "bulb"], "Longitudinal section of onion (tunicated bulb)")
        ]),
        # 41: alpha-Neoendorphin
        ("Screenshot_28-9-2026_173941_.jpeg", [
            ("dict_neoendorphin.png", None, ["neoendorphin", "alpha-neoendorphin", "endorphin"], "Chemical structure of alpha-Neoendorphin")
        ]),
        # 42: Optical fibre
        ("Screenshot_28-9-2026_173959_.jpeg", [
            ("dict_optical_fibre.png", None, ["optical fibre", "optical fiber", "total internal reflection", "core cladding"], "Optical fibre (laser light path and cladding)")
        ]),
        # 43: Optical Isomerism
        ("Screenshot_28-9-2026_174012_.jpeg", [
            ("dict_optical_isomerism.png", None, ["optical isomerism", "enantiomers", "chiral", "chirality"], "Optical Isomerism (non-superimposable mirror images)")
        ]),
        # 44: Optical pyrometer
        ("Screenshot_28-9-2026_174018_.jpeg", [
            ("dict_optical_pyrometer.png", None, ["optical pyrometer", "pyrometer"], "Optical pyrometer (apparatus diagram)")
        ]),
        # 45: OR truth table
        ("Screenshot_28-9-2026_174032_.jpeg", [
            ("dict_or_gate.png", None, ["or", "or gate", "or circuit", "disjunction"], "The operation of OR illustrated by the truth table")
        ]),
        # 46: Orange, Citrus spp.
        ("Screenshot_28-9-2026_174059_.jpeg", [
            ("dict_orange.png", None, ["orange", "citrus", "hesperidium"], "Orange, Citrus spp. (morphology & cross-section)")
        ]),
        # 47: S-orbital & P-orbital
        ("Screenshot_28-9-2026_174120_.jpeg", [
            ("dict_atomic_orbitals.png", None, ["orbital", "atomic orbital", "s-orbital", "p-orbital"], "S-orbital and P-orbital electron density shapes")
        ]),
        # 48: Orgel diagrams
        ("Screenshot_28-9-2026_174137_.jpeg", [
            ("dict_orgel_diagrams.png", None, ["orgel diagrams", "orgel diagram"], "Orgel diagrams (D, F and P energy state splitting)")
        ]),
        # 49: Orbicular Leaf
        ("Screenshot_28-9-2026_17418_.jpeg", [
            ("dict_orbicular_leaf.png", None, ["orbicular", "orbicular leaf"], "Orbicular Leaf")
        ]),
        # 50: Orthogonal circles
        ("Screenshot_28-9-2026_17420_.jpeg", [
            ("dict_orthogonal_circles.png", None, ["orthogonal", "orthogonal circles"], "Orthogonal circles")
        ]),
        # 51: Osmosis experiment
        ("Screenshot_28-9-2026_174246_.jpeg", [
            ("dict_osmosis_experiment.png", None, ["osmosis", "osmosis experiment", "semi-permeable membrane"], "An experimental set up to show the process of osmosis")
        ]),
        # 52: Ovate leaf
        ("Screenshot_28-9-2026_174320_.jpeg", [
            ("dict_ovate_leaf.png", None, ["ovate", "ovate leaf"], "Ovate leaf")
        ]),
        # 53: Otto cycle
        ("Screenshot_28-9-2026_17432_.jpeg", [
            ("dict_otto_cycle.png", None, ["otto cycle", "otto engine", "four-stroke cycle", "four stroke engine"], "Otto cycle (P-V indicator diagram)")
        ]),
        # 54: Oxalic acid
        ("Screenshot_28-9-2026_174338_.jpeg", [
            ("dict_oxalic_acid.png", None, ["oxalic acid", "ethanedioic acid"], "Chemical Structure of oxalic acid (ethanedioic acid)")
        ]),
        # 55: Oxazole
        ("Screenshot_28-9-2026_174410_.jpeg", [
            ("dict_oxazole.png", None, ["oxazole", "1,3-oxazole"], "Chemical structure of Oxazole")
        ]),
        # 56: Oxoanion examples (Sulphuric acid / Sodium bisulphite)
        ("Screenshot_28-9-2026_174444_.jpeg", [
            ("dict_oxoanion.png", None, ["oxoanion", "oxyanion", "sulphate", "sulphite"], "Chemical Structure of oxoanions (sulphate and sulphite)")
        ]),
        # 57: Oxoacid (Sulphuric acid) & Oxycodone
        ("Screenshot_28-9-2026_174456_.jpeg", [
            ("dict_oxoacid.png", (0.0, 0.0, 1.0, 0.49), ["oxoacid", "oxoacids", "sulphuric acid"], "Chemical Structure of sulphuric acid (an example of oxoacid)"),
            ("dict_oxycodone.png", (0.0, 0.49, 1.0, 1.0), ["oxycodone"], "Chemical structure of Oxycodone")
        ]),
        # 58: Ozone
        ("Screenshot_28-9-2026_174522_.jpeg", [
            ("dict_ozone.png", None, ["ozone", "trioxygen"], "Chemical structure of Ozone (bond length & angle)")
        ]),
        # 59: Ozonolysis
        ("Screenshot_28-9-2026_174534_.jpeg", [
            ("dict_ozonolysis.png", None, ["ozonolysis", "ozonide"], "Generalised reaction scheme of Ozonolysis")
        ]),
        # 60: Production of Oxygen gas
        ("Screenshot_28-9-2026_17457_.jpeg", [
            ("dict_oxygen_production.png", None, ["oxygen", "preparation of oxygen", "oxygen gas"], "The production of Oxygen gas (laboratory preparation)")
        ]),
    ]

    print(f"Processing {len(specifications)} screenshot specifications...")

    # Load existing map
    with open(map_json_path, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    processed_count = 0
    mapped_terms_count = 0
    batch_records = []

    for src_file, targets in specifications:
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print(f"WARNING: Source file {src_path} not found!")
            continue

        orig_img = Image.open(src_path)
        w, h = orig_img.size

        out_files = []
        all_terms = []
        caption_descs = []

        for tgt_file, box, terms, desc in targets:
            out_path = os.path.join(out_dir, tgt_file)
            cropped = clean_crop(orig_img, box)
            
            # Save in crisp PNG format
            cropped.save(out_path, format="PNG", optimize=True)
            processed_count += 1
            out_files.append(tgt_file)
            caption_descs.append(desc)

            # Update mapping
            rel_val = f"diagrams/{tgt_file}"
            for term in terms:
                term_clean = term.lower().strip()
                diag_map[term_clean] = rel_val
                mapped_terms_count += 1
                all_terms.append(f"`{term_clean}`")

        batch_records.append({
            "src": src_file,
            "desc": " / ".join(caption_descs),
            "targets": ", ".join(f"`{f}`" for f in out_files),
            "terms": ", ".join(all_terms[:8])
        })

    # Save sorted dictionary_diagrams_map.json
    sorted_map = dict(sorted(diag_map.items()))
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)
    print(f"Updated {map_json_path} (Total mapped terms: {len(sorted_map)})")

    # Regenerate core_dictionary_diagrams.js
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
    with open(diag_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Saved {diag_js_path}")

    # Append to DIAGRAM_BATCH_MAPPING_GUIDE.md
    with open(guide_path, "r", encoding="utf-8") as f:
        guide_content = f.read()

    new_section = f"\n\n---\n\n### Section N & O Series: Batch 1 (Completed) — Screenshots 1 to 60\n"
    new_section += f"Source Folder: `n-o diagrams/` (September 28, 2026 Pristine Author Captures)\n\n"
    new_section += f"| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |\n"
    new_section += f"|---|---|---|---|---|\n"

    for i, rec in enumerate(batch_records, 1):
        new_section += f"| {i} | `{rec['src']}` | {rec['desc']} | {rec['targets']} | {rec['terms']} |\n"

    # Avoid duplicate section if already present
    if "### Section N & O Series: Batch 1" not in guide_content:
        guide_content += new_section
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print(f"Appended Section N & O batch table to {guide_path}")
    else:
        print(f"Section N & O batch already in {guide_path}")

    print(f"\nSUCCESS: Generated {processed_count} diagrams, mapped {mapped_terms_count} terms!")

if __name__ == "__main__":
    main()
