"""
Safely synchronizes dictionary.json into core_dictionary.js without modifying
any engine logic, UI methods, or formulas.
"""
import json
import os

BASE = r"c:\Users\Desmond\Desktop\final_osmosis"
dict_json_path = os.path.join(BASE, "dictionary.json")
core_js_path = os.path.join(BASE, "core_dictionary.js")

print("1. Loading dictionary.json...")
with open(dict_json_path, "r", encoding="utf-8") as f:
    dict_data = json.load(f)

# Verify 'dc motor' is in the data
found_dc = False
for k, entries in dict_data.items():
    if isinstance(entries, list):
        for e in entries:
            if isinstance(e, dict) and e.get("word", "").lower() == "dc motor":
                found_dc = True
                print(f"   Found 'dc motor' in section '{k}'!")
                break
if not found_dc:
    print("WARNING: 'dc motor' not found in dictionary.json!")

print("2. Reading core_dictionary.js engine lines...")
with open(core_js_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

header_line = lines[0]  # Line 1: comment header
engine_lines = lines[2:]  # Lines 3 to end: the entire (function() { ... })(); engine

print(f"   Preserving {len(engine_lines)} lines of engine code (100% byte-for-byte).")

print("3. Generating updated const wordBank line...")
new_line_2 = "const wordBank = " + json.dumps(dict_data, ensure_ascii=False) + ";\n"

print("4. Writing back to core_dictionary.js...")
with open(core_js_path, "w", encoding="utf-8") as f:
    f.write(header_line)
    f.write(new_line_2)
    f.writelines(engine_lines)

print("5. Verification...")
with open(core_js_path, "r", encoding="utf-8") as f:
    v_lines = f.readlines()

print(f"   New line count: {len(v_lines)} lines.")
print(f"   Line 1: {v_lines[0].strip()}")
print(f"   Line 2 prefix: {v_lines[1][:40]}")
print(f"   Line 3: {repr(v_lines[2])}")
print(f"   Line 4: {repr(v_lines[3])}")
print(f"   Tail: {v_lines[-1].strip()}")
print("Synchronization complete!")
