import json
import io
import sys

with io.open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

d = {x['word'].lower(): x['definition'] for x in data.get('D', [])}
words = ['dummy suffix convention', 'dummy variable', 'durbin-watson test', 'dynamical time']

with io.open('d3.txt', 'w', encoding='utf-8') as f:
    for w in words:
        f.write(w + '\n')
        f.write(d.get(w, 'NOT FOUND') + '\n\n')
