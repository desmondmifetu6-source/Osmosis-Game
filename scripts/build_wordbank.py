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
                # escape quotes & newlines
                w = entry['word'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                d = entry['definition'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                f.write(f'    {{ word: "{w}", definition: "{d}" }},\n')
            f.write("  ],\n")
            
        f.write("};\n\n")
        
        # Attach STEMDictionary API with fast O(1) Map indexing
        f.write("""
// Initialize STEMDictionary helper engine with fast O(1) lookup
(function() {
  const definitionMap = new Map();
  const allWordsArray = [];

  for (const letter in wordBank) {
    const list = wordBank[letter];
    for (let i = 0; i < list.length; i++) {
      const entry = list[i];
      const wLower = entry.word.toLowerCase();
      definitionMap.set(wLower, entry.definition);
      allWordsArray.push(entry);
    }
  }

  const STEMDictionary = {
    wordBank: wordBank,
    getDefinition: function(query) {
      if (!query) return null;
      const normalized = query.trim().toLowerCase();
      return definitionMap.get(normalized) || null;
    },
    getWordsByLetter: function(letter) {
      if (!letter) return [];
      return wordBank[letter.toUpperCase()] || [];
    },
    getAllWords: function() {
      return allWordsArray;
    },
    getRandomLetter: function() {
      const keys = Object.keys(wordBank).filter(k => wordBank[k] && wordBank[k].length > 0);
      return keys[Math.floor(Math.random() * keys.length)];
    }
  };

  if (typeof window !== 'undefined') {
    window.wordBank = wordBank;
    window.STEMDictionary = STEMDictionary;
  }
})();
""")
        
    print("Successfully built core_dictionary.js with STEMDictionary API!")

if __name__ == "__main__":
    build_wordbank()
