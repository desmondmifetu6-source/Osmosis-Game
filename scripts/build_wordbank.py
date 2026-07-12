import json
import string

def build_wordbank():
    with open("dictionary_extracted.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        
    wordBank = {letter: [] for letter in string.ascii_uppercase}
    
    for item in data:
        word = item["word"]
        definition = item["definition"]
        if not word:
            continue
            
        first_char = word[0].upper()
        if first_char in wordBank:
            wordBank[first_char].append({
                "word": word.lower(),
                "definition": definition
            })
            
    # Write to core_dictionary.js
    with open("core_dictionary.js", "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary.js (The Game's Library)\n")
        f.write("// =====================================================================\n\n")
        f.write("const wordBank = {\n")
        
        for letter in sorted(wordBank.keys()):
            f.write(f'  "{letter}": [\n')
            for entry in wordBank[letter]:
                # escape quotes
                w = entry['word'].replace('"', '\\"').replace('\n', ' ')
                d = entry['definition'].replace('"', '\\"').replace('\n', ' ')
                f.write(f'    {{ word: "{w}", definition: "{d}" }},\n')
            f.write("  ],\n")
            
        f.write("};\n")
        
    print("Successfully built core_dictionary.js with massive data!")

if __name__ == "__main__":
    build_wordbank()
