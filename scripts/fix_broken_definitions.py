"""
fix_broken_definitions.py
=========================
Comprehensive fixer for three classes of definition defects:

1. Fig-label pollution  — strips embedded PDF diagram labels (Fig I, Fig II, etc.)
2. Spaced-character text — collapses spaced letters back into words  
3. Table-data contamination — removes raw element/data tables dumped into definitions
4. Known hard overrides — replaces completely broken entries with authoritative clean text

Run from final_osmosis/:
    python scripts/fix_broken_definitions.py

Output:
    - dictionary_extracted_final.json  (patched in-place with backup)
    - Prints a full report of every fix applied
"""

import json
import re
import sys
import os
import shutil

sys.stdout.reconfigure(encoding="utf-8")

INPUT_JSON   = "dictionary_extracted_final.json"
BACKUP_JSON  = "dictionary_extracted_final.bak.json"

# ─────────────────────────────────────────────────────────────────────────────
# HARD OVERRIDES: authoritative clean definitions for the worst offenders
# ─────────────────────────────────────────────────────────────────────────────
HARD_OVERRIDES = {

    "FLOWER": (
        "The reproductive structure in flowering plants that bears the organs of sexual "
        "reproduction, or the reproductive unit of a flowering plant. A typical flower "
        "consists of four whorls of modified leaves attached to the receptacle: the "
        "outermost whorl of sepals (calyx), then petals (corolla), then stamens (androecium) "
        "composed of an anther and filament, and the innermost whorl of carpels or pistils "
        "(gynoecium) which contains the ovary, style and stigma. The biological function of "
        "a flower is to mediate the union of male sperm with female ovum in order to produce "
        "seeds. The process begins with pollination, followed by fertilisation, leading to the "
        "formation and dispersal of the seeds. A Cut Flower is a flower that is harvested for "
        "its brightly coloured and showy blossom."
    ),

    "PERIODIC TABLE": (
        "A tabular display in which the chemical elements are arranged in increasing order of "
        "their atomic number. A group or family is a vertical column in the periodic table; "
        "groups are numbered 1 to 18 from the alkali metals (Group 1) to the noble gases "
        "(Group 18). Elements in the same group have similar chemical properties and show a "
        "clear trend in properties down the group. A period is a horizontal row in the "
        "periodic table (e.g. Li, Be, B, C, N, O, F, Ne). Moving left to right across a "
        "period, atomic radius usually decreases while ionisation energy, electron affinity "
        "and electronegativity generally increase. The f-block elements (lanthanides and "
        "actinides) form two substantial horizontal series placed below the main table. "
        "The periodic table was first proposed by Russian chemist Dmitri Mendeleev in 1869."
    ),

    "PERIODIC FUNCTION": (
        "A function f(x) of a real variable is periodic with period T if f(x + T) = f(x) "
        "for every value of x; that is, it repeats itself after every complete cycle of "
        "length T. Periodic functions are used to describe oscillations, waves and other "
        "phenomena that exhibit periodicity. The most important examples are the "
        "trigonometric functions: the sine and cosine functions have a period of 2π radians, "
        "while the tangent function has a period of π radians. A doubly periodic function is "
        "a complex function that is periodic in two independent directions (horizontal and "
        "vertical), satisfying f(z) = f(z + ω₁) = f(z + ω₂) for complex constants ω₁ and ω₂."
    ),

    "CELL": (
        "The basic structural, functional and biological unit of all known living organisms. "
        "A cell is the smallest unit of life that can replicate independently. There are two "
        "broad categories of cells: prokaryotic cells (without a membrane-bound nucleus, "
        "e.g. bacteria) and eukaryotic cells (with a nucleus enclosed within a membrane, "
        "e.g. animal, plant and fungal cells). Animal cells contain organelles such as the "
        "nucleus, mitochondria, ribosomes, endoplasmic reticulum, Golgi apparatus, "
        "lysosomes and cell membrane. Plant cells additionally have a cell wall, chloroplasts "
        "and a large central vacuole. Cells carry out all fundamental processes of life "
        "including metabolism, energy conversion, protein synthesis and reproduction."
    ),

    "ALIMENTARY CANAL": (
        "The long, continuous tube that runs from the mouth to the anus through which food "
        "passes and is digested. In humans it is approximately 9 metres (30 feet) long and "
        "includes the following regions in order: mouth, pharynx, oesophagus, stomach, small "
        "intestine (duodenum, jejunum, ileum), large intestine (caecum, colon, rectum) and "
        "anus. Digestion occurs as food is broken down mechanically and chemically along the "
        "canal, and nutrients are absorbed, primarily in the small intestine, into the "
        "bloodstream for use by the body."
    ),

    "BUDDING": (
        "A form of asexual reproduction in which a new organism develops from an outgrowth or "
        "bud of the parent organism. The bud develops while attached to the parent and, when "
        "it matures, detaches to become an independent individual. Budding is common in "
        "yeasts, hydra and some other invertebrates. In yeasts, a small bud grows on the "
        "parent cell, receives a copy of the nucleus, and then pinches off to form a new "
        "cell. In multicellular organisms such as Hydra, a group of cells on the body wall "
        "proliferates to form a new individual which eventually separates from the parent."
    ),

    "ADJACENT": (
        "In geometry and trigonometry, the side of a right-angled triangle that lies between "
        "the reference angle (not the right angle) and the right angle. In relation to angle θ, "
        "the adjacent side is the side that forms the angle with the hypotenuse. The cosine "
        "of angle θ is defined as the ratio of the adjacent side to the hypotenuse: "
        "cos θ = adjacent / hypotenuse. More generally, two geometric figures, vertices or "
        "angles are described as adjacent when they share a common edge, vertex or side."
    ),

    "BIMETALLIC STRIP": (
        "A mechanical device consisting of two strips of different metals bonded together "
        "along their length. Because the two metals have different coefficients of thermal "
        "expansion, when the temperature changes the strip bends or curves. The metal with "
        "the higher coefficient of expansion is on the outside of the curve when heated. "
        "Bimetallic strips are widely used in thermostats, circuit breakers, clocks and "
        "thermometers as a temperature-sensitive mechanical switch."
    ),

    "HEARING AID": (
        "A small electronic device worn in or behind the ear that amplifies sounds to help "
        "a person who has difficulty hearing. A basic hearing aid consists of a microphone "
        "that picks up sound, an amplifier that increases the signal strength, and a "
        "receiver or speaker that delivers the amplified sound into the ear canal. Modern "
        "digital hearing aids can process sound to reduce background noise, adjust frequency "
        "response and connect wirelessly to phones and other devices."
    ),
}

# ─────────────────────────────────────────────────────────────────────────────
# REGEX PATTERNS TO STRIP FROM DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

# Fig label blocks: "Fig I: <caption text>", "(Fig i)", "Fig II: ...", etc.
# These appear as caption lines embedded in definition text
FIG_LABEL_RE = re.compile(
    r'\s*\(?Fig(ure)?\s+[IVXivx]+\s*[:\-–]?\s*[^\)]*\)?\s*',
    re.IGNORECASE
)

# Strip long runs of dotted ellipsis separators from diagram labels
DOTS_RE = re.compile(r'(\s*\.{4,}\s*)+')

# Strip angle/axis labels like "0˚ 90˚ 180˚ 270˚ 360˚ 450˚" or numeric axis ticks
AXIS_TICK_RE = re.compile(r'\b\d{1,3}˚(\s+\d{1,3}˚)+')

# Strip y = sin(x) style inline math diagram labels that are stray graph labels
GRAPH_LABEL_RE = re.compile(r'\b[yx]\s*=\s*(sin|cos|tan)\s*[\(\s][^\s]+[\s\)]')

# Strip text that looks like element-table data blobs (element symbols with atomic masses)
# e.g. "H1.008 Li 6.941 Be 9.012 ..."
ELEMENT_TABLE_RE = re.compile(
    r'([A-Z][a-z]?\s*[\(\d]\d*[\.\d]*[\)]\s*){5,}',
)

# Remove periphyton-style column bleed text that starts with standalone "P P"
COL_BLEED_RE = re.compile(r'\s+P P for the removal.*$', re.DOTALL)

# Remove runs like "Lanthanides Actinides Th 232.0 Pa (231)..."
PERIODIC_TABLE_DATA_RE = re.compile(
    r'(Lanthanides|Actinides|Alkali metals|Transition metals|Nonmetals).*$',
    re.DOTALL
)


def fix_spaced_chars(text: str) -> str:
    """
    Collapse spaced-out individual characters within words.
    e.g. "r e p r o d u c t i o n" → "reproduction"
    
    Strategy: find runs of single letters separated by single spaces,
    that are preceded and followed by a word boundary or normal text.
    We only collapse if the run is ≥ 4 letters long (to avoid false positives).
    """
    def collapse_run(m):
        letters = m.group(0).replace(' ', '')
        return letters

    # Match 4+ single letters separated by single spaces
    text = re.sub(r'(?<!\w)([a-zA-Z]( [a-zA-Z]){3,})(?!\w)', collapse_run, text)
    return text


def strip_fig_labels(text: str) -> str:
    """Remove embedded diagram-label pollution."""
    # Remove (Fig i), (Fig ii), Fig I:, Fig II: blocks
    text = FIG_LABEL_RE.sub(' ', text)
    # Remove graph axis tick strings
    text = AXIS_TICK_RE.sub(' ', text)
    # Remove graph equation labels
    text = GRAPH_LABEL_RE.sub(' ', text)
    # Remove dotted separator runs
    text = DOTS_RE.sub(' ', text)
    # Collapse multiple spaces
    text = re.sub(r'  +', ' ', text).strip()
    return text


def fix_periodic_table(text: str) -> str:
    """Remove element-table data and column-bleed text from PERIODIC TABLE definition."""
    # Remove column bleed from PERIPHYTON entry
    text = COL_BLEED_RE.sub('', text)
    # Remove Lanthanides/Actinides keyword block onwards
    text = PERIODIC_TABLE_DATA_RE.sub('', text)
    # Remove pure element table data blobs
    text = ELEMENT_TABLE_RE.sub(' ', text)
    # Remove trailing "Russian" prefix artifact
    text = re.sub(r'\s+Russian\s*$', '', text)
    text = re.sub(r'  +', ' ', text).strip()
    return text


def clean_definition(word: str, definition: str) -> tuple[str, list]:
    """
    Apply all fixers to a single definition. Returns (cleaned_def, list_of_fixes_applied).
    """
    original = definition
    fixes = []

    # 1. Hard override takes total priority
    if word in HARD_OVERRIDES:
        return HARD_OVERRIDES[word], ['HARD_OVERRIDE']

    # 2. Periodic table special cleaner
    if word == 'PERIODIC TABLE' and 'Lanthanides' in definition:
        definition = fix_periodic_table(definition)
        fixes.append('periodic_table_data_stripped')

    # 3. Strip Fig-label pollution
    if re.search(r'Fig(ure)?\s+[IVXivx]+', definition, re.IGNORECASE):
        definition = strip_fig_labels(definition)
        fixes.append('fig_labels_stripped')

    # 4. Fix spaced-out characters
    if re.search(r'(?<!\w)([a-zA-Z]( [a-zA-Z]){3,})(?!\w)', definition):
        definition = fix_spaced_chars(definition)
        fixes.append('spaced_chars_collapsed')

    # 5. Remove element-table data blobs from any entry
    if re.search(r'([A-Z][a-z]?\s*\d+\.\d+\s*){4,}', definition):
        definition = ELEMENT_TABLE_RE.sub(' ', definition)
        definition = re.sub(r'  +', ' ', definition).strip()
        fixes.append('element_table_stripped')

    # 6. Remove column-bleed suffix (P P for the removal...)
    if 'P P for the removal' in definition:
        definition = COL_BLEED_RE.sub('', definition).strip()
        fixes.append('column_bleed_stripped')

    # 7. Remove stray axis numeric labels  
    if re.search(r'-360\s+-270\s+-180', definition):
        definition = re.sub(r'-?\d+(\.\d+)?\s+(-?\d+(\.\d+)?\s+){3,}', ' ', definition)
        definition = re.sub(r'Angle in degrees\s*', '', definition)
        definition = re.sub(r'  +', ' ', definition).strip()
        fixes.append('axis_ticks_stripped')

    return definition, fixes


def main():
    if not os.path.exists(INPUT_JSON):
        print(f"ERROR: {INPUT_JSON} not found.")
        sys.exit(1)

    # Backup
    shutil.copy2(INPUT_JSON, BACKUP_JSON)
    print(f"Backed up to {BACKUP_JSON}")

    print(f"Loading {INPUT_JSON}...")
    with open(INPUT_JSON, encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} entries. Applying fixes...\n")

    total_fixed = 0
    fix_report = []

    for item in data:
        word = item.get("word", "").strip().upper()
        orig_def = item.get("definition", "")

        cleaned_def, fixes = clean_definition(word, orig_def)

        if fixes:
            item["definition"] = cleaned_def
            total_fixed += 1
            fix_report.append({
                "word": word,
                "fixes": fixes,
                "before_length": len(orig_def),
                "after_length": len(cleaned_def),
            })

    print("=" * 65)
    print(f"TOTAL ENTRIES FIXED: {total_fixed}")
    print("=" * 65)
    for r in fix_report:
        print(f"  [{', '.join(r['fixes'])}]  {r['word']}"
              f"  ({r['before_length']} → {r['after_length']} chars)")

    # Save patched JSON
    with open(INPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved patched data back to {INPUT_JSON}")
    print("Next step: run  python scripts/build_core_dictionary.py  to regenerate dictionary.json + core_dictionary.js")


if __name__ == "__main__":
    main()
