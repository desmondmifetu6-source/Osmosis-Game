import os
import numpy as np
from PIL import Image

src_dir = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images"
out_dir = r"c:\Users\Desmond\Desktop\final_osmosis\diagrams"

def clean_and_crop_image(img_path):
    im = Image.open(img_path).convert("RGBA")
    # Convert transparent pixels or near-white to white
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    im = Image.alpha_composite(bg, im).convert("RGB")
    arr = np.array(im)
    
    # We want to identify horizontal separator lines that are near top or bottom.
    # Typically, a separator line is a row where many pixels are very dark (< 60) across >= 70% width.
    h, w, _ = arr.shape
    gray = np.mean(arr, axis=2)
    
    # Find separator lines near top (y < h * 0.15)
    top_crop = 0
    for y in range(int(h * 0.20)):
        dark_ratio = np.sum(gray[y, :] < 100) / w
        if dark_ratio > 0.4: # Horizontal line detected
            top_crop = y + 2
            
    # Find separator lines near bottom (y > h * 0.85)
    bottom_crop = h
    for y in range(h - 1, int(h * 0.80), -1):
        dark_ratio = np.sum(gray[y, :] < 100) / w
        if dark_ratio > 0.4: # Horizontal line detected
            bottom_crop = y - 2
            
    if top_crop >= bottom_crop:
        top_crop = 0
        bottom_crop = h

    cropped = im.crop((0, top_crop, w, bottom_crop))
    
    # Now trim remaining whitespace with a 10px margin
    c_arr = np.array(cropped)
    c_gray = np.mean(c_arr, axis=2)
    # find bounding box of content (pixels < 240)
    rows = np.any(c_gray < 240, axis=1)
    cols = np.any(c_gray < 240, axis=0)
    if np.any(rows) and np.any(cols):
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        # pad by 12px
        ch, cw, _ = c_arr.shape
        rmin = max(0, rmin - 12)
        rmax = min(ch, rmax + 13)
        cmin = max(0, cmin - 12)
        cmax = min(cw, cmax + 13)
        final_img = cropped.crop((cmin, rmin, cmax, rmax))
        return final_img
    return cropped

# Let's inspect cropping for Image 1 to 10
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

os.makedirs("scratch/batch1_preview", exist_ok=True)
for idx, f in enumerate(files):
    p = os.path.join(src_dir, f)
    res = clean_and_crop_image(p)
    out_p = f"scratch/batch1_preview/preview_{idx+1}.png"
    res.save(out_p)
    print(f"Processed {f} -> size {res.size} saved to {out_p}")
