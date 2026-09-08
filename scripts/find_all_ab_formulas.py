import json
import re

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Keywords indicating mathematical, physical, chemical formulas or equations
KEYWORDS = [
    'formula', 'equation', 'theorem', 'law', 'constant', 'series', 'ratio',
    'coefficient', 'integral', 'derivative', 'distribution', 'identity',
    'dimension', 'expressed as', 'given by', 'defined as', 'represented by',
    'function of', 'proportional to', 'inverse of', 'square of', 'reciprocal of',
    'calculat', 'measured by', 'stated as', 'relation'
]

def analyze_letter(letter):
    entries = data.get(letter, [])
    results = []
    
    for idx, entry in enumerate(entries):
        word = entry.get('word', '')
        defn = entry.get('definition', '')
        raw = entry.get('raw', '')
        
        has_eq = '=' in defn
        has_symbols = bool(re.search(r'[∑√∫±≠≤≥≈∞\^Δλμθπσωεαβγδ\\]', defn))
        has_math_spacing = bool(re.search(r'\b[a-zA-Z]\s*=\s*|\b[a-zA-Z]\s+[0-9]\b|\b[a-zA-Z]\s*[-–]\s*[0-9]\b|\b\d+\s*/\s*\d+\b', defn))
        has_kw = any(k in word.lower() or k in defn.lower() for k in KEYWORDS)
        has_broken_dollars = '$$$$$' in defn or '^-' in defn
        
        if (has_eq and (has_symbols or has_math_spacing or has_kw)) or has_broken_dollars or (has_kw and (has_symbols or has_eq)):
            results.append({
                'index': idx,
                'word': word,
                'raw': raw,
                'definition': defn
            })
            
    return results

a_formulas = analyze_letter('A')
b_formulas = analyze_letter('B')

print(f"Total formula candidates in Section A: {len(a_formulas)}")
print(f"Total formula candidates in Section B: {len(b_formulas)}")

with open('ab_formulas_to_enrich.json', 'w', encoding='utf-8') as f:
    json.dump({'A': a_formulas, 'B': b_formulas}, f, ensure_ascii=False, indent=2)

print("Saved to ab_formulas_to_enrich.json")
