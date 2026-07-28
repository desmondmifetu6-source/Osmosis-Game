import fitz
import os
import json
import re

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '_', text)
    return text.strip('_')

def extract_diagrams(pdf_path, output_dir="diagrams"):
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
        blocks = page.get_text("dict")["blocks"]
        
        words_with_bbox = []
        image_blocks = []
        
        for b in blocks:
            if b.get('type') == 0:  # Text block
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                        # Detect Dictionary Entry Word (Blue + Bold)
                        if s["color"] == 35533 and s["flags"] & 16:
                            clean_w = text.replace(":", "").strip()
                            if len(clean_w) > 1:
                                words_with_bbox.append({
                                    "word": clean_w,
                                    "bbox": s["bbox"], # (x0, y0, x1, y1)
                                    "y": s["bbox"][1]
                                })
            elif b.get('type') == 1:  # Image block
                w = b.get("width", 0)
                h = b.get("height", 0)
                bbox = b.get("bbox", [0, 0, 0, 0])
                
                # Filter out header/footer logos, small icons, page decor
                # Real diagrams usually have width & height >= 80px and are not on extreme page edges
                if w >= 80 and h >= 80:
                    # Ignore headers (y < 60) and footers (y > 750)
                    if bbox[1] > 60 and bbox[3] < 760:
                        image_blocks.append({
                            "bbox": bbox,
                            "width": w,
                            "height": h,
                            "ext": b.get("ext", "png"),
                            "image_bytes": b.get("image")
                        })
                        
        # Match each diagram to the closest preceding or nearby word entry
        for img in image_blocks:
            if not words_with_bbox or not img.get("image_bytes"):
                continue
                
            img_y0 = img["bbox"][1]
            img_x0 = img["bbox"][0]
            
            # Find words on the same side of the page (left column vs right column)
            # Left column x < 300, Right column x >= 300
            same_col_words = [
                w for w in words_with_bbox 
                if (w["bbox"][0] < 300 and img_x0 < 300) or (w["bbox"][0] >= 300 and img_x0 >= 300)
            ]
            
            target_words = same_col_words if same_col_words else words_with_bbox
            
            # Find the word closest above the image, or closest overall
            words_above = [w for w in target_words if w["y"] <= img_y0 + 20]
            if words_above:
                closest_word = max(words_above, key=lambda w: w["y"])
            else:
                closest_word = min(target_words, key=lambda w: abs(w["y"] - img_y0))
                
            word_name = closest_word["word"]
            word_slug = slugify(word_name)
            
            if not word_slug:
                continue
                
            file_filename = f"dict_{word_slug}.{img['ext']}"
            file_path = os.path.join(output_dir, file_filename)
            
            # Write image to disk
            with open(file_path, "wb") as f:
                f.write(img["image_bytes"])
                
            extracted_diagrams[word_name.lower()] = f"diagrams/{file_filename}"
            extracted_count += 1
            
    print(f"Finished extracting diagrams! Extracted {extracted_count} diagrams.")
    
    with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
        json.dump(extracted_diagrams, f, indent=4)
        
    print(f"Saved diagram map to dictionary_diagrams_map.json with {len(extracted_diagrams)} word mappings.")

if __name__ == "__main__":
    extract_diagrams("Dictionary Book 2.pdf")
