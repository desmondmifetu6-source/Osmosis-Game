import json

with open('detected_math_ab.json', 'r', encoding='utf-8') as f:
    cand = json.load(f)

test_words = [
    'abbe numb er', 'abc conjecture', 'abel test', 'abel test for uniform convergence',
    "abel's partial summation formula", 'abelian group', 'abelian theorem',
    'absolute convergence', 'absolute value', 'absolute value function',
    'absolute zero', 'absorbance', 'absorbed dose', 'absorption law', 'absorptive power',
    'acceleration', 'acceleration due to gravity'
]

with open('batch_a_inspect.txt', 'w', encoding='utf-8') as out:
    for item in cand['A']:
        if item['word'] in test_words:
            out.write(f"=== {item['word']} ===\n")
            out.write(item['definition'] + "\n\n")

print("Saved batch_a_inspect.txt successfully.")
