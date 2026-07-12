import json
import re

data = json.load(open('dictionary_extracted.json', encoding='utf-8'))

print(f"Starting count: {len(data)}")

cleaned = []
for item in data:
    w = item['word'].strip()
    d = item['definition'].strip()
    
    # RULE: A word is malformed if it STARTS with a closing paren/bracket
    # or if it starts with a comma, period or semicolon (broken fragment from PDF split)
    if re.match(r'^[\)\],\.;]', w):
        continue
    
    # RULE: A word that ends with ')' is ONLY malformed if it has NO opening paren
    # e.g. "BOMB)" is bad (no opening paren)
    # but "ABATTOIR (SLAUGHTERHOUSE)" or "A HORIZON (HORIZON A)" are FINE
    if w.endswith(')') and '(' not in w:
        continue
    
    # RULE: Same logic for square brackets
    if w.endswith(']') and '[' not in w:
        continue
        
    # RULE: If the word is missing its first letters (e.g., "NERVE, CN6)" - fragment)
    # These typically have ) at the end and no ( anywhere OR start with lowercase 
    # after a space (mid-sentence fragment). Already caught by rules above mostly.
    
    cleaned.append({"word": w, "definition": d})

print(f"Final count: {len(cleaned)}")
print(f"Removed {len(data) - len(cleaned)} malformed fragments!")

with open('dictionary_extracted.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned, f, indent=4, ensure_ascii=False)
    
print("Saved clean dictionary!")
