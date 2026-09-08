import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('cd_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_c_items_101_200.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['C'][100:200]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+101}. [{w}]\n{d}\n" + "="*50 + "\n")

print(f"Saved {len(cand['C'][100:200])} items to batch_c_items_101_200.txt")
