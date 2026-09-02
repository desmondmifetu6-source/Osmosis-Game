import os
import shutil
import json

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"
map_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
core_js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"

def process_batch_20():
    batch_copies = [
        ("Screenshot 2026-08-03 162637.png", ["dict_acetyl_coa.png", "dict_acetyl_coenzyme_a_acetyl_coa.png"]),
        ("Screenshot 2026-08-03 162648.png", ["dict_achromatic_lens.png", "dict_achromat.png"]),
        ("Screenshot 2026-08-03 162714.png", ["dict_acid_anhydride.png"]),
        ("Screenshot 2026-08-03 162725.png", ["dict_acrylamide.png"]),
        ("Screenshot 2026-08-03 162733.png", ["dict_acrylonitrile.png", "dict_acrylonitrile_propenenitrile.png", "dict_propenenitrile.png"]),
        ("Screenshot 2026-08-03 162744.png", ["dict_activation_energy.png", "dict_reaction_coordinate.png", "dict_transition_state.png"]),
        ("Screenshot 2026-08-03 162804.png", ["dict_activity_series.png", "dict_reactivity_series.png", "dict_electrochemical_series.png"]),
        ("Screenshot 2026-08-03 162814.png", ["dict_acuminate.png", "dict_acuminate_leaf.png"]),
        ("Screenshot 2026-08-03 162822.png", ["dict_acute_angle.png"]),
        ("Screenshot 2026-08-03 162834.png", ["dict_acyclovir.png"]),
        ("Screenshot 2026-08-03 162845.png", ["dict_adaptive_frequency_hopping.png", "dict_frequency_hopping.png"]),
        ("Screenshot 2026-08-03 162858.png", ["dict_adaxial.png", "dict_abaxial.png"]),
        ("Screenshot 2026-08-03 162910.png", ["dict_addition_of_vectors.png", "dict_vector_addition.png"]),
        ("Screenshot 2026-08-03 162919.png", ["dict_adenosine_triphosphate.png", "dict_atp.png", "dict_adenosine_triphosphate_atp.png"]),
        ("Screenshot 2026-08-03 162927.png", ["dict_adipic_acid.png", "dict_hexanedioic_acid.png"]),
        ("Screenshot 2026-08-03 162934.png", ["dict_adipocyte.png", "dict_adipocyte_fat_cell.png", "dict_fat_cell.png"]),
        ("Screenshot 2026-08-03 162941.png", ["dict_adjacent_angles.png", "dict_adjacent.png", "dict_adjacent_side.png"]),
        ("Screenshot 2026-08-03 162948.png", ["dict_adrenaline.png", "dict_epinephrine.png"]),
        ("Screenshot 2026-08-03 211010.png", ["dict_aflatoxin.png", "dict_aflatoxin_b1.png"]),
        ("Screenshot 2026-08-03 211033.png", ["dict_air_layering.png", "dict_air_layering_marcotting.png", "dict_marcotting.png"]),
    ]

    print("Copying screenshots 21-40 into diagrams/...")
    for src_file, targets in batch_copies:
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print(f"WARNING: Source not found: {src_path}")
            continue
        for tgt in targets:
            tgt_path = os.path.join(out_dir, tgt)
            shutil.copy2(src_path, tgt_path)
            print(f"Saved: {tgt} <- {src_file}")

    # Load existing dictionary diagrams map
    with open(map_json_path, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    # Dictionary mappings for 21-40
    new_mappings = {
        # 21: Acetyl-CoA
        "acetyl coenzyme a": "diagrams/dict_acetyl_coenzyme_a_acetyl_coa.png",
        "acetyl coenzyme a (acetyl coa)": "diagrams/dict_acetyl_coenzyme_a_acetyl_coa.png",
        "acetyl-coa": "diagrams/dict_acetyl_coa.png",
        "acetyl coa": "diagrams/dict_acetyl_coa.png",

        # 22: Achromatic lens
        "achromat": "diagrams/dict_achromat.png",
        "achromatic lens": "diagrams/dict_achromatic_lens.png",

        # 23: Acid anhydride
        "acid anhydride": "diagrams/dict_acid_anhydride.png",

        # 24: Acrylamide
        "acrylamide": "diagrams/dict_acrylamide.png",

        # 25: Acrylonitrile
        "acrylonitrile": "diagrams/dict_acrylonitrile.png",
        "acrylonitrile (propenenitrile)": "diagrams/dict_acrylonitrile_propenenitrile.png",
        "propenenitrile": "diagrams/dict_propenenitrile.png",
        "acrylic": "diagrams/dict_acrylonitrile.png",

        # 26: Activation energy / SN2 reaction coordinate
        "activation energy": "diagrams/dict_activation_energy.png",
        "reaction coordinate": "diagrams/dict_reaction_coordinate.png",
        "transition state": "diagrams/dict_transition_state.png",

        # 27: Activity series
        "activity series": "diagrams/dict_activity_series.png",
        "reactivity series": "diagrams/dict_reactivity_series.png",
        "electrochemical series": "diagrams/dict_electrochemical_series.png",

        # 28: Acuminate leaf
        "acuminate": "diagrams/dict_acuminate.png",
        "acuminate leaf": "diagrams/dict_acuminate_leaf.png",

        # 29: Acute angle
        "acute angle": "diagrams/dict_acute_angle.png",

        # 30: Acyclovir
        "acyclovir": "diagrams/dict_acyclovir.png",

        # 31: Adaptive frequency hopping
        "adaptive frequency hopping": "diagrams/dict_adaptive_frequency_hopping.png",
        "frequency hopping": "diagrams/dict_frequency_hopping.png",

        # 32: Adaxial
        "adaxial": "diagrams/dict_adaxial.png",
        "abaxial": "diagrams/dict_abaxial.png",

        # 33: Addition of vectors
        "addition of vectors": "diagrams/dict_addition_of_vectors.png",
        "vector addition": "diagrams/dict_vector_addition.png",

        # 34: Adenosine triphosphate
        "adenosine triphosphate": "diagrams/dict_adenosine_triphosphate.png",
        "adenosine triphosphate (atp)": "diagrams/dict_adenosine_triphosphate_atp.png",
        "atp": "diagrams/dict_atp.png",

        # 35: Adipic acid
        "adipic acid": "diagrams/dict_adipic_acid.png",
        "hexanedioic acid": "diagrams/dict_hexanedioic_acid.png",

        # 36: Adipocyte
        "adipocyte": "diagrams/dict_adipocyte.png",
        "adipocyte (fat cell)": "diagrams/dict_adipocyte_fat_cell.png",
        "fat cell": "diagrams/dict_fat_cell.png",

        # 37: Adjacent angles / Adjacent side
        "adjacent": "diagrams/dict_adjacent.png",
        "adjacent angles": "diagrams/dict_adjacent_angles.png",
        "adjacent side": "diagrams/dict_adjacent_side.png",

        # 38: Adrenaline
        "adrenaline": "diagrams/dict_adrenaline.png",
        "epinephrine": "diagrams/dict_epinephrine.png",

        # 39: Aflatoxin
        "aflatoxin": "diagrams/dict_aflatoxin.png",
        "aflatoxin b1": "diagrams/dict_aflatoxin_b1.png",

        # 40: Air layering
        "air layering": "diagrams/dict_air_layering.png",
        "air layering (marcotting)": "diagrams/dict_air_layering_marcotting.png",
        "marcotting": "diagrams/dict_marcotting.png"
    }

    diag_map.update(new_mappings)

    sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)

    js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ";\n"
    with open(core_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Updated dictionary_diagrams_map.json and core_dictionary_diagrams.js successfully.")

if __name__ == "__main__":
    process_batch_20()
