import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_word_in_pdf(pdf_path, query_hw):
    doc = fitz.open(pdf_path)
    print(f"Searching for '{query_hw}' in {pdf_path} ({len(doc)} pages)...")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        if query_hw.upper() in text.upper():
            print(f"\n--- Found on Page {page_num + 1} ---")
            # print surrounding lines
            lines = text.split('\n')
            for i, line in enumerate(lines):
                if query_hw.upper() in line.upper():
                    start = max(0, i - 2)
                    end = min(len(lines), i + 25)
                    print('\n'.join(lines[start:end]))
                    print("=" * 40)

if __name__ == "__main__":
    find_word_in_pdf("Dictionary Book 2.pdf", "ACCESS CONTROL LIST")
    find_word_in_pdf("Dictionary Book 2.pdf", "AGRICULTURAL ADVISORY SERVICES")
    find_word_in_pdf("Dictionary Book 2.pdf", "AMORPHOUS CARBON")
