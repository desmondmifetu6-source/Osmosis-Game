import fitz
import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def extract_all_vector_diagrams(pdf_path, output_dir="diagrams"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    diagram_map = {}
    total_diagrams_extracted = 0
    
    for page_num in range(40, len(doc)):
        if page_num % 100 == 0:
            print(f"Processing page {page_num}/{len(doc)}...")
            
        page = doc.load_page(page_num)
        
        # 1. Get Dictionary Entry Words on this page (Blue + Bold)
        blocks = page.get_text("dict")["blocks"]
        words_on_page = []
        for b in blocks:
            if b.get('type') == 0:  # Text block
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                        if s["color"] == 35533 and s["flags"] & 16:
                            clean_w = text.replace(":", "").strip()
                            # Filter out single letters or noise
                            if len(clean_w) > 1 and not clean_w.startswith("A Science") and not clean_w.startswith("Science"):
                                words_on_page.append({
                                    "word": clean_w,
                                    "bbox": s["bbox"],
                                    "x0": s["bbox"][0],
                                    "y0": s["bbox"][1]
                                })
                                
        if not words_on_page:
            continue
            
        # 2. Get Vector Drawings
        drawings = page.get_drawings()
        candidate_rects = []
        for d in drawings:
            r = d["rect"]
            # Exclude full page lines / column borders
            if r.width < 450 and r.height < 650:
                # Exclude thin lines
                if r.width >= 35 and r.height >= 30:
                    # Content area bounds
                    if 50 <= r.y0 and r.y1 <= 750 and 20 <= r.x0 and r.x1 <= 670:
                        # Exclude header/footer logos
                        if not ((r.x0 < 70 or r.x0 > 600) and (240 < r.y0 < 300) and (r.height < 65)):
                            candidate_rects.append(r)
                            
        if not candidate_rects:
            continue
            
        # 3. Merge overlapping / nearby drawing rects
        merged_rects = []
        for r in candidate_rects:
            matched = False
            for i, m in enumerate(merged_rects):
                # If rects are close (within 25 pt) and in same column region
                if abs(r.x0 - m.x0) < 180 and (m.y0 - 25 <= r.y0 <= m.y1 + 25 or r.y0 - 25 <= m.y0 <= r.y1 + 25):
                    merged_rects[i] = m | r
                    matched = True
                    break
            if not matched:
                merged_rects.append(r)
                
        # 4. Map each merged diagram rect to closest entry word
        for rect in merged_rects:
            # Must be substantial size
            if rect.width < 40 or rect.height < 35:
                continue
                
            img_x0 = rect.x0
            img_y0 = rect.y0
            
            # Find words in same column (Left x < 320 vs Right x >= 320)
            same_col_words = [
                w for w in words_on_page 
                if (w["x0"] < 320 and img_x0 < 320) or (w["x0"] >= 320 and img_x0 >= 320)
            ]
            target_words = same_col_words if same_col_words else words_on_page
            
            # Find word above diagram or closest vertically
            words_above = [w for w in target_words if w["y0"] <= img_y0 + 25]
            if words_above:
                closest_word = max(words_above, key=lambda w: w["y0"])
            else:
                closest_word = min(target_words, key=lambda w: abs(w["y0"] - img_y0))
                
            word_name = closest_word["word"]
            word_slug = slugify(word_name)
            if not word_slug:
                continue
                
            file_filename = f"dict_{word_slug}.png"
            file_path = os.path.join(output_dir, file_filename)
            
            # Add small padding around diagram
            crop_rect = fitz.Rect(
                max(0, rect.x0 - 8),
                max(0, rect.y0 - 8),
                min(page.rect.width, rect.x1 + 8),
                min(page.rect.height, rect.y1 + 8)
            )
            
            # Render crisp 150 DPI PNG
            pix = page.get_pixmap(clip=crop_rect, dpi=150)
            pix.save(file_path)
            
            clean_key = word_name.lower().strip()
            diagram_map[clean_key] = f"diagrams/{file_filename}"
            total_diagrams_extracted += 1
            
    print(f"Extracted {total_diagrams_extracted} vector diagrams for {len(diagram_map)} unique dictionary words!")
    
    # Save JSON map
    with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
        json.dump(diagram_map, f, indent=4)
        
    # Generate updated core_dictionary_diagrams.js
    with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary_diagrams.js (Auto-extracted Dictionary Diagrams)\n")
        f.write("// =====================================================================\n\n")
        f.write("const DictionaryDiagrams = ")
        
        # Include hardcoded cell fallbacks
        full_map = dict(diagram_map)
        full_map["animal cell"] = "diagrams/animal_cell.jpeg"
        full_map["plant cell"] = "diagrams/plant_cell.jpeg"
        if "cell" not in full_map:
            full_map["cell"] = "diagrams/animal_cell.jpeg"
            
        json.dump(full_map, f, indent=4)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("  window.DictionaryDiagrams = DictionaryDiagrams;\n")
        f.write("}\n")
        
    print("Successfully updated core_dictionary_diagrams.js!")

if __name__ == "__main__":
    extract_all_vector_diagrams("Dictionary Book 2.pdf")
