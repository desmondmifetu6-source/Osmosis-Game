import os
import json

with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    diag_map = json.load(f)

missing = []
for k, path in diag_map.items():
    if not os.path.exists(path):
        missing.append((k, path))

print(f"Total entries in map: {len(diag_map)}")
print(f"Missing image files: {len(missing)}")
if missing:
    for k, path in missing[:10]:
        print(f"  Missing: {k} -> {path}")
