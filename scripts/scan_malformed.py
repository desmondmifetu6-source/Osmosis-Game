import json

data = json.load(open('dictionary_extracted.json', encoding='utf-8'))

# Find malformed words
problems = []
for i, item in enumerate(data):
    w = item['word']
    # starts or ends with ) or other junk punctuation
    if w.startswith(')') or w.endswith(')') or w.startswith(',') or w.startswith('.') or w.startswith(';'):
        problems.append((i, w))
        
print(f'Malformed words found: {len(problems)}')
for idx, w in problems[:50]:
    print(f'  [{idx}] "{w}"')
