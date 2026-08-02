import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_exact_end(pdf_path):
    doc = fitz.open(pdf_path)
    for p in range(1460, 1478):
        text = doc[p].get_text()
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        snippet = " | ".join(lines[:3]) if lines else "EMPTY"
        print(f"Page {p+1}: {snippet[:120]}")

if __name__ == "__main__":
    find_exact_end("Dictionary Book 2.pdf")
