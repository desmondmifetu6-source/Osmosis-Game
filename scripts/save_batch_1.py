import os
import json
from PIL import Image

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"
map_json_path = r"c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json"
core_js_path = r"c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js"

def trim_borders(im, top_offset=0, bottom_offset=0, left_offset=0, right_offset=0):
    w, h = im.size
    crop_box = (
        max(0, left_offset),
        max(0, top_offset),
        min(w, w - right_offset),
        min(h, h - bottom_offset)
    )
    return im.crop(crop_box)

def process_batch_1():
    # 1. Axis vertebra: (324, 161)
    im1 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 161441.png"))
    # remove top line (y: ~5) and bottom line (y: ~152)
    crop1 = trim_borders(im1, top_offset=8, bottom_offset=10)
    crop1.save(os.path.join(out_dir, "dict_axis_vertebra.png"))

    # 2. Azo dye: (267, 216)
    im2 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 161817.png"))
    crop2 = trim_borders(im2, top_offset=16, bottom_offset=12)
    crop2.save(os.path.join(out_dir, "dict_azo_compound.png"))
    crop2.save(os.path.join(out_dir, "dict_azo_dye.png"))

    # 3. Axis of symmetry: (242, 317)
    im3 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 161835.png"))
    crop3 = trim_borders(im3, top_offset=12, bottom_offset=12)
    crop3.save(os.path.join(out_dir, "dict_axis_of_symmetry.png"))

    # 4. Screenshot 162009: (533, 560) -> Fig 1 Astigmatism (top) & Fig II Distortion (bottom)
    im4 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162009.png"))
    # Astigmatism is from top down to horizontal separator around y=275
    crop4_astig = trim_borders(im4.crop((0, 10, 533, 275)), top_offset=5, bottom_offset=5)
    crop4_astig.save(os.path.join(out_dir, "dict_astigmatism.png"))
    # Distortion is from y=285 to bottom line around y=530
    crop4_dist = trim_borders(im4.crop((0, 285, 533, 535)), top_offset=5, bottom_offset=5)
    crop4_dist.save(os.path.join(out_dir, "dict_distortion.png"))

    # 5. Screenshot 162107: (377, 837) -> Fig III Chromatic (top), Fig IV Spherical lens, Fig V Spherical mirror
    im5 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162107.png"))
    # Fig III Chromatic aberration: y=15 to y=440
    crop5_chrom = trim_borders(im5.crop((0, 15, 377, 440)), top_offset=5, bottom_offset=5)
    crop5_chrom.save(os.path.join(out_dir, "dict_chromatic_aberration.png"))
    # Fig IV & V Spherical aberration: y=445 to y=815
    crop5_spher = trim_borders(im5.crop((0, 445, 377, 815)), top_offset=5, bottom_offset=5)
    crop5_spher.save(os.path.join(out_dir, "dict_spherical_aberration.png"))
    # Entire cleaned aberration
    crop5_all = trim_borders(im5, top_offset=15, bottom_offset=25)
    crop5_all.save(os.path.join(out_dir, "dict_aberration.png"))

    # 6. Screenshot 162120: (383, 220) -> Blue light focuses at B vs Red at R
    im6 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162120.png"))
    crop6 = trim_borders(im6, top_offset=22, bottom_offset=22)
    crop6.save(os.path.join(out_dir, "dict_chromatic_aberration_focus.png"))

    # 7. Screenshot 162141: (494, 258) -> ABO Blood Group System
    im7 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162141.png"))
    crop7 = trim_borders(im7, top_offset=14, bottom_offset=14)
    crop7.save(os.path.join(out_dir, "dict_abo_blood_group_system.png"))
    crop7.save(os.path.join(out_dir, "dict_abo_blood_group.png"))

    # 8. Screenshot 162157: (465, 310) -> Abomasum of a cow
    im8 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162157.png"))
    crop8 = trim_borders(im8, top_offset=16, bottom_offset=16)
    crop8.save(os.path.join(out_dir, "dict_abomasum.png"))
    crop8.save(os.path.join(out_dir, "dict_abomasum_true_stomach.png"))

    # 9. Screenshot 162218: (472, 219) -> Absorption spectrum
    im9 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162218.png"))
    crop9 = trim_borders(im9, top_offset=14, bottom_offset=10)
    crop9.save(os.path.join(out_dir, "dict_absorption_spectrum.png"))

    # 10. Screenshot 162233: (267, 268) -> Instantaneous Acceleration Graph
    im10 = Image.open(os.path.join(src_dir, "Screenshot 2026-08-03 162233.png"))
    crop10 = trim_borders(im10, top_offset=12, bottom_offset=12)
    crop10.save(os.path.join(out_dir, "dict_acceleration_time_graph.png"))
    crop10.save(os.path.join(out_dir, "dict_instantaneous_acceleration.png"))

    print("Cropping and saving images complete.")

    # Update dictionary_diagrams_map.json
    with open(map_json_path, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    new_mappings = {
        "axis": "diagrams/dict_axis_vertebra.png",
        "axis vertebra": "diagrams/dict_axis_vertebra.png",
        "azo compound": "diagrams/dict_azo_compound.png",
        "azo dye": "diagrams/dict_azo_dye.png",
        "axis of symmetry": "diagrams/dict_axis_of_symmetry.png",
        "astigmatism": "diagrams/dict_astigmatism.png",
        "distortion": "diagrams/dict_distortion.png",
        "distortion aberration": "diagrams/dict_distortion.png",
        "aberration": "diagrams/dict_aberration.png",
        "chromatic aberration": "diagrams/dict_chromatic_aberration.png",
        "spherical aberration": "diagrams/dict_spherical_aberration.png",
        "abo blood group": "diagrams/dict_abo_blood_group.png",
        "abo blood group system": "diagrams/dict_abo_blood_group_system.png",
        "abomasum": "diagrams/dict_abomasum.png",
        "abomasum (true stomach)": "diagrams/dict_abomasum_true_stomach.png",
        "absorption spectrum": "diagrams/dict_absorption_spectrum.png",
        "acceleration": "diagrams/dict_acceleration_time_graph.png",
        "acceleration-time graph": "diagrams/dict_acceleration_time_graph.png",
        "acceleration-time-graph": "diagrams/dict_acceleration_time_graph.png",
        "instantaneous acceleration": "diagrams/dict_instantaneous_acceleration.png"
    }

    diag_map.update(new_mappings)

    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(diag_map, f, indent=4, ensure_ascii=False)

    # Update core_dictionary_diagrams.js
    js_content = "// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = " + json.dumps(diag_map, indent=4, ensure_ascii=False) + ";\n"
    with open(core_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)

    print("Updated dictionary_diagrams_map.json and core_dictionary_diagrams.js successfully.")

if __name__ == "__main__":
    process_batch_1()
