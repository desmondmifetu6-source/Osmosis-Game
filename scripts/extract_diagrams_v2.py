"""
extract_diagrams_v2.py
======================
Improved diagram extractor using black horizontal separator lines as crop boundaries.

Strategy:
  1. Detect dark horizontal separator lines on each page (not header/footer, not white).
  2. Group lines within 15pt of each other → single "border marker".
  3. Pair consecutive border markers in the same column → diagram zones.
  4. The X crop bounds come from the separator lines themselves (which already span
     the full label width).  Expand bounds further if text/drawings go wider.
  5. Render at 200 DPI PNG for crisp output.
  6. Also clean up entry-word key names (strip trailing brackets, deduplicate aliases).

Run from the final_osmosis/ root:
    python scripts/extract_diagrams_v2.py
"""

import fitz
import os
import re
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ── Configuration ─────────────────────────────────────────────────────────────
PDF_PATH      = "Dictionary Book 2.pdf"
OUTPUT_DIR    = "diagrams"
MAP_JSON      = "dictionary_diagrams_map.json"
DIAGRAMS_JS   = "core_dictionary_diagrams.js"

START_PAGE    = 72      # page 73 (0-indexed) — dictionary begins
END_PAGE      = 1100    # page 1101 (0-indexed) — dictionary ends

DPI           = 200     # render resolution
PAD           = 10      # padding (pts) around crop rect

# Colour threshold: treat a drawing stroke as "dark" if all channels < this value
DARK_THRESH   = 0.30

# Minimum separator line dimensions
MIN_SEP_WIDTH  = 50     # pts — ignore very short lines
MAX_SEP_HEIGHT = 3      # pts — lines must be thin

# Minimum / maximum diagram zone height
MIN_ZONE_H = 25         # pts — skip tiny zones (double-border artefacts)
MAX_ZONE_H = 700        # pts — skip full-page zones

# Column split x-coordinate (vertical column separator is at x≈346)
COL_SPLIT = 340

# y-range of actual content (exclude header y<70 and footer y>820)
CONTENT_Y0 = 70
CONTENT_Y1 = 820

# Group separator lines within this vertical proximity
GROUP_THRESH = 15       # pts
# ──────────────────────────────────────────────────────────────────────────────


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def clean_word_key(raw: str) -> str:
    """Strip trailing colons, clean up parentheses-only suffixes, and collapse spaced characters."""
    raw = raw.strip().rstrip(":")

    # Remove leading/trailing brackets that are incomplete
    if raw.endswith(")") and "(" not in raw:
        raw = raw.rsplit(")", 1)[0].strip()
    if raw.startswith("(") and ")" not in raw:
        raw = raw.split("(", 1)[1].strip()

    raw = raw.strip()

    # Collapse single-letter spaced tokens e.g. "a c u p u n c t u r e" -> "acupuncture"
    tokens = raw.split()
    if len(tokens) >= 3 and (sum(1 for t in tokens if len(t) == 1) / len(tokens)) >= 0.6:
        raw = "".join(tokens)

    return raw.strip()


def is_dark(color) -> bool:
    """Return True if a color tuple represents a dark (near-black) colour."""
    if color is None:
        return False
    if isinstance(color, (int, float)):
        return color < DARK_THRESH
    # Tuple (r, g, b) or (r, g, b, a)
    try:
        return all(c < DARK_THRESH for c in color[:3])
    except Exception:
        return False


def get_separator_lines(page):
    """
    Return all dark horizontal separator lines on a page that fall
    within the content area.
    """
    seps = []
    for d in page.get_drawings():
        r = d["rect"]
        # Must be thin (horizontal line)
        if r.height > MAX_SEP_HEIGHT:
            continue
        # Must be wide enough to be meaningful
        if r.width < MIN_SEP_WIDTH:
            continue
        # Must be inside content area
        if r.y0 < CONTENT_Y0 or r.y1 > CONTENT_Y1:
            continue
        # Must be dark coloured
        stroke = d.get("color") or d.get("fill")
        if not is_dark(stroke):
            continue
        seps.append({
            "y":   r.y0,
            "x0":  r.x0,
            "x1":  r.x1,
            "w":   r.width,
        })
    return seps


def group_seps_by_proximity(seps: list) -> list:
    """
    Group separator lines that are within GROUP_THRESH pts of each other
    vertically.  Returns list of groups, each group is a list of sep dicts.
    """
    if not seps:
        return []
    sorted_seps = sorted(seps, key=lambda s: s["y"])
    groups = [[sorted_seps[0]]]
    for s in sorted_seps[1:]:
        if s["y"] - groups[-1][-1]["y"] <= GROUP_THRESH:
            groups[-1].append(s)
        else:
            groups.append([s])
    return groups


def get_entry_words(page):
    """Return blue+bold entry words with their bounding boxes."""
    words = []
    for b in page.get_text("dict")["blocks"]:
        if b.get("type") != 0:
            continue
        for l in b["lines"]:
            for s in l["spans"]:
                text = s["text"].strip()
                if not text:
                    continue
                # Blue (colour=35533) + bold (flag 16)
                if s["color"] == 35533 and (s["flags"] & 16):
                    clean = clean_word_key(text)
                    if len(clean) < 2:
                        continue
                    if clean.startswith("Science") or clean.startswith("A Science"):
                        continue
                    words.append({
                        "word": clean,
                        "x0":  s["bbox"][0],
                        "y0":  s["bbox"][1],
                        "x1":  s["bbox"][2],
                        "y1":  s["bbox"][3],
                    })
    return words



def get_all_drawings_in_band(page, y0: float, y1: float):
    """Return all drawing rects whose y-centre lies within [y0, y1]."""
    rects = []
    for d in page.get_drawings():
        r = d["rect"]
        cy = (r.y0 + r.y1) / 2
        if y0 <= cy <= y1:
            # Exclude full-page-height vertical column separator
            if r.width < 2 and r.height > 200:
                continue
            rects.append(r)
    return rects


def assign_column(x_center: float) -> str:
    return "left" if x_center < COL_SPLIT else "right"


def find_closest_word(words: list, zone_y0: float, col: str):
    """Find the entry word directly above the diagram zone in the same column."""
    col_words = [w for w in words
                 if assign_column((w["x0"] + w["x1"]) / 2) == col
                 and w["y0"] <= zone_y0 + 30]
    if not col_words:
        # Fallback: any word above in any column
        col_words = [w for w in words if w["y0"] <= zone_y0 + 30]
    if not col_words:
        return None
    return max(col_words, key=lambda w: w["y0"])


def extract_diagrams():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    doc = fitz.open(PDF_PATH)
    total = len(doc)
    print(f"Opened '{PDF_PATH}' — {total} pages.")
    print(f"Processing pages {START_PAGE+1}–{END_PAGE+1}...\n")

    diagram_map  = {}   # word_key → path
    extracted    = 0
    skipped_tiny = 0
    skipped_no_drawing = 0

    for page_num in range(START_PAGE, min(END_PAGE + 1, total)):
        if (page_num - START_PAGE) % 200 == 0:
            pct = (page_num - START_PAGE) / (END_PAGE - START_PAGE) * 100
            print(f"  Page {page_num+1}/{END_PAGE+1}  ({pct:.0f}%)  "
                  f"extracted so far: {extracted}")

        page = doc[page_num]

        # ── Entry words ──
        words = get_entry_words(page)
        if not words:
            continue

        # ── Separator lines ──
        all_seps = get_separator_lines(page)
        if not all_seps:
            continue

        # Split by column and group vertically
        left_seps  = [s for s in all_seps if (s["x0"] + s["x1"]) / 2 < COL_SPLIT]
        right_seps = [s for s in all_seps if (s["x0"] + s["x1"]) / 2 >= COL_SPLIT]

        for col_seps, col_name in [(left_seps, "left"), (right_seps, "right")]:
            groups = group_seps_by_proximity(col_seps)
            if len(groups) < 2:
                continue

            # Pair consecutive border-marker groups
            for i in range(len(groups) - 1):
                top_grp = groups[i]
                bot_grp = groups[i + 1]

                # The diagram zone starts at the bottom of the top group
                # and ends at the top of the bottom group
                zone_y0 = max(s["y"] for s in top_grp)
                zone_y1 = min(s["y"] for s in bot_grp)

                zone_h = zone_y1 - zone_y0
                if zone_h < MIN_ZONE_H or zone_h > MAX_ZONE_H:
                    skipped_tiny += 1
                    continue

                # ── Derive X bounds from separator lines ──
                all_grp_lines = top_grp + bot_grp
                x0 = min(s["x0"] for s in all_grp_lines)
                x1 = max(s["x1"] for s in all_grp_lines)

                # ── Expand X to include all drawings in this zone ──
                drawings = get_all_drawings_in_band(page, zone_y0 - 5, zone_y1 + 5)
                if not drawings:
                    skipped_no_drawing += 1
                    continue  # no actual diagram content in this zone

                for r in drawings:
                    x0 = min(x0, r.x0)
                    x1 = max(x1, r.x1)

                # ── Column boundary clamp ──
                if col_name == "left":
                    x0 = max(x0, 20)
                    x1 = min(x1, COL_SPLIT + 5)
                else:
                    x0 = max(x0, COL_SPLIT - 5)
                    x1 = min(x1, 660)

                # ── Find entry word for this zone ──
                word_entry = find_closest_word(words, zone_y0, col_name)
                if not word_entry:
                    continue

                word_key  = word_entry["word"].lower().strip()
                word_slug = slugify(word_key)
                if not word_slug:
                    continue

                # ── Render crop at 200 DPI (Snap exactly to black separator lines) ──
                crop = fitz.Rect(
                    max(0,                x0 - 2),
                    max(0,                zone_y0 - 1),
                    min(page.rect.width,  x1 + 2),
                    min(page.rect.height, zone_y1 + 1.5),
                )

                filename = f"dict_{word_slug}.png"
                out_path = os.path.join(OUTPUT_DIR, filename)

                mat = fitz.Matrix(DPI / 72, DPI / 72)
                pix = page.get_pixmap(matrix=mat, clip=crop)
                pix.save(out_path)

                rel_path = f"diagrams/{filename}"
                diagram_map[word_key] = rel_path
                extracted += 1

    # ── Hardcoded fallbacks ──
    diagram_map.setdefault("animal cell", "diagrams/animal_cell.jpeg")
    diagram_map.setdefault("plant cell",  "diagrams/plant_cell.jpeg")
    diagram_map.setdefault("cell",        "diagrams/animal_cell.jpeg")

    print(f"\n✅ Done!  Extracted {extracted} diagram zones.")
    print(f"   Skipped (too small/large): {skipped_tiny}")
    print(f"   Skipped (no drawing content): {skipped_no_drawing}")
    print(f"   Unique word keys mapped: {len(diagram_map)}")

    # ── Save JSON map ──
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(diagram_map, f, indent=4, ensure_ascii=False)
    print(f"   Saved {MAP_JSON}")

    # ── Regenerate core_dictionary_diagrams.js ──
    with open(DIAGRAMS_JS, "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary_diagrams.js (Auto-extracted — v2)\n")
        f.write("// =====================================================================\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(diagram_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("  window.DictionaryDiagrams = DictionaryDiagrams;\n")
        f.write("}\n")
    print(f"   Regenerated {DIAGRAMS_JS}")


if __name__ == "__main__":
    extract_diagrams()
