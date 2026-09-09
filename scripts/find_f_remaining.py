"""
find_f_remaining.py
===================
Identify the remaining 4 Section F formula candidates that haven't been enriched yet.
"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
with open('ef_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    ef = json.load(f)

f_entries = data.get('F', [])
f_cands = ef.get('F', [])

remaining = []
for c in f_cands:
    idx = c['index']
    entry = f_entries[idx]
    defn = entry.get('definition', '')
    if '$' not in defn:
        remaining.append((idx, entry['word'], defn))

print(f"Remaining Section F formulas to enrich: {len(remaining)}")
print()
for idx, word, defn in remaining:
    print(f"INDEX: {idx}")
    print(f"WORD:  {word}")
    print(f"DEF:   {defn[:300]}")
    print("-" * 60)
