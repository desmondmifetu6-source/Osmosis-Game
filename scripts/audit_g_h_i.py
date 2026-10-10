"""
Audit formula enrichment coverage for Sections G, H, and I — summary only.
"""
import json, os

dictPath = os.path.join(os.path.dirname(__file__), '..', 'dictionary.json')
with open(dictPath, 'r', encoding='utf-8') as f:
    d = json.load(f)

for section in ['G', 'H', 'I']:
    entries = d.get(section, [])
    enriched = [e for e in entries if '$' in e.get('definition','') or 'formula' in e]
    unenriched = [e for e in entries if '$' not in e.get('definition','') and 'formula' not in e]
    print(f"\n=== Section {section} ===")
    print(f"  Total     : {len(entries)}")
    print(f"  Enriched  : {len(enriched)} ({round(100*len(enriched)/len(entries))}%)" if entries else "  (empty)")
    print(f"  Unenriched: {len(unenriched)}")
    # Show first 30 unenriched terms for scoping
    print(f"  First 30 unenriched:")
    for e in unenriched[:30]:
        print(f"    - {e['word']}")
