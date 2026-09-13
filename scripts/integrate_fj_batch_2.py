"""
integrate_fj_batch_2.py
=======================
Integration of F-J Diagrams - Batch 2 (Screenshots 31 to 60)
"""

import os
import shutil
import json
from PIL import Image

SCREENSHOT_DIR = "f-j diagrams"
DIAGRAMS_DIR = "diagrams"

# List of (source_screenshot, destination_filename)
copies = [
    # 31. Gravitation (duplicate of 30, already in diagrams/dict_gravitation.png)
    ("Screenshot_11-9-2026_154155_.jpeg", "dict_gravitation.png"),

    # 32. Greatest integer function
    ("Screenshot_11-9-2026_154217_.jpeg", "dict_greatest_integer_function.png"),

    # 33. Grouped data frequency distribution
    ("Screenshot_11-9-2026_154234_.jpeg", "dict_grouped_data_frequency_distribution.png"),

    # 34. Guanosine
    ("Screenshot_11-9-2026_154246_.jpeg", "dict_guanosine.png"),

    # 35. Guanidine
    ("Screenshot_11-9-2026_154255_.jpeg", "dict_guanidine.png"),

    # 36. Great circle
    ("Screenshot_11-9-2026_15429_.jpeg",  "dict_great_circle.png"),

    # 37. Guanine
    ("Screenshot_11-9-2026_15431_.jpeg",  "dict_guanine.png"),

    # 38. Haematoxylin
    ("Screenshot_11-9-2026_154325_.jpeg", "dict_haematoxylin.png"),

    # 39. Structure of hair follicle
    ("Screenshot_11-9-2026_154335_.jpeg", "dict_hair_follicle.png"),

    # 40. Half-wave rectification
    ("Screenshot_11-9-2026_154343_.jpeg", "dict_half_wave_rectification.png"),

    # 41. Hastate leaf
    ("Screenshot_11-9-2026_154412_.jpeg", "dict_hastate_leaf.png"),

    # 42. Haustorium
    ("Screenshot_11-9-2026_154420_.jpeg", "dict_haustorium.png"),

    # 43. Head (capitulum)
    ("Screenshot_11-9-2026_154430_.jpeg", "dict_capitulum_head.png"),

    # 44. Heart (combined full)
    ("Screenshot_11-9-2026_154455_.jpeg", "dict_heart.png"),

    # 45. Heat engine
    ("Screenshot_11-9-2026_154513_.jpeg", "dict_heat_engine.png"),

    # 46. Parallelogram height
    ("Screenshot_11-9-2026_154528_.jpeg", "dict_height_parallelogram.png"),

    # 47. Prism height
    ("Screenshot_11-9-2026_154549_.jpeg", "dict_height_prism.png"),

    # 48. Height of pyramid/cone
    ("Screenshot_11-9-2026_154557_.jpeg", "dict_height_pyramid_cone.png"),

    # 49. Height of triangle
    ("Screenshot_11-9-2026_154629_.jpeg", "dict_height_triangle.png"),

    # 50. 3D Helix
    ("Screenshot_11-9-2026_154638_.jpeg", "dict_helix_3d.png"),

    # 51. Hemiacetal
    ("Screenshot_11-9-2026_154648_.jpeg", "dict_hemiacetal.png"),

    # 52. Hesperidium
    ("Screenshot_11-9-2026_154717_.jpeg", "dict_hesperidium.png"),

    # 53. Heterocyclic compound
    ("Screenshot_11-9-2026_154727_.jpeg", "dict_heterocyclic_compound.png"),

    # 54. Heroin
    ("Screenshot_11-9-2026_15472_.jpeg",  "dict_heroin.png"),

    # 55. Heterosporous
    ("Screenshot_11-9-2026_154740_.jpeg", "dict_heterosporous.png"),

    # 56. Heterostylic
    ("Screenshot_11-9-2026_154749_.jpeg", "dict_heterostylic.png"),

    # 57. Heroin (duplicate of 54)
    # merged into dict_heroin.png

    # 58. Hexane
    ("Screenshot_11-9-2026_154811_.jpeg", "dict_hexane.png"),

    # 59. Hexagonal prism
    ("Screenshot_11-9-2026_154825_.jpeg", "dict_hexagonal_prism.png"),

    # 60. Hexagram
    ("Screenshot_11-9-2026_154833_.jpeg", "dict_hexagram.png"),
]

print("== Step 1: Copying screenshots to diagrams/ ==")
for src_name, dst_name in copies:
    src = os.path.join(SCREENSHOT_DIR, src_name)
    dst = os.path.join(DIAGRAMS_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  [WARN] NOT FOUND: {src}")
        continue
    shutil.copy2(src, dst)
    print(f"  [OK] {src_name} -> {dst_name}")

# Split Heart image (Fig 1 & Fig 2)
heart_src = os.path.join(SCREENSHOT_DIR, "Screenshot_11-9-2026_154455_.jpeg")
if os.path.exists(heart_src):
    try:
        with Image.open(heart_src) as img:
            w, h = img.size
            # Fig 1 is top half (~0 to 52%), Fig 2 is bottom half (~52% to 100%)
            split_y = int(h * 0.51)
            fig1 = img.crop((0, 0, w, split_y))
            fig2 = img.crop((0, split_y, w, h))
            
            fig1.save(os.path.join(DIAGRAMS_DIR, "dict_mammalian_heart_vertical_section.png"))
            fig2.save(os.path.join(DIAGRAMS_DIR, "dict_human_heart_external.png"))
            print("  [OK] Split Heart diagram into Fig 1 (Vertical section) and Fig 2 (External view)")
    except Exception as e:
        print(f"  [WARN] Heart split error: {e}")

NEW_MAPPINGS = {
    # 31. Gravitation
    "gravitation": "diagrams/dict_gravitation.png",
    "newton's law of gravitation": "diagrams/dict_gravitation.png",
    "universal gravitation": "diagrams/dict_gravitation.png",

    # 32. Greatest integer function
    "greatest integer function": "diagrams/dict_greatest_integer_function.png",
    "floor function": "diagrams/dict_greatest_integer_function.png",
    "step function": "diagrams/dict_greatest_integer_function.png",

    # 33. Grouped data frequency distribution
    "grouped data": "diagrams/dict_grouped_data_frequency_distribution.png",
    "frequency distribution": "diagrams/dict_grouped_data_frequency_distribution.png",
    "grouped data frequency distribution": "diagrams/dict_grouped_data_frequency_distribution.png",

    # 34. Guanosine
    "guanosine": "diagrams/dict_guanosine.png",
    "cyclic guanosine monophosphate": "diagrams/dict_guanosine.png",
    "guanosine triphosphate": "diagrams/dict_guanosine.png",

    # 35. Guanidine
    "guanidine": "diagrams/dict_guanidine.png",

    # 36. Great circle
    "great circle": "diagrams/dict_great_circle.png",
    "spherical triangle": "diagrams/dict_great_circle.png",

    # 37. Guanine
    "guanine": "diagrams/dict_guanine.png",
    "guan ine": "diagrams/dict_guanine.png",
    "guanine riboside": "diagrams/dict_guanine.png",

    # 38. Haematoxylin
    "haematoxylin": "diagrams/dict_haematoxylin.png",
    "hematoxylin": "diagrams/dict_haematoxylin.png",

    # 39. Structure of hair follicle
    "hair follicle": "diagrams/dict_hair_follicle.png",
    "hair": "diagrams/dict_hair_follicle.png",
    "structure of the hair follicle": "diagrams/dict_hair_follicle.png",

    # 40. Half-wave rectification
    "half-wave rectification": "diagrams/dict_half_wave_rectification.png",
    "half-wave rectifier": "diagrams/dict_half_wave_rectification.png",
    "half wave rectification": "diagrams/dict_half_wave_rectification.png",
    "rectification": "diagrams/dict_half_wave_rectification.png",

    # 41. Hastate leaf
    "hastate": "diagrams/dict_hastate_leaf.png",
    "hastate leaf": "diagrams/dict_hastate_leaf.png",

    # 42. Haustorium
    "haustorium": "diagrams/dict_haustorium.png",
    "haustorium of dodder": "diagrams/dict_haustorium.png",
    "dodder": "diagrams/dict_haustorium.png",

    # 43. Head (capitulum)
    "head": "diagrams/dict_capitulum_head.png",
    "capitulum": "diagrams/dict_capitulum_head.png",
    "head (capitulum)": "diagrams/dict_capitulum_head.png",
    "head inflorescence": "diagrams/dict_capitulum_head.png",

    # 44. Heart
    "heart": "diagrams/dict_heart.png",
    "mammalian heart": "diagrams/dict_mammalian_heart_vertical_section.png",
    "human heart": "diagrams/dict_human_heart_external.png",
    "vertical section of a heart": "diagrams/dict_mammalian_heart_vertical_section.png",
    "external appearance of a human heart": "diagrams/dict_human_heart_external.png",

    # 45. Heat engine
    "heat engine": "diagrams/dict_heat_engine.png",
    "simplified heat engine": "diagrams/dict_heat_engine.png",

    # 46. Parallelogram height
    "height": "diagrams/dict_height_parallelogram.png",
    "height of a parallelogram": "diagrams/dict_height_parallelogram.png",

    # 47. Prism height
    "prism height": "diagrams/dict_height_prism.png",
    "height of a prism": "diagrams/dict_height_prism.png",

    # 48. Height of pyramid/cone
    "height of a pyramid": "diagrams/dict_height_pyramid_cone.png",
    "height of a cone": "diagrams/dict_height_pyramid_cone.png",
    "pyramid height": "diagrams/dict_height_pyramid_cone.png",

    # 49. Height of triangle
    "height of a triangle": "diagrams/dict_height_triangle.png",
    "altitude of a triangle": "diagrams/dict_height_triangle.png",

    # 50. 3D Helix
    "helix": "diagrams/dict_helix_3d.png",
    "helix in a three dimensional plane": "diagrams/dict_helix_3d.png",
    "three dimensional helix": "diagrams/dict_helix_3d.png",

    # 51. Hemiacetal
    "hemiacetal": "diagrams/dict_hemiacetal.png",
    "general formula of a hemiacetal": "diagrams/dict_hemiacetal.png",

    # 52. Hesperidium
    "hesperidium": "diagrams/dict_hesperidium.png",
    "hesperidium fruit": "diagrams/dict_hesperidium.png",

    # 53. Heterocyclic compound
    "heterocyclic compound": "diagrams/dict_heterocyclic_compound.png",
    "heterocyclic": "diagrams/dict_heterocyclic_compound.png",
    "thiophene": "diagrams/dict_heterocyclic_compound.png",
    "oxazole": "diagrams/dict_heterocyclic_compound.png",
    "imidazole": "diagrams/dict_heterocyclic_compound.png",
    "pyridine": "diagrams/dict_heterocyclic_compound.png",

    # 54 & 57. Heroin
    "heroin": "diagrams/dict_heroin.png",
    "diacetylmorphine": "diagrams/dict_heroin.png",

    # 55. Heterosporous
    "heterosporous": "diagrams/dict_heterosporous.png",
    "heterospory": "diagrams/dict_heterosporous.png",
    "microspore": "diagrams/dict_heterosporous.png",
    "microspores": "diagrams/dict_heterosporous.png",
    "megaspore": "diagrams/dict_heterosporous.png",

    # 56. Heterostylic
    "heterostylic": "diagrams/dict_heterostylic.png",
    "heterostyly": "diagrams/dict_heterostylic.png",
    "style": "diagrams/dict_heterostylic.png",

    # 58. Hexane
    "hexane": "diagrams/dict_hexane.png",
    "structure of hexane": "diagrams/dict_hexane.png",

    # 59. Hexagonal prism
    "hexagonal prism": "diagrams/dict_hexagonal_prism.png",
    "prism": "diagrams/dict_hexagonal_prism.png",

    # 60. Hexagram
    "hexagram": "diagrams/dict_hexagram.png",
}

MAP_FILE = "dictionary_diagrams_map.json"
print(f"\n== Step 2: Updating {MAP_FILE} ==")

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

added = 0
for term, path in NEW_MAPPINGS.items():
    if term not in diagram_map:
        diagram_map[term] = path
        print(f"  + Added:   \"{term}\"")
        added += 1
    else:
        print(f"  ~ Updated: \"{term}\" -> {path}")
        diagram_map[term] = path
        added += 1

diagram_map_sorted = dict(sorted(diagram_map.items()))
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(diagram_map_sorted, f, indent=2, ensure_ascii=False)

print(f"\n  [OK] {MAP_FILE} saved. Updated/Added: {added}")

print("\n== Step 3: Rebuilding core_dictionary_diagrams.js ==")
js_lines = ["const DictionaryDiagrams = {"]
items = list(diagram_map_sorted.items())
for i, (term, path) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    js_lines.append(f'  "{term}": "{path}"{comma}')
js_lines.append("};")
js_lines.append("")
js_lines.append("if (typeof window !== 'undefined') {")
js_lines.append("  window.DictionaryDiagrams = DictionaryDiagrams;")
js_lines.append("}")
js_lines.append("if (typeof module !== 'undefined') {")
js_lines.append("  module.exports = DictionaryDiagrams;")
js_lines.append("}")

with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
    f.write("\n".join(js_lines) + "\n")

print("  [OK] core_dictionary_diagrams.js rebuilt successfully.")
print(f"Total mapped entries in dictionary: {len(diagram_map_sorted)}")
