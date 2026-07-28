import fitz
import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def extract_all_diagrams(pdf_path, output_dir="diagrams"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    extracted_diagrams = {} # word -> image path
    extracted_count = 0
    
    for page_num in range(40, len(doc)):
        if page_num % 100 == 0:
            print(f"Processing page {page_num}/{len(doc)}...")
            
        page = doc.load_page(page_num)
        
        # Get entry words on this page
        blocks = page.get_text("dict")["blocks"]
        words_with_bbox = []
        for b in blocks:
            if b.get('type') == 0:  # Text block
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                        if s["color"] == 35533 and s["flags"] & 16:
                            clean_w = text.replace(":", "").strip()
                            if len(clean_w) > 1:
                                words_with_bbox.append({
                                    "word": clean_w,
                                    "bbox": s["bbox"],
                                    "y": s["bbox"][1]
                                })
                                
        image_list = page.get_images(full=True)
        if not image_list or not words_with_bbox:
            continue
            
        for img_info in image_list:
            xref = img_info[0]
            base_image = doc.extract_image(xref)
            if not base_image:
                continue
                
            w = base_image["width"]
            h = base_image["height"]
            ext = base_image["ext"]
            image_bytes = base_image["image"]
            
            # Get placement rect on page
            rects = page.get_image_rects(xref)
            if not rects:
                continue
                
            rect = rects[0] # (x0, y0, x1, y1)
            
            # Filter out tiny icons, logos, header/footer decors
            # Real figures usually have width & height >= 60 and are within page bounds
            if w >= 60 and h >= 60:
                if rect.y0 > 50 and rect.y1 < 760:
                    # Ignore repetitive header logos by checking bounding box width/height or position
                    # Header logo is around x0=20 or x0=615 and y0=250, height around 57
                    if (rect.x0 < 65 or rect.x0 > 600) and (240 < rect.y0 < 300) and (rect.height < 65):
                        continue
                        
                    img_y0 = rect.y0
                    img_x0 = rect.x0
                    
                    # Same column words
                    same_col_words = [
                        w for w in words_with_bbox 
                        if (w["bbox"][0] < 300 and img_x0 < 300) or (w["bbox"][0] >= 300 and img_x0 >= 300)
                    ]
                    target_words = same_col_words if same_col_words else words_with_bbox
                    
                    words_above = [w for w in target_words if w["y"] <= img_y0 + 20]
                    if words_above:
                        closest_word = max(words_above, key=lambda w: w["y"])
                    else:
                        closest_word = min(target_words, key=lambda w: abs(w["y"] - img_y0))
                        
                    word_name = closest_word["word"]
                    word_slug = slugify(word_name)
                    if not word_slug:
                        continue
                        
                    file_filename = f"dict_{word_slug}.{ext}"
                    file_path = os.path.join(output_dir, file_filename)
                    
                    with open(file_path, "wb") as f:
                        f.write(image_bytes)
                        
                    extracted_diagrams[word_name.lower()] = f"diagrams/{file_filename}"
                    extracted_count += 1
                    
    print(f"Finished! Extracted {extracted_count} diagram files.")
    
    with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
        json.dump(extracted_diagrams, f, indent=4)
        
    print(f"Saved diagram map with {len(extracted_diagrams)} word mappings to dictionary_diagrams_map.json.")

if __name__ == "__main__":
    extract_all_diagrams("Dictionary Book 2.pdf")
