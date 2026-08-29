import json, os

DICT_JSON = "dictionary.json"

with open(DICT_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

# Update group ring
updated = False
for item in data.get("G", []):
    if item.get("word", "").lower() == "group ring":
        print("Found group ring! Updating definition...")
        item["definition"] = (
            "The set of all formal sums $\\sum_{x} \\alpha_x x$, where $x$ ranges over a multiplicative group "
            "and the $\\alpha_x$ of which all but finitely many are zero, are elements of a field (usually taken to be the complex numbers). "
            "The group ring of the group $G$ over a field is usually denoted $RG$. Multiplication and addition are defined by:\n\n"
            "$$\\sum_{x \\in G} \\alpha_x x + \\sum_{x \\in G} \\beta_x x = \\sum_{x \\in G} (\\alpha_x + \\beta_x) x$$\n\n"
            "and\n\n"
            "$$\\left( \\sum_{x \\in G} \\alpha_x x \\right) \\left( \\sum_{x \\in G} \\beta_x x \\right) = \\sum_{x \\in G} \\left( \\sum_{st = x} \\alpha_s \\beta_t \\right) x$$"
        )
        updated = True
        break

if updated:
    with open(DICT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("Saved dictionary.json.")
else:
    print("Could not find group ring in G.")
