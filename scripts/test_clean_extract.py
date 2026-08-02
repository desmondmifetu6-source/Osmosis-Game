import fitz
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def clean_headword(hw):
    if not hw:
        return ""
    # Collapse spaced characters/pairs in headwords like "AC ET AM ID OP HE NO L" -> "ACETAMIDOPHENOL"
    prev = None
    curr = hw
    while prev != curr:
        prev = curr
        curr = re.sub(r'(\b[A-Za-z0-9]{1,2})\s+([A-Za-z0-9]{1,2}\b)', r'\1\2', curr)
    
    curr = re.sub(r'\s+', ' ', curr).strip()
    return curr

def clean_text(text):
    if not text:
        return ""
    
    # Common PDF ligature spacing fixes
    text = re.sub(r'fi\s+([a-z])', r'fi\1', text)
    text = re.sub(r'fl\s+([a-z])', r'fl\1', text)
    text = re.sub(r'ff\s+([a-z])', r'ff\1', text)
    text = re.sub(r'ti\s+([a-z])', r'ti\1', text)
    
    # Fix subscript/superscript space gaps in units & chemical formulas (e.g., C 5 H 11 -> C5H11, g/cm 3 -> g/cm3)
    text = re.sub(r'([A-Z])\s+([0-9]+)', r'\1\2', text)
    text = re.sub(r'(cm|m|mm|g)\s+([23])\b', r'\1\2', text)
    
    # Fix multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def test_extract(pdf_path, max_entries=None):
    doc = fitz.open(pdf_path)
    entries = []
    
    current_headword = None
    current_raw_headword = None
    current_hw_spans = []
    current_def_spans = []
    
    # Dictionary body starts on Page 73 (0-indexed 72) and ends on Page 1473 (0-indexed 1472)
    start_page = 72
    end_page = 1473
    
    print(f"Extracting dictionary pages {start_page+1} to {end_page}...")
    
    for page_num in range(start_page, end_page):
        if (page_num - start_page) % 100 == 0:
            print(f"Processing page {page_num+1}/{end_page} (Extracted {len(entries)} words so far)...")
            
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if b.get("type") != 0:
                continue
                
            # Filter top margin (headers) and bottom margin (footers/page numbers)
            bbox = b.get("bbox", (0, 0, 0, 0))
            if bbox[1] < 80 or bbox[3] > 815:
                continue
                
            for line in b["lines"]:
                line_spans = line["spans"]
                if not line_spans:
                    continue
                    
                full_line_text = "".join(s["text"] for s in line_spans).strip()
                
                # Filter page headers/footers
                if "Science, Technology And Mathematics Dictionary" in full_line_text:
                    continue
                if full_line_text.startswith("HEADER:") or full_line_text.isdigit():
                    continue
                    
                for s in line_spans:
                    stext = s["text"]
                    if not stext.strip():
                        continue
                        
                    font = s["font"]
                    color = s["color"]
                    flags = s["flags"]
                    
                    # Is this a Headword span?
                    # Color 35533 (blue) and Bold (flags 16 or Tahoma-Bold)
                    is_blue_bold = (color == 35533) and (flags & 16 or "Bold" in font)
                    
                    if is_blue_bold:
                        # Accumulate headword span
                        current_hw_spans.append(stext)
                        if ":" in stext:
                            # Complete headword reached!
                            raw_hw = "".join(current_hw_spans).strip()
                            clean_hw = re.sub(r':$', '', raw_hw).strip()
                            clean_hw = clean_headword(clean_hw)
                            
                            # Save previous entry if exists
                            if current_headword and current_def_spans:
                                raw_def = " ".join(current_def_spans)
                                clean_def = clean_text(raw_def)
                                if len(clean_def) > 3:
                                    entries.append({
                                        "word": current_headword,
                                        "raw_headword": current_raw_headword,
                                        "definition": clean_def
                                    })
                                
                                if max_entries and len(entries) >= max_entries:
                                    return entries
                                    
                            # Extract main word (e.g. "ABACUS" from "ABACUS (CALCULATOR):")
                            main_word = clean_hw.split('(')[0].split('[')[0].strip()
                            if not main_word:
                                main_word = clean_hw
                                
                            current_headword = main_word
                            current_raw_headword = clean_hw
                            current_def_spans = []
                            current_hw_spans = []
                    else:
                        if current_headword is not None:
                            current_def_spans.append(stext)
                            
    if current_headword and current_def_spans:
        raw_def = " ".join(current_def_spans)
        clean_def = clean_text(raw_def)
        if len(clean_def) > 3:
            entries.append({
                "word": current_headword,
                "raw_headword": current_raw_headword,
                "definition": clean_def
            })
        
    return entries

if __name__ == "__main__":
    extracted = test_extract("Dictionary Book 2.pdf")
    print(f"\nExtraction COMPLETE! Extracted total of {len(extracted)} clean dictionary entries.")
    
    out_file = "dictionary_extracted_new.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(extracted, f, indent=2, ensure_ascii=False)
        
    print(f"Saved complete cleaned dictionary to {out_file}")

