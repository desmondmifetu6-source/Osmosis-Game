import json

with open('ab_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_a_items.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['A'][:35]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+1}. [{w}]\n{d}\n" + "="*50 + "\n")

print("Saved batch_a_items.txt successfully.")
