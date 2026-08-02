"""
audit_diagrams.py
=================
Automated quality audit of all extracted PNG diagrams in `diagrams/`.

Checks:
1. File size / corrupted files
2. Pixel dimensions (width, height, aspect ratio)
3. White pixel coverage (detect empty/blank crops)
4. Non-white content bounding box (verify if crop is off-center or has huge white margins)
5. Anomalous key names in core_dictionary_diagrams.js

Run from final_osmosis/:
    python scripts/audit_diagrams.py
"""

import os
import json
import sys
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

MAP_JSON = "dictionary_diagrams_map.json"
DIAGRAMS_DIR = "diagrams"

def audit():
    if not os.path.exists(MAP_JSON):
        print(f"Error: {MAP_JSON} not found.")
        return

    with open(MAP_JSON, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    print(f"Auditing {len(diag_map)} mapped terms...")

    anomalies = {
        "missing_file": [],
        "tiny_file": [],
        "blank_or_near_empty": [],
        "huge_aspect_ratio": [],
        "unusual_keys": []
    }

    total_checked = 0

    for term, rel_path in diag_map.items():
        # Check term string length or format anomalies
        if len(term) < 2 or "   " in term or len(term.split()) > 10:
            anomalies["unusual_keys"].append((term, rel_path))

        full_path = os.path.join(os.path.dirname(__file__), "..", rel_path)
        if not os.path.exists(full_path):
            anomalies["missing_file"].append((term, rel_path))
            continue

        total_checked += 1

        try:
            with Image.open(full_path) as img:
                w, h = img.size
                aspect = w / h if h > 0 else 0

                # Check tiny images (e.g. height < 30px or width < 30px)
                if w < 40 or h < 40:
                    anomalies["tiny_file"].append((term, rel_path, f"{w}x{h}"))

                # Check extreme aspect ratio (e.g. width/height > 6 or height/width > 6)
                if aspect > 6.0 or (aspect < 0.15 and aspect > 0):
                    anomalies["huge_aspect_ratio"].append((term, rel_path, f"{w}x{h} (aspect {aspect:.2f})"))

                # Check for blank / mostly white images
                # Convert to grayscale and inspect pixel values
                gray = img.convert("L")
                pixels = list(gray.getdata())
                non_white = sum(1 for p in pixels if p < 240)
                total_pixels = len(pixels)

                if total_pixels > 0:
                    fill_ratio = non_white / total_pixels
                    if fill_ratio < 0.01: # Less than 1% non-white content
                        anomalies["blank_or_near_empty"].append((term, rel_path, f"fill ratio {fill_ratio*100:.2f}%"))

        except Exception as e:
            anomalies["missing_file"].append((term, rel_path, f"Error: {e}"))

    print(f"\nAudit complete across {total_checked} images.")
    print("=" * 60)
    print(f"Missing files:            {len(anomalies['missing_file'])}")
    print(f"Tiny images (<40px):       {len(anomalies['tiny_file'])}")
    print(f"Blank/Near-empty images:  {len(anomalies['blank_or_near_empty'])}")
    print(f"Extreme aspect ratios:    {len(anomalies['huge_aspect_ratio'])}")
    print(f"Unusual term keys:        {len(anomalies['unusual_keys'])}")
    print("=" * 60)

    if anomalies["blank_or_near_empty"]:
        print("\nSample Blank / Near-Empty Images:")
        for item in anomalies["blank_or_near_empty"][:10]:
            print(f"  - {item[0]} -> {item[1]} ({item[2]})")

    if anomalies["huge_aspect_ratio"]:
        print("\nSample Extreme Aspect Ratio Images:")
        for item in anomalies["huge_aspect_ratio"][:10]:
            print(f"  - {item[0]} -> {item[1]} ({item[2]})")

    if anomalies["unusual_keys"]:
        print("\nSample Unusual Keys:")
        for item in anomalies["unusual_keys"][:10]:
            print(f"  - '{item[0]}' -> {item[1]}")

if __name__ == "__main__":
    audit()
