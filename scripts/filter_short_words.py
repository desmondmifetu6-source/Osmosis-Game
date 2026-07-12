import json

data = json.load(open('dictionary_extracted.json', encoding='utf-8'))
print(f"Starting count: {len(data)}")

# Show all words that are too short to be game words
short_words = [(i, item['word']) for i, item in enumerate(data) if len(item['word']) < 3]
print(f"\nWords shorter than 3 chars: {len(short_words)}")
for idx, w in short_words:
    print(f"  [{idx}] \"{w}\"")

# Filter: minimum 3 characters in the word
cleaned = [item for item in data if len(item['word']) >= 3]
print(f"\nFinal count after filtering: {len(cleaned)}")
print(f"Removed: {len(data) - len(cleaned)} too-short entries")

with open('dictionary_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)

print("Saved!")
