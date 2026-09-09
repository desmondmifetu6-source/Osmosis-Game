import json

data = json.load(open('ef_formulas_to_enrich.json', encoding='utf-8'))['E']
print(f"Total candidates in E: {len(data)}")
for i, c in enumerate(data[:35]):
    word = c['word']
    definition = c['definition'].replace('\n', ' ')
    if len(definition) > 120:
        definition = definition[:117] + "..."
    print(f"{i+1:3d}. [{c['index']:4d}] {word}: {definition}")
