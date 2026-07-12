import json
import re

def clean_dictionary():
    print("Loading extracted dictionary...")
    with open("dictionary_extracted.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    cleaned_data = []
    
    url_pattern = re.compile(r'http|www\.|/[a-zA-Z0-9]+', re.IGNORECASE)
    blacklist = [
        "HEADER", "ADVERT SPACE", "SELECTED BIBLIOGRAPHY", "REFERENCES", 
        "INDEX", "GLOSSARY", "PAGES", "REFERENCE PAGES", "CONCLUSION", 
        "DICTIONARY REFERENCE PAGES"
    ]
    
    print(f"Original word count: {len(data)}")
    
    for item in data:
        word = item.get("word", "").strip()
        definition = item.get("definition", "").strip()
        
        # 1. Existence check
        if not word or not definition:
            continue
            
        # 2. Clean parentheses and their content from the word
        # E.g. "ABALONE (EAR SHELLS; ORMER)" -> "ABALONE"
        word = re.sub(r'\(.*?\)', '', word)
        
        # Replace curly apostrophes/quotes
        word = word.replace('’', "'").replace('‘', "'")
        
        # Normalize whitespace
        word = re.sub(r'\s+', ' ', word).strip()
        
        # 3. Skip prefixes, suffixes, and single letter/character words
        # e.g., "ABEO-", "-ASE", "A"
        if word.startswith('-') or word.endswith('-'):
            continue
        if len(word) <= 1:
            continue
            
        # 4. Skip if the word contains invalid characters
        # We only allow: uppercase letters, numbers, spaces, hyphens, and apostrophes
        if not re.match(r"^[A-Z0-9\s'\-]+$", word, re.IGNORECASE):
            continue
            
        # 5. Skip too long words
        if len(word) > 50:
            continue
            
        # 6. Skip words with too many spaces
        if word.count(" ") > 5:
            continue
            
        # 7. No URLs in word
        if url_pattern.search(word):
            continue
            
        # 8. Must start with a letter (filter out words starting with numbers or symbols)
        if not word[0].isalpha():
            continue
            
        # 9. Blacklist exact garbage words
        word_upper = word.upper()
        if word_upper in blacklist or any(word_upper.startswith(b) for b in blacklist):
            continue
            
        # 10. Clean definition whitespace & junk
        definition = re.sub(r'\s+', ' ', definition).strip()
        if definition == "FIRST WORD" or definition.startswith("LAST WORD"):
            continue
        if "Ref: STEM Dic." in definition or "[BECE " in definition:
            continue
        if len(definition) > 1000 and url_pattern.search(definition[:50]):
            continue
        if len(definition) > 2000 and "www." in definition.lower():
            continue
            
        cleaned_data.append({
            "word": word_upper,
            "definition": definition
        })
        
    # Slicing out intro/outro pages if necessary based on letter structure
    start_idx = 0
    end_idx = len(cleaned_data) - 1
    
    for i, item in enumerate(cleaned_data):
        w = item["word"]
        if w.startswith("A") and len(item["definition"]) > 10:
            start_idx = i
            break
            
    for i in range(len(cleaned_data)-1, -1, -1):
        w = cleaned_data[i]["word"]
        if w.startswith("Z") and len(cleaned_data[i]["definition"]) > 10:
            end_idx = i
            break
            
    final_data = cleaned_data[start_idx:end_idx+1]

    print(f"Cleaned word count: {len(final_data)}")
    print(f"Removed {len(data) - len(final_data)} garbage/malformed entries!")
    
    # Save it back
    with open("dictionary_extracted.json", "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4, ensure_ascii=False)
        
    print("Saved cleaned dictionary!")

if __name__ == "__main__":
    clean_dictionary()
