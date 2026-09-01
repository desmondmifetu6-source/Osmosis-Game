# STEM Dictionary Diagram Integration & Audit Guide
*A Technical Playbook for AI Coding Assistants*

---

## 📌 Executive Summary & Philosophy

When integrating user-extracted educational diagrams (such as chemistry structures, physics schematics, and biology illustrations) into a STEM dictionary application, traditional automated OCR often fails due to complex chemical notation, mathematical symbols, and non-standard typography. Running continuous blind CLI commands or relying solely on OCR scripts causes data corruption, misassigned images, and missing entries.

This guide details the **multimodal batch-integration methodology** used to achieve 100% accuracy in mapping, replacing, and indexing over 1,000+ STEM diagrams in the Osmosis dictionary system.

---

## 🏗 System Architecture

The Osmosis dictionary relies on a strict 3-tier diagram pipeline:

```
[Raw User Screenshots] ──(Visual Audit & Script)──> [diagrams/dict_[word].png]
                                                            │
                                                            ▼
                                           [dictionary_diagrams_map.json]
                                                            │
                                                            ▼
                                            [core_dictionary_diagrams.js]
```

1. **Physical Assets Directory**: `diagrams/dict_[word].png`
   - Filenames must follow lower-snake-case convention: `dict_[normalized_word].png`.
2. **JSON Registry (Source of Truth)**: `dictionary_diagrams_map.json`
   - Key-value mapping of lowercased term strings to relative image paths:
     ```json
     {
         "propenenitrile": "diagrams/dict_acrylonitrile_propenenitrile.png",
         "propenonitrile": "diagrams/dict_acrylonitrile_propenenitrile.png",
         "acrylonitrile": "diagrams/dict_acrylonitrile_propenenitrile.png"
     }
     ```
3. **Frontend Bundle**: `core_dictionary_diagrams.js`
   - Auto-generated JavaScript module that attaches `DictionaryDiagrams` object to `window` for client-side lookup.

---

## 🚀 The 4-Step Breakthrough Workflow

Future AI agents working on diagram integration MUST follow these four steps rather than running exploratory command loops:

### Step 1: Multimodal Visual Inspection (Human-in-the-Loop Vision)
- **Do NOT** rely solely on OCR CLI binaries when captions contain scientific nomenclature.
- **DO** use multimodal image viewing capabilities (`view_file` tool on image paths) in batches of 10–20 files.
- Inspect the caption text (typically at the bottom of the diagram, e.g., *"Chemical Structure of Acrylonitrile"* or *"Angle of deviation in a prism"*).

### Step 2: Synonym & Alternative Nomenclature Mapping
- Identify all IUPAC names, common names, and spelling variants for each term:
  - Example: `acrylonitrile` ↔ `propenenitrile` ↔ `propenonitrile`.
  - Example: `acetyl-coa` ↔ `acetyl coenzyme a`.
  - Example: `air layering` ↔ `marcotting`.
- Include all variants as separate keys in the assignments table pointing to the same high-resolution target image.

### Step 3: Deterministic Python Batch Integration
Write a dedicated, self-contained Python script (refer to `scripts/integrate_section_ab_batch.py`) that performs the following operations atomically:

1. **Copying Assets**: Copies raw screenshots from `section a-b images/` to `diagrams/` with target `dict_[word].png` names. Overwrites any existing low-quality placeholders.
2. **Updating JSON Map**: Updates `dictionary_diagrams_map.json` and sorts keys alphabetically.
3. **Regenerating JS Bundle**: Rewrites `core_dictionary_diagrams.js` with the updated JSON dictionary mapping.

```python
import os, json, shutil

# Example snippet from integrate_section_ab_batch.py
with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    diag_map = json.load(f)

for src_file, (dest_file, keys) in ASSIGNMENTS.items():
    src_path = os.path.join(SRC_DIR, src_file)
    dest_path = os.path.join(DEST_DIR, dest_file)
    shutil.copy2(src_path, dest_path)
    for key in keys:
        diag_map[key.lower().strip()] = f"diagrams/{dest_file}"

sorted_map = dict(sorted(diag_map.items()))
with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
    json.dump(sorted_map, f, indent=4, ensure_ascii=False)
```

### Step 4: Empirical Integrity Verification
Never declare success after file edits until you run a validation script (e.g., `scripts/verify_map_integrity.py`).

The script must verify:
- Total number of keys registered in `dictionary_diagrams_map.json`.
- `os.path.exists()` for 100% of target image paths listed in the JSON file.
- Zero missing image files or broken paths.

---

## ⚡ Golden Rules for AI Assistants

1. **Prioritize User Screenshots Over AI Generations**: User-extracted screenshots are human-verified, textbook-accurate diagrams. Always prefer them over synthetic AI generations.
2. **Never Run Endless Terminal Trial-and-Error**: Do not loop endlessly through failing shell commands. Formulate a complete batch plan, inspect visual inputs directly, and execute via a single clean script.
3. **Map Spelling Variations Explicitly**: STEM students search terms using different standard spellings (e.g., British vs. American English, trivial vs. IUPAC names). Always map all variants to the diagram asset.
4. **Maintain Synchronization**: `dictionary_diagrams_map.json` and `core_dictionary_diagrams.js` MUST ALWAYS remain in sync. Never edit one without updating the other.

---
*Created for future AI pair-programmers working on the Osmosis STEM platform.*
