import json
import re

def fix_spaced_word(text):
    if not text:
        return text
    # Replace double spaces with a placeholder tag __WORD_SEP__
    temp = re.sub(r'\s{2,}', ' __WORD_SEP__ ', text)
    # Remove single spaces between individual single letters (e.g. "a c u p u n c t u r e" -> "acupuncture")
    fixed = re.sub(r'(?<=\b[a-zA-Z0-9])\s+(?=[a-zA-Z0-9]\b)', '', temp)
    # Restore double space word boundaries as a single space
    fixed = fixed.replace('__WORD_SEP__', ' ')
    # Normalize remaining spaces
    fixed = re.sub(r'\s+', ' ', fixed).strip()
    return fixed

def clean_all_dictionaries():
    print("1. Cleaning dictionary_extracted.json...")
    with open("dictionary_extracted.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    fixed_data = []
    fixed_count = 0
    for item in data:
        orig_word = item["word"]
        clean_w = fix_spaced_word(orig_word)
        if clean_w != orig_word:
            fixed_count += 1
        fixed_data.append({
            "word": clean_w,
            "definition": item["definition"]
        })
        
    print(f"Fixed {fixed_count} spaced-out entry words in dictionary_extracted.json!")
    with open("dictionary_extracted.json", "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, indent=4, ensure_ascii=False)
        
    print("2. Cleaning dictionary_diagrams_map.json...")
    with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
        diag_map = json.load(f)
        
    fixed_diag_map = {}
    for key, path in diag_map.items():
        clean_k = fix_spaced_word(key).lower()
        fixed_diag_map[clean_k] = path
        
    with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
        json.dump(fixed_diag_map, f, indent=4, ensure_ascii=False)
        
    print("3. Updating core_dictionary_diagrams.js...")
    with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary_diagrams.js (Cleaned Dictionary Diagrams)\n")
        f.write("// =====================================================================\n\n")
        f.write("const DictionaryDiagrams = ")
        
        full_map = dict(fixed_diag_map)
        full_map["animal cell"] = "diagrams/animal_cell.jpeg"
        full_map["plant cell"] = "diagrams/plant_cell.jpeg"
        if "cell" not in full_map:
            full_map["cell"] = "diagrams/animal_cell.jpeg"
            
        json.dump(full_map, f, indent=4)
        f.write(";\n\n")
        f.write("if (typeof window !== 'undefined') {\n")
        f.write("  window.DictionaryDiagrams = DictionaryDiagrams;\n")
        f.write("}\n")

    print("Cleaning complete!")

if __name__ == "__main__":
    clean_all_dictionaries()
