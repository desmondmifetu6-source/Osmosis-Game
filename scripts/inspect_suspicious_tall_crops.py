import fitz, os, json

doc = fitz.open("Dictionary Book 2.pdf")

terms_to_check = [
    "AEROPLANE", "ANOMERS", "APOTHECIUM", "BLAST FURNACE",
    "CUBIC RESOLVENT EQUATION", "DISTORTION", "HAUSTORIUM", "NERVINES"
]

print("=== INSPECTING SUSPICIOUS TALL CROPS IN PDF ===\n")

for term in terms_to_check:
    for pno in range(len(doc)):
        txt = doc[pno].get_text()
        if f"{term}:" in txt or f"{term} (" in txt or f"\n{term}\n" in txt:
            idx = txt.find(term)
            snippet = txt[max(0, idx-5):min(len(txt), idx+300)].replace("\n", " ")
            print(f"TERM: {term} (Page {pno+1})")
            print(f"  Snippet: {snippet[:150]}...")
            print("-" * 50)
            break
