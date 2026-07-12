import sys
try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF (fitz) is not installed. Please run: pip install pymupdf")
    sys.exit(1)

def test_extraction(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc.load_page(page_num)
    
    # Extract raw dictionaries
    blocks = page.get_text("dict")["blocks"]
    
    print(f"--- Analyzing Page {page_num} ---")
    
    for b in blocks:
        if b['type'] == 0:  # text block
            for l in b["lines"]:
                for s in l["spans"]:
                    text = s["text"].strip()
                    if text:
                        print(f"TEXT: {text[:50]}... | FONT: {s['font']} | SIZE: {s['size']:.1f} | COLOR: {s['color']} | FLAGS: {s['flags']}")

if __name__ == "__main__":
    test_extraction("Dictionary Book 2.pdf", 100) # Test page 100
