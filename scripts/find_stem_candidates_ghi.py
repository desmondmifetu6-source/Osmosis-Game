"""
After Sprint 2: Audit remaining unenriched STEM-relevant terms in G, H, I.
Focus: show the terms that look like they SHOULD have formulas but don't.
"""
import json, os, re

dictPath = os.path.join(os.path.dirname(__file__), '..', 'dictionary.json')
with open(dictPath, 'r', encoding='utf-8') as f:
    d = json.load(f)

# Keywords that suggest a term SHOULD have a formula
formula_keywords = re.compile(
    r'\b(law|theorem|equation|formula|distribution|constant|energy|force|'
    r'principle|rule|function|integral|derivative|transform|field|potential|'
    r'coefficient|rate|velocity|acceleration|momentum|frequency|wavelength|'
    r'resistance|current|voltage|power|entropy|enthalpy|pressure|density|'
    r'mass|charge|flux|matrix|vector|series|sequence|modulus|number|ratio|'
    r'factor|reaction|process|orbit|decay|radiation|spectrum|wave|oscillat|'
    r'circuit|capacit|conduct|permittiv|permeab|geometry|calculus)\b',
    re.IGNORECASE
)

for section in ['G', 'H', 'I']:
    entries = d.get(section, [])
    unenriched = [e for e in entries if '$' not in e.get('definition','') and 'formula' not in e]
    # Filter to likely STEM formula candidates
    candidates = [e for e in unenriched if formula_keywords.search(e['word'])]
    print(f"\n=== Section {section}: {len(unenriched)} unenriched total, {len(candidates)} STEM candidates ===")
    for e in candidates:
        print(f"  - {e['word']}")
