import json

with open("dictionary.json", "r", encoding="utf-8") as f:
    d = json.load(f)

targets = ["hydraulic", "hydrogen", "hydromet"]
results = {t: [] for t in targets}

for sec, entries in d.items():
    if isinstance(entries, list):
        for item in entries:
            w = item.get("word", "").strip()
            raw = item.get("raw_headword", "").strip()
            syns = item.get("synonyms", [])
            all_str = [w, raw] + syns
            for t in targets:
                if any(t in s.lower() for s in all_str if isinstance(s, str)):
                    results[t].append((w, raw, syns))

with open("scripts/verify_results.txt", "w", encoding="utf-8") as out:
    for t, hits in results.items():
        out.write(f"=== {t} ===\n")
        for h in hits:
            out.write(f"  {h[0]} | {h[1]} | {h[2]}\n")

print("Wrote results to scripts/verify_results.txt")
