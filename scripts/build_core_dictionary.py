import json
import string
import re

def build_core_dictionary(input_json="dictionary_extracted_final.json", output_js="core_dictionary.js", output_json="dictionary.json"):
    print(f"Reading {input_json}...")
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print(f"Loaded {len(data)} raw entries.")
    
    wordBank = {letter: [] for letter in string.ascii_uppercase}
    
    processed_count = 0
    synonym_count = 0
    
    for item in data:
        word = item["word"].strip()
        raw_hw = item.get("raw_headword", word).strip()
        definition = item["definition"].strip()
        
        if not word or not definition:
            continue
            
        first_char = word[0].upper()
        if first_char not in wordBank:
            # Handle non-alpha first chars like numbers or symbols
            first_char = 'A' if not first_char.isalnum() else first_char
            if first_char not in wordBank:
                wordBank[first_char] = []
                
        # Extract synonyms from raw_headword e.g. "A BOMB (A-BOMB; ATOM BOMB; ATOMIC BOMB; NUCLEAR BOMB)"
        synonyms = []
        paren_matches = re.findall(r'\((.*?)\)', raw_hw)
        bracket_matches = re.findall(r'\[(.*?)\]', raw_hw)
        
        for group in paren_matches + bracket_matches:
            # Split by ';' or ',' or '/'
            parts = re.split(r'[;,/]', group)
            for p in parts:
                p_clean = p.strip()
                if len(p_clean) >= 2 and not p_clean.lower().startswith("see ") and not p_clean.isdigit():
                    synonyms.append(p_clean.lower())
                    synonym_count += 1
                    
        wordBank[first_char].append({
            "word": word.lower(),
            "raw_headword": raw_hw,
            "synonyms": synonyms,
            "definition": definition
        })
        processed_count += 1
        
    print(f"Processed {processed_count} main entries and identified {synonym_count} synonyms/alias terms.")
    
    # Save formatted dictionary.json
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(wordBank, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON wordbank to {output_json}")
    
    # Write core_dictionary.js
    with open(output_js, "w", encoding="utf-8") as f:
        f.write("// =====================================================================\n")
        f.write("// FILE: core_dictionary.js (Osmosis STEM Game Dictionary Library)\n")
        f.write("// =====================================================================\n\n")
        f.write("const wordBank = {\n")
        
        for letter in sorted(wordBank.keys()):
            f.write(f'  "{letter}": [\n')
            for entry in wordBank[letter]:
                w = entry['word'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                raw_hw = entry['raw_headword'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                d = entry['definition'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
                syns_json = json.dumps(entry['synonyms'], ensure_ascii=False)
                f.write(f'    {{ word: "{w}", raw: "{raw_hw}", synonyms: {syns_json}, definition: "{d}" }},\n')
            f.write("  ],\n")
            
        f.write("};\n\n")
        
        # STEMDictionary O(1) Engine with Synonym & Fuzzy Fallback
        f.write("""
(function() {
  const definitionMap = new Map();
  const allWordsArray = [];

  for (const letter in wordBank) {
    const list = wordBank[letter];
    for (let i = 0; i < list.length; i++) {
      const entry = list[i];
      const wLower = entry.word.toLowerCase();
      definitionMap.set(wLower, entry);
      allWordsArray.push(entry);

      // Index all parenthetical synonyms for instant lookup
      if (entry.synonyms && entry.synonyms.length > 0) {
        for (let s = 0; s < entry.synonyms.length; s++) {
          const synLower = entry.synonyms[s].toLowerCase();
          if (!definitionMap.has(synLower)) {
            definitionMap.set(synLower, entry);
          }
        }
      }
    }
  }

  const STEMDictionary = {
    wordBank: wordBank,
    getEntry: function(query) {
      if (!query) return null;
      const normalized = query.trim().toLowerCase();
      
      // 1. Exact match (main word or synonym)
      if (definitionMap.has(normalized)) {
        return definitionMap.get(normalized);
      }
      
      // 2. Fallback prefix/substring search
      for (let i = 0; i < allWordsArray.length; i++) {
        const item = allWordsArray[i];
        if (item.word.startsWith(normalized) || normalized.startsWith(item.word)) {
          return item;
        }
      }
      
      return null;
    },
    getDefinition: function(query) {
      const entry = this.getEntry(query);
      return entry ? entry.definition : null;
    },
    getDefinitionSnippet: function(query, maxLength = 140) {
      const entry = this.getEntry(query);
      if (!entry) return null;
      const def = entry.definition;
      if (def.length <= maxLength) return def;
      const truncated = def.substring(0, maxLength);
      const lastSpace = truncated.lastIndexOf(' ');
      return (lastSpace > 0 ? truncated.substring(0, lastSpace) : truncated) + '...';
    },
    predictWords: function(query, limit = 8) {
      if (!query || typeof query !== 'string') return [];
      const q = query.trim().toLowerCase();
      if (q.length === 0) return [];
      
      const exactPrefixMatches = [];
      const synonymPrefixMatches = [];
      const substringMatches = [];
      const seenWords = new Set();
      
      // Stage 1 & 2: Fast index lookup
      for (let i = 0; i < allWordsArray.length; i++) {
        const entry = allWordsArray[i];
        const w = entry.word.toLowerCase();
        
        if (seenWords.has(w)) continue;
        
        if (w.startsWith(q)) {
          seenWords.add(w);
          exactPrefixMatches.push({
            word: entry.word,
            raw: entry.raw,
            display: entry.raw.split('(')[0].trim(),
            definition: entry.definition,
            matchType: 'prefix',
            score: w.length - q.length
          });
          continue;
        }
        
        // Check synonyms
        if (entry.synonyms && entry.synonyms.length > 0) {
          for (let s = 0; s < entry.synonyms.length; s++) {
            const syn = entry.synonyms[s].toLowerCase();
            if (syn.startsWith(q)) {
              seenWords.add(w);
              synonymPrefixMatches.push({
                word: entry.word,
                raw: entry.raw,
                display: `${syn.toUpperCase()} (${entry.word.toUpperCase()})`,
                definition: entry.definition,
                matchType: 'synonym',
                score: syn.length - q.length
              });
              break;
            }
          }
        }
      }
      
      // Sort exact prefix matches (shorter words first)
      exactPrefixMatches.sort((a, b) => a.score - b.score);
      synonymPrefixMatches.sort((a, b) => a.score - b.score);
      
      let results = [...exactPrefixMatches, ...synonymPrefixMatches];
      
      // Stage 3: Substring matches if more predictions needed
      if (results.length < limit) {
        for (let i = 0; i < allWordsArray.length && results.length < limit; i++) {
          const entry = allWordsArray[i];
          const w = entry.word.toLowerCase();
          if (seenWords.has(w)) continue;
          
          if (w.includes(q) || (entry.raw && entry.raw.toLowerCase().includes(q))) {
            seenWords.add(w);
            substringMatches.push({
              word: entry.word,
              raw: entry.raw,
              display: entry.raw.split('(')[0].trim(),
              definition: entry.definition,
              matchType: 'contains',
              score: w.indexOf(q)
            });
          }
        }
        substringMatches.sort((a, b) => a.score - b.score);
        results = results.concat(substringMatches);
      }
      
      return results.slice(0, limit);
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
    },
    attachAutocomplete: function(inputElem, containerElem, onSelect) {
      if (!inputElem || !containerElem) return;
      
      let debounceTimer = null;
      
      const renderPredictions = (predictions) => {
        containerElem.innerHTML = '';
        if (!predictions || predictions.length === 0) {
          containerElem.style.display = 'none';
          return;
        }
        
        containerElem.style.display = 'block';
        
        predictions.forEach(p => {
          const item = document.createElement('div');
          item.className = 'stem-autocomplete-item';
          item.style.padding = '8px 12px';
          item.style.cursor = 'pointer';
          item.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
          item.style.color = '#fff';
          item.style.fontSize = '14px';

          const title = document.createElement('strong');
          title.style.color = '#00d2ff';
          title.textContent = p.display || p.word;

          const snippet = document.createElement('div');
          snippet.style.fontSize = '11px';
          snippet.style.opacity = '0.75';
          snippet.style.whiteSpace = 'nowrap';
          snippet.style.overflow = 'hidden';
          snippet.style.textOverflow = 'ellipsis';
          snippet.textContent = p.definition;

          item.appendChild(title);
          item.appendChild(snippet);
          
          item.addEventListener('click', () => {
            inputElem.value = p.word;
            containerElem.style.display = 'none';
            if (typeof onSelect === 'function') {
              onSelect(p);
            }
          });
          
          containerElem.appendChild(item);
        });
      };
      
      inputElem.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        const query = e.target.value;
        debounceTimer = setTimeout(() => {
          const preds = STEMDictionary.predictWords(query, 6);
          renderPredictions(preds);
        }, 120);
      });
      
      document.addEventListener('click', (e) => {
        if (!inputElem.contains(e.target) && !containerElem.contains(e.target)) {
          containerElem.style.display = 'none';
        }
      });
    }
  };

  if (typeof window !== 'undefined') {
    window.wordBank = wordBank;
    window.STEMDictionary = STEMDictionary;
  }
})();
""")

    print(f"Successfully generated updated {output_js}!")

if __name__ == "__main__":
    build_core_dictionary()
