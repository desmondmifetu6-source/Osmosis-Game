import json
import re

with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    diag_map = json.load(f)

print(f"Total entries in map: {len(diag_map)}")

# Let's inspect all keys and categorize them
malformed_keys = []
short_keys = []
bracket_keys = []
number_prefix_keys = []
formula_fragments = []
valid_keys = []

for k in diag_map:
    k_clean = k.strip()
    if len(k_clean) <= 3:
        short_keys.append(k_clean)
    elif k_clean.startswith("(") or k_clean.endswith("]") or k_clean.startswith("["):
        bracket_keys.append(k_clean)
    elif re.match(r'^\d+[\,\-]', k_clean):
        number_prefix_keys.append(k_clean)
    elif ";" in k_clean or "" in k_clean or "->" in k_clean:
        malformed_keys.append(k_clean)
    else:
        valid_keys.append(k_clean)

print(f"Short keys (<=3 chars, lethal for substring matching): {len(short_keys)} -> {short_keys}")
print(f"Bracket / fragment keys: {len(bracket_keys)} -> {bracket_keys[:10]}")
print(f"Number prefix keys: {len(number_prefix_keys)} -> {number_prefix_keys[:10]}")
print(f"Malformed / punctuation corrupted keys: {len(malformed_keys)} -> {malformed_keys[:10]}")
print(f"Clean keys: {len(valid_keys)}")
