import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

all_words = {}
for letter, entries in data.items():
    for idx, item in enumerate(entries):
        w = item.get('word', '').lower().strip()
        all_words[w] = (letter, idx)
        for s in item.get('synonyms', []):
            all_words[s.lower().strip()] = (letter, idx)

test_terms = [
    "carnot cycle",
    "carrot",
    "taproot",
    "cashew",
    "cashew tree",
    "cashew nut",
    "cassegrain arrangement",
    "cassegrain telescope",
    "cassegrain reflector",
    "castor tree",
    "castor oil",
    "ricinus communis",
    "cathode ray tube",
    "crt",
    "cathode ray",
    "cartesian coordinates",
    "rectangular coordinates",
    "caudate",
    "caudate leaf",
    "animal cell",
    "cell",
    "plant cell"
]

print("=== CHECKING TERMS BATCH 3 (21-30) ===")
missing = []
for t in test_terms:
    if t in all_words:
        letter, idx = all_words[t]
        print(f"  FOUND: '{t}' in {letter} [{idx}]")
    else:
        missing.append(t)

print("\n=== MISSING ===")
for m in missing:
    print(f"  MISSING: '{m}'")
