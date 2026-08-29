import fitz
import json

def crop_exact_kidney():
    doc = fitz.open("split_sections/778_PDFsam_Dictionary Book 2.pdf")
    page = doc[4]
    
    # Exact bounding box encompassing all labels and caption cleanly
    # Left: 340 (covers Ureter, Renal vein, Renal artery)
    # Top: 140 (covers top line / Minor calyx)
    # Right: 580 (covers Nephron enlarged, Capsule of kidney, etc.)
    # Bottom: 360 (covers 'Anatomy of the kidney' caption without any bottom definition text)
    crop_rect = fitz.Rect(340, 140, 580, 360)
    
    # Render at 3x resolution (crisp quality)
    mat = fitz.Matrix(3.0, 3.0)
    pix = page.get_pixmap(matrix=mat, clip=crop_rect)
    
    output_path = "diagrams/dict_kidney.png"
    pix.save(output_path)
    print(f"Saved exact diagram to {output_path} ({pix.width}x{pix.height})")

    # Update dictionary_diagrams_map.json
    map_file = "dictionary_diagrams_map.json"
    with open(map_file, "r", encoding="utf-8") as f:
        diag_map = json.load(f)
        
    diag_map["kidney"] = "diagrams/dict_kidney.png"
    sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}
    
    with open(map_file, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
        
    # Sync core_dictionary_diagrams.js
    with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
        f.write("window.DictionaryDiagrams = " + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ";\n")
        
    print("All done and synced!")

if __name__ == "__main__":
    crop_exact_kidney()
