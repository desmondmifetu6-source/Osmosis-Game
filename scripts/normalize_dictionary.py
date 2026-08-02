import json
import re
import unicodedata
import sys

sys.stdout.reconfigure(encoding='utf-8')

LIGATURE_MAP = {
    '\ufb00': 'ff',
    '\ufb01': 'fi',
    '\ufb02': 'fl',
    '\ufb03': 'ffi',
    '\ufb04': 'ffl',
    '\ufb05': 'st',
    '\ufb06': 'st',
    '…': '...',
    '’': "'",
    '‘': "'",
    '”': '"',
    '“': '"',
    '–': '-',
    '—': '-',
    '\u00a0': ' ',  # non-breaking space
}

def clean_string(text):
    if not text:
        return ""
    # 1. Replace explicit Unicode ligatures & curly quotes
    for k, v in LIGATURE_MAP.items():
        text = text.replace(k, v)
        
    # 2. Normalize Unicode (NFKD)
    # text = unicodedata.normalize('NFKD', text)
    
    # 3. Clean spaces around ligatures / kerning
    text = re.sub(r'fi\s+([a-z])', r'fi\1', text)
    text = re.sub(r'fl\s+([a-z])', r'fl\1', text)
    text = re.sub(r'ff\s+([a-z])', r'ff\1', text)
    text = re.sub(r'ti\s+([a-z])', r'ti\1', text)
    
    # 4. Clean extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def normalize_file(input_file="dictionary_extracted_new.json", output_file="dictionary_extracted_final.json"):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} entries from {input_file}...")
    
    cleaned_entries = []
    seen_words = set()
    
    for item in data:
        raw_word = item["word"]
        raw_hw = item.get("raw_headword", raw_word)
        raw_def = item["definition"]
        
        c_word = clean_string(raw_word)
        c_hw = clean_string(raw_hw)
        c_def = clean_string(raw_def)
        
        # Ensure word is clean uppercase for index matching or title case
        if not c_word or len(c_def) < 5:
            continue
            
        cleaned_entries.append({
            "word": c_word,
            "raw_headword": c_hw,
            "definition": c_def
        })
        
    print(f"Cleaned {len(cleaned_entries)} valid entries.")
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(cleaned_entries, f, indent=2, ensure_ascii=False)
        
    print(f"Saved normalized dictionary to {output_file}")
    
    # Print sample entries across different letters
    sample_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'M', 'P', 'S', 'T', 'Z']
    seen_samples = set()
    print("\n--- SAMPLE CLEANED ENTRIES ---")
    for item in cleaned_entries:
        first_char = item["word"][0].upper()
        if first_char in sample_letters and first_char not in seen_samples:
            seen_samples.add(first_char)
            print(f"\n[{first_char}] Word: '{item['word']}'")
            print(f"    Raw Headword: '{item['raw_headword']}'")
            print(f"    Definition: {item['definition'][:130]}...")

if __name__ == "__main__":
    normalize_file()
