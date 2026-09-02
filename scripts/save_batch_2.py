import os
import shutil
import json

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"
map_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
core_js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"
guide_path = r"c:\Users\Desmond\Desktop\final_osmosis\DIAGRAM_BATCH_MAPPING_GUIDE.md"

def process_batch_2():
    # As requested: direct integration without cropping for speed & preserving author framing.
    batch_copies = [
        # (source_screenshot, [target_diagram_names])
        ("Screenshot 2026-08-03 162247.png", ["dict_acceleration_time_graph_constant.png", "dict_acceleration_time_graph.png"]),
        ("Screenshot 2026-08-03 162308.png", ["dict_acceleration_due_to_gravity.png"]),
        ("Screenshot 2026-08-03 162326.png", ["dict_base_station_system.png", "dict_bss.png"]),
        ("Screenshot 2026-08-03 162355.png", ["dict_acetanilide.png", "dict_acetanilide_n_phenylethanamide.png"]),
        ("Screenshot 2026-08-03 162409.png", ["dict_acetaldehyde.png"]),
        ("Screenshot 2026-08-03 162423.png", ["dict_acetamide.png", "dict_acetamide_ethanamide.png"]),
        ("Screenshot 2026-08-03 162440.png", ["dict_acetylacetone.png"]),
        ("Screenshot 2026-08-03 162453.png", ["dict_acetophenone.png"]),
        ("Screenshot 2026-08-03 162508.png", ["dict_acetylation.png", "dict_acetylation_ethanoylation.png"]),
        ("Screenshot 2026-08-03 162521.png", ["dict_acetylcholine.png", "dict_acetylcholine_ach.png"]),
    ]

    print("Copying screenshots to diagrams/...")
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

    # Dictionary mappings for Batch 2
    new_mappings = {
        "acceleration-time graph": "diagrams/dict_acceleration_time_graph.png",
        "acceleration time graph": "diagrams/dict_acceleration_time_graph.png",
        "acceleration-time-graph": "diagrams/dict_acceleration_time_graph.png",
        "acceleration due to gravity": "diagrams/dict_acceleration_due_to_gravity.png",
        "base station system": "diagrams/dict_base_station_system.png",
        "base station system (bss)": "diagrams/dict_base_station_system.png",
        "bss": "diagrams/dict_base_station_system.png",
        "base station controller": "diagrams/dict_base_station_system.png",
        "acetanilide": "diagrams/dict_acetanilide.png",
        "acetanilide (n-phenylethanamide)": "diagrams/dict_acetanilide.png",
        "n-phenylethanamide": "diagrams/dict_acetanilide.png",
        "acetaldehyde": "diagrams/dict_acetaldehyde.png",
        "ethanal": "diagrams/dict_acetaldehyde.png",
        "acetamide": "diagrams/dict_acetamide.png",
        "acetamide (ethanamide)": "diagrams/dict_acetamide.png",
        "ethanamide": "diagrams/dict_acetamide.png",
        "acetylacetone": "diagrams/dict_acetylacetone.png",
        "pentane-2,4-dione": "diagrams/dict_acetylacetone.png",
        "acetophenone": "diagrams/dict_acetophenone.png",
        "phenylethanone": "diagrams/dict_acetophenone.png",
        "acetylation": "diagrams/dict_acetylation.png",
        "acetylation (ethanoylation)": "diagrams/dict_acetylation.png",
        "ethanoylation": "diagrams/dict_acetylation.png",
        "acetylcholine": "diagrams/dict_acetylcholine.png",
        "acetylcholine (ach)": "diagrams/dict_acetylcholine.png",
        "ach": "diagrams/dict_acetylcholine.png"
    }

    diag_map.update(new_mappings)

    # Save sorted dictionary_diagrams_map.json
    sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)

    # Save core_dictionary_diagrams.js
    js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ";\n"
    with open(core_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Updated dictionary_diagrams_map.json and core_dictionary_diagrams.js.")

if __name__ == "__main__":
    process_batch_2()
