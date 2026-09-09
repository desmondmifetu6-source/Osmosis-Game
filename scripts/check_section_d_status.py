import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d_words = {x['word'].lower(): x['definition'] for x in d.get('D', [])}

b1_samples = ["dalton's law", "de broglie equation", "decay constant", "definite integral"]
b2_samples = ["differential equation", "dirac equation", "doppler effect", "dulong and petit's law"]
remaining = ["dummy suffix convention", "dummy variable", "durbin-watson test", "dynamical time"]

print("--- Batch 1 Samples ---")
for w in b1_samples:
    print(f"{w}: {'HAS_LATEX' if '$' in d_words.get(w, '') else 'PLAIN'}")

print("\n--- Batch 2 Samples ---")
for w in b2_samples:
    print(f"{w}: {'HAS_LATEX' if '$' in d_words.get(w, '') else 'PLAIN'}")

print("\n--- Remaining D Words ---")
for w in remaining:
    print(f"{w}: {'HAS_LATEX' if '$' in d_words.get(w, '') else 'PLAIN'}")
    print(f"   Definition: {d_words.get(w, 'NOT FOUND')[:120]}...")
