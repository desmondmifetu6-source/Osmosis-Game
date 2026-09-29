import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
with open('dictionary.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

indices = [0, 30, 33, 37, 97, 98, 99, 100, 102, 103, 104, 105, 106, 126, 127, 161, 168, 172, 173, 186, 187, 188, 189, 190, 203, 225, 254, 266]
for idx in indices:
    e = d['L'][idx]
    print(f"=== [{idx}] {e.get('word')} ===")
    print(e.get('definition'))
