import json

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("DEEP CHECK - Sections A through K")
print("=" * 60)

for sec in 'ABCDEFGHIJK':
    if sec not in data:
        print(f"Section {sec}: NOT FOUND")
        continue
    entries = data[sec]
    
    has_formula_field = [e for e in entries if 'formula' in e]
    has_latex_in_def  = [e for e in entries if '$$' in e.get('definition', '')]
    has_formula_desc  = [e for e in entries if 'formula_description' in e]
    
    print(f"\nSection {sec} ({len(entries)} entries):")
    print(f"  'formula' field present:        {len(has_formula_field)}")
    print(f"  '$$ LaTeX' in definition:        {len(has_latex_in_def)}")
    print(f"  'formula_description' present:   {len(has_formula_desc)}")
    
    # Show a sample with latex
    if has_latex_in_def:
        sample = has_latex_in_def[0]
        print(f"  Sample: [{sample.get('word','')}]")
        print(f"    formula field: {'YES' if 'formula' in sample else 'NO'}")
        defn = sample.get('definition','')
        idx = defn.find('$$')
        if idx >= 0:
            print(f"    LaTeX snippet: {defn[idx:idx+60]}...")
