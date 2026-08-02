import fitz
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def deep_scan_diagrams(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Scanning {total_pages} pages in {pdf_path}...")

    total_raster = 0
    total_vector = 0
    word_to_diagram = {}

    for page_num in range(40, total_pages - 15):
        page = doc[page_num]
        
        # 1. Extract entry words on this page
        blocks = page.get_text("dict")["blocks"]
        words_on_page = []
        for b in blocks:
            if b.get('type') == 0:
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                        # Entry word detection: blue color (35533) + bold flag (16)
                        if s["color"] == 35533 and (s["flags"] & 16):
                            clean_w = re.sub(r'[\:\(\)]', '', text).strip()
                            if len(clean_w) > 1 and not clean_w.startswith("Science") and not clean_w.startswith("A Science"):
                                words_on_page.append({
                                    "raw": text,
                                    "clean": clean_w,
                                    "bbox": s["bbox"],
                                    "x0": s["bbox"][0],
                                    "y0": s["bbox"][1]
                                })

        if not words_on_page:
            continue

        # 2. Check raster image blocks
        for b in blocks:
            if b.get('type') == 1:
                w = b.get("width", 0)
                h = b.get("height", 0)
                bbox = b.get("bbox", [0, 0, 0, 0])
                if w >= 60 and h >= 60 and bbox[1] > 50 and bbox[3] < 760:
                    total_raster += 1

        # 3. Check vector drawing bounding rects
        drawings = page.get_drawings()
        candidate_rects = []
        for d in drawings:
            r = d["rect"]
            if 35 <= r.width < 450 and 30 <= r.height < 600:
                if 50 <= r.y0 and r.y1 <= 750 and 20 <= r.x0 and r.x1 <= 670:
                    candidate_rects.append(r)

        if candidate_rects:
            # Merge nearby drawing rects
            merged = []
            for r in candidate_rects:
                matched = False
                for i, m in enumerate(merged):
                    if abs(r.x0 - m.x0) < 180 and (m.y0 - 20 <= r.y0 <= m.y1 + 20 or r.y0 - 20 <= m.y0 <= r.y1 + 20):
                        merged[i] = m | r
                        matched = True
                        break
                if not matched:
                    merged.append(r)

            for rect in merged:
                if rect.width >= 40 and rect.height >= 35:
                    total_vector += 1
                    # Associate with closest word in same column
                    img_x0 = rect.x0
                    img_y0 = rect.y0
                    same_col = [w for w in words_on_page if (w["x0"] < 320 and img_x0 < 320) or (w["x0"] >= 320 and img_x0 >= 320)]
                    target_words = same_col if same_col else words_on_page
                    words_above = [w for w in target_words if w["y0"] <= img_y0 + 25]
                    closest = max(words_above, key=lambda w: w["y0"]) if words_above else min(target_words, key=lambda w: abs(w["y0"] - img_y0))
                    
                    slug = slugify(closest["clean"])
                    if slug and slug not in word_to_diagram:
                        word_to_diagram[slug] = {
                            "word": closest["clean"],
                            "page": page_num + 1,
                            "bbox": [rect.x0, rect.y0, rect.x1, rect.y1]
                        }

    print(f"\n--- SCAN RESULTS ---")
    print(f"Total Raster Images found: {total_raster}")
    print(f"Total Vector Diagram clusters found: {total_vector}")
    print(f"Total Unique Words mapped with diagrams: {len(word_to_diagram)}")

if __name__ == "__main__":
    deep_scan_diagrams("Dictionary Book 2.pdf")
