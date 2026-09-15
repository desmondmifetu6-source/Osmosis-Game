import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('ghij_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

g_cands = data['G']

with open('g_candidates_batch_1.txt', 'w', encoding='utf-8') as out:
    for i, c in enumerate(g_cands[:40]):
        out.write(f"=== CANDIDATE {i+1} / 40 | Index: {c['index']} | Word: {c['word']} ===\n")
        out.write(f"Definition:\n{c['definition']}\n\n")

print(f"Dumped 40 candidates of Section G to g_candidates_batch_1.txt")
