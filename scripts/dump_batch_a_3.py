import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ab_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_a_items_71_110.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['A'][70:110]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+71}. [{w}]\n{d}\n" + "="*50 + "\n")

print("Saved batch_a_items_71_110.txt successfully.")
