import json
import re

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

MATH_PATTERNS = [
    r'=', r'∑', r'√', r'∫', r'±', r'≠', r'≤', r'≥', r'≈', r'∞', r'\^', r'Δ', r'λ', r'μ', r'θ', r'π', r'σ', r'ω',
    r'\bformula\b', r'\bequation\b', r'\btheorem\b', r'\blaw\b', r'\bconstant\b', r'\bseries\b',
    r'\bpolynomial\b', r'\bfunction\b', r'\bderivative\b', r'\bintegral\b', r'\bmatrix\b',
    r'\bvector\b', r'\bratio\b', r'\bdimension\b', r'\bdecay\b', r'\bhalf-life\b',
    r'\b[a-zA-Z]\s*=\s*', r'\b[a-zA-Z]\s*[0-9]\b', r'\b\d+\s*/\s*\d+\b', r'\b[a-zA-Z]\s*\^\s*\d+',
    r'\$', r'\\'
]

combined_regex = re.compile('|'.join(MATH_PATTERNS), re.IGNORECASE)

with open('ab_formula_audit.txt', 'w', encoding='utf-8') as out:
    for letter in ['A', 'B']:
        out.write(f"==================================================\n")
        out.write(f"           SECTION {letter} FORMULA AUDIT\n")
        out.write(f"==================================================\n\n")
        entries = data.get(letter, [])
        count = 0
        for entry in entries:
            word = entry.get('word', '')
            defn = entry.get('definition', '')
            raw = entry.get('raw', '')
            
            # Check if definition has formulas or math content
            if combined_regex.search(defn) or 'formula' in word.lower() or 'equation' in word.lower() or 'law' in word.lower() or 'theorem' in word.lower() or 'constant' in word.lower():
                count += 1
                out.write(f"WORD: {word}\n")
                if raw and raw != word:
                    out.write(f"RAW:  {raw}\n")
                out.write(f"DEFN: {defn}\n")
                out.write("-" * 60 + "\n")
        out.write(f"\nTotal flagged entries in {letter}: {count}\n\n")

print("Generated ab_formula_audit.txt successfully.")
