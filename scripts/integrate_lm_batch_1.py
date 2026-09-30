"""
integrate_lm_batch_1.py — Processes Section L Diagrams (Screenshots 1-10)
from folder 'l-m diagrams' and synchronizes dictionary maps.
"""
import os, json, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR      = 'l-m diagrams'
DIAGRAMS_DIR = 'diagrams'
MAP_JSON     = 'dictionary_diagrams_map.json'
DIAGRAMS_JS  = 'core_dictionary_diagrams.js'
DICT_JSON    = 'dictionary.json'

BATCH = [
    ('Screenshot_25-9-2026_172950_.jpeg', 'dict_labiate.png',
     ['labiate', 'labiate corolla', 'labiate flower']),
    ('Screenshot_25-9-2026_173027_.jpeg', 'dict_lacerate_leaf.png',
     ['lacerate', 'lacerate leaf']),
    ('Screenshot_25-9-2026_173038_.jpeg', 'dict_laciniate_leaf.png',
     ['laciniate', 'laciniate leaf']),
    ('Screenshot_25-9-2026_17307_.jpeg', 'dict_lactic_acid.png',
     ['lactic acid', '2-hydroxypropanoic acid']),
    ('Screenshot_25-9-2026_173155_.jpeg', 'dict_lactam_lactim.png',
     ['lactam', 'lactim', 'lactam-lactim tautomerism']),
    ('Screenshot_25-9-2026_173249_.jpeg', 'dict_lamis_theorem.png',
     ["lami's theorem", 'lamis theorem', 'lami theorem']),
    ('Screenshot_25-9-2026_173321_.jpeg', 'dict_lanceolate_leaf.png',
     ['lanceolate', 'lanceolate leaf']),
    ('Screenshot_25-9-2026_17335_.jpeg', 'dict_lamina.png',
     ['lamina', 'leaf lamina', 'petal lamina']),
    ('Screenshot_25-9-2026_173437_.jpeg', 'dict_latin_square.png',
     ['latin square', '3 x 3 latin square']),
    ('Screenshot_25-9-2026_17346_.jpeg', 'dict_latent_heat_of_evaporation.png',
     ['latent heat of evaporation', 'latent heat', 'latent heat of vaporization']),
]

os.makedirs(DIAGRAMS_DIR, exist_ok=True)

with open(DICT_JSON, 'r', encoding='utf-8') as f:
    dict_data = json.load(f)
dict_words = set()
for letter, entries in dict_data.items():
    if isinstance(entries, list):
        for e in entries:
            if isinstance(e, dict) and 'word' in e:
                dict_words.add(e['word'].lower().strip())

with open(MAP_JSON, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

print(f"Loaded {len(diag_map)} existing diagram mappings.")

# Verify each term against dictionary.json
print("\n--- DICTIONARY TERM VERIFICATION ---")
for src_name, dest_name, terms in BATCH:
    matched = [t for t in terms if t in dict_words]
    print(f"{dest_name}: matched in dictionary.json -> {matched}")

# Copy images and update map
copied = 0
for src_name, dest_name, terms in BATCH:
    src_path = os.path.join(SRC_DIR, src_name)
    dest_path = os.path.join(DIAGRAMS_DIR, dest_name)
    rel_path = f'diagrams/{dest_name}'
    if not os.path.exists(src_path):
        print(f'  MISSING: {src_path}')
        continue
    shutil.copy2(src_path, dest_path)
    size_kb = os.path.getsize(dest_path) / 1024
    print(f'  OK  {dest_name}  ({size_kb:.1f} KB)')
    copied += 1
    for term in terms:
        diag_map[term.lower().strip()] = rel_path

print(f'\nCopied: {copied}/{len(BATCH)} Section L diagrams')

# Sort and save JSON map
diag_map_sorted = dict(sorted(diag_map.items()))
with open(MAP_JSON, 'w', encoding='utf-8') as f:
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
print(f'Saved {MAP_JSON} ({len(diag_map_sorted)} entries)')

# Regenerate JS bundle
with open(DIAGRAMS_JS, 'w', encoding='utf-8') as f:
    f.write('// core_dictionary_diagrams.js — Auto-generated. DO NOT EDIT MANUALLY.\n')
    f.write('// Last updated: Section L-M Batch 1 (screenshots 1-10)\n\n')
    f.write('var DictionaryDiagrams = ')
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
    f.write(';\n\nif (typeof module !== "undefined") { module.exports = DictionaryDiagrams; }\n')
print(f'Regenerated {DIAGRAMS_JS}')

# Integrity Check
missing = []
for k, v in diag_map_sorted.items():
    if not os.path.exists(v):
        missing.append((k, v))

print(f'\n--- INTEGRITY AUDIT ---')
print(f'Total Registered Terms: {len(diag_map_sorted)}')
print(f'Total Missing Files on Disk: {len(missing)}')
if missing:
    print('WARNING: Still missing:')
    for k, v in missing[:10]:
        print(f'  {k} -> {v}')
else:
    print('SUCCESS: 100% of diagram paths exist on disk!')
