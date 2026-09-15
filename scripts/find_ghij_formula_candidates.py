import json
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

KEYWORDS = [
    'formula', 'equation', 'theorem', 'law', 'constant', 'series', 'ratio',
    'coefficient', 'integral', 'derivative', 'distribution', 'identity',
    'dimension', 'expressed as', 'given by', 'defined as', 'represented by',
    'function of', 'proportional to', 'inverse of', 'square of', 'reciprocal of',
    'calculat', 'measured by', 'stated as', 'relation', 'decay', 'half-life',
    'probability', 'rule', 'matrix', 'vector', 'polynomial', 'equilibrium',
    'enthalpy', 'entropy', 'gibbs', 'hamiltonian', 'lagrangian', 'laplace',
    'fourier', 'wavefunction', 'reaction', 'stoichiometry', 'molar', 'isotope'
]

SYMBOLS = ['∑', '√', '∫', '±', '≠', '≤', '≥', '≈', '∞', '^', 'Δ', 'λ', 'μ', 'θ', 'π', 'σ', 'ω', 'ε', 'α', 'β', 'γ', 'δ', 'φ', 'ψ', '\\', '→', '⇌', '×', '÷', '·', '°', 'Å']

def scan_section(letter):
    entries = data.get(letter, [])
    candidates = []
    for idx, entry in enumerate(entries):
        w = entry.get('word', '')
        d = entry.get('definition', '')
        raw = entry.get('raw', '')
        
        has_eq = '=' in d
        has_symbols = any(c in d for c in SYMBOLS)
        has_kw = any(k in w.lower() or k in d.lower() for k in KEYWORDS)
        has_chem_arrow = ('->' in d or '→' in d or '⇌' in d)
        
        # Check if already enriched with proper KaTeX formulas (contains $ ... $)
        already_has_katex = '$' in d
        
        is_candidate = (
            (has_eq and (has_symbols or has_kw)) or 
            (has_symbols and has_kw) or 
            has_chem_arrow or
            any(k in w.lower() for k in ['law', 'theorem', 'formula', 'equation', 'constant', 'number', 'series', 'ratio', 'coefficient', 'effect', 'rule', 'distribution', 'function'])
        )
        
        if is_candidate:
            candidates.append({
                'index': idx,
                'word': w,
                'raw': raw,
                'has_dollar': already_has_katex,
                'definition': d
            })
    return candidates

results = {}
for letter in ['G', 'H', 'I', 'J']:
    cands = scan_section(letter)
    results[letter] = cands
    print(f"Total entries in {letter}: {len(data.get(letter, []))}, Flagged candidates: {len(cands)}")

with open('ghij_formulas_to_enrich.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Saved ghij_formulas_to_enrich.json successfully.")
