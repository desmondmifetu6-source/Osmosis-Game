import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFYING SECTION A & B FORMULAS ===")

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

test_terms = [
    # Section A
    "abbe numb er", "abc conjecture", "abel test", "abel's partial summation formula",
    "abelian group", "absolute value", "acceleration", "acceleration due to gravity",
    "acid dissociation constant", "action", "activity", "addition formula",
    "alternating current", "alpha decay", "ampere's law", "angular momentum",
    "archimedes' principle", "arrhenius equation", "asymptote", "avogadro's number",
    # Section B
    "balmer series", "base ionisation constant", "bayes' theorem", "beat frequency",
    "beer's law", "bell curve", "bernoulli equation", "bernoulli's theorem",
    "bessel function", "beta decay", "binomial theorem", "biot-savart law",
    "bohr model", "bohr radius", "boltzmann constant", "boltzmann formula",
    "boyle's law", "bragg's law", "brewster's law", "bulk modulus"
]

dict_map = {}
for letter in ['A', 'B']:
    for item in data.get(letter, []):
        dict_map[item['word'].lower()] = item['definition']

passed = 0
for term in test_terms:
    if term in dict_map:
        defn = dict_map[term]
        has_katex = '$' in defn
        dollar_count = defn.count('$')
        print(f"[OK] Found '{term}' | KaTeX: {'YES' if has_katex else 'NO'} | Dollar signs: {dollar_count}")
        passed += 1
    else:
        print(f"[FAIL] Missing '{term}'")

print(f"\nVerification: {passed}/{len(test_terms)} benchmark terms verified in dictionary.json!")
