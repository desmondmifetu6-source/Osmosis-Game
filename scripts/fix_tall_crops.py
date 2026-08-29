import json, os, re

MAP_FILE = "dictionary_diagrams_map.json"
JS_FILE = "core_dictionary_diagrams.js"

with open(MAP_FILE, "r", encoding="utf-8") as f:
    diag_map = json.load(f)

# 1. Remove cubic resolvent equation (text formula crop)
if "cubic resolvent equation" in diag_map:
    del diag_map["cubic resolvent equation"]
    print("Removed cubic resolvent equation")

# 2. Fix nervines -> reassign to nervous system
if "nervines" in diag_map:
    nervines_img = diag_map.pop("nervines")
    diag_map["nervous system"] = nervines_img
    print("Reassigned nervines diagram to 'nervous system'")

# Save cleaned map
with open(MAP_FILE, "w", encoding="utf-8") as f:
    json.dump(diag_map, f, ensure_ascii=False, indent=4)

# Regenerate core_dictionary_diagrams.js
lines = [
    "// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)",
    "",
    "const DictionaryDiagrams = {"
]
sorted_keys = sorted(diag_map.keys())
for i, k in enumerate(sorted_keys):
    comma = "," if i < len(sorted_keys) - 1 else ""
    escaped_k = json.dumps(k)
    escaped_v = json.dumps(diag_map[k])
    lines.append(f"    {escaped_k}: {escaped_v}{comma}")
lines.append("};")
lines.append("")
lines.append("if (typeof window !== 'undefined') {")
lines.append("    window.DictionaryDiagrams = DictionaryDiagrams;")
lines.append("}")
lines.append("")
lines.append("if (typeof module !== 'undefined' && module.exports) {")
lines.append("    module.exports = DictionaryDiagrams;")
lines.append("}")
lines.append("")

with open(JS_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"Updated {JS_FILE} successfully with {len(diag_map)} clean diagrams.")
