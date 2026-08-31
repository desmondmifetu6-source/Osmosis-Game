import json

with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    d = json.load(f)

for k, v in d.items():
    if "propen" in k or "acrylo" in k:
        print(f"'{k}' -> '{v}'")
