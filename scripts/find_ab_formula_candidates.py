import json
import re

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

MATH_SIGNS = [
    '=', '∑', '√', '∫', '±', '≠', '≤', '≥', '≈', '∞', '^', 'Δ', 'λ', 'μ', 'θ', 'π', 'σ', 'ω',
    'alpha', 'beta', 'gamma', 'delta', 'theta', 'lambda', 'sigma', 'omega'
]

FORMULA_KEYWORDS = [
    'formula', 'equation', 'theorem', 'law', 'constant', 'series', 'ratio',
    'coefficient', 'integral', 'derivative', 'distribution', 'identity',
    'dimension', 'expressed as', 'given by', 'defined as', 'represented by', 'where', 'form:'
]

def scan_section(letter):
    entries = data.get(letter, [])
    candidates = []
    
    for idx, entry in enumerate(entries):
        word = entry.get('word', '')
        defn = entry.get('definition', '')
        
        # Check if contains LaTeX already
        has_katex = '$' in defn
        
        # Check for formula indicators
        has_math_sign = any(s in defn for s in MATH_SIGNS)
        has_equal = '=' in defn
        has_keyword = any(k in word.lower() or k in defn.lower() for k in FORMULA_KEYWORDS)
        has_ocr_math = bool(re.search(r'\b[a-zA-Z]\s*=\s*|\b[a-zA-Z]\s*[0-9]\b|\b\d+\s*/\s*\d+\b|\b[a-zA-Z]\s*\^\s*\d+', defn))
        
        score = 0
        if has_equal: score += 3
        if has_math_sign: score += 2
        if has_ocr_math: score += 2
        if has_keyword: score += 1
        
        if score >= 2 or has_katex or 'formula' in word.lower() or 'equation' in word.lower() or 'law' in word.lower() or 'theorem' in word.lower():
            candidates.append({
                'index': idx,
                'word': word,
                'definition': defn,
                'has_katex': has_katex,
                'score': score
            })
            
    return candidates

cand_a = scan_section('A')
cand_b = scan_section('B')

print(f"Total candidates in A: {len(cand_a)} (Already with KaTeX: {sum(1 for c in cand_a if c['has_katex'])})")
print(f"Total candidates in B: {len(cand_b)} (Already with KaTeX: {sum(1 for c in cand_b if c['has_katex'])})")

with open('ab_formula_candidates.json', 'w', encoding='utf-8') as f:
    json.dump({'A': cand_a, 'B': cand_b}, f, ensure_ascii=False, indent=2)
print("Saved candidates to ab_formula_candidates.json")
