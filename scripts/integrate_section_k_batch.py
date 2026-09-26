"""
integrate_section_k_batch.py — Processes Section K Diagrams (Screenshots 1-12)
and normalizes all diagram map paths.
"""
import os, json, shutil, sys

sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR      = 'k_diagrams'
DIAGRAMS_DIR = 'diagrams'
MAP_JSON     = 'dictionary_diagrams_map.json'
DIAGRAMS_JS  = 'core_dictionary_diagrams.js'

BATCH = [
    ('Screenshot_24-9-2026_171045_.jpeg', 'dict_kainic_acid.png',
     ['kainic acid', 'chemical structure of kainic acid', 'kainate', '2-carboxy-3-carboxymethyl-4-isopropenylpyrrolidine']),
    ('Screenshot_24-9-2026_171110_.jpeg', 'dict_keeper.png',
     ['keeper', 'magnetic keeper', 'keepers for bar magnets', 'keeper for horse-shoe magnet', 'horseshoe magnet keeper']),
    ('Screenshot_24-9-2026_171123_.jpeg', 'dict_kekule_structure_of_benzene.png',
     ['kekule structure', 'kekule structure of benzene', 'kekule formula', 'kekulé structure', 'kekulé structure of benzene']),
    ('Screenshot_24-9-2026_171151_.jpeg', 'dict_ketal.png',
     ['ketal', 'formation of a ketal', 'hemiketal']),
    ('Screenshot_24-9-2026_171217_.jpeg', 'dict_ketose.png',
     ['ketose', 'types of ketose', 'ketose sugar', 'ketoses']),
    ('Screenshot_24-9-2026_17126_.jpeg', 'dict_ketamine.png',
     ['ketamine', 'chemical structure of ketamine']),
    ('Screenshot_24-9-2026_17133_.jpeg', 'dict_kidney_anatomy.png',
     ['anatomy of the kidney', 'kidney anatomy', 'renal cortex', 'renal medulla', 'renal pyramid', 'renal pelvis', 'nephron', 'major calyx', 'minor calyx']),
    ('Screenshot_24-9-2026_171434_.jpeg', 'dict_kirchoffs_first_law.png',
     ["kirchoff's first law", 'kirchoffs first law', "kirchoff's current law", 'kirchoffs current law', 'kcl', 'junction rule']),
    ('Screenshot_24-9-2026_171446_.jpeg', 'dict_kirchoffs_second_law.png',
     ["kirchoff's second law", 'kirchoffs second law', "kirchoff's voltage law", 'kirchoffs voltage law', 'kvl', 'loop rule']),
    ('Screenshot_24-9-2026_171458_.jpeg', 'dict_kjeldahls_method.png',
     ["kjeldahl's method", 'kjeldahls method', 'kjeldahl method', "kjeldahl's flask", 'kjeldahls flask', "estimating nitrogen by kjeldahl's method", 'estimating nitrogen by kjeldahls method']),
    ('Screenshot_24-9-2026_171514_.jpeg', 'dict_kite.png',
     ['kite', 'kite (a geometric figure)', 'geometric kite']),
    ('Screenshot_24-9-2026_171540_.jpeg', 'dict_knoevenagel_reaction.png',
     ['knoevenagel reaction', 'knoevenagel condensation']),
]

os.makedirs(DIAGRAMS_DIR, exist_ok=True)

with open(MAP_JSON, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

# 1. Normalize existing keys missing 'diagrams/' prefix
fixed_prefixes = 0
for k, v in list(diag_map.items()):
    if not v.startswith('diagrams/') and not v.startswith('assets/'):
        target = f'diagrams/{v}'
        if os.path.exists(target):
            diag_map[k] = target
            fixed_prefixes += 1

print(f'Normalized {fixed_prefixes} paths missing diagrams/ prefix')

# 2. Copy and map new Section K images
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

print(f'\nCopied: {copied}/{len(BATCH)} Section K diagrams')

# 3. Sort and save JSON map
diag_map_sorted = dict(sorted(diag_map.items()))
with open(MAP_JSON, 'w', encoding='utf-8') as f:
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
print(f'Saved {MAP_JSON} ({len(diag_map_sorted)} entries)')

# 4. Regenerate JS bundle
with open(DIAGRAMS_JS, 'w', encoding='utf-8') as f:
    f.write('// core_dictionary_diagrams.js — Auto-generated. DO NOT EDIT MANUALLY.\n')
    f.write('// Last updated: Section K Batch (screenshots 1-12)\n\n')
    f.write('var DictionaryDiagrams = ')
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
    f.write(';\n\nif (typeof module !== "undefined") { module.exports = DictionaryDiagrams; }\n')
print(f'Regenerated {DIAGRAMS_JS}')

# 5. Integrity Check
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
