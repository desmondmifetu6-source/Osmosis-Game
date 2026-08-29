import json, os, re
import fitz
from PIL import Image

def deep_audit():
    with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    print(f"Deep auditing all {len(diag_map)} mapped diagrams...")

    text_rich_images = []
    
    for term, path in diag_map.items():
        if not os.path.exists(path):
            continue
            
        try:
            with Image.open(path) as img:
                w, h = img.size
                
                # Check aspect ratios and dimensions that typically correlate with column screenshots
                # A standard book text column is ~300-350 px wide and >350 px tall
                if (w >= 250 and w <= 380) and h > 450:
                    text_rich_images.append((term, path, f"Tall column crop ({w}x{h})"))
                elif w < 100 or h < 60:
                    text_rich_images.append((term, path, f"Tiny/fragment crop ({w}x{h})"))
        except Exception as e:
            pass

    print(f"\nSuspicious text-column crops found: {len(text_rich_images)}")
    for t, p, r in text_rich_images:
        print(f"  - {t:35} -> {r} ({p})")

if __name__ == "__main__":
    deep_audit()
