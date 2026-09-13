import os
files = sorted(os.listdir('f-j diagrams'))
batch = files[60:70]
for idx, f in enumerate(batch, start=61):
    print(f"{idx}: {f}")
