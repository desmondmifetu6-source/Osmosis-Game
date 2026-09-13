"""
Batch 3 F-J Diagrams Integration Script — Images 61 to 70
Copies source screenshots into diagrams/ folder with standardized names,
then updates dictionary_diagrams_map.json and core_dictionary_diagrams.js.
"""

import os
import json
import shutil
import re

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "f-j diagrams")
DEST_DIR = os.path.join(BASE_DIR, "diagrams")
MAP_JSON = os.path.join(BASE_DIR, "dictionary_diagrams_map.json")
MAP_JS = os.path.join(BASE_DIR, "core_dictionary_diagrams.js")

# ── Mappings ───────────────────────────────────────────────────────────────────
# Format: (source_filename, [dest_filenames], [dictionary_terms])
MAPPINGS = [
    (
        "Screenshot_11-9-2026_15483_.jpeg",
        ["dict_hexamine.png"],
        ["hexamine", "methenamine"]
    ),
    (
        "Screenshot_11-9-2026_154855_.jpeg",
        ["dict_hilum.png", "dict_hilum_seed_coat.png", "dict_hilum_kidney.png"],
        ["hilum", "hilum of seed coat", "hilum of kidney"]
    ),
    (
        "Screenshot_11-9-2026_154923_.jpeg",
        ["dict_histogram.png"],
        ["histogram", "histogram on cartesian plane"]
    ),
    (
        "Screenshot_11-9-2026_154938_.jpeg",
        ["dict_hoffmanns_reaction.png", "dict_hoffmann_rearrangement.png"],
        ["hoffmann's reaction", "hoffmann rearrangement", "hoffmann degradation"]
    ),
    (
        "Screenshot_11-9-2026_154947_.jpeg",
        ["dict_hoffman_voltammeter.png"],
        ["hoffman voltammeter", "hoffmann voltammeter", "voltammeter"]
    ),
    (
        "Screenshot_11-9-2026_15499_.jpeg",
        ["dict_histamine.png"],
        ["histamine"]
    ),
    (
        "Screenshot_11-9-2026_155021_.jpeg",
        ["dict_horizontal_line_test.png"],
        ["horizontal line test", "one-to-one function"]
    ),
    # Image 68 is a supplementary view of same topic (horizontal line test y=x²)
    # merged into the same diagram file
    (
        "Screenshot_11-9-2026_155029_.jpeg",
        ["dict_horizontal_line_test_not_one_to_one.png"],
        ["horizontal line test not one-to-one", "many-to-one function"]
    ),
    (
        "Screenshot_11-9-2026_155057_.jpeg",
        ["dict_hot_wire_ammeter.png"],
        ["hot-wire ammeter", "hot wire ammeter"]
    ),
    (
        "Screenshot_11-9-2026_155111_.jpeg",
        ["dict_huygens_eyepiece.png"],
        ["huygens' eyepiece", "huygens eyepiece", "eyepiece"]
    ),
]

os.makedirs(DEST_DIR, exist_ok=True)

# ── Step 1: Copy images ────────────────────────────────────────────────────────
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

# ── Step 2: Update dictionary_diagrams_map.json ────────────────────────────────
print("\n=== Updating dictionary_diagrams_map.json ===")
with open(MAP_JSON, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

for _, dest_names, terms in MAPPINGS:
    primary_image = dest_names[0]
    for term in terms:
        diagram_map[term] = primary_image
        print(f"  [MAP] '{term}' -> '{primary_image}'")

# Sort keys alphabetically
diagram_map = dict(sorted(diagram_map.items()))

with open(MAP_JSON, "w", encoding="utf-8") as f:
    json.dump(diagram_map, f, indent=2, ensure_ascii=False)
print("  [SAVED] dictionary_diagrams_map.json")

# ── Step 3: Update core_dictionary_diagrams.js ────────────────────────────────
print("\n=== Updating core_dictionary_diagrams.js ===")
with open(MAP_JS, "r", encoding="utf-8") as f:
    js_content = f.read()

# Extract existing entries from JS object
existing_entries = re.findall(r'"([^"]+)":\s*"([^"]+)"', js_content)
js_dict = dict(existing_entries)

# Add new entries
for _, dest_names, terms in MAPPINGS:
    primary_image = dest_names[0]
    for term in terms:
        js_dict[term] = primary_image

# Sort and rebuild
sorted_entries = sorted(js_dict.items())
entries_str = ",\n  ".join(f'"{k}": "{v}"' for k, v in sorted_entries)
new_js = f"var DictionaryDiagrams = {{\n  {entries_str}\n}};\n"

with open(MAP_JS, "w", encoding="utf-8") as f:
    f.write(new_js)
print("  [SAVED] core_dictionary_diagrams.js")

print("\n✅ Batch 3 (F-J #61–70) complete!")
