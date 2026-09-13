import os

files = sorted(os.listdir('f-j diagrams'))
batch_2 = files[30:60]
for idx, f in enumerate(batch_2, start=31):
    print(f"{idx}: {f}")
