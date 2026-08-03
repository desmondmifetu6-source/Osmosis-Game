"""
match_and_assign_cropped_diagrams.py
=====================================
Matches cropped diagram screenshots to existing dict_*.png files
using perceptual hashing + ORB feature matching (OpenCV).
Then replaces the matched dict_*.png with the higher-quality cropped screenshot.
"""
import os
import sys
import json
import shutil
import struct

sys.stdout.reconfigure(encoding="utf-8")

from PIL import Image

CROP_DIR = "cropped diagrams"
DIAG_DIR = "diagrams"
MAP_JSON = "dictionary_diagrams_map.json"

def dhash(image_path, hash_size=16):
    """Difference hash - better than average hash for structural similarity."""
    try:
        with Image.open(image_path) as im:
            im = im.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.BILINEAR)
            pixels = list(im.getdata())
            bits = []
            for row in range(hash_size):
                for col in range(hash_size):
                    left = pixels[row * (hash_size + 1) + col]
                    right = pixels[row * (hash_size + 1) + col + 1]
                    bits.append('1' if left > right else '0')
            return ''.join(bits)
    except Exception:
        return None

def hamming(h1, h2):
    return sum(c1 != c2 for c1, c2 in zip(h1, h2))

def main():
    crop_files = sorted(os.listdir(CROP_DIR))
    diag_files = [f for f in os.listdir(DIAG_DIR) if os.path.isfile(os.path.join(DIAG_DIR, f))]

    print(f"Loading hashes for {len(diag_files)} dictionary diagrams...")
    diag_hashes = {}
    for df in diag_files:
        h = dhash(os.path.join(DIAG_DIR, df))
        if h:
            diag_hashes[df] = h
    print(f"Loaded {len(diag_hashes)} hashes.")

    print(f"\nMatching {len(crop_files)} cropped screenshots...")
    matches = {}  # crop_file -> (best_diag_file, hamming_distance)
    
    for cf in crop_files:
        ch = dhash(os.path.join(CROP_DIR, cf))
        if not ch:
            continue
        best_file = None
        best_dist = 999
        for df, dh in diag_hashes.items():
            dist = hamming(ch, dh)
            if dist < best_dist:
                best_dist = dist
                best_file = df
        matches[cf] = (best_file, best_dist)

    # Sort by match quality
    matched_strong = {k: v for k, v in matches.items() if v[1] <= 30}
    matched_medium = {k: v for k, v in matches.items() if 30 < v[1] <= 45}
    unmatched = {k: v for k, v in matches.items() if v[1] > 45}

    print(f"\nResults:")
    print(f"  Strong matches (diff <= 30): {len(matched_strong)}")
    print(f"  Medium matches (diff 31-45): {len(matched_medium)}")
    print(f"  Unmatched (diff > 45): {len(unmatched)}")

    # Save the mapping results to JSON for review
    results = {
        "strong": {cf: {"matched_to": v[0], "diff": v[1]} for cf, v in matched_strong.items()},
        "medium": {cf: {"matched_to": v[0], "diff": v[1]} for cf, v in matched_medium.items()},
        "unmatched": {cf: {"matched_to": v[0], "diff": v[1]} for cf, v in unmatched.items()},
    }
    with open("scripts/cropped_match_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("\nAll match results saved to scripts/cropped_match_results.json")

    # Now: Replace matched dict files with the high-quality cropped screenshots
    print("\n=== Replacing matched dict files with cropped screenshots ===")
    replaced = 0
    with open(MAP_JSON, encoding="utf-8") as f:
        diag_map = json.load(f)

    for cf, (df, dist) in matched_strong.items():
        src = os.path.join(CROP_DIR, cf)
        dest = os.path.join(DIAG_DIR, df)
        shutil.copy2(src, dest)
        print(f"  Replaced {df} with {cf} (diff={dist})")
        replaced += 1

    print(f"\nReplaced {replaced} dictionary diagram files with higher-quality cropped screenshots.")
    print("\n=== Unmatched screenshots (need manual identification) ===")
    for cf, (df, dist) in unmatched.items():
        print(f"  {cf}  (best guess: {df}, diff={dist})")

if __name__ == "__main__":
    main()
