import json
import os
import re

def main():
    dict_path = 'dictionary.json'
    with open(dict_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    loose_keys = [k for k in list(data.keys()) if len(k) > 1 and not k.isdigit()]
    print(f"Found {len(loose_keys)} loose top-level keys in {dict_path}.")

    moved_count = 0
    for k in loose_keys:
        val = data.pop(k)
        # Determine first alphabetic character
        first_char = None
        for ch in k:
            if ch.isalpha():
                first_char = ch.upper()
                break
        if not first_char:
            first_char = '1'

        if first_char not in data:
            data[first_char] = []

        # Parse definition and headword if available
        def_text = val if isinstance(val, str) else json.dumps(val)
        
        # Check if already present in data[first_char]
        existing = any(item.get('word', '').lower() == k.lower() for item in data[first_char] if isinstance(item, dict))
        if not existing:
            # Try to extract synonyms from raw headword if present, e.g. "WORD (SYNONYM1; SYNONYM2)"
            synonyms = []
            m = re.match(r'^([A-Za-z0-9\s,\-\.]+)\s*\(([^)]+)\)', def_text[:120])
            if m:
                syn_str = m.group(2)
                synonyms = [s.strip().lower() for s in syn_str.split(';') if s.strip()]

            entry = {
                "word": k.lower().strip(),
                "raw_headword": k.upper().strip(),
                "synonyms": synonyms,
                "definition": def_text.strip()
            }
            data[first_char].append(entry)
            moved_count += 1

    print(f"Successfully integrated {moved_count} loose terms into proper letter buckets!")

    # Sort entries in each letter bucket alphabetically
    for letter in data:
        if isinstance(data[letter], list):
            data[letter].sort(key=lambda x: x.get('word', '').lower() if isinstance(x, dict) else str(x).lower())

    with open(dict_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("Saved clean dictionary.json.")

if __name__ == '__main__':
    main()
