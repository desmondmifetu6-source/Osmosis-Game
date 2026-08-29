import fitz
import json
import os

def update_kidney():
    pdf_path = "split_sections/778_PDFsam_Dictionary Book 2.pdf"
    if not os.path.exists(pdf_path):
        pdf_path = "Dictionary Book 2.pdf"
    
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    
    target_page = None
    target_rect = None
    
    for i, page in enumerate(doc):
        text_instances = page.search_for("Anatomy of the kidney")
        if text_instances:
            print(f"Found 'Anatomy of the kidney' on page {i}")
            target_page = page
            # The caption is at text_instances[0]
            caption_rect = text_instances[0]
            
            # The drawing is directly above this caption
            # Let's get drawings or search for diagram rect
            drawings = page.get_drawings()
            diag_rect = None
            for d in drawings:
                r = d["rect"]
                if r.y1 <= caption_rect.y1 + 10 and r.y0 >= caption_rect.y0 - 450:
                    if r.width > 100 and r.height > 100:
                        if diag_rect is None:
                            diag_rect = fitz.Rect(r)
                        else:
                            diag_rect |= r
                            
            if diag_rect:
                # Include caption text area and some padding
                crop_rect = fitz.Rect(
                    min(diag_rect.x0, caption_rect.x0) - 15,
                    diag_rect.y0 - 15,
                    max(diag_rect.x1, caption_rect.x1) + 15,
                    caption_rect.y1 + 15
                )
            else:
                # Fallback based on caption position
                crop_rect = fitz.Rect(
                    caption_rect.x0 - 120,
                    caption_rect.y0 - 320,
                    caption_rect.x1 + 120,
                    caption_rect.y1 + 15
                )
            target_rect = crop_rect
            break

    if target_page and target_rect:
        # Render high-resolution (3x zoom)
        mat = fitz.Matrix(3.0, 3.0)
        pix = target_page.get_pixmap(matrix=mat, clip=target_rect)
        output_path = "diagrams/dict_kidney.png"
        pix.save(output_path)
        print(f"Saved crisp kidney diagram to {output_path} ({pix.width}x{pix.height})")
    else:
        print("Could not find kidney diagram automatically in PDF.")
        return

    # Update dictionary_diagrams_map.json
    map_file = "dictionary_diagrams_map.json"
    with open(map_file, "r", encoding="utf-8") as f:
        diag_map = json.load(f)
        
    diag_map["kidney"] = "diagrams/dict_kidney.png"
    # Sort alphabetically
    sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}
    
    with open(map_file, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    print("Updated dictionary_diagrams_map.json with 'kidney'")

    # Also sync core_dictionary_diagrams.js
    js_content = "window.DictionaryDiagrams = " + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ";\n"
    with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("Synchronized core_dictionary_diagrams.js successfully!")

if __name__ == "__main__":
    update_kidney()
