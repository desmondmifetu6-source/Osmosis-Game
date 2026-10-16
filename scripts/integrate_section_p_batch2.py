"""
integrate_section_p_batch2.py
==============================
Precision cropping, high-resolution generation, and dual-map integration
for Section P Batch 2 (Screenshots 51 through 85 of 'p_diagrams/').

Replaces bad/miscropped vector-extracted images with pristine, complete-label captures.
Updates:
  - diagrams/dict_*.png
  - dictionary_diagrams_map.json
  - core_dictionary_diagrams.js
  - DIAGRAM_BATCH_MAPPING_GUIDE.md

Run from the project root:
  python scripts/integrate_section_p_batch2.py
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
    # SPECIFICATIONS (Screenshots 51 through 85)
    # Each entry: (source_screenshot, [ (out_filename, crop_box, [dict_terms], caption) ])
    # ---------------------------------------------------------------
    specifications = [
        # 51: Phenolphthalein
        ("Screenshot_29-9-2026_153954_.jpeg", [
            ("dict_phenolphthalein.png", None,
             ["phenolphthalein", "ph indicator phenolphthalein", "phenolphthalein indicator"],
             "Chemical Structure of Phenolphthalein")
        ]),

        # 52: Phenothiazine
        ("Screenshot_29-9-2026_154013_.jpeg", [
            ("dict_phenothiazine.png", None,
             ["phenothiazine", "thiodiphenylamine", "dibenzothiazine"],
             "Chemical Structure of Phenothiazine")
        ]),

        # 53: Phenylhydrazine
        ("Screenshot_29-9-2026_154023_.jpeg", [
            ("dict_phenylhydrazine.png", None,
             ["phenylhydrazine", "hydrazinobenzene"],
             "Chemical Structure of Phenylhydrazine")
        ]),

        # 54: Phenyl Methyl Ketone (Acetophenone)
        ("Screenshot_29-9-2026_154033_.jpeg", [
            ("dict_acetophenone.png", None,
             ["phenyl methyl ketone", "acetophenone", "methyl phenyl ketone", "acetylbenzene"],
             "Chemical Structure of Phenyl Methyl Ketone")
        ]),

        # 55: Phenylthiocarbamide
        ("Screenshot_29-9-2026_154043_.jpeg", [
            ("dict_phenylthiocarbamide.png", None,
             ["phenylthiocarbamide", "ptc", "phenylthiourea"],
             "Chemical Structure of Phenylthiocarbamide")
        ]),

        # 56: Phenylethene (Styrene)
        ("Screenshot_29-9-2026_15405_.jpeg", [
            ("dict_styrene.png", None,
             ["phenylethene", "styrene", "vinylbenzene", "ethenylbenzene"],
             "Chemical Structure of Phenylethene")
        ]),

        # 57: Phosphoglycerate
        ("Screenshot_29-9-2026_154112_.jpeg", [
            ("dict_phosphoglycerate.png", None,
             ["phosphoglycerate", "3-phosphoglycerate", "3-phosphoglyceric acid", "pga"],
             "Chemical Structure of Phosphoglycerate")
        ]),

        # 58: Phosphodiester Bond
        ("Screenshot_29-9-2026_15414_.jpeg", [
            ("dict_phosphodiester_bond.png", None,
             ["phosphodiester bond", "phosphodiester linkage", "phosphodiester"],
             "Phosphodiester Bond")
        ]),

        # 59: Photovoltaic cell
        ("Screenshot_29-9-2026_154150_.jpeg", [
            ("dict_photovoltaic_cell.png", None,
             ["photovoltaic cell", "solar cell", "photovoltaic effect"],
             "Photovoltaic cell")
        ]),

        # 60: Phthalocyanine
        ("Screenshot_29-9-2026_15420_.jpeg", [
            ("dict_phthalocyanine.png", None,
             ["phthalocyanine", "tetrabenzoporphyrazine"],
             "Chemical Structure of Phthalocyanine")
        ]),

        # 61: Phthalic Acid
        ("Screenshot_29-9-2026_154210_.jpeg", [
            ("dict_phthalic_acid.png", None,
             ["phthalic acid", "benzene-1,2-dicarboxylic acid", "o-phthalic acid"],
             "Chemical Structure of Phthalic Acid")
        ]),

        # 62: SI Derived Units
        ("Screenshot_29-9-2026_154228_.jpeg", [
            ("dict_si_derived_units.png", None,
             ["si derived units", "derived units", "units and symbols", "derived physical quantities"],
             "Physical Quantities, Symbols, and Units (Part 2)")
        ]),

        # 63: Types of physical topologies
        ("Screenshot_29-9-2026_154240_.jpeg", [
            ("dict_physical_topologies.png", None,
             ["types of physical topologies", "network topology", "physical topology",
              "bus topology", "ring topology", "star topology", "mesh topology", "tree topology"],
             "Types of physical topologies")
        ]),

        # 64: Physical Quantities & Base Units
        ("Screenshot_29-9-2026_154248_.jpeg", [
            ("dict_physical_quantities.png", None,
             ["physical quantities", "physical quantity", "base physical quantities"],
             "Physical Quantity, Symbol, and Unit (Part 1)")
        ]),

        # 65: Picoline isomers
        ("Screenshot_29-9-2026_154259_.jpeg", [
            ("dict_picoline.png", None,
             ["picoline", "methylpyridine", "alpha-picoline", "beta-picoline", "gamma-picoline",
              "2-methylpyridine", "3-methylpyridine", "4-methylpyridine"],
             "Picoline isomers")
        ]),

        # 66: Pi Molecular Orbital
        ("Screenshot_29-9-2026_154312_.jpeg", [
            ("dict_pi_molecular_orbital.png", None,
             ["pi molecular orbital", "pi orbital", "pi bond formation"],
             "Pi Molecular Orbital")
        ]),

        # 67: Picric Acid
        ("Screenshot_29-9-2026_154323_.jpeg", [
            ("dict_picric_acid.png", None,
             ["picric acid", "2,4,6-trinitrophenol", "tnp"],
             "Chemical Structure of Picric Acid")
        ]),

        # 68: External features of a pig
        ("Screenshot_29-9-2026_154340_.jpeg", [
            ("dict_pig_external_features.png", None,
             ["external features of a pig", "pig anatomy", "swine", "pig external features"],
             "External features of a pig")
        ]),

        # 69: Pie Chart
        ("Screenshot_29-9-2026_154348_.jpeg", [
            ("dict_pie_chart.png", None,
             ["pie chart", "pie graph", "circle chart"],
             "Pie Chart")
        ]),

        # 70: Pi Bond
        ("Screenshot_29-9-2026_15436_.jpeg", [
            ("dict_pi_bond.png", None,
             ["pi bond", "pi bonding", "double bond pi component"],
             "Pi Bond")
        ]),

        # 71: Pinnipalmate leaf
        ("Screenshot_29-9-2026_154410_.jpeg", [
            ("dict_pinnipalmate.png", None,
             ["pinnipalmate", "pinnipalmate leaf", "pinnipalmate venation"],
             "Pinnipalmate leaf")
        ]),

        # 72: Pinnule
        ("Screenshot_29-9-2026_154418_.jpeg", [
            ("dict_pinnule.png", None,
             ["pinnule", "pinnules", "fern pinnule"],
             "Pinnule")
        ]),

        # 73: Pinhole Camera
        ("Screenshot_29-9-2026_154424_.jpeg", [
            ("dict_pinhole_camera.png", None,
             ["pinhole camera", "pinhole camera image formation", "camera obscura"],
             "Pinhole Camera")
        ]),

        # 74: Pinnatilobate leaf
        ("Screenshot_29-9-2026_15442_.jpeg", [
            ("dict_pinnatilobate.png", None,
             ["pinnatilobate", "pinnatilobate leaf", "pinnately lobed"],
             "Pinnatilobate leaf")
        ]),

        # 75: Odd-pinnate & Even-pinnate leaves (Split)
        ("Screenshot_29-9-2026_154434_.jpeg", [
            ("dict_odd_pinnate.png", (0.0, 0.0, 0.52, 1.0),
             ["odd-pinnate", "imparipinnate", "odd-pinnate leaf", "imparipinnate leaf"],
             "Odd-pinnate leaf"),
            ("dict_even_pinnate.png", (0.48, 0.0, 1.0, 1.0),
             ["even-pinnate", "paripinnate leaf even", "even pinnate leaf"],
             "Even-pinnate leaf"),
        ]),

        # 76: Piperidine
        ("Screenshot_29-9-2026_154441_.jpeg", [
            ("dict_piperidine.png", None,
             ["piperidine", "hexahydropyridine", "azacyclohexane"],
             "Chemical Structure of Piperidine")
        ]),

        # 77: Pistil of a flower
        ("Screenshot_29-9-2026_154448_.jpeg", [
            ("dict_pistil.png", None,
             ["pistil", "pistil of a flower", "carpel", "stigma style ovary"],
             "A section of the pistil of a flower")
        ]),

        # 78: Pit of a fruit or drupe
        ("Screenshot_29-9-2026_154459_.jpeg", [
            ("dict_pit.png", None,
             ["pit", "pit of a fruit", "pit (botany)", "stone of a fruit", "pit (drupe)", "drupe pit"],
             "Pit of a fruit or drupe")
        ]),

        # 79: Plastoquinone
        ("Screenshot_29-9-2026_154532_.jpeg", [
            ("dict_plastoquinone.png", None,
             ["plastoquinone", "pq", "plastoquinone structure"],
             "Chemical Structure of Plastoquinone")
        ]),

        # 80: Pleiochasium cyme
        ("Screenshot_29-9-2026_154546_.jpeg", [
            ("dict_pleiochasium.png", None,
             ["pleiochasium", "pleiochasium cyme", "pleiochaxial cyme", "polychasium"],
             "Pleiochasium cyme")
        ]),

        # 81: Placenta (plants)
        ("Screenshot_29-9-2026_15458_.jpeg", [
            ("dict_placenta_plants.png", None,
             ["placenta (plants)", "plant placenta", "placentation placenta"],
             "Placenta (plants)")
        ]),

        # 82: Plicate flower
        ("Screenshot_29-9-2026_15463_.jpeg", [
            ("dict_plicate_flower.png", None,
             ["plicate flower", "plicate", "plicate corolla"],
             "Plicate flower")
        ]),

        # 83: Polarization Angle (Brewster's Angle)
        ("Screenshot_29-9-2026_154726_.jpeg", [
            ("dict_brewsters_angle.png", None,
             ["polarization angle", "brewster's angle", "brewsters angle", "polarisation angle", "brewster angle"],
             "Polarization Angle (Brewster's Angle)")
        ]),

        # 84: Point of inflection
        ("Screenshot_29-9-2026_15472_.jpeg", [
            ("dict_point_of_inflection.png", None,
             ["point of inflection", "inflection point", "points of inflection"],
             "Point of inflection")
        ]),

        # 85: Polarimeter
        ("Screenshot_29-9-2026_154736_.jpeg", [
            ("dict_polarimeter.png", None,
             ["polarimeter", "polarimetry", "optical rotation"],
             "Polarimeter")
        ]),
    ]

    print("=" * 60)
    print("STEP 1: Generating diagram PNGs from screenshots (Section P Batch 2: 51-85)")
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

    new_section = f"\n\n---\n\n### Section P Series: Batch 2 (Completed) — Screenshots 51 to 85\n"
    new_section += f"Source Folder: `p_diagrams/` (September 29, 2026 Pristine Author Captures)\n\n"
    new_section += f"| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |\n"
    new_section += f"|---|---|---|---|---|\n"

    for i, rec in enumerate(batch_records, 51):
        new_section += f"| {i} | `{rec['src']}` | {rec['desc']} | {rec['targets']} | {rec['terms']} |\n"

    if "### Section P Series: Batch 2" not in guide_content:
        guide_content += new_section
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print(f"Appended Section P Batch 2 table to {guide_path}")
    else:
        print(f"Section P Batch 2 already in {guide_path}")

    print("\n" + "=" * 60)
    print(f"SUCCESS: Generated {generated_count} diagrams, mapped {mapped_terms_count} terms!")
    print("=" * 60)

if __name__ == "__main__":
    main()
