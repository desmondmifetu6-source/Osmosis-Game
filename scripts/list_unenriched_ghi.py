"""
Pull ALL unenriched terms for sections G, H, I into a plain list.
Used to decide which terms get formula enrichment.
"""
import json, os

dictPath = os.path.join(os.path.dirname(__file__), '..', 'dictionary.json')
with open(dictPath, 'r', encoding='utf-8') as f:
    d = json.load(f)

for section in ['G', 'H', 'I']:
    entries = d.get(section, [])
    unenriched = [e['word'] for e in entries if '$' not in e.get('definition','') and 'formula' not in e]
    print(f"\n--- Section {section} unenriched ({len(unenriched)} total) ---")
    for w in unenriched:
        print(w)
