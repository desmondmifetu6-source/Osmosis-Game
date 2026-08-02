import json

def test_search():
    with open("dictionary_extracted_final.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Total dictionary entries: {len(data)}")
    
    # Build fast lookup map
    lookup = {}
    for item in data:
        w = item["word"].upper().strip()
        lookup[w] = item
        
    test_words = ["VALINE", "ABACUS", "ALANINE", "PARACETAMOL", "ATOM BOMB", "DNA", "GRAVITY", "PHOTOSYNTHESIS", "OXYGEN", "Z BOSON"]
    
    print("\n--- TESTING WORD SEARCH LOOKUP ---")
    for tw in test_words:
        found = False
        # Exact match or startswith match
        if tw in lookup:
            item = lookup[tw]
            print(f"\n[EXACT MATCH] '{tw}' -> Word: '{item['word']}'")
            print(f"  Definition: {item['definition'][:120]}...")
            found = True
        else:
            # Partial match search
            matches = [item for item in data if tw in item['word'].upper() or tw in item['raw_headword'].upper()]
            if matches:
                item = matches[0]
                print(f"\n[PARTIAL MATCH] '{tw}' matched '{item['word']}' (Raw: '{item['raw_headword']}')")
                print(f"  Definition: {item['definition'][:120]}...")
                found = True
                
        if not found:
            print(f"\n[NOT FOUND] '{tw}'")

if __name__ == "__main__":
    test_search()
