import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 60)
print("  OSMOSIS DICTIONARY - FORMULA ENRICHMENT AUDIT")
print("=" * 60)

total_entries = 0
total_with_formula = 0

# Check all sections A-Z plus numeric
sections_order = [str(i) for i in range(1, 10)] + list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

for sec in sections_order:
    if sec not in data:
        continue
    entries = data[sec]
    count = len(entries)
    with_formula = sum(1 for e in entries if 'formula' in e)
    total_entries += count
    total_with_formula += with_formula
    pct = (with_formula / count * 100) if count > 0 else 0
    bar = '#' * int(pct / 5) + '.' * (20 - int(pct / 5))
    print(f"  Section {sec:>3}: {count:>5} entries | {with_formula:>4} formulas [{bar}] {pct:.1f}%")

print("=" * 60)
print(f"  TOTAL:    {total_entries:>5} entries | {total_with_formula:>4} formulas")
print(f"  OVERALL COVERAGE: {total_with_formula/total_entries*100:.2f}%")
print("=" * 60)

# Spot check a few entries in S, T, R, Q
spot_check = [
    ('Q', 'quotient rule'),
    ('R', 'resistance'),
    ('R', 'rydberg formula'),
    ('S', 'standard deviation'),
    ('S', 'sine rule'),
    ('T', 'torque'),
    ('U', 'universal law of gravitation'),
    ('V', 'velocity'),
    ('W', 'work'),
    ('Y', "young's modulus"),
    ('Z', 'z-score'),
]

print("\n  SPOT CHECKS:")
print("-" * 60)
for sec, word in spot_check:
    if sec not in data:
        print(f"  MISS Section {sec} missing!")
        continue
    found = next((e for e in data[sec] if e.get('word','').strip().lower() == word), None)
    if found and 'formula' in found:
        print(f"  OK  [{sec}] {word}")
        print(f"      formula: {found['formula'][:70]}...")
    elif found:
        print(f"  FAIL[{sec}] {word} -- FOUND but NO FORMULA!")
    else:
        print(f"  ??? [{sec}] '{word}' -- not found in section {sec}")

print("=" * 60)
