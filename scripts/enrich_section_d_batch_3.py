"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION D (BATCH 3 - FINAL)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section D:
Final 4 terms completing 100% of Section D:
- dummy suffix convention
- dummy variable
- durbin-watson test
- dynamical time
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_D3_DEFINITIONS = {
    "dummy suffix convention": (
        "A shorthand notation (also known as the Einstein summation convention) used in manipulating components of vectors and tensors, "
        "in accordance with which the summation symbol $\\sum$ is omitted and the sum is implied by the repetition of an index. "
        "For example, the scalar product: "
        "$$\\mathbf{a} \\cdot \\mathbf{b} = a_1 b_1 + a_2 b_2 + a_3 b_3 = \\sum_{i=1}^3 a_i b_i$$ "
        "is compactly written as $a_i b_i$ (or $a^i b_i$ in contravariant/covariant tensor notation)."
    ),
    "dummy variable": (
        "A variable in an expression or equation whose symbol can be replaced with any other arbitrary symbol without changing the value or meaning of the expression. "
        "In definite integrals, the variable of integration is a dummy variable: "
        "$$\\int_a^b x^3 \\, dx = \\int_a^b u^3 \\, du$$ "
        "Similarly, the index of summation in a series is a dummy index: "
        "$$\\sum_{i=1}^n a_i = \\sum_{k=1}^n a_k$$"
    ),
    "durbin-watson test": (
        "A statistical test used to detect the presence of first-order autocorrelation in the residuals from a linear regression analysis. "
        "The Durbin-Watson test statistic $d$ is defined as: "
        "$$d = \\frac{\\sum_{t=2}^T (e_t - e_{t-1})^2}{\\sum_{t=1}^T e_t^2}$$ "
        "where $e_t$ is the residual at observation $t$ and $T$ is the total number of observations. "
        "The statistic approximately satisfies $d \\approx 2(1 - r)$, where $r$ is the sample autocorrelation of the residuals. "
        "A value of $d$ close to $2$ indicates no autocorrelation; values approaching $0$ indicate positive autocorrelation, "
        "and values approaching $4$ indicate negative autocorrelation."
    ),
    "dynamical time": (
        "A uniform astronomical timescale used in gravitational calculations of planetary and orbital motions within the Solar System (replacing Ephemeris Time, ET). "
        "The primary standard, Terrestrial Time (TT) (formerly Terrestrial Dynamical Time, TDT), uses the SI day of $86{,}400\\text{ s}$ as its fundamental unit "
        "and is related to International Atomic Time (TAI) by the fixed offset: "
        "$$\\text{TT} = \\text{TAI} + 32.184\\text{ s}$$ "
        "For interplanetary orbits, Barycentric Dynamical Time (TDB) is used to account for relativistic corrections at the Solar System barycentre."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    d_entries = data.get('D', [])
    word_map = {item.get('word', '').strip().lower(): item for item in d_entries}

    for target_word, new_def in BATCH_D3_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section D: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_D3_DEFINITIONS)} definitions in Section D Batch 3 (FINAL).")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    print("Rebuilding core_dictionary.js index...")
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
