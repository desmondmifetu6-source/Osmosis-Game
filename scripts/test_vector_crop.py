import fitz
import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

doc = fitz.open("Dictionary Book 2.pdf")
output_dir = "diagrams"

# Let's inspect page 75 (Abdomen / Abaxial / ABC Model)
page_num = 74 # 0-indexed page 75
page = doc.load_page(page_num)

# Get vector drawing rects
drawings = page.get_drawings()
print(f"Page {page_num+1} total drawings: {len(drawings)}")

# Group drawing bounding boxes
# Exclude lines/rectangles that span the whole page width or height (page borders/column dividers)
diagram_rects = []
for d in drawings:
    r = d["rect"]
    # Filter out page borders/header lines
    if r.width < 500 and r.height < 700:
        if r.y0 > 50 and r.y1 < 750:
            if r.width > 30 or r.height > 30:
                diagram_rects.append(r)

print(f"Filtered candidate drawing rects: {len(diagram_rects)}")

if diagram_rects:
    # Union of bounding boxes that overlap or are close to each other
    merged_rects = []
    for r in diagram_rects:
        matched = False
        for i, m in enumerate(merged_rects):
            # Check if rects are near each other (within 30 points)
            if abs(r.x0 - m.x0) < 150 and (m.y0 - 40 <= r.y0 <= m.y1 + 40 or r.y0 - 40 <= m.y0 <= r.y1 + 40):
                merged_rects[i] = m | r # Union rect
                matched = True
                break
        if not matched:
            merged_rects.append(r)
            
    print(f"Merged diagram bounding boxes: {len(merged_rects)}")
    for idx, rect in enumerate(merged_rects):
        print(f"Diagram {idx+1}: {rect}")
        # Add padding around diagram
        crop_rect = fitz.Rect(max(0, rect.x0 - 10), max(0, rect.y0 - 10), min(page.rect.width, rect.x1 + 10), min(page.rect.height, rect.y1 + 10))
        pix = page.get_pixmap(clip=crop_rect, dpi=150)
        pix.save(f"{output_dir}/test_page75_diag{idx+1}.png")
        print(f"Saved {output_dir}/test_page75_diag{idx+1}.png")
