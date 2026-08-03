"""
assign_identified_cropped_diagrams.py
======================================
Copies all identified cropped screenshots to their correct dict_*.png target files.
Also ensures dictionary_diagrams_map.json and core_dictionary_diagrams.js are updated.
"""
import os
import sys
import json
import shutil

sys.stdout.reconfigure(encoding="utf-8")

CROP_DIR = "cropped diagrams"
DIAG_DIR = "diagrams"
MAP_JSON = "dictionary_diagrams_map.json"
DIAG_JS  = "core_dictionary_diagrams.js"

# Complete manual mapping: {screenshot_filename: dict_target_filename}
MAPPINGS = {
    # Previously matched by perceptual hash
    "Screenshot 2026-07-11 142817.png": ("dict_abdomen_abdominal_cavity.png", "abdomen (abdominal cavity)"),
    "Screenshot 2026-07-11 142955.png": ("dict_absorption_spectrum.png", "absorption spectrum"),
    "Screenshot 2026-08-02 151824.png": ("dict_gravitation.png", "gravitation"),
    "Screenshot 2026-08-02 152646.png": ("dict_corm_bulbo_tuber_bulbotuber.png", "corm (bulbo tuber, bulbotuber)"),

    # Medium hash matches (7 items) - visually confirmed
    "Screenshot 2026-07-11 142738.png": ("dict_abaxial.png", "abaxial"),
    "Screenshot 2026-07-11 143027.png": ("dict_access_point_base_station.png", "access point (base station)"),
    "Screenshot 2026-07-11 143102.png": ("dict_acicular.png", "acicular"),
    "Screenshot 2026-07-11 143216.png": ("dict_actinodromous_venation.png", "actinodromous venation"),
    "Screenshot 2026-07-11 143245.png": ("dict_activated_complex.png", "activated complex"),
    "Screenshot 2026-07-11 143320.png": ("dict_adaxial.png", "adaxial"),
    "Screenshot 2026-07-11 144018.png": ("dict_annular_eclipse.png", "annular eclipse"),

    # === Manually identified from visual inspection ===
    "Screenshot 2026-07-11 142642.png": ("dict_abacus.png", "abacus"),
    "Screenshot 2026-07-11 142719.png": ("dict_2_amino_3_methylbutanoic_acid_valine.png", "2-amino-3-methylbutanoic acid (valine)"),
    "Screenshot 2026-07-11 142800.png": ("dict_abbe_refractometer.png", "abbe refractometer"),
    "Screenshot 2026-07-11 142837.png": ("dict_astigmatism.png", "astigmatism"),
    "Screenshot 2026-07-11 142901.png": ("dict_abo_blood_group.png", "abo blood group"),
    "Screenshot 2026-07-11 142916.png": ("dict_abomasum_true_stomach.png", "abomasum (true stomach)"),
    "Screenshot 2026-07-11 142931.png": ("dict_abruptly_pinnate_even_pinnate.png", "abruptly pinnate (even pinnate)"),
    "Screenshot 2026-07-11 143047.png": ("dict_acenaphthene.png", "acenaphthene"),
    "Screenshot 2026-07-11 143119.png": ("dict_acetabulum.png", "acetabulum"),
    "Screenshot 2026-07-11 143135.png": ("dict_acetal.png", "acetal"),
    "Screenshot 2026-07-11 143414.png": ("dict_adipocyte_fat_cell.png", "adipocyte (fat cell)"),
    "Screenshot 2026-07-11 143437.png": ("dict_aerofoil.png", "aerofoil"),
    "Screenshot 2026-07-11 143456.png": ("dict_aeroplane_airplane.png", "aeroplane (airplane)"),
    "Screenshot 2026-07-11 143508.png": ("dict_aeroplane_airplane.png", "aeroplane (airplane)"),
    "Screenshot 2026-07-11 143548.png": ("dict_alimentary_canal.png", "alimentary canal"),
    "Screenshot 2026-07-11 143603.png": ("dict_alimentary_canal.png", "alimentary canal"),
    "Screenshot 2026-07-11 143702.png": ("dict_alternate_angles.png", "alternate angles"),
    "Screenshot 2026-07-11 143754.png": ("dict_ammonia.png", "ammonia"),
    "Screenshot 2026-07-11 143811.png": ("dict_ammeter.png", "ammeter"),
    "Screenshot 2026-07-11 143825.png": ("dict_amoeba.png", "amoeba"),
    "Screenshot 2026-07-11 143848.png": ("dict_amplifier.png", "amplifier"),
    "Screenshot 2026-07-11 143908.png": ("dict_amplitude.png", "amplitude"),
    "Screenshot 2026-07-11 143958.png": ("dict_animal_husbandry.png", "animal husbandry"),
    "Screenshot 2026-07-11 144050.png": ("dict_anthocarp.png", "anthocarp"),
    "Screenshot 2026-07-11 144113.png": ("dict_antinode.png", "antinode"),
    "Screenshot 2026-07-11 144138.png": ("dict_anvil_incus.png", "anvil (incus)"),
    "Screenshot 2026-08-02 151931.png": ("dict_great_circle.png", "great circle"),
    "Screenshot 2026-08-02 152414.png": ("dict_concave_polygon.png", "concave polygon"),
    "Screenshot 2026-08-02 152452.png": ("dict_consecutive_angles.png", "consecutive angles"),
    "Screenshot 2026-08-02 152505.png": ("dict_connate.png", "connate"),
    "Screenshot 2026-08-02 152608.png": ("dict_convex.png", "convex"),
    "Screenshot 2026-08-02 152713.png": ("dict_corniculate.png", "corniculate"),
    "Screenshot 2026-08-02 152733.png": ("dict_coroniform.png", "coroniform"),
    "Screenshot 2026-08-02 152807.png": ("dict_cosine.png", "cosine"),
    "Screenshot 2026-08-02 152830.png": ("dict_coterminal_angles.png", "coterminal angles"),
    "Screenshot 2026-08-02 153709.png": ("dict_coumarin.png", "coumarin"),
    "Screenshot 2026-08-02 153751.png": ("dict_crab.png", "crab"),
}

def main():
    copied = 0
    skipped = 0

    # Load existing diagram map if present
    diag_map = {}
    if os.path.exists(MAP_JSON):
        with open(MAP_JSON, "r", encoding="utf-8") as f:
            diag_map = json.load(f)

    for src_name, (dest_name, term) in MAPPINGS.items():
        src_path = os.path.join(CROP_DIR, src_name)
        dest_path = os.path.join(DIAG_DIR, dest_name)

        if not os.path.exists(src_path):
            print(f"[SKIP] Source not found: {src_name}")
            skipped += 1
            continue

        shutil.copy2(src_path, dest_path)
        rel_path = f"diagrams/{dest_name}"
        diag_map[term] = rel_path
        print(f"[OK]   {src_name} -> {dest_name} ({term})")
        copied += 1

    # Save updated dictionary_diagrams_map.json
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(diag_map, f, indent=4, ensure_ascii=False)
    print(f"\nUpdated {MAP_JSON} ({len(diag_map)} entries)")

    # Save core_dictionary_diagrams.js
    with open(DIAG_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Auto-extracted + Online-sourced v3)\n\n")
        f.write("const DictionaryDiagrams = {\n")
        for term, rel_path in sorted(diag_map.items()):
            t_escaped = term.replace('"', '\\"')
            f.write(f'    "{t_escaped}": "{rel_path}",\n')
        f.write("};\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("    window.DictionaryDiagrams = DictionaryDiagrams;\n")
        f.write("}\n\n")
        f.write("if (typeof module !== 'undefined' && module.exports) {\n")
        f.write("    module.exports = DictionaryDiagrams;\n")
        f.write("}\n")
    print(f"Updated {DIAG_JS}")

    print(f"\n{'='*60}")
    print(f"Successfully processed {copied} diagrams | Skipped: {skipped}")

if __name__ == "__main__":
    main()
