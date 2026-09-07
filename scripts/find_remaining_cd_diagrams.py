import os
import glob
import re

processed = set()
for s in glob.glob('scripts/integrate_cd*.py'):
    with open(s, 'r', encoding='utf-8') as f:
        content = f.read()
    for m in re.findall(r'Screenshot[^\'",\s]+\.(?:jpeg|png)', content):
        processed.add(m)

all_files = sorted(os.listdir('c-d didagrams'))
remaining = [f for f in all_files if f not in processed]
print(f"Total files: {len(all_files)}")
print(f"Already processed in scripts: {len(processed)}")
print(f"Remaining unprocessed: {len(remaining)}")
for i, f in enumerate(remaining):
    print(f"{i+1}: {f}")
