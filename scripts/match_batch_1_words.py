import json

with open("dictionary.json", "r", encoding="utf-8") as f:
    data = json.load(f)

terms_to_check = [
    "axis", "azo", "symmetry", "parabola", "astigmatism", 
    "distortion", "aberration", "chromatic", "spherical",
    "abo", "blood group", "abomasum", "absorption", "acceleration"
]

results = {}
for letter, entries in data.items():
    for entry in entries:
        w = entry.get("word", "").lower()
        raw = entry.get("raw_headword", "").lower()
        syns = [s.lower() for s in entry.get("synonyms", [])]
        all_names = [w, raw] + syns
        for term in terms_to_check:
            for n in all_names:
                if term in n:
                    if term not in results:
                        results[term] = set()
                    results[term].add((w, raw))

for term, matches in results.items():
    print(f"=== {term} ===")
    for w, raw in sorted(list(matches))[:10]:
        print(f"  word: '{w}', raw: '{raw}'")
