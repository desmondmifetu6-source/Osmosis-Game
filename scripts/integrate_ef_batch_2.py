"""
integrate_ef_batch_2.py
=======================
Section E-F Diagram Integration — Batch 2 (Screenshots 11–20)

Diagrams processed (Pure Vision — no blind OCR):
  11. Screenshot_8-9-2026_112525_  → Simple electric motor
  12. Screenshot_8-9-2026_112635_  → Electrolytic cell
  13. Screenshot_8-9-2026_112647_  → Electromagnetic radiation (EM wave)
  14. Screenshot_8-9-2026_112730_  → Electromagnetic spectrum
  15. Screenshot_8-9-2026_11279_   → Electromagnetic induction
  16. Screenshot_8-9-2026_112926_  → Electrophilic substitution in aromatics
  17. Screenshot_8-9-2026_113049_  → Elliptic curve
  18. Screenshot_8-9-2026_11309_   → Gold-Leaf Electroscope
  19. Screenshot_8-9-2026_113613_  → Ellipsoid
  20. Screenshot_8-9-2026_11362_   → Ellipse with its various parts
"""

import json
import shutil
import os

# ── Source screenshots → dest diagram filenames ───────────────────────────────
SCREENSHOT_DIR = "e-d diagrams"
DIAGRAMS_DIR   = "diagrams"

copies = [
    ("Screenshot_8-9-2026_112525_.jpeg",  "dict_electric_motor.png"),
    ("Screenshot_8-9-2026_112635_.jpeg",  "dict_electrolytic_cell.png"),
    ("Screenshot_8-9-2026_112647_.jpeg",  "dict_electromagnetic_radiation.png"),
    ("Screenshot_8-9-2026_112730_.jpeg",  "dict_electromagnetic_spectrum.png"),
    ("Screenshot_8-9-2026_11279_.jpeg",   "dict_electromagnetic_induction.png"),
    ("Screenshot_8-9-2026_112926_.jpeg",  "dict_electrophilic_substitution.png"),
    ("Screenshot_8-9-2026_113049_.jpeg",  "dict_elliptic_curve.png"),
    ("Screenshot_8-9-2026_11309_.jpeg",   "dict_gold_leaf_electroscope.png"),
    ("Screenshot_8-9-2026_113613_.jpeg",  "dict_ellipsoid.png"),
    ("Screenshot_8-9-2026_11362_.jpeg",   "dict_ellipse.png"),
]

print("── Step 1: Copying screenshots → diagrams/ ──────────────────────────────")
for src_name, dst_name in copies:
    src = os.path.join(SCREENSHOT_DIR, src_name)
    dst = os.path.join(DIAGRAMS_DIR, dst_name)
    if not os.path.exists(src):
        print(f"  ⚠ SOURCE NOT FOUND: {src}")
        continue
    shutil.copy2(src, dst)
    print(f"  ✅ {src_name}  →  {dst_name}")

# ── New term → diagram mappings ───────────────────────────────────────────────
NEW_MAPPINGS = {
    # Screenshot 11 — Simple electric motor
    "electric motor":           "diagrams/dict_electric_motor.png",
    "simple electric motor":    "diagrams/dict_electric_motor.png",
    "commutator":               "diagrams/dict_electric_motor.png",
    "carbon brush":             "diagrams/dict_electric_motor.png",

    # Screenshot 12 — Electrolytic cell
    "electrolytic cell":        "diagrams/dict_electrolytic_cell.png",
    "electrolysis":             "diagrams/dict_electrolytic_cell.png",
    "anode":                    "diagrams/dict_electrolytic_cell.png",
    "cathode":                  "diagrams/dict_electrolytic_cell.png",
    "electrolyte":              "diagrams/dict_electrolytic_cell.png",

    # Screenshot 13 — Electromagnetic radiation / EM wave
    "electromagnetic radiation": "diagrams/dict_electromagnetic_radiation.png",
    "electromagnetic wave":      "diagrams/dict_electromagnetic_radiation.png",

    # Screenshot 14 — Electromagnetic spectrum
    "electromagnetic spectrum":  "diagrams/dict_electromagnetic_spectrum.png",
    "visible spectrum":          "diagrams/dict_electromagnetic_spectrum.png",
    "gamma ray":                 "diagrams/dict_electromagnetic_spectrum.png",
    "infrared":                  "diagrams/dict_electromagnetic_spectrum.png",
    "ultraviolet":               "diagrams/dict_electromagnetic_spectrum.png",
    "radio wave":                "diagrams/dict_electromagnetic_spectrum.png",
    "microwave":                 "diagrams/dict_electromagnetic_spectrum.png",

    # Screenshot 15 — Electromagnetic induction
    "electromagnetic induction": "diagrams/dict_electromagnetic_induction.png",
    "magnetic flux":             "diagrams/dict_electromagnetic_induction.png",
    "galvanometer":              "diagrams/dict_electromagnetic_induction.png",

    # Screenshot 16 — Electrophilic substitution
    "electrophilic substitution":          "diagrams/dict_electrophilic_substitution.png",
    "electrophilic substitution in aromatics": "diagrams/dict_electrophilic_substitution.png",
    "electrophile":              "diagrams/dict_electrophilic_substitution.png",

    # Screenshot 17 — Elliptic curve
    "elliptic curve":            "diagrams/dict_elliptic_curve.png",

    # Screenshot 18 — Gold-Leaf Electroscope
    "gold-leaf electroscope":    "diagrams/dict_gold_leaf_electroscope.png",
    "electroscope":              "diagrams/dict_gold_leaf_electroscope.png",
    "gold leaf electroscope":    "diagrams/dict_gold_leaf_electroscope.png",

    # Screenshot 19 — Ellipsoid
    "ellipsoid":                 "diagrams/dict_ellipsoid.png",

    # Screenshot 20 — Ellipse
    "ellipse":                   "diagrams/dict_ellipse.png",
    "major axis":                "diagrams/dict_ellipse.png",
    "minor axis":                "diagrams/dict_ellipse.png",
    "semi-major axis":           "diagrams/dict_ellipse.png",
    "focus":                     "diagrams/dict_ellipse.png",
}

# ── Load & update dictionary_diagrams_map.json ────────────────────────────────
MAP_FILE = "dictionary_diagrams_map.json"
print(f"\n── Step 2: Updating {MAP_FILE} ──────────────────────────────────────────")

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diagram_map = json.load(f)

added = 0
skipped = 0
for term, path in NEW_MAPPINGS.items():
    if term not in diagram_map:
        diagram_map[term] = path
        print(f"  + Added:   \"{term}\"")
        added += 1
    else:
        print(f"  ~ Skipped: \"{term}\" (already exists → {diagram_map[term]})")
        skipped += 1

# Sort alphabetically and save
diagram_map_sorted = dict(sorted(diagram_map.items()))
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(diagram_map_sorted, f, indent=2, ensure_ascii=False)

print(f"\n  ✅ {MAP_FILE} saved. Added: {added}, Skipped: {skipped}")

# ── Rebuild core_dictionary_diagrams.js ──────────────────────────────────────
print("\n── Step 3: Rebuilding core_dictionary_diagrams.js ───────────────────────")
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

print("  ✅ core_dictionary_diagrams.js rebuilt successfully.")
print("\n🎉 Batch 2 integration complete! Run git add/commit/push next.")
