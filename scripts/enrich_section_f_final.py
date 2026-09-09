"""
enrich_section_f_final.py
=========================
Section F Formula Enrichment - Final 4 Remaining Terms
Typesetting mathematical, scientific, and physical formulas into KaTeX ($ ... $ and $$ ... $$).

Terms to enrich:
  342  - filter
  787  - formula bar
  790  - formulation
  1066 - fundamental theorem of projectivity
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

f_entries = data.get('F', [])

UPDATES = {

    # -------------------------------------------------------------------------
    # 1. filter (index 342)
    # Mathematical definition: a filter on a set S is a nonempty family F subseteq P(S)
    # satisfying: (i) empty-set not in F, (ii) upward-closed, (iii) finite-intersection-closed.
    # Signal processing: frequency-selective linear systems.
    # -------------------------------------------------------------------------
    342: (
        "1. A porous material on which solid particles present in air or other fluid which "
        "flows through it are largely caught and retained. Filters are made with a variety of "
        "materials: cellulose and derivatives, glass fibre, ceramic, synthetic plastics and fibres. "
        "Filters may be naturally porous or be made so by mechanical or other means. Membrane/ceramic "
        "filters are prepared with highly controlled pore size in a sheet of suitable material such as "
        "polyfluoroethylene, polycarbonate or cellulose esters. Nylon mesh is sometimes used for "
        "reinforcement. The pores constitute 80\u201385% of the filter volume commonly and several pore "
        "sizes are available for air sampling ($0.45$\u2013$0.8\\,\\mu\\text{m}$ are commonly employed). "
        "2. In mathematics, a **filter** on a set $S$ is a nonempty collection $\\mathcal{F} "
        "\\subseteq \\mathcal{P}(S)$ (where $\\mathcal{P}(S)$ denotes the power set of $S$) "
        "satisfying three axioms:\n\n"
        "$$\\emptyset \\notin \\mathcal{F}$$\n\n"
        "$$A \\in \\mathcal{F},\\; A \\subseteq B \\implies B \\in \\mathcal{F} "
        "\\quad \\text{(upward-closed / isotone)}$$\n\n"
        "$$A, B \\in \\mathcal{F} \\implies A \\cap B \\in \\mathcal{F} "
        "\\quad \\text{(closed under finite intersection)}$$\n\n"
        "A filter $\\mathcal{F}$ on $S$ **converges** to a point $x \\in S$ if every "
        "neighbourhood $U \\ni x$ satisfies $U \\in \\mathcal{F}$. This provides a general "
        "framework for convergence equivalent to that of nets (Moore\u2013Smith sequences). "
        "3. A device that allows only one band of wavelengths to pass through it, or absorbs "
        "some part of the visible spectrum and transmits others. In photometry, the spectral "
        "transmittance $T(\\lambda)$ of a bandpass filter is characterised by its centre "
        "wavelength $\\lambda_0$ and half-power bandwidth $\\Delta\\lambda$. "
        "4. A device placed in the path of a beam of radiation to alter its frequency distribution. "
        "5. In electronics, a circuit designed to pass signals of certain frequencies while "
        "attenuating others. An ideal low-pass filter has transfer function\n\n"
        "$$H(f) = \\begin{cases} 1 & |f| \\leq f_c \\\\ 0 & |f| > f_c \\end{cases}$$\n\n"
        "where $f_c$ is the cut-off frequency. Real filters approximate this with Butterworth, "
        "Chebyshev, or elliptic designs. 6. A computer program or device that allows the passage "
        "of some data elements and blocks others. 7. A tinted glass or dyed gelatin screen placed "
        "on a camera lens to control light, colour, or distant image."
    ),

    # -------------------------------------------------------------------------
    # 2. formula bar (index 787)
    # Spreadsheet UI concept. Renders typical formula syntax inline with KaTeX.
    # -------------------------------------------------------------------------
    787: (
        "A dedicated input region in spreadsheet applications (such as Microsoft Excel, Google "
        "Sheets, or LibreOffice Calc) that displays the raw data value or formula expression "
        "stored in the currently active cell, and allows the user to directly enter or edit "
        "content. In Microsoft Excel it is located immediately above the column headers. "
        "When a cell contains a static value, the formula bar shows that value (e.g. $42$ or "
        "$3.14159$). When a cell contains a formula, the bar displays the formula text rather "
        "than the computed result \u2014 for example, the aggregation formula\n\n"
        "$$\\texttt{=SUM(A1:A10)}$$\n\n"
        "computes $\\displaystyle\\sum_{i=1}^{10} A_i$, and the weighted-average formula\n\n"
        "$$\\texttt{=SUMPRODUCT(B1:B10,\\, C1:C10)\\,/\\,SUM(C1:C10)}$$\n\n"
        "computes the weighted mean $\\bar{x}_w = "
        "\\dfrac{\\displaystyle\\sum_{i} w_i x_i}{\\displaystyle\\sum_{i} w_i}$. "
        "The formula bar thus provides a transparent view of the underlying mathematical "
        "expressions that drive computed cell outputs, distinguishing formula-driven cells "
        "from cells containing literal constants."
    ),

    # -------------------------------------------------------------------------
    # 3. formulation (index 790)
    # Pharmaceutical / chemical formulation. Henderson-Hasselbalch + Noyes-Whitney.
    # -------------------------------------------------------------------------
    790: (
        "1. The systematic process of combining components in precise relationships or structures "
        "according to a defined formula or recipe. 2. The particular mixture of active ingredients "
        "and excipients required for a product. In **pharmaceutical formulation**, the active "
        "pharmaceutical ingredient (API) is combined with excipients to achieve a target "
        "bioavailability and release profile. The pH of an aqueous formulation is governed by "
        "the Henderson\u2013Hasselbalch equation:\n\n"
        "$$\\text{pH} = \\text{p}K_a + \\log_{10}\\!\\left(\\frac{[\\text{A}^-]}{[\\text{HA}]}\\right)$$\n\n"
        "where $[\\text{HA}]$ is the molar concentration of the weak acid and $[\\text{A}^-]$ "
        "is the conjugate base concentration. Drug dissolution from a solid formulation obeys "
        "the Noyes\u2013Whitney equation:\n\n"
        "$$\\frac{dm}{dt} = \\frac{D \\cdot A}{h}\\,(C_s - C_t)$$\n\n"
        "where $D$ is the diffusion coefficient, $A$ the surface area of dissolving solid, "
        "$h$ the diffusion layer thickness, $C_s$ the saturation solubility, and $C_t$ the "
        "concentration in bulk solution at time $t$. "
        "3. Formulation science is concerned with the knowledge and practice of blending and "
        "mixing various components (chemical molecules) so that they do not react with each "
        "other, but interact to provide a final product with specific desirable properties. "
        "A general pharmaceutical formulation may be represented as a vector of component "
        "concentrations $\\mathbf{c} = (c_1, c_2, \\ldots, c_n)$ subject to the constraint "
        "$\\displaystyle\\sum_{i=1}^{n} c_i = C_{\\text{total}}$. "
        "Formulation science encompasses physical and colloid chemistry, analytical chemistry, "
        "chemical engineering, and pharmaceutical and biological sciences."
    ),

    # -------------------------------------------------------------------------
    # 4. fundamental theorem of projectivity (index 1066)
    # Projective geometry: a projectivity from P^1 to P^1 is uniquely determined by 3 points.
    # Homogeneous coordinates, PGL_2, cross-ratio.
    # -------------------------------------------------------------------------
    1066: (
        "In projective geometry, the theorem stating that a projective transformation "
        "(projectivity) between two one-dimensional projective spaces (projective lines) "
        "is **uniquely and completely determined** by specifying the images of three distinct "
        "points. Formally, if $\\ell$ and $\\ell'$ are projective lines over a field $\\mathbb{F}$ "
        "and $p_1, p_2, p_3 \\in \\ell$ are three distinct points with prescribed "
        "images $p_1', p_2', p_3' \\in \\ell'$, then there exists a **unique projectivity** "
        "$\\varphi: \\ell \\to \\ell'$ satisfying $\\varphi(p_i) = p_i'$ for $i = 1, 2, 3$.\n\n"
        "In homogeneous coordinates, a projectivity of $\\mathbb{P}^1(\\mathbb{F})$ is "
        "represented by an invertible $2 \\times 2$ matrix $M \\in \\mathrm{GL}_2(\\mathbb{F})$ "
        "acting on coordinate vectors $\\mathbf{x} = [x_0 : x_1]^\\top$:\n\n"
        "$$\\varphi(\\mathbf{x}) = M\\mathbf{x} = "
        "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}"
        "\\begin{pmatrix} x_0 \\\\ x_1 \\end{pmatrix}, "
        "\\quad ad - bc \\neq 0$$\n\n"
        "Two matrices $M$ and $\\lambda M$ (for scalar $\\lambda \\neq 0$) define the same "
        "projectivity, so the group of projectivities is $\\mathrm{PGL}_2(\\mathbb{F})$. "
        "The **cross-ratio** $[p_1, p_2; p_3, p_4]$ is the fundamental invariant preserved "
        "by all projectivities:\n\n"
        "$$[p_1, p_2; p_3, p_4] = "
        "\\frac{(p_3 - p_1)(p_4 - p_2)}{(p_3 - p_2)(p_4 - p_1)}$$\n\n"
        "The theorem is a cornerstone of classical projective geometry and underlies the "
        "construction of projective coordinates and the classification of conics."
    ),
}

# Apply updates
applied = 0
for idx, new_def in UPDATES.items():
    if idx < len(f_entries):
        f_entries[idx]['definition'] = new_def
        word = f_entries[idx]['word']
        has_katex = '$' in new_def
        print(f"[{'OK' if has_katex else 'WARN'}] Updated index {idx}: '{word}' (KaTeX: {has_katex})")
        applied += 1
    else:
        print(f"[ERROR] Index {idx} out of range (F has {len(f_entries)} entries)")

print(f"\nApplied {applied} of {len(UPDATES)} updates.")

# Save back to dictionary.json
data['F'] = f_entries
with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("dictionary.json saved successfully.\n")

# Quick inline verification
with open('ef_formulas_to_enrich.json', 'r', encoding='utf-8') as f2:
    ef = json.load(f2)

f_cands = ef.get('F', [])
enriched = [c for c in f_cands if '$' in f_entries[c['index']].get('definition', '')]
missing  = [c for c in f_cands if '$' not in f_entries[c['index']].get('definition', '')]

print("=== Final Section F Verification ===")
print(f"  Total candidates : {len(f_cands)}")
print(f"  Enriched (with $): {len(enriched)}")
print(f"  Still missing    : {len(missing)}")
if missing:
    for c in missing:
        print(f"    - index {c['index']}: {f_entries[c['index']]['word']}")
else:
    print("  ALL SECTION F FORMULAS ENRICHED! 🎉")
