"""
=====================================================================
CLEAN AND ENRICH STEM FORMULAS PIPELINE (Osmosis Dictionary Engine)
=====================================================================
Scans dictionary.json for scientific equations, chemical reactions,
and mathematical expressions corrupted during OCR extraction, and
normalizes them into clean LaTeX and structured scientific notation.
"""

import json
import re
import sys
import os

def clean_ocr_equation_artifacts(text):
    if not text:
        return text

    # Specific known dictionary corruptions from OCR (exact string replacements or callbacks)
    fixed_replacements = [
        # Abbe number
        (
            r"V\s*=\s*n\s*d\s*−\s*1\s*/\s*n\s*f\s*−\s*n\s*[cC]",
            r"$$V = \frac{n_d - 1}{n_f - n_c}$$"
        ),
        # Abel's partial summation formula
        (
            r"a\s*k\s*k\s*=\s*1\s*n\s*∑\s*=\s*A\s*n,\s*has\s*akbkk\s*=\s*m\s*n\s*∑\s*=\s*A\s*k\s*k\s*=\s*m\s*n\s*∑\s*\(\s*b\s*k\s*−\s*b\s*k\s*\+\s*1\s*\)\s*\+\s*Anbn\s*\+\s*1\s*−\s*A\s*m\s*−\s*1\s*b\s*m",
            r"$$\sum_{k=m}^{n} a_k b_k = A_n b_{n+1} - A_{m-1} b_m + \sum_{k=m}^{n} A_k (b_k - b_{k+1})$$"
        ),
        # Abel's theorem convolution series
        (
            r"c\s*n\s*=\s*a\s*0\s*b\s*n\s*\+\s*a\s*1\s*b\s*n\s*−\s*1\s*\+\s*\.\.\.\s*\+\s*a\s*n\s*b\s*0",
            r"$$c_n = a_0 b_n + a_1 b_{n-1} + \dots + a_n b_0$$"
        ),
        # abc conjecture
        (
            r"satisfy\s+a\s*\+\s*b\s*=\s*c",
            r"satisfy $a + b = c$"
        ),
        # Abelian group
        (
            r"ab\s*=\s*ba\s+or\s+a\s*\+\s*b\s*=\s*b\s*\+\s*a",
            r"$ab = ba$ or $a + b = b + a$"
        ),
        # Functions and limits in power series
        (
            r"f\s*\(\s*z\s*\)\s+for\s+\|z\|\s*<\s*1",
            r"$f(z)$ for $|z| < 1$"
        ),
        (
            r"for\s+z\s*=\s*1\b",
            r"for $z = 1$"
        ),
        (
            r"for\s+z\s*=\s*a\s*,",
            r"for $z = a$,"
        ),
        (
            r"\|\s*z\s*\|\s*<\s*\|\s*a\s*\|",
            r"$|z| < |a|$"
        ),
        # Spaced subscripts: e.g. "n d ," -> "$n_d$," or "n f" -> "$n_f$"
        (
            r"\bn\s+d\b",
            r"$n_d$"
        ),
        (
            r"\bn\s+f\b",
            r"$n_f$"
        ),
        (
            r"\bn\s+c\b",
            r"$n_c$"
        ),
        # Fix spaced arithmetic equality in definitions: e.g. "E = m c 2" or "F = m a"
        (
            r"\bE\s*=\s*m\s*c\s*\^?\s*2\b",
            r"$$E = mc^2$$"
        ),
        (
            r"\bF\s*=\s*m\s*a\b",
            r"$$F = ma$$"
        ),
        (
            r"\bP\s*V\s*=\s*n\s*R\s*T\b",
            r"$$PV = nRT$$"
        ),
        (
            r"\bv\s*=\s*u\s*\+\s*a\s*t\b",
            r"$$v = u + at$$"
        ),
        (
            r"\bs\s*=\s*u\s*t\s*\+\s*1/2\s*a\s*t\s*\^?\s*2\b",
            r"$$s = ut + \frac{1}{2}at^2$$"
        ),
        (
            r"\bv\s*\^?\s*2\s*=\s*u\s*\^?\s*2\s*\+\s*2\s*a\s*s\b",
            r"$$v^2 = u^2 + 2as$$"
        ),
        (
            r"\bI\s*=\s*V\s*/\s*R\b",
            r"$$I = \frac{V}{R}$$"
        ),
        (
            r"\bV\s*=\s*I\s*R\b",
            r"$$V = IR$$"
        ),
    ]

    for pattern, repl_str in fixed_replacements:
        text = re.sub(pattern, lambda m, r=repl_str: r, text)

    # Dynamic group replacement for powers & dimensions: e.g. "m s - 1" or "mol dm − 3" -> "m s^-1"
    text = re.sub(r"\b([a-zA-Z]+)\s*[−-]\s*(\d+)\b", lambda m: f"{m.group(1)}^-{m.group(2)}", text)

    # Convert common minus signs in expressions to standard unicode / LaTeX
    text = text.replace("−", "-")

    # Clean double spaces caused by regex replacements
    text = re.sub(r" {2,}", " ", text)

    return text.strip()

def process_dictionary(input_json_path, output_json_path, output_js_path=None):
    print(f"Loading dictionary from {input_json_path}...")
    with open(input_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_words = 0
    updated_words = 0

    if isinstance(data, dict):
        for letter, entries in data.items():
            if isinstance(entries, list):
                for item in entries:
                    total_words += 1
                    orig_def = item.get("definition", "")
                    cleaned_def = clean_ocr_equation_artifacts(orig_def)
                    if orig_def != cleaned_def:
                        item["definition"] = cleaned_def
                        updated_words += 1
    elif isinstance(data, list):
        for item in data:
            total_words += 1
            orig_def = item.get("definition", "")
            cleaned_def = clean_ocr_equation_artifacts(orig_def)
            if orig_def != cleaned_def:
                item["definition"] = cleaned_def
                updated_words += 1

    print(f"Scanned {total_words} entries. Enriched formulas in {updated_words} definitions.")

    print(f"Saving updated dictionary to {output_json_path}...")
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    if output_js_path:
        print(f"Regenerating {output_js_path} with full search & autocomplete index...")
        with open(output_js_path, "w", encoding="utf-8") as f:
            f.write("// STEM Core Dictionary Data Auto-Generated with Full Search & Autocomplete Engine\n")
            f.write("const wordBank = ")
            json.dump(data, f, ensure_ascii=False)
            f.write(";\n\n")
            f.write("""(function() {
  const definitionMap = new Map();
  const allWordsArray = [];

  for (const letter in wordBank) {
    const list = wordBank[letter];
    if (Array.isArray(list)) {
      for (let i = 0; i < list.length; i++) {
        const entry = list[i];
        if (!entry || !entry.word) continue;
        const wLower = entry.word.toLowerCase();
        if (!definitionMap.has(wLower)) {
          definitionMap.set(wLower, entry);
        }
        allWordsArray.push(entry);

        // Index all parenthetical synonyms for instant lookup
        if (entry.synonyms && Array.isArray(entry.synonyms)) {
          for (let s = 0; s < entry.synonyms.length; s++) {
            const synLower = entry.synonyms[s].toLowerCase();
            if (!definitionMap.has(synLower)) {
              definitionMap.set(synLower, entry);
            }
          }
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
})();
""")
        print(f"Successfully generated {output_js_path}!")

if __name__ == "__main__":
    dict_json = "dictionary.json"
    dict_js = "core_dictionary.js"
    process_dictionary(dict_json, dict_json, dict_js)
