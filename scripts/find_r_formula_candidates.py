import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

r_candidates = []
for key, entry in data.items():
    if isinstance(entry, dict):
        word = entry.get('word', '')
        if word.lower().startswith('r'):
            has_formula = 'formula' in entry
            defn = entry.get('definition', '')
            r_candidates.append((key, word, has_formula, defn[:80]))

print(f"Total R terms: {len(r_candidates)}")
print(f"R terms already with formulas: {sum(1 for c in r_candidates if c[2])}")
print("\nSample R terms missing formulas:")
missing = [c for c in r_candidates if not c[2]]
for k, w, h, d in missing[:35]:
    print(f"Key: {k} | Word: {w}")
