import json
import os

def main():
    map_path = 'dictionary_diagrams_map.json'
    js_path = 'core_dictionary_diagrams.js'

    print("Loading", map_path)
    with open(map_path, 'r', encoding='utf-8') as f:
        diag_map = json.load(f)

    updated_count = 0
    clean_map = {}
    for k, v in diag_map.items():
        val = v.strip()
        if not val.startswith('diagrams/') and not val.startswith('http') and not val.startswith('/'):
            val = 'diagrams/' + val
            updated_count += 1
        clean_map[k.lower().strip()] = val

    sorted_map = dict(sorted(clean_map.items()))

    print(f"Fixed {updated_count} paths to have 'diagrams/' prefix.")
    print(f"Total entries: {len(sorted_map)}")

    with open(map_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)
    print("Saved updated", map_path)

    json_str = json.dumps(sorted_map, indent=2, ensure_ascii=False)
    js_content = f"""// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)

const DictionaryDiagrams = {json_str};

if (typeof window !== 'undefined') {{
  window.DictionaryDiagrams = DictionaryDiagrams;
  window.DICTIONARY_DIAGRAMS = DictionaryDiagrams;
}}
if (typeof module !== 'undefined') {{
  module.exports = DictionaryDiagrams;
}}
"""

    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print("Saved updated", js_path)

if __name__ == '__main__':
    main()
