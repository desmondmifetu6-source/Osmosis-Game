import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    dict_data = json.load(f)
with open('ef_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    ef = json.load(f)

e_entries = dict_data['E']
remaining = [c for c in ef['E'] if '$' not in e_entries[c['index']]['definition']]

with open('scripts/e_remaining_19.txt', 'w', encoding='utf-8') as out:
    out.write(f"Remaining in E: {len(remaining)}\n\n")
    for c in remaining:
        out.write(f"=== [{c['index']}] {c['word']} ===\nDEF: {e_entries[c['index']]['definition']}\n\n")

print(f"Wrote {len(remaining)} items to scripts/e_remaining_19.txt")
