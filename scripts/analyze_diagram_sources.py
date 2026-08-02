import fitz
import json
import re

def analyze_pdf_diagrams(pdf_path):
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    print(f"Total pages in PDF: {total_pages}")

    raster_count = 0
    vector_cluster_count = 0
    words_with_diagrams = {}
    malformed_keys = []

    # Check mapping in current core_dictionary_diagrams.js / dictionary_diagrams_map.json
    try:
        with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
            existing_map = json.load(f)
            print(f"Existing mapped diagrams: {len(existing_map)}")
            for w in existing_map:
                if w.endswith(")") or len(w) < 3 or re.search(r'[^a-zA-Z0-9\s\-\(\)]', w):
                    malformed_keys.append(w)
    except Exception as e:
        print("No existing map:", e)

    print(f"Malformed key samples ({len(malformed_keys)} found): {malformed_keys[:10]}")

if __name__ == "__main__":
    analyze_pdf_diagrams("Dictionary Book 2.pdf")
