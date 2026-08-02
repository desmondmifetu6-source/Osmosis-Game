"""
test_caption_parsing.py
"""
import fitz
import re

doc = fitz.open("Dictionary Book 2.pdf")

def parse_caption(text):
    # Matches "Fig. I: The alimentary canal of a human" -> "alimentary canal"
    # Matches "Fig 1: Structure of atom" -> "structure of atom"
    # Matches "Fig. IV: Spherical aberration (lens)" -> "spherical aberration"
    m = re.search(r"Fig\.?\s+[I|V|X|\d]+\s*:\s*(?:The\s+)?([^.\n\r]+)", text, re.IGNORECASE)
    if m:
        cap = m.group(1).strip()
        # Remove parenthetical info if any, e.g. "of a human" -> "alimentary canal"
        cap_clean = re.sub(r"\s*\(.*?\)", "", cap)
        cap_clean = re.sub(r"\s+of\s+(?:a|an|the)\s+.*$", "", cap_clean, flags=re.IGNORECASE)
        return cap_clean.strip()
    return None

test_cases = [
    "Fig. I: The alimentary canal of a human",
    "Fig II: The alimentary canal of a rabbit",
    "Fig. IV: Spherical aberration (lens)",
    "Fig. 3: Structure of a plant cell",
    "Fig. I: Types of Distortion"
]

for tc in test_cases:
    print(f"'{tc}'  -->  '{parse_caption(tc)}'")
