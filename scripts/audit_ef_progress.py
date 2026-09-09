import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    dict_data = json.load(f)
with open('ef_formulas_to_enrich.json', 'r', encoding='utf-8') as f:
    ef = json.load(f)

for section in ['E', 'F']:
    entries = dict_data.get(section, [])
    cands = ef.get(section, [])
    has_formula = [c for c in cands if '$' in entries[c['index']]['definition']]
    no_formula = [c for c in cands if '$' not in entries[c['index']]['definition']]
    print(f"Section {section}: total {len(entries)} entries, {len(cands)} formula candidates")
    print(f"  Enriched with KaTeX ($): {len(has_formula)}")
    print(f"  Awaiting review/enrichment: {len(no_formula)}")
