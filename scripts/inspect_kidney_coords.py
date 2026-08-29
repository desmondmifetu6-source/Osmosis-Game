import fitz
import json

doc = fitz.open("split_sections/778_PDFsam_Dictionary Book 2.pdf")
page = doc[4]

# Let's inspect text blocks and drawings
caption = page.search_for("Anatomy of the kidney")[0]
print("Caption rect:", caption)

# Let's find all text blocks and drawings near this caption
blocks = page.get_text("dict")["blocks"]
for b in blocks:
    if b.get("type") == 0:
        for l in b["lines"]:
            for s in l["spans"]:
                if "Renal" in s["text"] or "Nephron" in s["text"] or "Ureter" in s["text"]:
                    print("Label span:", s["text"], s["bbox"])

# Let's also check column bounds
# In this 2-column layout:
# The diagram is in one of the columns.
