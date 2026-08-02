"""
source_online_diagrams_v2.py
============================
Fixed downloader using the Wikimedia Commons REST API to resolve correct
thumbnail URLs before downloading. This handles Wikimedia's size restrictions.

Run from final_osmosis/:
    python scripts/source_online_diagrams_v2.py
"""

import os, json, sys, time, re
import urllib.request
import urllib.parse
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

DIAGRAMS_DIR = "diagrams"
MAP_JSON     = "dictionary_diagrams_map.json"
DIAGRAMS_JS  = "core_dictionary_diagrams.js"

# Wikimedia Commons API endpoint
WM_API = "https://commons.wikimedia.org/w/api.php"

# ─────────────────────────────────────────────────────────────────────────────
# Catalog: term_key → (dest_path, wikimedia_filename)
# Uses exact Wikimedia Commons file names so the API can resolve them properly
# ─────────────────────────────────────────────────────────────────────────────
DIAGRAM_SOURCES = {
    # ── BAD ASPECT RATIO REPLACEMENTS ───────────────────────────────────────
    "bell jar":                             ("diagrams/dict_bell_jar.png",              "Bell_jar.svg"),
    "ammeter":                              ("diagrams/dict_ammeter.png",               "Galvanometer_diagram.svg"),
    "parallel circuit":                     ("diagrams/dict_parallel_circuit.png",       "Parallel_circuit.svg"),
    "cell division":                        ("diagrams/dict_cell_division.png",          "Animal_cell_cycle-en.svg"),
    "myopia (nearsightedness)":             ("diagrams/dict_myopia_nearsightedness.png", "Myopia_diagram.svg"),
    "acceleration-time-graph (a-t graph)": ("diagrams/dict_acceleration_time_graph_a_t_graph.png","Velocity-time_graph_example.svg"),
    "cycloid":                              ("diagrams/dict_cycloid.png",                "Cycloid_f.gif"),
    "abscissa":                             ("diagrams/dict_abscissa.png",               "Cartesian-coordinate-system.svg"),
    "galilean telescope":                   ("diagrams/dict_galilean_telescope.png",      "Galilean_telescope_raya.svg"),
    "cubic function":                       ("diagrams/dict_cubic_function.png",          "Polynomialdeg3.svg"),
    "alloy":                                ("diagrams/dict_alloy.png",                  "Alloy_interstitial_example.svg"),
    "potometer":                            ("diagrams/dict_potometer.png",               "Photosynthesisfactory.svg"),
    "density":                              ("diagrams/dict_density.png",                "Density_column.svg"),
    "number line (real line)":              ("diagrams/dict_number_line_real_line.png",   "Number-line.svg"),
    "demodulation":                         ("diagrams/dict_demodulation.png",            "Demodulation_AM_signal.svg"),
    "horizontal line test":                 ("diagrams/dict_horizontal_line_test.png",    "Injective_function.svg"),

    # ── KEY STEM TERMS — ADDING CLEAN LABELED DIAGRAMS ──────────────────────
    "flower":                               ("diagrams/dict_flower.png",               "Mature_flower_diagram.svg"),
    "periodic table":                       ("diagrams/dict_periodic_table.png",        "Simple_Periodic_Table_Chart-en.svg"),
    "atom":                                 ("diagrams/dict_atom.png",                 "Atom_diagram.svg"),
    "mitosis":                              ("diagrams/dict_mitosis.png",               "Animal_cell_cycle-en.svg"),
    "meiosis":                              ("diagrams/dict_meiosis.png",               "Meiosis_diagram.svg"),
    "photosynthesis":                       ("diagrams/dict_photosynthesis.png",         "Photosynthesis_en.svg"),
    "heart":                                ("diagrams/dict_heart.png",                 "Diagram_of_the_human_heart_(cropped).svg"),
    "human eye":                            ("diagrams/dict_human_eye.png",             "Schematic_diagram_of_the_human_eye_en.svg"),
    "brain":                                ("diagrams/dict_brain.png",                 "Human_brain_NIH.png"),
    "kidney":                               ("diagrams/dict_kidney.png",                "KidneyStructures_PioM.svg"),
    "dna":                                  ("diagrams/dict_dna.png",                   "DNA_Structure+Key+Labelled.pn_NoBB.png"),
    "water cycle":                          ("diagrams/dict_water_cycle.png",            "Water_cycle.svg"),
    "electromagnetic spectrum":             ("diagrams/dict_electromagnetic_spectrum.png","EM_spectrum.svg"),
    "refraction":                           ("diagrams/dict_refraction.png",             "Snells_law2.svg"),
    "reflection":                           ("diagrams/dict_reflection.png",             "Reflection_angles.svg"),
    "diffraction":                          ("diagrams/dict_diffraction.png",            "Diffraction_grating.svg"),
    "osmosis":                              ("diagrams/dict_osmosis.png",               "Osmosis_diagram.svg"),
    "diffusion":                            ("diagrams/dict_diffusion.png",              "Diffusion.svg"),
    "food chain":                           ("diagrams/dict_food_chain.png",             "FoodChain.svg"),
    "mitochondria":                         ("diagrams/dict_mitochondria.png",           "Mitochondrion_mini.svg"),
    "chloroplast":                          ("diagrams/dict_chloroplast.png",            "Chloroplast_II.svg"),
    "neuron":                               ("diagrams/dict_neuron.png",                "Blausen_0657_MultipolarNeuron.png"),
    "pulley":                               ("diagrams/dict_pulley.png",                "Pulley1a.svg"),
    "lever":                                ("diagrams/dict_lever.png",                 "Lever_force_diagram.svg"),
    "prism":                                ("diagrams/dict_prism.png",                 "Prism_rainbow_schema.png"),
    "lens":                                 ("diagrams/dict_lens.png",                  "Lenses_en.svg"),
    "wave":                                 ("diagrams/dict_wave.png",                  "Sine_wavelength.svg"),
    "volcano":                              ("diagrams/dict_volcano.png",               "Volcano_scheme.svg"),
    "solar system":                         ("diagrams/dict_solar_system.png",           "Planets2013.svg"),
    "plant":                                ("diagrams/dict_plant.png",                 "Morphology_of_a_flowering_plant.svg"),
    "leaf":                                 ("diagrams/dict_leaf.png",                  "Leaf_anatomy_en.svg"),
    "plant cell":                           ("diagrams/plant_cell.jpeg",                "Plant_cell_structure_svg_labels.svg"),
    "animal cell":                          ("diagrams/animal_cell.jpeg",               "Animal_Cell.svg"),
    "cell":                                 ("diagrams/animal_cell.jpeg",               "Animal_Cell.svg"),
    "ecosystem":                            ("diagrams/dict_ecosystem.png",              "Ecological_Pyramid.svg"),
}

HEADERS = {
    "User-Agent": "OsmosisSTEMDictionary/2.0 (educational project; https://github.com/osmosis)"
}


def api_get_thumb_url(filename: str, width: int = 600) -> str | None:
    """Use the Wikimedia Commons API to resolve the correct thumbnail URL."""
    params = urllib.parse.urlencode({
        "action": "query",
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": str(width),
        "titles": f"File:{filename}",
        "format": "json",
    })
    url = f"{WM_API}?{params}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            thumb = info.get("thumburl") or info.get("url")
            if thumb:
                return thumb
    except Exception as e:
        print(f"    API error for '{filename}': {e}")
    return None


def download_url(url: str, dest: str) -> bool:
    """Download url to dest. Returns True on success."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 500:
            print(f"    WARN: suspiciously small download ({len(data)} bytes)")
            return False
        with open(dest, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    DL error: {e}")
        return False


def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)

    with open(MAP_JSON, encoding="utf-8") as f:
        diag_map = json.load(f)

    print(f"Loaded {len(diag_map)} existing mappings. Starting downloads...\n")

    success, failed = 0, []

    for term, (rel_path, wm_filename) in DIAGRAM_SOURCES.items():
        print(f"[{term}]  File: {wm_filename}")

        # Step 1: resolve URL via API
        thumb_url = api_get_thumb_url(wm_filename, width=600)
        if not thumb_url:
            print(f"  ❌  Could not resolve URL for '{wm_filename}'")
            failed.append((term, wm_filename, "API resolution failed"))
            time.sleep(0.5)
            continue

        print(f"  URL: {thumb_url}")

        # Step 2: download
        ok = download_url(thumb_url, rel_path)
        if ok:
            term_key = term.lower().strip()
            diag_map[term_key] = rel_path
            # Also patch any existing alternate spellings
            for k in list(diag_map):
                if k.strip() == term_key:
                    diag_map[k] = rel_path
            size = os.path.getsize(rel_path)
            print(f"  ✅  Saved {rel_path} ({size:,} bytes)")
            success += 1
        else:
            failed.append((term, wm_filename, thumb_url))
            print(f"  ❌  Download failed")

        time.sleep(0.4)

    print(f"\n{'='*60}")
    print(f"Downloaded: {success} / {len(DIAGRAM_SOURCES)}")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for t, fn, info in failed:
            print(f"  - {t}: {fn}  [{info}]")

    # Save updated map
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(diag_map, f, indent=4, ensure_ascii=False)
    print(f"\nSaved {MAP_JSON}")

    # Regenerate JS
    with open(DIAGRAMS_JS, "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary_diagrams.js (Auto-extracted + Online-sourced v2)\n")
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
