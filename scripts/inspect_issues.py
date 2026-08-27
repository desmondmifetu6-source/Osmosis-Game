import json

with open("scripts/dictionary_issues_report.json", "r", encoding="utf-8") as f:
    rep = json.load(f)

issues = rep["issues"]
print(f"Truncated count: {len(issues['truncated_endings'])}")
for i, item in enumerate(issues["truncated_endings"]):
    print(f"{i+1}. [{item['letter']}] {item['raw']}")
    print(f"   DEF: {item['def']}\n")
