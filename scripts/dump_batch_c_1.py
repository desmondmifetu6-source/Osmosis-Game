import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('cd_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_c_items_1_50.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['C'][:50]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+1}. [{w}]\n{d}\n" + "="*50 + "\n")

print("Saved batch_c_items_1_50.txt successfully.")
