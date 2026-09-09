import json

with open('ef_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    ef = json.load(f)

e_cands = ef['E']
with open('scripts/e_candidates_batch_3_full.txt', 'w', encoding='utf-8') as out:
    for i in range(90, len(e_cands)):
        c = e_cands[i]
        out.write(f"=== {i+1}. [{c['index']}] {c['word']} ===\nDEF: {c['definition']}\n\n")

f_cands = ef['F']
with open('scripts/f_candidates_full.txt', 'w', encoding='utf-8') as out:
    for i, c in enumerate(f_cands):
        out.write(f"=== {i+1}. [{c['index']}] {c['word']} ===\nDEF: {c['definition']}\n\n")

print(f"Dumped E batch 3: {len(e_cands)-90} items.")
print(f"Dumped F all: {len(f_cands)} items.")
