import json

with open("dictionary.json", "r", encoding="utf-8") as f:
    dict_data = json.load(f)

all_words = {}
for section, entries in dict_data.items():
    if isinstance(entries, list):
        for item in entries:
            w = item.get("word", "").strip().lower()
            if w:
                all_words[w] = section
            for syn in item.get("synonyms", []):
                s = syn.strip().lower()
                if s:
                    all_words[s] = section

print(f"Total searchable words & synonyms: {len(all_words)}")

queries = [
    "gravitation", "newton's law of gravitation", "universal gravitation",
    "greatest integer function", "floor function", "step function",
    "grouped data", "frequency distribution", "grouped data frequency distribution",
    "guanosine", "guanidine", "great circle", "guanine",
    "haematoxylin", "hematoxylin",
    "hair follicle", "hair", "structure of the hair follicle",
    "half-wave rectification", "half-wave rectifier", "half wave rectification", "rectification",
    "hastate", "hastate leaf",
    "haustorium", "haustorium of dodder", "dodder",
    "head", "capitulum", "head (capitulum)", "head inflorescence",
    "heart", "mammalian heart", "human heart", "external appearance of a human heart", "vertical section of a heart",
    "heat engine", "simplified heat engine",
    "height", "height of a parallelogram", "prism height", "height of a pyramid", "height of a cone", "height of a triangle",
    "helix", "three dimensional helix", "helix in a three dimensional plane",
    "hemiacetal", "general formula of a hemiacetal",
    "hesperidium", "hesperidium fruit",
    "heterocyclic compound", "heterocyclic", "thiophene", "oxazole", "imidazole", "pyridine",
    "heroin", "diacetylmorphine",
    "heterosporous", "heterospory", "microspore", "microspores", "megaspore",
    "heterostylic", "heterostyly", "style",
    "hexane", "structure of hexane",
    "hexagonal prism", "prism",
    "hexagram"
]

for q in queries:
    status = "EXACT MATCH" if q in all_words else "NOT FOUND"
    print(f"{q}: {status}")

print("\n--- Fuzzy search for unmatched ---")
for q in queries:
    if q not in all_words:
        # find partial matches
        matches = [w for w in all_words.keys() if q in w or (len(q)>4 and any(part in w for part in q.split()))][:3]
        if matches:
            print(f"Candidates for '{q}': {matches}")
