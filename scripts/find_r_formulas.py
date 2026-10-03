import json
import re

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

r_entries = data.get('R', [])
print(f"Total R entries: {len(r_entries)}")

already_formula = [e for e in r_entries if 'formula' in e]
print(f"R entries already with formula: {len(already_formula)}")

KEYWORDS = [
    'formula', 'equation', 'theorem', 'law', 'constant', 'series', 'ratio',
    'coefficient', 'integral', 'derivative', 'distribution', 'identity',
    'dimension', 'expressed as', 'given by', 'defined as', 'represented by',
    'function of', 'proportional to', 'inverse of', 'square of', 'reciprocal of',
    'calculat', 'measured by', 'stated as', 'relation', 'rule', 'matrix', 'vector',
    'force', 'energy', 'velocity', 'acceleration', 'pressure', 'density', 'resistance'
]

candidates = []
for idx, entry in enumerate(r_entries):
    word = entry.get('word', '')
    defn = entry.get('definition', '')
    
    has_eq = '=' in defn
    has_symbols = bool(re.search(r'[∑√∫±≠≤≥≈∞\^Δλμθπσωεαβγδ\\]', defn))
    has_kw = any(k in word.lower() or k in defn.lower() for k in KEYWORDS)
    
    if has_eq or has_symbols or has_kw:
        candidates.append((idx, word, 'formula' in entry, defn[:100]))

with open('r_candidates.txt', 'w', encoding='utf-8') as out:
    out.write(f"Total candidates: {len(candidates)}\n\n")
    for idx, word, has_f, d in candidates:
        out.write(f"Index {idx} | Word: {word} | Has Formula: {has_f}\n  Def: {d}\n\n")

print(f"Saved {len(candidates)} candidates to r_candidates.txt")
