"""
integrate_section_p_diagrams.py
================================
Precision cropping, high-resolution generation, and dual-map integration
for user-captured screenshots in 'p_diagrams/' (Section P of Dictionary).

Replaces bad/miscropped vector-extracted images with pristine, complete-label captures.
Updates:
  - diagrams/dict_*.png
  - dictionary_diagrams_map.json
  - core_dictionary_diagrams.js
  - DIAGRAM_BATCH_MAPPING_GUIDE.md

Run from the project root:
  python scripts/integrate_section_p_diagrams.py
"""
import os
import sys
import json
from PIL import Image

# Ensure stdout handles utf-8 on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def clean_crop(img, box=None):
    """
    Crops an image.
    box format: (left, top, right, bottom) in pixels or relative (0.0 - 1.0).
    If box is None, returns the original image unchanged.
    """
    if box is None:
        return img
    w, h = img.size
    left, top, right, bottom = box
    if isinstance(left, float):
        box = (int(left * w), int(top * h), int(right * w), int(bottom * h))
    return img.crop(box)

def main():
    src_dir  = "p_diagrams"
    out_dir  = "diagrams"
    map_json_path = "dictionary_diagrams_map.json"
    diag_js_path  = "core_dictionary_diagrams.js"
    guide_path    = "DIAGRAM_BATCH_MAPPING_GUIDE.md"

    os.makedirs(out_dir, exist_ok=True)

    # ---------------------------------------------------------------
    # SPECIFICATIONS (Images 1 through 50)
    # Each entry: (source_screenshot, [ (out_filename, crop_box, [dict_terms], caption) ])
    # ---------------------------------------------------------------
    specifications = [
        # 1: 3-Phosphoglyceraldehyde
        ("Screenshot_29-9-2026_152717_.jpeg", [
            ("dict_3_phosphoglyceraldehyde.png", None,
             ["3-phosphoglyceraldehyde", "glyceraldehyde-3-phosphate", "g3p",
              "3-phospho-d-glyceraldehyde"],
             "Chemical Structure of 3-Phosphoglyceraldehyde")
        ]),

        # 2: Paleolate / Lodicule
        ("Screenshot_29-9-2026_152738_.jpeg", [
            ("dict_paleolate.png", None,
             ["paleolate", "lodicule", "paleola", "lodicules"],
             "Paleolate (Lodicule)")
        ]),

        # 3: Palmately-lobed simple leaf & Palmate compound leaf
        ("Screenshot_29-9-2026_152747_.jpeg", [
            ("dict_palmately_lobed_leaf.png", (0.0, 0.0, 0.52, 1.0),
             ["palmately lobed", "palmately-lobed leaf", "palmatifid",
              "palmately lobed leaf"],
             "Palmately-lobed, simple leaf"),
            ("dict_palmate_compound_leaf.png", (0.48, 0.0, 1.0, 1.0),
             ["palmate", "palmate leaf", "palmate compound leaf",
              "palmately compound leaf", "digitate leaf"],
             "Palmate compound leaf"),
        ]),

        # 4: Palmatisect leaf
        ("Screenshot_29-9-2026_152752_.jpeg", [
            ("dict_palmatisect.png", None,
             ["palmatisect", "palmatisect leaf", "palmatisect venation"],
             "Palmatisect leaf")
        ]),

        # 5: Voltage-current characteristic of p-n junction
        ("Screenshot_29-9-2026_15279_.jpeg", [
            ("dict_pn_junction.png", None,
             ["p-n junction", "pn junction", "p-n junction diode",
              "junction diode", "semiconductor diode",
              "voltage-current characteristic of p-n junction"],
             "Voltage-current characteristic of p-n junction")
        ]),

        # 6: Pandurate leaf
        ("Screenshot_29-9-2026_15280_.jpeg", [
            ("dict_pandurate_leaf.png", None,
             ["pandurate", "pandurate leaf", "panduriform",
              "panduriform leaf"],
             "Pandurate leaf")
        ]),

        # 7: Pantothenic Acid
        ("Screenshot_29-9-2026_152816_.jpeg", [
            ("dict_pantothenic_acid.png", None,
             ["pantothenic acid", "vitamin b5", "pantothenate",
              "pantothenate (vitamin b5)"],
             "Chemical Structure of Pantothenic Acid")
        ]),

        # 8: Papilionaceous corolla
        ("Screenshot_29-9-2026_152825_.jpeg", [
            ("dict_papilionaceous.png", None,
             ["papilionaceous", "papilionaceous corolla",
              "butterfly flower", "papilionate", "papilionaceus"],
             "Papilionaceous corolla")
        ]),

        # 9: Parabolic reflection
        ("Screenshot_29-9-2026_152832_.jpeg", [
            ("dict_parabolic_reflection.png", None,
             ["parabolic reflection", "parabolic dish",
              "parabolic reflector", "parabola (optics)"],
             "Parabolic reflection")
        ]),

        # 10: Parallax Error
        ("Screenshot_29-9-2026_152843_.jpeg", [
            ("dict_parallax_error.png", None,
             ["parallax error", "parallax", "parallax (measurement)"],
             "Parallax Error")
        ]),

        # 11: Paraldehyde
        ("Screenshot_29-9-2026_152850_.jpeg", [
            ("dict_paraldehyde.png", None,
             ["paraldehyde", "2,4,6-trimethyl-1,3,5-trioxane",
              "para-acetaldehyde"],
             "Chemical Structure of Paraldehyde")
        ]),

        # 12: Parallel Circuit
        ("Screenshot_29-9-2026_152856_.jpeg", [
            ("dict_parallel_circuit.png", None,
             ["parallel circuit", "parallel connection",
              "resistors in parallel", "parallel combination"],
             "Parallel Circuit")
        ]),

        # 13: Panicle inflorescence
        ("Screenshot_29-9-2026_15288_.jpeg", [
            ("dict_panicle.png", None,
             ["panicle", "panicle inflorescence", "paniculate",
              "paniculate inflorescence"],
             "Panicle inflorescence")
        ]),

        # 14: Parallelodromous leaf
        ("Screenshot_29-9-2026_152915_.jpeg", [
            ("dict_parallelodromous_leaf.png", None,
             ["parallelodromous", "parallelodromous leaf",
              "parallel venation", "parallel-veined leaf",
              "parelleldromous"],
             "Parallelodromous leaf")
        ]),

        # 15: Parallelogram of vectors
        ("Screenshot_29-9-2026_152922_.jpeg", [
            ("dict_parallelogram_of_vectors.png", None,
             ["parallelogram of vectors", "parallelogram law of vectors",
              "parallelogram law", "parallelogram rule"],
             "Parallelogram of vectors")
        ]),

        # 16: Parallelogram
        ("Screenshot_29-9-2026_152931_.jpeg", [
            ("dict_parallelogram.png", None,
             ["parallelogram", "parallelogram (shape)",
              "height of a parallelogram"],
             "Parallelogram")
        ]),

        # 17: Paramecium
        ("Screenshot_29-9-2026_152939_.jpeg", [
            ("dict_paramecium.png", None,
             ["paramecium", "paramecia", "slipper animalcule",
              "paramecium caudatum", "ciliophora"],
             "Paramecium")
        ]),

        # 18: Ectoparasites
        ("Screenshot_29-9-2026_152947_.jpeg", [
            ("dict_ectoparasite.png", None,
             ["ectoparasite", "ectoparasites", "louse", "tick",
              "tsetse fly", "tsetsefly", "external parasite"],
             "Ectoparasites (louse, tick, tsetsefly)")
        ]),

        # 19: Parathion
        ("Screenshot_29-9-2026_152955_.jpeg", [
            ("dict_parathion.png", None,
             ["parathion", "o,o-diethyl o-(4-nitrophenyl) phosphorothioate",
              "parathion-ethyl"],
             "Chemical Structure of Parathion")
        ]),

        # 20: Parallelogram of forces
        ("Screenshot_29-9-2026_15297_.jpeg", [
            ("dict_parallelogram_of_forces.png", None,
             ["parallelogram of forces", "parallelogram law of forces",
              "resultant force parallelogram"],
             "Parallelogram of forces")
        ]),

        # 21: Paripinnate leaves
        ("Screenshot_29-9-2026_153010_.jpeg", [
            ("dict_paripinnate_leaf.png", None,
             ["paripinnate", "paripinnate leaf", "even-pinnate",
              "even pinnate", "abruptly pinnate"],
             "Paripinnate leaves")
        ]),

        # 22: Parking Orbit
        ("Screenshot_29-9-2026_153020_.jpeg", [
            ("dict_parking_orbit.png", None,
             ["parking orbit", "geostationary orbit", "transfer orbit",
              "low earth orbit", "geosynchronous transfer orbit"],
             "Parking Orbit")
        ]),

        # 23: Parted leaf
        ("Screenshot_29-9-2026_153027_.jpeg", [
            ("dict_parted_leaf.png", None,
             ["parted", "parted leaf", "partite leaf", "partite"],
             "Parted leaf")
        ]),

        # 24: Parietal placentation
        ("Screenshot_29-9-2026_15303_.jpeg", [
            ("dict_parietal_placentation.png", None,
             ["parietal placentation", "parietal", "placentation",
              "parietal structure", "ovule placentation"],
             "Parietal structure (placentation)")
        ]),

        # 25: Pascal's Triangle
        ("Screenshot_29-9-2026_153052_.jpeg", [
            ("dict_pascals_triangle.png", None,
             ["pascal's triangle", "pascals triangle",
              "binomial coefficients", "pascal triangle"],
             "Pascal's Triangle")
        ]),

        # 26: Pectoral girdle
        ("Screenshot_29-9-2026_153129_.jpeg", [
            ("dict_pectoral_girdle.png", None,
             ["pectoral girdle", "shoulder girdle",
              "pectoral limb girdle", "scapula", "glenoid cavity",
              "pectoral girdle of a mammal"],
             "Pectoral girdle")
        ]),

        # 27: Peltate leaf
        ("Screenshot_29-9-2026_153141_.jpeg", [
            ("dict_peltate_leaf.png", None,
             ["peltate", "peltate leaf", "shield-shaped leaf"],
             "Peltate leaf")
        ]),

        # 28: Pelvic girdle
        ("Screenshot_29-9-2026_153155_.jpeg", [
            ("dict_pelvic_girdle.png", None,
             ["pelvic girdle", "pelvic limb girdle", "ilium", "ischium",
              "pubis", "acetabulum", "hip bone", "os coxae",
              "mammalian pelvic girdle", "pubic symphysis"],
             "A mammalian pelvic girdle")
        ]),

        # 29: Pedate leaves
        ("Screenshot_29-9-2026_15317_.jpeg", [
            ("dict_pedate_leaf.png", None,
             ["pedate", "pedate leaf", "pedate venation",
              "pedately compound"],
             "Pedate leaves")
        ]),

        # 30: Pentaerythritol
        ("Screenshot_29-9-2026_153222_.jpeg", [
            ("dict_pentaerythritol.png", None,
             ["pentaerythritol", "2,2-bis(hydroxymethyl)-1,3-propanediol",
              "tetramethylolmethane"],
             "Chemical Structure of Pentaerythritol")
        ]),

        # 31: Pentaerythritol Tetranitrate (PETN)
        ("Screenshot_29-9-2026_153229_.jpeg", [
            ("dict_pentaerythritol_tetranitrate.png", None,
             ["pentaerythritol tetranitrate", "petn", "pentrite"],
             "Structural formula of Pentaerythritol Tetranitrate")
        ]),

        # 32: Pentagon
        ("Screenshot_29-9-2026_153239_.jpeg", [
            ("dict_pentagon.png", None,
             ["pentagon", "regular pentagon", "pentagonal",
              "five-sided polygon"],
             "Pentagon")
        ]),

        # 33: Peptide Bond
        ("Screenshot_29-9-2026_153256_.jpeg", [
            ("dict_peptide_bond.png", None,
             ["peptide bond", "peptide linkage", "peptide",
              "dipeptide", "formation of peptide bond"],
             "Formation of peptide bond")
        ]),

        # 34: Penicillin
        ("Screenshot_29-9-2026_15327_.jpeg", [
            ("dict_penicillin.png", None,
             ["penicillin", "penicillin g", "benzylpenicillin",
              "beta-lactam", "beta-lactam antibiotic"],
             "Structural formula of Penicillin")
        ]),

        # 35: Perfoliate leaf
        ("Screenshot_29-9-2026_153310_.jpeg", [
            ("dict_perfoliate_leaf.png", None,
             ["perfoliate", "perfoliate leaf", "perfoliatum"],
             "Perfoliate leaf")
        ]),

        # 36: Pericyclic Reaction
        ("Screenshot_29-9-2026_153325_.jpeg", [
            ("dict_pericyclic_reaction.png", None,
             ["pericyclic reaction", "pericyclic reactions",
              "cycloaddition", "electrocyclic reaction", "sigmatropic reaction"],
             "Pericyclic Reaction")
        ]),

        # 37: Periodic Functions
        ("Screenshot_29-9-2026_153356_.jpeg", [
            ("dict_tangent_periodic_function.png", (0.0, 0.0, 1.0, 0.54),
             ["tangent periodic function", "tangent function"],
             "Tangent Periodic Function"),
            ("dict_sine_cosine_periodic_function.png", (0.0, 0.53, 1.0, 1.0),
             ["sine and cosine periodic functions", "sine function", "cosine function",
              "periodic functions", "periodic function"],
             "Sine and Cosine Periodic Functions")
        ]),

        # 38: Periodic Table of the Elements
        ("Screenshot_29-9-2026_153626_.jpeg", [
            ("dict_periodic_table.png", None,
             ["periodic table", "periodic table of the elements",
              "mendeleev periodic table", "elements"],
             "Periodic Table of the Elements")
        ]),

        # 39: Periscope
        ("Screenshot_29-9-2026_153645_.jpeg", [
            ("dict_periscope.png", None,
             ["periscope", "prism periscope", "reflection in periscope"],
             "Periscope")
        ]),

        # 40: Peristalsis of bolus in the oesophagus
        ("Screenshot_29-9-2026_15370_.jpeg", [
            ("dict_peristalsis.png", None,
             ["peristalsis", "peristaltic movement", "bolus", "oesophagus"],
             "Peristalsis of bolus in the oesophagus")
        ]),

        # 41: Examples of permanent magnet moving-coil instrument
        ("Screenshot_29-9-2026_153727_.jpeg", [
            ("dict_moving_coil_instrument.png", None,
             ["permanent magnet moving-coil instrument", "moving-coil galvanometer",
              "moving coil galvanometer", "galvanometer"],
             "Examples of permanent magnet moving-coil instrument")
        ]),

        # 42: Peroxide Ion
        ("Screenshot_29-9-2026_153742_.jpeg", [
            ("dict_peroxide_ion.png", None,
             ["peroxide ion", "peroxide", "peroxides", "o2 2-"],
             "Chemical Structure of Peroxide Ion")
        ]),

        # 43: Peroxymonosulfuric Acid
        ("Screenshot_29-9-2026_153750_.jpeg", [
            ("dict_peroxymonosulfuric_acid.png", None,
             ["peroxymonosulfuric acid", "caro's acid", "persulfuric acid"],
             "Chemical Structure of Peroxymonosulfuric Acid")
        ]),

        # 44: Perpendicular distance
        ("Screenshot_29-9-2026_153758_.jpeg", [
            ("dict_perpendicular_distance.png", None,
             ["perpendicular distance", "perpendicular", "shortest distance to a line"],
             "Perpendicular distance")
        ]),

        # 45: Personate structure
        ("Screenshot_29-9-2026_153813_.jpeg", [
            ("dict_personate.png", None,
             ["personate", "personate corolla", "personate structure"],
             "Personate structure")
        ]),

        # 46: Petiole
        ("Screenshot_29-9-2026_153830_.jpeg", [
            ("dict_petiole.png", None,
             ["petiole", "leaf stalk", "petiolate"],
             "Petiole")
        ]),

        # 47: Phase Diagram
        ("Screenshot_29-9-2026_153854_.jpeg", [
            ("dict_phase_diagram.png", None,
             ["phase diagram", "phases of matter", "phase transitions",
              "triple point", "critical point"],
             "Phase Diagram - Phases of Matter and Phase Transitions")
        ]),

        # 48: Phase difference of two waves
        ("Screenshot_29-9-2026_153910_.jpeg", [
            ("dict_phase_difference.png", None,
             ["phase difference", "phase difference of two waves",
              "phase angle", "out of phase"],
             "Phase difference of two waves")
        ]),

        # 49: Phenol / Phenolic acid
        ("Screenshot_29-9-2026_153927_.jpeg", [
            ("dict_phenol.png", None,
             ["phenol", "phenolic acid", "carbolic acid", "hydroxybenzene"],
             "Chemical Structure of phenol or phenolic acid")
        ]),

        # 50: Phencyclidine
        ("Screenshot_29-9-2026_153939_.jpeg", [
            ("dict_phencyclidine.png", None,
             ["phencyclidine", "pcp", "phenylcyclohexyl piperidine"],
             "Chemical Structure of Phencyclidine")
        ]),
    ]

    print("=" * 60)
    print("STEP 1: Generating diagram PNGs from screenshots (Section P Batch 1)")
    print("=" * 60)

    # Load existing dictionary_diagrams_map.json
    with open(map_json_path, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    batch_records = []
    generated_count = 0
    mapped_terms_count = 0

    for src_file, outputs in specifications:
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print(f"[MISSING] {src_path}")
            continue

        try:
            img = Image.open(src_path).convert("RGB")
        except Exception as e:
            print(f"[ERROR] Could not open {src_path}: {e}")
            continue

        out_files = []
        caption_descs = []
        all_terms = []

        for out_name, crop_box, terms, caption in outputs:
            out_path = os.path.join(out_dir, out_name)
            cropped = clean_crop(img, crop_box)
            cropped.save(out_path, "PNG", quality=95)
            generated_count += 1
            out_files.append(out_name)
            caption_descs.append(caption)

            rel_path = f"diagrams/{out_name}"
            for term in terms:
                key = term.lower().strip()
                diag_map[key] = rel_path
                all_terms.append(term)
                mapped_terms_count += 1

            print(f"  [OK] Saved {out_name} -> {caption}")

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
    print(f"\nUpdated {map_json_path} (Total mapped terms: {len(sorted_map)})")

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

    new_section = f"\n\n---\n\n### Section P Series: Batch 1 (Completed) — Screenshots 1 to 50\n"
    new_section += f"Source Folder: `p_diagrams/` (September 29, 2026 Pristine Author Captures)\n\n"
    new_section += f"| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |\n"
    new_section += f"|---|---|---|---|---|\n"

    for i, rec in enumerate(batch_records, 1):
        new_section += f"| {i} | `{rec['src']}` | {rec['desc']} | {rec['targets']} | {rec['terms']} |\n"

    if "### Section P Series: Batch 1" not in guide_content:
        guide_content += new_section
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print(f"Appended Section P batch table to {guide_path}")
    else:
        print(f"Section P batch already in {guide_path}")

    print("\n" + "=" * 60)
    print(f"SUCCESS: Generated {generated_count} diagrams, mapped {mapped_terms_count} terms!")
    print("=" * 60)

if __name__ == "__main__":
    main()
