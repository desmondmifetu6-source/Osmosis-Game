import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICTIONARY_JSON = os.path.join(BASE_DIR, 'dictionary.json')
OUTPUT_JS = os.path.join(BASE_DIR, 'core_dictionary.js')

IIFE_ENGINE = r"""(function() {
  const definitionMap = new Map();
  const allWordsArray = [];

  // Pass 1: Index all primary headwords first so exact words ALWAYS take precedence
  for (const letter in wordBank) {
    const list = wordBank[letter];
    if (Array.isArray(list)) {
      for (let i = 0; i < list.length; i++) {
        const entry = list[i];
        if (!entry || !entry.word) continue;
        const wLower = entry.word.toLowerCase();
        definitionMap.set(wLower, entry);
        allWordsArray.push(entry);
      }
    } else if (typeof list === 'string') {
      const wLower = letter.toLowerCase();
      const entry = {
        word: letter,
        raw: letter,
        definition: list,
        synonyms: []
      };
      definitionMap.set(wLower, entry);
      allWordsArray.push(entry);
    }
  }

  // Pass 2: Index parenthetical synonyms ONLY if not already claimed by a primary headword
  for (let i = 0; i < allWordsArray.length; i++) {
    const entry = allWordsArray[i];
    if (entry.synonyms && Array.isArray(entry.synonyms)) {
      for (let s = 0; s < entry.synonyms.length; s++) {
        const synLower = entry.synonyms[s].toLowerCase();
        if (!definitionMap.has(synLower)) {
          definitionMap.set(synLower, entry);
        }
      }
    }
  }

  const STEMDictionary = {
    wordBank: wordBank,
    data: wordBank,
    getEntry: function(query) {
      if (!query) return null;
      const normalized = query.trim().toLowerCase();

      // 1. Exact match (main word or synonym)
      if (definitionMap.has(normalized)) {
        return definitionMap.get(normalized);
      }

      // 2. Punctuation & spacing variants (e.g. "x-ray" vs "x ray")
      const spaceVariant = normalized.replace(/-/g, ' ');
      if (definitionMap.has(spaceVariant)) {
        return definitionMap.get(spaceVariant);
      }
      const hyphenVariant = normalized.replace(/\s+/g, '-');
      if (definitionMap.has(hyphenVariant)) {
        return definitionMap.get(hyphenVariant);
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

      // Stage 1 & 2: Fast prefix lookup (word & synonyms)
      for (let i = 0; i < allWordsArray.length; i++) {
        const entry = allWordsArray[i];
        const w = entry.word.toLowerCase();

        if (seenWords.has(w)) continue;

        if (w.startsWith(q)) {
          seenWords.add(w);
          exactPrefixMatches.push({
            word: entry.word,
            raw: entry.raw || entry.raw_headword || entry.word,
            display: (entry.raw || entry.raw_headword || entry.word).split('(')[0].trim(),
            definition: entry.definition,
            matchType: 'prefix',
            score: w.length - q.length
          });
          continue;
        }

        // Check synonyms
        if (entry.synonyms && Array.isArray(entry.synonyms) && entry.synonyms.length > 0) {
          for (let s = 0; s < entry.synonyms.length; s++) {
            const syn = entry.synonyms[s].toLowerCase();
            if (syn.startsWith(q)) {
              seenWords.add(w);
              synonymPrefixMatches.push({
                word: entry.word,
                raw: entry.raw || entry.raw_headword || entry.word,
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

          const rawStr = (entry.raw || entry.raw_headword || '').toLowerCase();
          if (w.includes(q) || rawStr.includes(q)) {
            seenWords.add(w);
            substringMatches.push({
              word: entry.word,
              raw: entry.raw || entry.raw_headword || entry.word,
              display: (entry.raw || entry.raw_headword || entry.word).split('(')[0].trim(),
              definition: entry.definition,
              matchType: 'contains',
              score: w.indexOf(q) >= 0 ? w.indexOf(q) : 50
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

          const title = document.createElement('div');
          title.className = 'ac-word';
          title.textContent = (p.display || p.word).toUpperCase();

          const badge = document.createElement('span');
          badge.className = `ac-match-badge ${p.matchType === 'prefix' ? 'ac-badge-prefix' : p.matchType === 'synonym' ? 'ac-badge-synonym' : 'ac-badge-contains'}`;
          badge.textContent = p.matchType === 'synonym' ? 'alias' : p.matchType;
          title.appendChild(badge);

          const snippet = document.createElement('div');
          snippet.className = 'ac-snippet';
          snippet.textContent = p.definition && p.definition.length > 80 ? p.definition.substring(0, 80) + '...' : (p.definition || '');

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
        if (query.trim().length < 2) {
          containerElem.style.display = 'none';
          return;
        }
        debounceTimer = setTimeout(() => {
          const preds = STEMDictionary.predictWords(query, 7);
          renderPredictions(preds);
        }, 100);
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
    window.STEM_DICTIONARY_DATA = wordBank;
    window.STEMDictionary = STEMDictionary;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { wordBank, STEMDictionary };
  }
})();
"""

def rebuild():
    print("Loading dictionary.json...")
    with open(DICTIONARY_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print("Serializing wordBank...")
    word_bank_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

    print("Writing core_dictionary.js...")
    header = "// STEM Core Dictionary Data Auto-Generated with Full Search & Autocomplete Engine\n"
    word_bank_line = f"const wordBank = {word_bank_json};\n\n"
    output = header + word_bank_line + IIFE_ENGINE

    with open(OUTPUT_JS, 'w', encoding='utf-8') as f:
        f.write(output)

    print(f"Done! Written {len(output):,} characters to {OUTPUT_JS}")

if __name__ == '__main__':
    rebuild()
