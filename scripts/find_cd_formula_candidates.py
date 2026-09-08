import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total entries in C: {len(data.get('C', []))}")
print(f"Total entries in D: {len(data.get('D', []))}")

KEYWORDS = [
    'formula', 'equation', 'theorem', 'law', 'constant', 'series', 'ratio',
    'coefficient', 'integral', 'derivative', 'distribution', 'identity',
    'dimension', 'expressed as', 'given by', 'defined as', 'represented by',
    'function of', 'proportional to', 'inverse of', 'square of', 'reciprocal of',
    'calculat', 'measured by', 'stated as', 'relation', 'decay', 'half-life',
    'probability', 'rule', 'matrix', 'vector', 'polynomial', 'equilibrium'
]

def scan_section(letter):
    entries = data.get(letter, [])
    candidates = []
    for idx, entry in enumerate(entries):
        w = entry.get('word', '')
        d = entry.get('definition', '')
        raw = entry.get('raw', '')
        
        has_eq = '=' in d
        has_symbols = any(c in d for c in ['∑', '√', '∫', '±', '≠', '≤', '≥', '≈', '∞', '^', 'Δ', 'λ', 'μ', 'θ', 'π', 'σ', 'ω', 'ε', 'α', 'β', 'γ', 'δ', 'φ', 'ψ', '\\'])
        has_kw = any(k in w.lower() or k in d.lower() for k in KEYWORDS)
        
        if (has_eq and (has_symbols or has_kw)) or (has_symbols and has_kw) or any(k in w.lower() for k in ['law', 'theorem', 'formula', 'equation', 'constant']):
            candidates.append({
                'index': idx,
                'word': w,
                'raw': raw,
                'definition': d
            })
    return candidates

c_cand = scan_section('C')
d_cand = scan_section('D')

print(f"Flagged candidates in C: {len(c_cand)}")
print(f"Flagged candidates in D: {len(d_cand)}")

with open('cd_formulas_to_enrich.json', 'w', encoding='utf-8') as f:
    json.dump({'C': c_cand, 'D': d_cand}, f, ensure_ascii=False, indent=2)

print("Saved cd_formulas_to_enrich.json successfully.")
