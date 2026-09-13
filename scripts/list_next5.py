import os
files = sorted(os.listdir('f-j diagrams'))
batch = files[70:75]
for idx, f in enumerate(batch, start=71):
    print(f"{idx}: {f}")
