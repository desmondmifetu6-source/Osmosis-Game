import json

data = json.load(open('ef_formulas_to_enrich.json', encoding='utf-8'))['E']
with open('scripts/e_candidates_batch_1_full.txt', 'w', encoding='utf-8') as f:
    for i, c in enumerate(data[:45]):
        f.write(f"=== {i+1}. [{c['index']}] {c['word']} ===\n")
        f.write(f"RAW: {c.get('raw', '')}\n")
        f.write(f"DEF: {c['definition']}\n\n")

print("Wrote scripts/e_candidates_batch_1_full.txt")
