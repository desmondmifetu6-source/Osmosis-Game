import fitz

doc = fitz.open("Dictionary Book 2.pdf")
page = doc[120] # page 121 (0-indexed 120)

blocks = page.get_text("dict")["blocks"]
print("--- ALL TEXT ON PAGE 121 ---")
for b in blocks:
    if b.get("type") == 0:
        for l in b["lines"]:
            for s in l["spans"]:
                if s["color"] == 35533: # blue
                    print(f"BLUE: '{s['text']}' at y0={s['bbox'][1]:.1f}, x0={s['bbox'][0]:.1f}, flags={s['flags']}")
                elif "ALIMENTARY" in s["text"].upper():
                    print(f"TEXT: '{s['text']}' at y0={s['bbox'][1]:.1f}, x0={s['bbox'][0]:.1f}, flags={s['flags']}, color={s['color']}")
