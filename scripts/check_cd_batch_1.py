import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Build a set of all words and synonyms in lowercase
all_words = {}
for letter, entries in data.items():
    for idx, item in enumerate(entries):
        w = item.get('word', '').lower().strip()
        all_words[w] = (letter, idx)
        for s in item.get('synonyms', []):
            all_words[s.lower().strip()] = (letter, idx)

test_terms = [
    "chloroprene",
    "caffeine",
    "calixarene",
    "phenol-derived calixarene",
    "vernier callipers",
    "callipers",
    "sliding callipers",
    "vernier scale",
    "calorimeter",
    "simple calorimeter",
    "specific heat capacity",
    "calomel electrode",
    "calomel half cell",
    "camphor",
    "cannizzaro reaction",
    "canine",
    "canines",
    "canine tooth",
    "cannabinoid",
    "thc",
    "tetrahydrocannabinol",
    "capillary",
    "vertebrate capillary",
    "blood capillary",
    "capacitor",
    "types of capacitor",
    "variable capacitor",
    "cantilever",
    "cantilever beam",
    "capitate",
    "capitate structure",
    "capitulum",
    "capitulum of a flower",
    "flower head",
    "carbocation",
    "carbocation structure",
    "carbon cycle",
    "carbon dioxide",
    "co2",
    "captan",
    "cardioid"
]

print("=== CHECKING TERMS IN DICTIONARY.JSON ===")
missing = []
found = []
for t in test_terms:
    if t in all_words:
        letter, idx = all_words[t]
        found.append(f"  FOUND: '{t}' in letter {letter} (idx {idx})")
    else:
        missing.append(t)

for f_str in found:
    print(f_str)

print("\n=== MISSING TERMS ===")
for m in missing:
    print(f"  MISSING: '{m}'")
