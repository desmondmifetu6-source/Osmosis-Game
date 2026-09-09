"""
get_full_defs.py
================
Print full definitions for the 4 remaining Section F terms.
"""
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

f_entries = data.get('F', [])
targets = [342, 787, 790, 1066]

for idx in targets:
    entry = f_entries[idx]
    print(f"INDEX: {idx}")
    print(f"WORD:  {entry['word']}")
    print(f"DEF:\n{entry['definition']}")
    print("=" * 70)
