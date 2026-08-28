import os
import json
import re

def main():
    print("--- 1. Checking core_dictionary_diagrams.js & dictionary_diagrams_map.json ---")
    if os.path.exists("dictionary_diagrams_map.json"):
        with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
            diag_map = json.load(f)
        print(f"Total entries in dictionary_diagrams_map.json: {len(diag_map)}")
    else:
        diag_map = {}

    # Inspect images in diagrams/
    diagrams_dir = "diagrams"
    files_in_dir = os.listdir(diagrams_dir) if os.path.exists(diagrams_dir) else []
    print(f"Total files in diagrams/ directory: {len(files_in_dir)}")

    # Check which mapped diagram files actually exist
    missing_files = []
    for k, path in diag_map.items():
        if not os.path.exists(path):
            missing_files.append((k, path))
    print(f"Missing image files referenced in map: {len(missing_files)}")

    # Let's inspect words in core_dictionary.js
    print("\n--- 2. Checking core_dictionary.js ---")
    with open("core_dictionary.js", "r", encoding="utf-8") as f:
        core_dict_content = f.read()

    # Find STEMDictionary word bank in core_dictionary.js
    matches = re.findall(r'word:\s*"([^"]+)"', core_dict_content)
    print(f"Found {len(matches)} words in core_dictionary.js")

    dict_words_set = set(w.lower().strip() for w in matches)

    # Check how many mapped diagram keys match an exact word in dictionary
    exact_matches = []
    unmatched_diag_keys = []
    for k in diag_map:
        clean_k = k.lower().strip()
        # Also clean up parenthetical aliases e.g. "abdomen (abdominal cavity)" -> "abdomen"
        base_k = re.sub(r'\(.*?\)', '', clean_k).strip()
        if clean_k in dict_words_set or base_k in dict_words_set:
            exact_matches.append(k)
        else:
            unmatched_diag_keys.append(k)

    print(f"Diagram keys exactly matching dictionary words (or base word): {len(exact_matches)}")
    print(f"Diagram keys NOT matching dictionary words: {len(unmatched_diag_keys)}")
    print("\nSample unmatched diagram keys:")
    for k in unmatched_diag_keys[:25]:
        print(f"  - {k} -> {diag_map[k]}")

if __name__ == "__main__":
    main()
