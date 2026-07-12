import json
import re
import sys

OUT = open('scripts/scan_results.txt', 'w', encoding='utf-8')

def p(s=''):
    OUT.write(s + '\n')

data = json.load(open('dictionary_extracted.json', encoding='utf-8'))

categories = {
    'single_letter': [],
    'single_digit': [],
    'symbol_only': [],
    'starts_with_number': [],
    'all_caps_single_word_abbreviation': [],
    'prefix_suffix_entry': [],
    'punctuation_heavy': [],
    'very_short_2_chars': [],
}

def is_prefix_suffix(word):
    """Detect entries that are clearly prefixes/suffixes/combining forms."""
    stripped = word.strip()
    return bool(re.match(r'^-\w+$', stripped) or re.match(r'^\w+-$', stripped) or re.match(r'^-\w+-$', stripped))

for i, item in enumerate(data):
    w = item.get('word', '').strip()

    if len(w) == 1 and w.isalpha():
        categories['single_letter'].append((i, w))
    elif len(w) == 1 and w.isdigit():
        categories['single_digit'].append((i, w))
    elif len(w) == 1:
        categories['symbol_only'].append((i, w))
    elif len(w) == 2 and w.isalpha() and w == w.upper():
        categories['very_short_2_chars'].append((i, w))
    elif re.match(r'^\d', w):
        categories['starts_with_number'].append((i, w))
    elif is_prefix_suffix(w):
        categories['prefix_suffix_entry'].append((i, w))
    elif re.search(r'[^a-zA-Z0-9\s\-\'\(\)\/\.,]', w):
        categories['punctuation_heavy'].append((i, w))

p("=" * 60)
p("SUSPICIOUS WORD ENTRIES IN dictionary_extracted.json")
p("=" * 60)
total = 0
for cat, items in categories.items():
    if items:
        p(f"\n[{cat.upper()}] - {len(items)} entries")
        for idx, w in items[:30]:
            definition_preview = data[idx].get('definition', '')[:100].replace('\n', ' ')
            # sanitize for safe output
            safe_def = definition_preview.encode('ascii', errors='replace').decode('ascii')
            safe_w = repr(w)
            p(f"  [{idx:5d}] word={safe_w}")
            p(f"          def: {safe_def}...")
        if len(items) > 30:
            p(f"  ... and {len(items) - 30} more")
        total += len(items)

p(f"\n{'=' * 60}")
p(f"TOTAL SUSPICIOUS ENTRIES: {total} out of {len(data)}")
p("=" * 60)
OUT.close()
print('Done! Results written to scripts/scan_results.txt')
