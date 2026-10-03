import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

r_list = data.get('R', [])

with open('r_words.txt', 'w', encoding='utf-8') as out:
    for idx, entry in enumerate(r_list):
        word = entry.get('word', '')
        defn = entry.get('definition', '')[:60].replace('\n', ' ')
        out.write(f"{idx} | {word} | {defn}\n")

print(f"Dumped {len(r_list)} R terms to r_words.txt")
