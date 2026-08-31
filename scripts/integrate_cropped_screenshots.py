"""
integrate_cropped_screenshots.py
=================================
Copies all manually-cropped screenshots from 'cropped diagrams/'
into 'diagrams/' with correct dict_ names, then adds them to
dictionary_diagrams_map.json and regenerates core_dictionary_diagrams.js
"""

import os
import json
import shutil
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ── Mapping: screenshot filename → (dict_filename, dictionary_key(s)) ──────
ASSIGNMENTS = {
    # July 11 batch
    "Screenshot 2026-07-11 142642.png": ("dict_abacus.png",               ["abacus"]),
    "Screenshot 2026-07-11 142719.png": ("dict_valine.png",                ["valine"]),
    "Screenshot 2026-07-11 142738.png": ("dict_abaxial.png",               ["abaxial"]),
    "Screenshot 2026-07-11 142800.png": ("dict_abbe_refractometer.png",    ["abbe refractometer"]),
    "Screenshot 2026-07-11 142817.png": ("dict_abdomen.png",               ["abdomen"]),
    "Screenshot 2026-07-11 142837.png": ("dict_astigmatism.png",           ["astigmatism"]),
    "Screenshot 2026-07-11 142901.png": ("dict_abo_blood_group_system.png",["abo blood group system", "abo blood group"]),
    "Screenshot 2026-07-11 142916.png": ("dict_abomasum.png",              ["abomasum"]),
    "Screenshot 2026-07-11 142931.png": ("dict_abruptly_pinnate.png",      ["abruptly pinnate"]),
    "Screenshot 2026-07-11 142955.png": ("dict_absorption_spectrum.png",   ["absorption spectrum"]),
    "Screenshot 2026-07-11 143027.png": ("dict_base_station_system.png",   ["base station system", "base station (access point)"]),
    "Screenshot 2026-07-11 143047.png": ("dict_acenaphthene.png",          ["acenaphthene"]),
    "Screenshot 2026-07-11 143135.png": ("dict_acetal.png",                ["acetal"]),
    "Screenshot 2026-07-11 143216.png": ("dict_actinodromous_venation.png",["actinodromous venation", "actinodromous"]),
    "Screenshot 2026-07-11 143245.png": ("dict_activation_energy.png",     ["activation energy"]),
    "Screenshot 2026-07-11 143320.png": ("dict_adaxial.png",               ["adaxial"]),
    "Screenshot 2026-07-11 143414.png": ("dict_adipocyte.png",             ["adipocyte", "fat cell"]),
    "Screenshot 2026-07-11 143437.png": ("dict_aerofoil.png",              ["aerofoil"]),
    "Screenshot 2026-07-11 143456.png": ("dict_aeroplane_forces.png",      ["aeroplane"]),
    "Screenshot 2026-07-11 143508.png": ("dict_aeroplane_forces.png",      []),   # same diagram, second crop – skip
    "Screenshot 2026-07-11 143548.png": ("dict_alimentary_canal_human.png",["alimentary canal"]),
    "Screenshot 2026-07-11 143603.png": ("dict_alimentary_canal_rabbit.png",["alimentary canal of a rabbit"]),
    "Screenshot 2026-07-11 143702.png": ("dict_alternate_angles.png",      ["alternate angles"]),
    "Screenshot 2026-07-11 143754.png": ("dict_ammonia_preparation.png",   ["ammonia"]),
    "Screenshot 2026-07-11 143811.png": ("dict_ammeter_hot_wire.png",      ["ammeter"]),
    "Screenshot 2026-07-11 143825.png": ("dict_amoeba.png",                ["amoeba"]),
    "Screenshot 2026-07-11 143848.png": ("dict_amplifier_single_stage.png",["amplifier"]),
    "Screenshot 2026-07-11 143908.png": ("dict_amplitude.png",             ["amplitude"]),
    "Screenshot 2026-07-11 143958.png": ("dict_animal_husbandry.png",      ["animal husbandry"]),
    "Screenshot 2026-07-11 144018.png": ("dict_annular_eclipse.png",       ["annular eclipse"]),
    "Screenshot 2026-07-11 144050.png": ("dict_anthocarp.png",             ["anthocarp"]),
    "Screenshot 2026-07-11 144113.png": ("dict_antinode.png",              ["antinode"]),
    "Screenshot 2026-07-11 144138.png": ("dict_anvil.png",                 ["anvil"]),
    # August 2 batch
    "Screenshot 2026-08-02 151824.png": ("dict_gravitation.png",           ["gravitation"]),
    "Screenshot 2026-08-02 151931.png": ("dict_great_circle.png",          ["great circle"]),
    "Screenshot 2026-08-02 152414.png": ("dict_concave_polygon.png",       ["concave polygon"]),
    "Screenshot 2026-08-02 152452.png": ("dict_consecutive_angles.png",    ["consecutive angles"]),
    "Screenshot 2026-08-02 152505.png": ("dict_connate_perfoliate.png",    ["connate-perfoliate", "connate perfoliate"]),
    "Screenshot 2026-08-02 152608.png": ("dict_convex_surface.png",        ["convex"]),
    "Screenshot 2026-08-02 152646.png": ("dict_cocoyam_corm.png",          ["corm"]),
    "Screenshot 2026-08-02 152713.png": ("dict_corniculate.png",           ["corniculate"]),
    "Screenshot 2026-08-02 152733.png": ("dict_coroniform.png",            ["coroniform"]),
    "Screenshot 2026-08-02 152807.png": ("dict_cosine_rule.png",           ["cosine rule", "cosine law"]),
    "Screenshot 2026-08-02 152830.png": ("dict_coterminal_angles.png",     ["coterminal angles"]),
    "Screenshot 2026-08-02 153709.png": ("dict_coumarin.png",              ["coumarin"]),
    "Screenshot 2026-08-02 153751.png": ("dict_crab.png",                  ["crab"]),
    # Already-named files in cropped diagrams/
    "acerose.png":    ("dict_acerose.png",    ["acerose"]),
    "acetabulum.png": ("dict_acetabulum.png", ["acetabulum"]),
}

SRC_DIR  = "cropped diagrams"
DEST_DIR = "diagrams"
MAP_JSON = "dictionary_diagrams_map.json"
DIAG_JS  = "core_dictionary_diagrams.js"

def run():
    with open(MAP_JSON, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    added   = []
    skipped = []
    already = []

    for src_name, (dest_name, keys) in ASSIGNMENTS.items():
        src_path  = os.path.join(SRC_DIR, src_name)
        dest_path = os.path.join(DEST_DIR, dest_name)

        if not os.path.exists(src_path):
            print(f"  [MISSING SRC] {src_name}")
            skipped.append(src_name)
            continue

        if not keys:
            print(f"  [SKIP – duplicate crop] {src_name}")
            skipped.append(src_name)
            continue

        # Copy the file
        shutil.copy2(src_path, dest_path)

        # Add keys to map
        rel_dest = f"diagrams/{dest_name}"
        for key in keys:
            k = key.lower().strip()
            if k in diag_map:
                already.append(k)
            else:
                diag_map[k] = rel_dest
                added.append(k)

    # Sort and save JSON
    sorted_map = dict(sorted(diag_map.items()))
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    print(f"\nSaved {MAP_JSON}  ({len(sorted_map)} total entries)")

    # Regenerate JS
    with open(DIAG_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")
    print(f"Regenerated {DIAG_JS}")

    print(f"\n{'─'*50}")
    print(f"  New keys added:     {len(added)}")
    print(f"  Already existed:    {len(already)}")
    print(f"  Skipped/missing:    {len(skipped)}")
    if added:
        print("\n  New keys:")
        for k in sorted(added):
            print(f"    + {k}")
    if already:
        print("\n  Already in map (not overwritten):")
        for k in sorted(already):
            print(f"    = {k}")

if __name__ == "__main__":
    run()
