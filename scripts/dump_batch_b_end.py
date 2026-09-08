import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ab_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_b_items_51_end.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['B'][50:]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+51}. [{w}]\n{d}\n" + "="*50 + "\n")

print(f"Saved {len(cand['B'][50:])} items to batch_b_items_51_end.txt")
