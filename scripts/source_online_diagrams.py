"""
source_online_diagrams.py
=========================
Sources high-quality labeled educational diagrams from Wikimedia Commons
for dictionary terms that have:
  (a) bad/corrupt extracted diagrams (extreme aspect ratios)
  (b) no diagram at all but are important STEM concepts

Downloads images into diagrams/ and updates dictionary_diagrams_map.json
and regenerates core_dictionary_diagrams.js.

Run from final_osmosis/:
    python scripts/source_online_diagrams.py
"""

import os, json, sys, time, re
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

DIAGRAMS_DIR = "diagrams"
MAP_JSON     = "dictionary_diagrams_map.json"
DIAGRAMS_JS  = "core_dictionary_diagrams.js"

# ─────────────────────────────────────────────────────────────────────────────
# Master catalog: term → Wikimedia Commons direct download URL
# All images are freely licensed (CC-BY-SA / Public Domain) labeled diagrams.
# Grouped by: BAD_ASPECT (replacing corrupt crops) and MISSING (adding new ones)
# ─────────────────────────────────────────────────────────────────────────────
DIAGRAM_SOURCES = {

    # ── BAD ASPECT RATIO REPLACEMENTS ───────────────────────────────────────

    "bell jar": (
        "diagrams/dict_bell_jar.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Bell_jar.svg/400px-Bell_jar.svg.png"
    ),
    "ammeter": (
        "diagrams/dict_ammeter.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Galvanometer.png/320px-Galvanometer.png"
    ),
    "parallel circuit": (
        "diagrams/dict_parallel_circuit.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Parallel_circuit.svg/400px-Parallel_circuit.svg.png"
    ),
    "cell division": (
        "diagrams/dict_cell_division.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Animal_cell_cycle-en.svg/500px-Animal_cell_cycle-en.svg.png"
    ),
    "myopia (nearsightedness)": (
        "diagrams/dict_myopia_nearsightedness.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Myopia_diagram.svg/500px-Myopia_diagram.svg.png"
    ),
    "acceleration-time-graph (a-t graph)": (
        "diagrams/dict_acceleration_time_graph_a_t_graph.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Velocity_vs_time_graph.png/400px-Velocity_vs_time_graph.png"
    ),
    "cycloid": (
        "diagrams/dict_cycloid.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Cycloid_f.gif/400px-Cycloid_f.gif"
    ),
    "abscissa": (
        "diagrams/dict_abscissa.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Cartesian-coordinate-system.svg/400px-Cartesian-coordinate-system.svg.png"
    ),
    "galilean telescope": (
        "diagrams/dict_galilean_telescope.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Galilean_telescope_raya.svg/500px-Galilean_telescope_raya.svg.png"
    ),
    "number line (real line)": (
        "diagrams/dict_number_line_real_line.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Number-line.svg/500px-Number-line.svg.png"
    ),
    "cubic function": (
        "diagrams/dict_cubic_function.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Polynomialdeg3.svg/400px-Polynomialdeg3.svg.png"
    ),
    "alloy": (
        "diagrams/dict_alloy.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Alloy_interstitial_example.svg/400px-Alloy_interstitial_example.svg.png"
    ),
    "potometer": (
        "diagrams/dict_potometer.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Potometer_diagram.svg/350px-Potometer_diagram.svg.png"
    ),
    "density": (
        "diagrams/dict_density.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Density_block.svg/400px-Density_block.svg.png"
    ),

    # ── KEY STEM TERMS — ADDING CLEAN LABELED DIAGRAMS ─────────────────────

    "flower": (
        "diagrams/dict_flower.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Mature_flower_diagram.svg/500px-Mature_flower_diagram.svg.png"
    ),
    "periodic table": (
        "diagrams/dict_periodic_table.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Simple_Periodic_Table_Chart-en.svg/800px-Simple_Periodic_Table_Chart-en.svg.png"
    ),
    "cell": (
        "diagrams/animal_cell.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Animal_Cell.svg/500px-Animal_Cell.svg.png"
    ),
    "animal cell": (
        "diagrams/animal_cell.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Animal_Cell.svg/500px-Animal_Cell.svg.png"
    ),
    "plant cell": (
        "diagrams/plant_cell.jpeg",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/28/Plant_cell_structure_svg_labels.svg/500px-Plant_cell_structure_svg_labels.svg.png"
    ),
    "atom": (
        "diagrams/dict_atom.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/23/Helium_atom_QM.svg/400px-Helium_atom_QM.svg.png"
    ),
    "mitosis": (
        "diagrams/dict_mitosis.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Animal_cell_cycle-en.svg/500px-Animal_cell_cycle-en.svg.png"
    ),
    "meiosis": (
        "diagrams/dict_meiosis.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Meiosis_diagram.svg/500px-Meiosis_diagram.svg.png"
    ),
    "photosynthesis": (
        "diagrams/dict_photosynthesis.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Photosynthesis_en.svg/500px-Photosynthesis_en.svg.png"
    ),
    "heart": (
        "diagrams/dict_heart.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Diagram_of_the_human_heart_%28cropped%29.svg/500px-Diagram_of_the_human_heart_%28cropped%29.svg.png"
    ),
    "human eye": (
        "diagrams/dict_human_eye.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Schematic_diagram_of_the_human_eye_en.svg/500px-Schematic_diagram_of_the_human_eye_en.svg.png"
    ),
    "brain": (
        "diagrams/dict_brain.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Human_brain_-_midsagittal_cut.svg/500px-Human_brain_-_midsagittal_cut.svg.png"
    ),
    "kidney": (
        "diagrams/dict_kidney.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/KidneyStructures_PioM.svg/400px-KidneyStructures_PioM.svg.png"
    ),
    "dna": (
        "diagrams/dict_dna.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/DNA_Structure%2BKey%2BLabelled.pn_NoBB.png/400px-DNA_Structure%2BKey%2BLabelled.pn_NoBB.png"
    ),
    "water cycle": (
        "diagrams/dict_water_cycle.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Water_cycle.png/600px-Water_cycle.png"
    ),
    "electromagnetic spectrum": (
        "diagrams/dict_electromagnetic_spectrum.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/EM_spectrum.svg/600px-EM_spectrum.svg.png"
    ),
    "Newton's laws of motion": (
        "diagrams/dict_newtons_laws_of_motion.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/ForceDiagram.svg/400px-ForceDiagram.svg.png"
    ),
    "electrical circuit": (
        "diagrams/dict_electrical_circuit.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Electric_circuit_elements.svg/500px-Electric_circuit_elements.svg.png"
    ),
    "refraction": (
        "diagrams/dict_refraction.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Snells_law2.svg/400px-Snells_law2.svg.png"
    ),
    "reflection": (
        "diagrams/dict_reflection.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Reflection_angles.svg/400px-Reflection_angles.svg.png"
    ),
    "diffraction": (
        "diagrams/dict_diffraction.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Diffraction1.png/400px-Diffraction1.png"
    ),
    "osmosis": (
        "diagrams/dict_osmosis.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Osmose_en.svg/400px-Osmose_en.svg.png"
    ),
    "diffusion": (
        "diagrams/dict_diffusion.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Diffusion.svg/400px-Diffusion.svg.png"
    ),
    "ecosystem": (
        "diagrams/dict_ecosystem.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/Conifer_forest_food_web.png/500px-Conifer_forest_food_web.png"
    ),
    "food chain": (
        "diagrams/dict_food_chain.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9f/FoodChain.svg/400px-FoodChain.svg.png"
    ),
    "mitochondria": (
        "diagrams/dict_mitochondria.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Mitochondrion_mini.svg/400px-Mitochondrion_mini.svg.png"
    ),
    "chloroplast": (
        "diagrams/dict_chloroplast.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Chloroplast_II.svg/400px-Chloroplast_II.svg.png"
    ),
    "neuron": (
        "diagrams/dict_neuron.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Blausen_0657_MultipolarNeuron.png/500px-Blausen_0657_MultipolarNeuron.png"
    ),
    "pulley": (
        "diagrams/dict_pulley.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Pulley1a.svg/300px-Pulley1a.svg.png"
    ),
    "lever": (
        "diagrams/dict_lever.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Lever_force_diagram.svg/400px-Lever_force_diagram.svg.png"
    ),
    "prism": (
        "diagrams/dict_prism.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Prism_rainbow_schema.png/400px-Prism_rainbow_schema.png"
    ),
    "lens": (
        "diagrams/dict_lens.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Lens1.svg/400px-Lens1.svg.png"
    ),
    "wave": (
        "diagrams/dict_wave.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Sine_wavelength.svg/500px-Sine_wavelength.svg.png"
    ),
    "volcano": (
        "diagrams/dict_volcano.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Volcano_scheme.svg/500px-Volcano_scheme.svg.png"
    ),
    "solar system": (
        "diagrams/dict_solar_system.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Planets2013.svg/600px-Planets2013.svg.png"
    ),
    "blood": (
        "diagrams/dict_blood.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Blausen_0083_Blood_Composition.png/400px-Blausen_0083_Blood_Composition.png"
    ),
    "plant": (
        "diagrams/dict_plant.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Morphology_of_a_flowering_plant.svg/400px-Morphology_of_a_flowering_plant.svg.png"
    ),
    "root": (
        "diagrams/dict_root.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Root-tip-tag.png/300px-Root-tip-tag.png"
    ),
    "leaf": (
        "diagrams/dict_leaf.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Leaf_Tissue_Structure.svg/500px-Leaf_Tissue_Structure.svg.png"
    ),
    "stem": (
        "diagrams/dict_stem.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/65/Stem_cross_section_tag.png/300px-Stem_cross_section_tag.png"
    ),
}


def slugify(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9]+", "_", t)
    return t.strip("_")


def download_image(url: str, dest_path: str) -> bool:
    """Download url to dest_path. Returns True on success."""
    headers = {"User-Agent": "OsmosisSTEMDictionary/1.0 (educational; contact@osmosis.game)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        # Basic check — must be a real image (not empty or HTML error page)
        if len(data) < 1000:
            return False
        with open(dest_path, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    ERROR downloading {url}: {e}")
        return False


def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)

    # Load existing map
    with open(MAP_JSON, encoding="utf-8") as f:
        diag_map = json.load(f)

    print(f"Loaded {len(diag_map)} existing diagram mappings.\n")

    success = 0
    failed  = []

    for term, (rel_path, url) in DIAGRAM_SOURCES.items():
        dest = rel_path  # e.g. "diagrams/dict_flower.png"
        term_key = term.lower().strip()

        print(f"[{term}]")
        print(f"  URL:  {url}")
        print(f"  DEST: {dest}")

        ok = download_image(url, dest)
        if ok:
            # Update map for all matching keys (canonical + lower)
            diag_map[term_key] = rel_path
            # Also update for any existing slightly different key spellings
            for existing_key in list(diag_map.keys()):
                if existing_key.strip() == term_key:
                    diag_map[existing_key] = rel_path
            success += 1
            print(f"  ✅  Saved ({os.path.getsize(dest):,} bytes)")
        else:
            failed.append((term, url))
            print(f"  ❌  FAILED")

        time.sleep(0.3)   # polite pause

    print(f"\n{'='*60}")
    print(f"Downloaded: {success} / {len(DIAGRAM_SOURCES)}")
    if failed:
        print(f"Failed ({len(failed)}):")
        for t, u in failed:
            print(f"  - {t} -> {u}")

    # Save updated map
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(diag_map, f, indent=4, ensure_ascii=False)
    print(f"\nSaved updated {MAP_JSON}")

    # Regenerate core_dictionary_diagrams.js
    with open(DIAGRAMS_JS, "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary_diagrams.js (Auto-extracted + Online-sourced)\n")
        f.write("// =====================================================================\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(diag_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("  window.DictionaryDiagrams = DictionaryDiagrams;\n")
        f.write("}\n")
    print(f"Regenerated {DIAGRAMS_JS}")


if __name__ == "__main__":
    main()
