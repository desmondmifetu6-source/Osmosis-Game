import json
import re
from collections import Counter

def validate():
    with open("dictionary_extracted_new.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Total entries loaded: {len(data)}")
    
    # 1. First letter distribution
    first_letters = Counter()
    short_words = 0
    empty_defs = 0
    spaced_words = []
    
    for item in data:
        w = item["word"]
        d = item["definition"]
        if not d:
            empty_defs += 1
        first_char = w[0].upper() if w else "?"
        first_letters[first_char] += 1
        
        # Check for spaced characters in words e.g. "A B A C U S"
        if re.search(r'\b[A-Za-z]\s+[A-Za-z]\s+[A-Za-z]\b', w):
            spaced_words.append(w)
            
    print("\n--- FIRST LETTER DISTRIBUTION ---")
    for letter in sorted(first_letters.keys()):
        print(f"  {letter}: {first_letters[letter]} entries")
        
    print(f"\nEmpty definitions: {empty_defs}")
    print(f"Words with lingering spaced characters: {len(spaced_words)}")
    if spaced_words:
        print("  Sample spaced words:", spaced_words[:10])
        
    print("\n--- SAMPLES ACROSS THE ALPHABET ---")
    sample_letters = ['A', 'B', 'C', 'M', 'P', 'T', 'Z']
    seen_letters = set()
    for item in data:
        char = item["word"][0].upper()
        if char in sample_letters and char not in seen_letters:
            seen_letters.add(char)
            print(f"\n[Letter {char}] Word: '{item['word']}'")
            print(f"  Raw Headword: '{item['raw_headword']}'")
            print(f"  Definition: {item['definition'][:140]}...")

if __name__ == "__main__":
    validate()
