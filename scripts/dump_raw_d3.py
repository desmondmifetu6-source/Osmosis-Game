import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

d_words = {x['word'].lower(): x['definition'] for x in d.get('D', [])}
targets = ['dummy suffix convention', 'dummy variable', 'durbin-watson test', 'dynamical time']

with open('d3_raw.txt', 'w', encoding='utf-8') as out:
    for t in targets:
        out.write(f"=== {t} ===\n{d_words.get(t, '')}\n\n")

print("Wrote d3_raw.txt successfully!")
