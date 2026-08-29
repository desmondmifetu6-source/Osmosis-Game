import json, sys, os

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

TRUE_ACID_DEF = (
    "1. It is generally defined as a sour-tasting compound that releases excess hydrogen ions (H+) "
    "in aqueous solution with a pH of less than 7, reacts with a base to form a salt and turns blue "
    "litmus red or a compound that can donate a proton or accept a pair of electrons to form a covalent "
    "bond with a base. Specifically, there are three common definitions for acids: the Arrhenius definition, "
    "the Brønsted-Lowry definition and the Lewis definition. The Arrhenius definition is a sour-tasting compound "
    "that releases excess hydrogen ions in an aqueous medium to form a solution with a pH less than 7. "
    "The Brønsted-Lowry definition is a compound that can donate a proton. The Lewis definition is a compound "
    "that can donate a proton or accept a pair of electrons to form a covalent bond with a base. Acids turn "
    "blue litmus paper red. Strong acids ionise completely (complete dissociation) in solution. Examples are "
    "hydrogen chloride acid (HCl), tetraoxosulfate(VI) acid (H2SO4) and trioxonitrate(V) acid (HNO3). On the other "
    "hand, weak acids only slightly ionise in solution. An example is ethanoic acid (CH3COOH). Acids can be "
    "solutions, liquids or solids. Acidification is the addition of acid to a solution to make it distinctly "
    "acidic or to make the pH to fall below 7. It also refers to the fall in the pH of less than 7 of water in "
    "lakes, rivers, wells and in the ground due to contamination by acidic gases such as sulfur dioxide (SO2), "
    "nitrogen oxides (NOx) and ammonia (NH3). 2. In computer science, it is also known as atomicity, "
    "consistency, isolation, durability and is a set of properties that guarantee that database transactions "
    "are processed reliably. In the context of databases, a single logical operation on the data is called "
    "a transaction. For example, a transfer of funds from one bank account to another, even involving multiple "
    "changes such as debiting one account and crediting another, is a single transaction."
)

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data.get('A', []):
    if item.get('word', '').lower() == 'acid':
        item['definition'] = TRUE_ACID_DEF
        item['raw_headword'] = 'ACID'
        break

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
print("Successfully corrected acid definition and synchronized core_dictionary.js!")
