import os
from PIL import Image

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"

def get_dimensions():
    files = [
        "Screenshot 2026-08-03 161441.png",
        "Screenshot 2026-08-03 161817.png",
        "Screenshot 2026-08-03 161835.png",
        "Screenshot 2026-08-03 162009.png",
        "Screenshot 2026-08-03 162107.png",
        "Screenshot 2026-08-03 162120.png",
        "Screenshot 2026-08-03 162141.png",
        "Screenshot 2026-08-03 162157.png",
        "Screenshot 2026-08-03 162218.png",
        "Screenshot 2026-08-03 162233.png"
    ]
    for f in files:
        p = os.path.join(src_dir, f)
        im = Image.open(p)
        print(f"{f}: size={im.size}, mode={im.mode}")

if __name__ == "__main__":
    get_dimensions()
