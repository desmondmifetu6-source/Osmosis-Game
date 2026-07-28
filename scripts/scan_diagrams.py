import fitz
import os
import json

def scan_images(pdf_path):
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    print(f"Total pages: {len(doc)}")
    
    diagram_count = 0
    pages_with_images = []
    
    # We check pages 40 to len(doc)
    for page_num in range(40, len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        page_images = []
        words_on_page = []
        
        for b in blocks:
            if b.get('type') == 0: # Text
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                        if s["color"] == 35533 and s["flags"] & 16:
                            words_on_page.append({
                                "word": text.replace(":", "").strip(),
                                "bbox": s["bbox"]
                            })
            elif b.get('type') == 1: # Image
                page_images.append({
                    "bbox": b["bbox"],
                    "ext": b.get("ext", "png"),
                    "width": b.get("width"),
                    "height": b.get("height")
                })
                
        if page_images:
            diagram_count += len(page_images)
            pages_with_images.append({
                "page": page_num + 1,
                "image_count": len(page_images),
                "words": [w["word"] for w in words_on_page[:10]],
                "images": page_images
            })
            
    print(f"Total images found across pages: {diagram_count}")
    print(f"Total pages with images: {len(pages_with_images)}")
    
    with open("diagram_scan_summary.json", "w", encoding="utf-8") as f:
        json.dump(pages_with_images[:20], f, indent=2)
        
    print("Saved sample summary to diagram_scan_summary.json")

if __name__ == "__main__":
    scan_images("Dictionary Book 2.pdf")
