"""
enrich_section_e_final.py
=========================
Section E Formula Enrichment - Final 19 terms
Completing 100% of formula enrichment candidates in Section E.
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

e_entries = data.get('E', [])

UPDATES = {
    # 28. earnshaw's theorem
    28: (
        "A foundational theorem in classical electrodynamics stating that a collection of point charges cannot be maintained in a stable stationary equilibrium configuration solely by electrostatic (Coulomb) interactions. Because the electrostatic potential $V$ in charge-free space satisfies Laplace's equation:\n\n"
        "$$\\nabla^2 V = \\frac{\\partial^2 V}{\\partial x^2} + \\frac{\\partial^2 V}{\\partial y^2} + \\frac{\\partial^2 V}{\\partial z^2} = 0$$\n\n"
        "$V$ cannot possess local isolated minima or maxima in all three spatial dimensions. Consequently, static magnetic or electrostatic levitation is impossible for purely paramagnetic or permanent magnetic materials, but can be circumvented using diamagnetic materials (where relative permeability $\\mu_r < 1$) or dynamic feedback fields."
    ),

    # 49. eberlein-smulian theorem
    49: (
        "A deep theorem in functional analysis, proved by William Frederick Eberlein and Witold Lwowitsch Schmulian, stating that for any subset $A$ of a Banach space $X$, the following topological conditions under the weak topology are strictly equivalent:\n\n"
        "1. $A$ is relatively weakly compact (its weak closure is weakly compact).\n"
        "2. $A$ is relatively weakly sequentially compact (every sequence in $A$ has a subsequence weakly converging to an element in $X$)."
    ),

    # 53. ebullioscope constant
    53: (
        "The molal boiling-point elevation constant, denoted $K_b$, relating the elevation in boiling point $\\Delta T_b$ of a solvent to the molal concentration $m$ of a non-volatile dissolved solute:\n\n"
        "$$\\Delta T_b = i K_b m$$\n\n"
        "where $i$ is the van 't Hoff factor. Thermodynamically, $K_b$ depends solely on solvent properties:\n\n"
        "$$K_b = \\frac{R T_b^2 M}{1000\\,\\Delta H_{\\text{vap}}}$$\n\n"
        "where $R$ is the universal gas constant, $T_b$ is the pure solvent boiling point, $M$ is molar mass, and $\\Delta H_{\\text{vap}}$ is the latent heat of vaporization (e.g., for water, $K_b = 0.512\\,\\text{K}\\cdot\\text{kg}\\cdot\\text{mol}^{-1}$)."
    ),

    # 198. ehrenfest theorem
    198: (
        "A fundamental theorem in quantum mechanics established by Paul Ehrenfest (1927), proving that the expectation values of quantum-mechanical observables follow the classical Newton-Hamilton equations of motion:\n\n"
        "$$\\frac{d}{dt}\\langle \\mathbf{r} \\rangle = \\frac{1}{m}\\langle \\mathbf{p} \\rangle$$\n\n"
        "$$\\frac{d}{dt}\\langle \\mathbf{p} \\rangle = -\\langle \\nabla V(\\mathbf{r}) \\rangle$$\n\n"
        "Derived directly from the Heisenberg equation of motion $\\frac{d}{dt}\\langle A \\rangle = \\frac{1}{i\\hbar}\\langle [A, H] \\rangle + \\left\\langle \\frac{\\partial A}{\\partial t} \\right\\rangle$, establishing the formal correspondence principle between quantum and classical mechanics."
    ),

    # 332. electromagnetic potentials
    332: (
        "The scalar potential $\\phi$ and magnetic vector potential $\\mathbf{A}$ in terms of which electric and magnetic fields $\\mathbf{E}$ and $\\mathbf{B}$ are completely expressed in electrodynamics:\n\n"
        "$$\\mathbf{B} = \\nabla \\times \\mathbf{A}$$\n\n"
        "$$\\mathbf{E} = -\\nabla \\phi - \\frac{\\partial \\mathbf{A}}{\\partial t}$$\n\n"
        "Under the Lorenz gauge condition $\\nabla \\cdot \\mathbf{A} + \\frac{1}{c^2}\\frac{\\partial \\phi}{\\partial t} = 0$, Maxwell's equations decouple into inhomogeneous wave equations for $\\phi$ and $\\mathbf{A}$, compacting into four-vector potential form $A^\\mu = (\\phi/c, \\mathbf{A})$."
    ),

    # 352. electron capture
    352: (
        "A radioactive decay mode in proton-rich atomic nuclei where an inner atomic orbital electron (typically from the $K$ or $L$ shell) is captured by a nuclear proton, converting into a neutron and emitting an electron neutrino:\n\n"
        "$${}_Z^A X + e^- \\to {}_{Z-1}^A Y + \\nu_e$$\n\n"
        "The mass number $A$ remains unchanged while atomic number decreases by $1$. When the decay energy $Q < 2m_e c^2 = 1.022\\,\\text{MeV}$, positron emission is energetically forbidden and electron capture is the sole decay route (e.g., ${}^{83}_{37}\\text{Rb} + e^- \\to {}^{83}_{36}\\text{Kr} + \\nu_e$)."
    ),

    # 418. electrophilic addition
    418: (
        "An addition reaction in organic chemistry where a $\\pi$-bond in an unsaturated compound (such as an alkene $\\text{R}_2\\text{C}=\\text{CR}_2$ or alkyne) is cleaved by an electron-deficient electrophile $\\text{E}^+$, forming two new $\\sigma$-bonds:\n\n"
        "$$\\text{R}_2\\text{C}=\\text{CR}_2 + \\text{E}-\\text{Nu} \\to \\text{R}_2\\text{C}(\\text{E})-\\text{C}(\\text{Nu})\\text{R}_2$$\n\n"
        "Proceeds through a carbocation or cyclic halonium ion intermediate following Markovnikov's rule for unsymmetrical reagents."
    ),

    # 456. elementarily equivalent
    456: (
        "In mathematical logic and model theory, two structures $\\mathcal{M}$ and $\\mathcal{N}$ sharing signature $\\sigma$ are elementarily equivalent (denoted $\\mathcal{M} \\equiv \\mathcal{N}$) if they satisfy exactly the same first-order sentences:\n\n"
        "$$\\mathcal{M} \\models \\varphi \\iff \\mathcal{N} \\models \\varphi$$\n\n"
        "for every first-order $\\sigma$-sentence $\\varphi$ without free variables. Every pair of isomorphic structures is elementarily equivalent ($\\mathcal{M} \\cong \\mathcal{N} \\implies \\mathcal{M} \\equiv \\mathcal{N}$), but the converse does not generally hold."
    ),

    # 667. energy balance equation
    667: (
        "In continuum mechanics and thermodynamics, the mathematical formulation of the first law of thermodynamics stating that the time rate of change of total energy (kinetic energy $K$ plus internal energy $U$) of a body equals the sum of mechanical power input $\\mathcal{P}$ and thermal heating rate $\\mathcal{Q}$:\n\n"
        "$$\\frac{d}{dt}(K + U) = \\mathcal{P} + \\mathcal{Q}$$\n\n"
        "Expressed locally in differential form as $\\rho \\frac{du}{dt} = \\boldsymbol{\\sigma} : \\mathbf{D} - \\nabla \\cdot \\mathbf{q} + \\rho r$."
    ),

    # 707. enormous theorem
    707: (
        "The theorem classifying all finite simple groups (often termed the CFSG or 'Enormous Theorem' because its complete proof spans over 10,000 journal pages by hundreds of mathematicians). It establishes that every finite simple group belongs to one of four classes:\n\n"
        "1. Cyclic groups of prime order: $\\mathbb{Z}_p$\n"
        "2. Alternating groups of degree $n \\ge 5$: $A_n$\n"
        "3. Simple groups of Lie type (including classical matrix groups over finite fields)\n"
        "4. Exactly 26 sporadic simple groups (the largest being the Monster group $M$)."
    ),

    # 710. enrichment
    710: (
        "1. In nuclear engineering, the physical process of increasing the isotopic abundance of fissile uranium-235 (${}^{235}\\text{U}$) relative to non-fissile uranium-238 (${}^{238}\\text{U}$) above its natural abundance of $\\approx 0.72\\%$ (using gas centrifuges or gaseous diffusion of $\\text{UF}_6$). 2. In analytical chemistry, preconcentration techniques used to increase the trace analyte concentration relative to matrix components."
    ),

    # 850: epoxy compounds
    850: (
        "Organic compounds characterized by a three-membered cyclic ether containing one oxygen atom bonded to two adjacent carbon atoms (an oxirane ring). Represented by the general structural formula:\n\n"
        "$$\\text{R}_2\\text{C}\\frac{\\quad}{\\quad}\\text{O}\\frac{\\quad}{\\quad}\\text{CR}_2$$\n\n"
        "The high ring strain ($\x7e114\\,\\text{kJ}\\cdot\\text{mol}^{-1}$) makes epoxides exceptionally susceptible to nucleophilic ring-opening additions under both acidic and basic catalysis."
    ),

    # 870: equals sign
    870: (
        "The mathematical symbol '$=$' introduced by Robert Recorde in 1557 to denote identity of reference or numerical equality between two expressions ($a = b$). In mathematical logic and computing, definitive equality is written as $A := B$, $A \\equiv B$, or $A \\stackrel{\\text{def}}{=} B$."
    ),

    # 873: equation of time
    873: (
        "The difference between apparent solar time (indicated by a sundial) and mean solar time (measured by a uniform clock):\n\n"
        "$$\\Delta t = T_{\\text{apparent}} - T_{\\text{mean}}$$\n\n"
        "Arising from two astronomical phenomena: the obliquity of the ecliptic (Earth's axial tilt of $\\varepsilon \\approx 23.44^\\circ$) and the eccentricity of Earth's elliptical orbit ($e \\approx 0.0167$). It oscillates between $-14.2$ minutes (February) and $+16.4$ minutes (November)."
    ),

    # 1209: excluded middle law
    1209: (
        "The principle of excluded middle (principium tertii exclusi) in classical two-valued logic, asserting that for any proposition $P$, either $P$ is true or its negation $\\neg P$ is true:\n\n"
        "$$P \\lor \\neg P = \\top$$\n\n"
        "There is no third truth value. It is accepted in classical mathematics but rejected in intuitionistic logic."
    ),

    # 1289: explicit function
    1289: (
        "A function in which the dependent variable $y$ is isolated and expressed directly as an explicit formula of the independent variable(s) $x$, written in the canonical form:\n\n"
        "$$y = f(x)$$\n\n"
        "For example, $y = x^2 - 4x + 7$ or $y = \\log_2(x)$, contrasted with implicit equations where variables are intermingled ($F(x, y) = 0$)."
    ),

    # 1328: extended real numbers
    1328: (
        "The extended real number system $\\overline{\\mathbb{R}} = [-\\infty, +\\infty]$, formed by augmenting the real numbers $\\mathbb{R}$ with positive and negative infinity:\n\n"
        "$$\\overline{\\mathbb{R}} = \\mathbb{R} \\cup \\{-\\infty, +\\infty\\}$$\n\n"
        "Endowed with the standard extended arithmetic operations: $a + (+\\infty) = +\\infty$ for $a > -\\infty$, and $a \\cdot (+\\infty) = +\\infty$ for $a > 0$. It forms a compact Hausdorff space homeomorphic to the closed interval $[0, 1]$."
    ),

    # 1348: external direct product
    1348: (
        "In abstract algebra, the Cartesian product $M = M_1 \\times M_2 \\times \\dots \\times M_n$ of modules or groups endowed with component-wise operations:\n\n"
        "$$(x_1, \\dots, x_n) + (y_1, \\dots, y_n) = (x_1 + y_1, \\dots, x_n + y_n)$$\n\n"
        "$$r(x_1, \\dots, x_n) = (rx_1, \\dots, rx_n)$$\n\n"
        "For finite collections, the external direct product is isomorphic to the internal direct sum $\\bigoplus_{i=1}^n M_i$."
    ),

    # 1349: external division
    1349: (
        "In Euclidean geometry, the division of a line segment $AB$ by an external point $P$ lying on the extended line collinear with $A$ and $B$, such that the directed ratio of segments satisfies:\n\n"
        "$$\\frac{\\vec{AP}}{\\vec{PB}} = \\lambda < 0$$\n\n"
        "In coordinates, for $A(x_1, y_1)$ and $B(x_2, y_2)$, the external division point with ratio $k = |\\lambda| \\neq 1$ has coordinates $P\\left(\\frac{x_1 - k x_2}{1 - k}, \\frac{y_1 - k y_2}{1 - k}\\right)$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(e_entries):
        w = e_entries[idx]['word']
        e_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")

data['E'] = e_entries

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section E Final Batch.")
