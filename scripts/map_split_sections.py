import os
import fitz
import json

files = sorted(os.listdir('split_sections'))
result = []
for f in files:
    if f.endswith('.pdf'):
        path = os.path.join('split_sections', f)
        doc = fitz.open(path)
        first_txt = doc[0].get_text()[:200].replace('\n', ' ')
        result.append({
            'file': f,
            'pages': len(doc),
            'sample': first_txt
        })

with open('scripts/split_sections_map.json', 'w', encoding='utf-8') as out:
    json.dump(result, out, indent=2)

print(f"Mapped {len(result)} split section files to scripts/split_sections_map.json")
