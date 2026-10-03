"""
integrate_lm_batch_2.py — Processes Section L-M Batch 2 Diagrams (Screenshots 11-20)
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
    ('Screenshot_26-9-2026_142138_.jpeg', 'dict_layering.png',
     ['layering', 'plant layering']),
    ('Screenshot_26-9-2026_142221_.jpeg', 'dict_leclanche_dry_cell.png',
     ['leclanche cell', 'leclanche dry cell', 'dry cell']),
    ('Screenshot_26-9-2026_142245_.jpeg', 'dict_types_of_lenses.png',
     ['lens', 'lenses', 'types of lenses', 'converging lens', 'diverging lens', 'convex lens', 'concave lens']),
    ('Screenshot_26-9-2026_14225_.jpeg', 'dict_parts_of_a_leaf.png',
     ['leaf', 'parts of a leaf', 'leaf structure', 'petiole']),
    ('Screenshot_26-9-2026_14232_.jpeg', 'dict_leslies_cube.png',
     ["leslie's cube", 'leslie cube']),
    ('Screenshot_26-9-2026_142343_.jpeg', 'dict_levers.png',
     ['lever', 'levers', 'first class lever', 'second class lever', 'third class lever', 'classes of levers']),
    ('Screenshot_26-9-2026_142429_.jpeg', 'dict_parabola_line_of_symmetry.png',
     ['line of symmetry', 'parabola line of symmetry', 'axis of symmetry of a parabola']),
    ('Screenshot_26-9-2026_142442_.jpeg', 'dict_lcao.png',
     ['linear combination of atomic orbitals', 'linear combination of atomic orbitals (lcao)', 'lcao']),
    ('Screenshot_26-9-2026_14248_.jpeg', 'dict_ligulate_corolla.png',
     ['ligulate', 'ligulate corolla']),
    ('Screenshot_26-9-2026_14267_.jpeg', 'dict_linear_leaf.png',
     ['linear leaf', 'linear']),
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

print("\n--- DICTIONARY TERM VERIFICATION ---")
for src_name, dest_name, terms in BATCH:
    matched = [t for t in terms if t in dict_words]
    print(f"{dest_name}: matched in dictionary.json -> {matched}")

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

print(f'\nCopied: {copied}/{len(BATCH)} Section L-M Batch 2 diagrams')

diag_map_sorted = dict(sorted(diag_map.items()))
with open(MAP_JSON, 'w', encoding='utf-8') as f:
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
print(f'Saved {MAP_JSON} ({len(diag_map_sorted)} entries)')

with open(DIAGRAMS_JS, 'w', encoding='utf-8') as f:
    f.write('// core_dictionary_diagrams.js — Auto-generated. DO NOT EDIT MANUALLY.\n')
    f.write('// Last updated: Section L-M Batch 2 (screenshots 11-20)\n\n')
    f.write('var DictionaryDiagrams = ')
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
    f.write(';\n\nif (typeof module !== "undefined") { module.exports = DictionaryDiagrams; }\n')
print(f'Regenerated {DIAGRAMS_JS}')

missing = []
for k, v in diag_map_sorted.items():
    if not os.path.exists(v):
        missing.append((k, v))

print(f'\n--- INTEGRITY AUDIT ---')
print(f'Total Registered Terms: {len(diag_map_sorted)}')
print(f'Total Missing Files on Disk: {len(missing)}')
if missing:
    print('WARNING: Missing files:')
    for k, v in missing[:10]:
        print(f'  {k} -> {v}')
else:
    print('SUCCESS: 100% of diagram paths exist on disk!')
