"""
Batch 3B (Screenshots 71 to 75) Integration Script
"""

import os
import json
import shutil
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "f-j diagrams")
DEST_DIR = os.path.join(BASE_DIR, "diagrams")
MAP_JSON = os.path.join(BASE_DIR, "dictionary_diagrams_map.json")
MAP_JS = os.path.join(BASE_DIR, "core_dictionary_diagrams.js")

MAPPINGS = [
    (
        "Screenshot_11-9-2026_155124_.jpeg",
        ["dict_hydraulic_machine.png", "dict_hydraulic_press.png"],
        ["hydraulic machine", "hydraulic press", "hydraulics"]
    ),
    (
        "Screenshot_11-9-2026_155138_.jpeg",
        ["dict_preparation_of_hydrogen.png", "dict_hydrogen.png"],
        ["hydrogen", "preparation of hydrogen", "preparation of hydrogen from zinc with dilute acids"]
    ),
    (
        "Screenshot_11-9-2026_155228_.jpeg",
        ["dict_hydrogen_bond.png", "dict_hydrogen_bonding.png"],
        ["hydrogen bond", "hydrogen bonding", "intermolecular hydrogen bonding", "intramolecular hydrogen bonding"]
    ),
    (
        "Screenshot_11-9-2026_155239_.jpeg",
        ["dict_hydrogen_electrode.png", "dict_standard_hydrogen_electrode.png"],
        ["hydrogen electrode", "standard hydrogen electrode", "she", "normal hydrogen electrode"]
    ),
    (
        "Screenshot_11-9-2026_155249_.jpeg",
        ["dict_hydrometer.png"],
        ["hydrometer"]
    ),
]

os.makedirs(DEST_DIR, exist_ok=True)

print("=== Copying images ===")
for src_name, dest_names, _ in MAPPINGS:
    src_path = os.path.join(SOURCE_DIR, src_name)
    if not os.path.exists(src_path):
        print(f"  [MISSING] {src_name}")
        continue
    for dest_name in dest_names:
        dest_path = os.path.join(DEST_DIR, dest_name)
        shutil.copy2(src_path, dest_path)
        print(f"  [COPIED] {src_name} -> {dest_name}")

print("\n=== Updating dictionary_diagrams_map.json ===")
with open(MAP_JSON, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

for _, dest_names, terms in MAPPINGS:
    primary_image = dest_names[0]
    for term in terms:
        diagram_map[term] = primary_image
        print(f"  [MAP] '{term}' -> '{primary_image}'")

diagram_map = dict(sorted(diagram_map.items()))

with open(MAP_JSON, "w", encoding="utf-8") as f:
    json.dump(diagram_map, f, indent=2, ensure_ascii=False)
print("  [SAVED] dictionary_diagrams_map.json (Total entries: " + str(len(diagram_map)) + ")")

print("\n=== Updating core_dictionary_diagrams.js ===")
with open(MAP_JS, "r", encoding="utf-8") as f:
    js_content = f.read()

existing_entries = re.findall(r'"([^"]+)":\s*"([^"]+)"', js_content)
js_dict = dict(existing_entries)

for _, dest_names, terms in MAPPINGS:
    primary_image = dest_names[0]
    for term in terms:
        js_dict[term] = primary_image

sorted_entries = sorted(js_dict.items())
entries_str = ",\n  ".join(f'"{k}": "{v}"' for k, v in sorted_entries)
new_js = f"var DictionaryDiagrams = {{\n  {entries_str}\n}};\n"

with open(MAP_JS, "w", encoding="utf-8") as f:
    f.write(new_js)
print("  [SAVED] core_dictionary_diagrams.js (Total entries: " + str(len(js_dict)) + ")")

print("\n[SUCCESS] Batch (Screenshots 71-75) complete!")
