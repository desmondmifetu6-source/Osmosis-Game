import json
import os
import re

def audit():
    dict_file = "dictionary.json"
    with open(dict_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_words = 0
    issues = {
        "truncated_endings": [],
        "ends_without_punctuation": [],
        "contains_diagram_ocr_garbage": [],
        "very_short": [],
        "cross_ref_only": [],
        "suspicious_headword": []
    }

    suspicious_ending_words = [
        "the", "a", "an", "of", "in", "to", "and", "or", "that", "which", "with",
        "for", "by", "from", "as", "at", "on", "into", "through", "during", "is",
        "are", "was", "were", "be", "been", "being", "have", "has", "had", "such",
        "respect to", "due to", "equal to", "called", "known as", "refers to"
    ]

    for letter, words in data.items():
        for item in words:
            total_words += 1
            w = item.get("word", "").strip()
            raw = item.get("raw_headword", item.get("raw", "")).strip()
            definition = item.get("definition", "").strip()

            # Check headwords
            if re.search(r'^\d+$', w) or len(w) == 1 or w.startswith('-') or w.endswith('-'):
                issues["suspicious_headword"].append({"letter": letter, "word": w, "raw": raw, "def": definition[:80]})

            # Check definition endings
            lower_def = definition.lower()
            ends_with_suspicious = False
            for end_word in suspicious_ending_words:
                if lower_def.endswith(" " + end_word) or lower_def.endswith("-" + end_word) or lower_def == end_word:
                    issues["truncated_endings"].append({
                        "letter": letter,
                        "word": w,
                        "raw": raw,
                        "def": definition
                    })
                    ends_with_suspicious = True
                    break

            if not ends_with_suspicious and not definition.endswith(('.', '!', '?', '"', "'", ')', ']', ';')):
                if len(definition) > 30:
                    issues["ends_without_punctuation"].append({
                        "letter": letter,
                        "word": w,
                        "raw": raw,
                        "def": definition
                    })

            # Check OCR diagram residue (e.g. strings of isolated single letters, formulas smashed together)
            if re.search(r'(Zwitter Ion Structure|Chemical Structure of|Diagram showing|CCN\+|HROOC|CNHH)', definition):
                issues["contains_diagram_ocr_garbage"].append({
                    "letter": letter,
                    "word": w,
                    "raw": raw,
                    "def": definition
                })

            if len(definition) < 15:
                issues["very_short"].append({
                    "letter": letter,
                    "word": w,
                    "raw": raw,
                    "def": definition
                })

    report = {
        "total_words": total_words,
        "truncated_endings_count": len(issues["truncated_endings"]),
        "ends_without_punctuation_count": len(issues["ends_without_punctuation"]),
        "contains_diagram_ocr_garbage_count": len(issues["contains_diagram_ocr_garbage"]),
        "very_short_count": len(issues["very_short"]),
        "suspicious_headword_count": len(issues["suspicious_headword"]),
        "issues": issues
    }

    with open("scripts/dictionary_issues_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("=== AUDIT SUMMARY ===")
    print(f"Total Words Analyzed: {total_words}")
    print(f"1. Truncated Endings (cut off mid-sentence): {len(issues['truncated_endings'])}")
    print(f"2. Ends Without Punctuation: {len(issues['ends_without_punctuation'])}")
    print(f"3. Diagram OCR Smashed Text: {len(issues['contains_diagram_ocr_garbage'])}")
    print(f"4. Very Short (<15 chars): {len(issues['very_short'])}")
    print(f"5. Suspicious Headwords: {len(issues['suspicious_headword'])}")
    print("Report written to scripts/dictionary_issues_report.json")

if __name__ == "__main__":
    audit()
