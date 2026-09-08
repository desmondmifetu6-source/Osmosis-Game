import json

with open('ab_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

with open('batch_a_items_36_70.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(cand['A'][35:70]):
        w = item['word']
        d = item['definition']
        out.write(f"{i+36}. [{w}]\n{d}\n" + "="*50 + "\n")

print("Saved batch_a_items_36_70.txt successfully.")
