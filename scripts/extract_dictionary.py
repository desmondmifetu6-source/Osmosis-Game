import fitz
import json
import sys

def extract_dictionary(pdf_path, output_json="dictionary_extracted.json"):
    print(f"Opening {pdf_path}...")
    doc = fitz.open(pdf_path)
    
    dictionary = []
    current_word = None
    current_def = ""
    
    print(f"Total pages: {len(doc)}")
    
    # Let's parse pages 40 to 1400 (skip intro and index)
    for page_num in range(40, len(doc)):
        if page_num % 50 == 0:
            print(f"Processing page {page_num}...")
            
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if b['type'] == 0:  # Text block
                for l in b["lines"]:
                    for s in l["spans"]:
                        text = s["text"].strip()
                        if not text:
                            continue
                            
                        # Detect Dictionary Word: 
                        # Color 35533 is the specific blue used in the PDF
                        # Flags 16 means Bold
                        if s["color"] == 35533 and s["flags"] & 16:
                            # Save the previous word if it exists
                            if current_word:
                                dictionary.append({
                                    "word": current_word.replace(":", "").strip(),
                                    "definition": current_def.strip()
                                })
                            
                            current_word = text
                            current_def = ""
                        else:
                            # It's part of the definition
                            if current_word:
                                current_def += " " + text
                                
    # Append the last word
    if current_word:
        dictionary.append({
            "word": current_word.replace(":", "").strip(),
            "definition": current_def.strip()
        })
        
    print(f"Extraction complete! Found {len(dictionary)} words.")
    
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=4, ensure_ascii=False)
        
    print(f"Saved to {output_json}")

if __name__ == "__main__":
    extract_dictionary("Dictionary Book 2.pdf")
