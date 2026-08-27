import json
import re

with open("dictionary_extracted_final.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total entries in dictionary_extracted_final.json: {len(data)}")

# Let's inspect definitions ending with " A", " B", " C", etc.
stray_letter_ends = []
for item in data:
    d = item.get("definition", "").strip()
    w = item.get("word", "")
    hw = item.get("raw_headword", "")
    
    # Check if definition ends with a stray single capital letter preceded by a space or period
    m = re.search(r'[\.\!\?]?\s+([A-Z])$', d)
    if m:
        stray_letter_ends.append((w, hw, d, m.group(1)))

print(f"Found {len(stray_letter_ends)} definitions ending with stray capital letter.")
print("Sample:")
for s in stray_letter_ends[:10]:
    print("  Word:", s[0])
    print("  End:", s[2][-40:])
