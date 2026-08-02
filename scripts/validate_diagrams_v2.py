"""
validate_diagrams_v2.py
=======================
Quick 5-page test of the separator-line based extraction.
Saves sample crops to diagrams/validation_test/ for visual inspection.
"""

import fitz
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

PDF_PATH   = "Dictionary Book 2.pdf"
OUT_DIR    = "diagrams/validation_test"
DPI        = 200
PAD        = 10
DARK_THRESH = 0.30
COL_SPLIT   = 340
CONTENT_Y0  = 70
CONTENT_Y1  = 820
MIN_SEP_WIDTH  = 50
MAX_SEP_HEIGHT = 3
GROUP_THRESH   = 15
MIN_ZONE_H     = 25
MAX_ZONE_H     = 700

# Test pages (0-indexed) — pick pages known to have diagrams
TEST_PAGES = [75, 76, 79, 86, 100, 110, 120, 130, 140, 150]


def is_dark(color):
    if color is None:
        return False
    if isinstance(color, (int, float)):
        return color < DARK_THRESH
    try:
        return all(c < DARK_THRESH for c in color[:3])
    except:
        return False


def get_separator_lines(page):
    seps = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.height > MAX_SEP_HEIGHT or r.width < MIN_SEP_WIDTH:
            continue
        if r.y0 < CONTENT_Y0 or r.y1 > CONTENT_Y1:
            continue
        stroke = d.get("color") or d.get("fill")
        if not is_dark(stroke):
            continue
        seps.append({"y": r.y0, "x0": r.x0, "x1": r.x1})
    return seps


def group_seps(seps):
    if not seps:
        return []
    s = sorted(seps, key=lambda x: x["y"])
    groups = [[s[0]]]
    for item in s[1:]:
        if item["y"] - groups[-1][-1]["y"] <= GROUP_THRESH:
            groups[-1].append(item)
        else:
            groups.append([item])
    return groups


def get_drawings_in_band(page, y0, y1):
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        cy = (r.y0 + r.y1) / 2
        if y0 <= cy <= y1:
            if r.width < 2 and r.height > 200:
                continue  # skip vertical column divider
            rects.append(r)
    return rects



def run_test():
    os.makedirs(OUT_DIR, exist_ok=True)
    doc = fitz.open(PDF_PATH)
    total_found = 0

    for page_num in TEST_PAGES:
        page = doc[page_num]
        all_seps = get_separator_lines(page)
        print(f"\nPage {page_num+1}: {len(all_seps)} dark separator lines found")

        for col_seps, col_name in [
            ([s for s in all_seps if (s["x0"]+s["x1"])/2 < COL_SPLIT], "left"),
            ([s for s in all_seps if (s["x0"]+s["x1"])/2 >= COL_SPLIT], "right"),
        ]:
            groups = group_seps(col_seps)
            print(f"  [{col_name}] {len(groups)} border-marker groups at y = "
                  f"{[round(g[0]['y']) for g in groups]}")

            for i in range(len(groups) - 1):
                top_grp = groups[i]
                bot_grp = groups[i + 1]

                zone_y0 = max(s["y"] for s in top_grp)
                zone_y1 = min(s["y"] for s in bot_grp)
                zone_h  = zone_y1 - zone_y0

                if zone_h < MIN_ZONE_H or zone_h > MAX_ZONE_H:
                    print(f"    SKIP zone y={zone_y0:.0f}→{zone_y1:.0f} h={zone_h:.0f} (out of range)")
                    continue

                drawings = get_drawings_in_band(page, zone_y0 - 5, zone_y1 + 5)
                if not drawings:
                    print(f"    SKIP zone y={zone_y0:.0f}→{zone_y1:.0f} (no drawings)")
                    continue

                all_lines = top_grp + bot_grp
                x0 = min(s["x0"] for s in all_lines)
                x1 = max(s["x1"] for s in all_lines)

                for r in drawings:
                    x0 = min(x0, r.x0)
                    x1 = max(x1, r.x1)

                if col_name == "left":
                    x0 = max(x0, 20);  x1 = min(x1, COL_SPLIT + 5)
                else:
                    x0 = max(x0, COL_SPLIT - 5); x1 = min(x1, 660)

                crop = fitz.Rect(
                    max(0, x0 - PAD),
                    max(0, zone_y0 - PAD),
                    min(670, x1 + PAD),
                    min(886, zone_y1 + PAD),
                )

                fname = f"p{page_num+1}_{col_name}_{i}.png"
                mat   = fitz.Matrix(DPI / 72, DPI / 72)
                pix   = page.get_pixmap(matrix=mat, clip=crop)
                pix.save(os.path.join(OUT_DIR, fname))

                print(f"    ✅ Zone y={zone_y0:.0f}→{zone_y1:.0f} h={zone_h:.0f}pt  "
                      f"x={x0:.0f}→{x1:.0f}  {len(drawings)} drawings  → {fname}")
                total_found += 1

    print(f"\n✅ Validation complete. {total_found} diagram zones saved to '{OUT_DIR}/'")


if __name__ == "__main__":
    run_test()
