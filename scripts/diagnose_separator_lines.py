"""
Diagnostic: Study separator lines & content layout on pages with known diagrams.
This helps us understand what "black horizontal separator" looks like in the PDF data.
Run from the final_osmosis/ root directory.
"""

import fitz
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

def analyze_page(doc, page_num):
    page = doc[page_num]
    print(f"\n{'='*60}")
    print(f"PAGE {page_num + 1}  (size: {page.rect.width:.0f} x {page.rect.height:.0f})")
    print(f"{'='*60}")

    # ── 1. Drawing paths ──────────────────────────────────────────
    drawings = page.get_drawings()
    h_lines = []
    other_paths = []

    for d in drawings:
        r = d["rect"]
        # Colour of the first stroke
        stroke_color = d.get("color") or d.get("fill")
        # Horizontal lines: very thin height, substantial width
        if r.height <= 3 and r.width >= 100:
            h_lines.append({
                "y":     round(r.y0, 2),
                "x0":    round(r.x0, 2),
                "x1":    round(r.x1, 2),
                "width": round(r.width, 1),
                "height":round(r.height, 2),
                "color": stroke_color,
            })
        else:
            other_paths.append(r)

    print(f"\n--- Horizontal lines (height ≤ 3, width ≥ 100): {len(h_lines)} found ---")
    for l in sorted(h_lines, key=lambda x: x["y"]):
        print(f"  y={l['y']:6.1f}  x0={l['x0']:5.1f}→{l['x1']:5.1f}  "
              f"w={l['width']:5.1f}  color={l['color']}")

    print(f"\n--- Other drawing rects (first 20): ---")
    for r in sorted(other_paths, key=lambda x: x.y0)[:20]:
        print(f"  ({r.x0:.0f},{r.y0:.0f}) → ({r.x1:.0f},{r.y1:.0f})  "
              f"w={r.width:.0f} h={r.height:.0f}")

    # ── 2. Text blocks (entry words only) ────────────────────────
    print(f"\n--- Blue+Bold entry words ---")
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                if s["color"] == 35533 and (s["flags"] & 16):
                    bbox = s["bbox"]
                    print(f"  WORD: '{s['text'].strip()}'  "
                          f"  y={bbox[1]:.0f}  x={bbox[0]:.0f}")

    # ── 3. Raster image blocks ───────────────────────────────────
    print(f"\n--- Raster image blocks ---")
    for b in blocks:
        if b.get("type") == 1:
            bbox = b["bbox"]
            print(f"  IMG  ({bbox[0]:.0f},{bbox[1]:.0f}) → ({bbox[2]:.0f},{bbox[3]:.0f})  "
                  f"w={b.get('width',0)}  h={b.get('height',0)}")


def main():
    pdf_path = "Dictionary Book 2.pdf"
    doc = fitz.open(pdf_path)
    print(f"Opened '{pdf_path}' — {len(doc)} pages total.")

    # Pages known to have diagrams (0-indexed = page_num)
    # Page 76 = ABERRATION diagram, page 80 = ABFARAD, page 87 = ABOMASUM
    test_pages = [75, 76, 79, 86, 100, 110, 120]

    for pn in test_pages:
        analyze_page(doc, pn)

if __name__ == "__main__":
    main()
