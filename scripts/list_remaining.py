import os

files = sorted(os.listdir('f-j diagrams'))
print(f"Total files in f-j diagrams: {len(files)}")
remaining = files[75:]
print(f"Remaining count: {len(remaining)}")
for idx, f in enumerate(remaining, start=76):
    print(f"{idx}: {f}")
