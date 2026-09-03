import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BASE_DEF = (
    "1. In chemistry, it is a substance which reacts with an acid to form salt and water only, "
    "or according to the Brønsted-Lowry theory it is a proton (hydrogen ion) acceptor, while "
    "the Lewis theory defines it as an electron pair donor. Bases are usually metal oxides or "
    "hydroxides. A soluble base is referred to as an alkali if it contains and releases hydroxide "
    "ions (OH−) quantitatively. Examples of common bases are sodium hydroxide and ammonia. Metal "
    "oxides, hydroxides and especially alkoxides are basic and counter anions of weak acids are "
    "weak bases. A base accepts protons from hydronium ions or donates hydroxide ions to a solution, "
    "thus lowering the concentration of hydronium ions and raising the pH. However, an acid donates "
    "protons to a solution or accepts OH−, thus increasing the concentration of hydronium and "
    "lowering the pH. The pH level of a basic solution is higher than 7. A strong base is a base "
    "which hydrolyses completely, raising the pH of the solution toward 14. Common examples of "
    "strong bases are the hydroxides of alkali metals and alkaline earth metals like NaOH and "
    "Ca(OH)2. Bases turn red litmus paper blue, phenolphthalein pink, keep bromothymol blue in "
    "its natural colour of blue and turns methyl orange yellow. Bases feel slimy or soapy on "
    "fingers, due to saponification of the lipids in human skin; however, concentrated bases are "
    "caustic on organic matter and react violently with acidic substances. Aqueous solutions or "
    "molten bases dissociate in ions and conduct electricity. "
    "2. In mathematics, also called radix, it is the number of different single digit symbols used "
    "in a particular number system. In the usual decimal counting system of numbers 0, 1, 2, 3, 4, "
    "5, 6, 7, 8, 9 the base is 10. "
    "3. A number that when raised to a potential power or when multiplied by itself a number of times "
    "has a logarithm equal to the power. For example, 10^3 = 10 × 10 × 10 = 1,000. "
    "4. The side or face of a geometric figure, usually the one at the bottom, to which an altitude "
    "is or is thought to be drawn. "
    "5. The number of distinct residues in a system of modular arithmetic. "
    "6. A substructure of a given mathematical structure from which the whole structure can be "
    "generated. "
    "7. A base for a topology; a collection of open sets such that every member of the topology is "
    "a union of members of the collection. "
    "8. In botany, it is the bottom or lower portion of the leaf blade nearest to the point of "
    "attachment."
)

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check if base already exists
already_exists = any(item.get('word', '').lower() == 'base' for item in data.get('B', []))
if already_exists:
    print("'base' entry already exists in dictionary.json — skipping insert.")
else:
    # Find the right position (alphabetically before 'base address')
    insert_index = 0
    for i, item in enumerate(data['B']):
        word = item.get('word', '').lower()
        if word == 'base address':
            insert_index = i
            break

    new_entry = {
        "word": "base",
        "raw_headword": "BASE",
        "synonyms": ["alkali", "radix"],
        "definition": BASE_DEF
    }

    data['B'].insert(insert_index, new_entry)
    print(f"Inserted 'base' entry at position {insert_index} in the B section.")

    with open('dictionary.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("dictionary.json updated successfully.")

cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
print("core_dictionary.js rebuilt successfully!")
