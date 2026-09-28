"""
enrich_section_j_batch.py
=========================
Section J Formula Enrichment - Complete Batch (Candidates 1 to 19)
Completing Section J formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys
import os
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_PATH = os.path.join(BASE_DIR, 'dictionary.json')

with open(DICT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

j_entries = data.get('J', [])

UPDATES = {
    # 1. jaccard coefficient (index 8)
    8: (
        "In statistics, numerical taxonomy, and data science, a similarity metric $J(A, B)$ measuring the overlap between two finite sample sets $A$ and $B$. "
        "Defined as the ratio of the cardinality of their intersection to the cardinality of their union:\n\n"
        "$$J(A, B) = \\frac{|A \\cap B|}{|A \\cup B|} = \\frac{|A \\cap B|}{|A| + |B| - |A \\cap B|}$$\n\n"
        "The Jaccard distance $d_J(A, B) = 1 - J(A, B) = \\frac{|A \\cup B| - |A \\cap B|}{|A \\cup B|}$ is a proper mathematical metric on the space of finite sets, "
        "satisfying the triangle inequality."
    ),

    # 2. jackson-bernstein theorems (index 12)
    12: (
        "Fundamental direct and converse approximation theorems in mathematical analysis established by Dunham Jackson (1911) and Sergei Bernstein (1912). "
        "They establish exact equivalences between the smoothness (differentiability or Hölder/Lipschitz regularity $\\alpha$) of a function $f$ and its rate of best "
        "uniform polynomial or trigonometric approximation $E_n(f)$ of degree $n$:\n\n"
        "$$E_n(f) = \\mathcal{O}\\left(n^{-\\alpha}\\right) \\iff f \\in \\text{Lip}(\\alpha) \\quad (0 < \\alpha < 1)$$\n\n"
        "For $k$-times continuously differentiable functions, Jackson's theorem provides upper bound $E_n(f) \\le \\frac{C_k}{n^k} \\omega(f^{(k)}, 1/n)$."
    ),

    # 3. jacobi iteration (index 14)
    14: (
        "In numerical linear algebra, an iterative algorithm for finding the solution vector $\\mathbf{x}$ to a square strictly diagonally dominant system of linear equations "
        "$\\mathbf{A}\\mathbf{x} = \\mathbf{b}$. Decomposing $\\mathbf{A} = \\mathbf{D} + \\mathbf{L} + \\mathbf{U}$ (diagonal, strictly lower, strictly upper):\n\n"
        "$$\\mathbf{x}^{(k+1)} = \\mathbf{D}^{-1} \\left( \\mathbf{b} - (\\mathbf{L} + \\mathbf{U})\\mathbf{x}^{(k)} \\right)$$\n\n"
        "In component form for each element $i = 1, \\dots, n$:\n\n"
        "$$x_i^{(k+1)} = \\frac{1}{a_{ii}} \\left( b_i - \\sum_{j \\neq i} a_{ij} x_j^{(k)} \\right)$$\n\n"
        "Guaranteed to converge if $\\mathbf{A}$ is strictly diagonally dominant ($|a_{ii}| > \\sum_{j \\neq i} |a_{ij}|$) or symmetric positive-definite."
    ),

    # 4. jacobi's method (index 15)
    15: (
        "1. In numerical linear algebra, the Jacobi eigenvalue algorithm: an iterative procedure that calculates all eigenvalues and eigenvectors of a real symmetric matrix "
        "$\\mathbf{A}$ via a sequence of orthogonal similarity transformations using Jacobi rotation matrices $\\mathbf{J}(p, q, \\theta)$:\n\n"
        "$$\\mathbf{A}_{k+1} = \\mathbf{J}_k^T \\mathbf{A}_k \\mathbf{J}_k, \\quad \\tan(2\\theta) = \\frac{2a_{pq}}{a_{qq} - a_{pp}}$$\n\n"
        "2. In partial differential equations, Jacobi's method for solving non-linear first-order PDEs $F(x_1, \\dots, x_n, p_1, \\dots, p_n) = 0$ lacking explicit dependent variable $z$, "
        "generalizing Charpit's method to $n$ independent variables using complete integrals."
    ),

    # 5. jacobian elliptic functions (index 17)
    17: (
        "A family of doubly periodic meromorphic functions on the complex plane $\\mathbb{C}$, introduced by Carl Gustav Jacobi in 1829. Arising as inverse functions "
        "of the incomplete elliptic integral of the first kind $u = F(\\phi, k) = \\int_0^\\phi \\frac{d\\theta}{\\sqrt{1 - k^2 \\sin^2 \\theta}}$:\n\n"
        "$$\\text{sn}(u, k) = \\sin \\phi, \\qquad \\text{cn}(u, k) = \\cos \\phi, \\qquad \\text{dn}(u, k) = \\sqrt{1 - k^2 \\sin^2 \\phi}$$\n\n"
        "They satisfy fundamental algebraic identities:\n\n"
        "$$\\text{sn}^2(u) + \\text{cn}^2(u) = 1, \\qquad k^2 \\text{sn}^2(u) + \\text{dn}^2(u) = 1$$\n\n"
        "Double periodicity periods are governed by the complete elliptic integrals $4K(k)$ and $2iK'(k)$. Widely used in the exact nonlinear pendulum solution and Korteweg-de Vries (KdV) solitons."
    ),

    # 6. jacobian matrix (index 18)
    18: (
        "In multivariable differential calculus, the $m \\times n$ matrix $\\mathbf{J}$ of all first-order partial derivatives of a vector-valued function "
        "$\\mathbf{f}: \\mathbb{R}^n \\to \\mathbb{R}^m$, representing the best linear local approximation (total derivative) of $\\mathbf{f}$ at $\\mathbf{x}$:\n\n"
        "$$\\mathbf{J} = \\frac{\\partial(f_1, \\dots, f_m)}{\\partial(x_1, \\dots, x_n)} = \\begin{bmatrix} "
        "\\frac{\\partial f_1}{\\partial x_1} & \\frac{\\partial f_1}{\\partial x_2} & \\dots & \\frac{\\partial f_1}{\\partial x_n} \\\\[6pt] "
        "\\frac{\\partial f_2}{\\partial x_1} & \\frac{\\partial f_2}{\\partial x_2} & \\dots & \\frac{\\partial f_2}{\\partial x_n} \\\\[6pt] "
        "\\vdots & \\vdots & \\ddots & \\vdots \\\\[6pt] "
        "\\frac{\\partial f_m}{\\partial x_1} & \\frac{\\partial f_m}{\\partial x_2} & \\dots & \\frac{\\partial f_m}{\\partial x_n} "
        "\\end{bmatrix}$$\n\n"
        "For square systems ($m = n$), the Jacobian determinant $\\det(\\mathbf{J})$ governs multivariable change of variables in integration: "
        "$dx_1 \\dots dx_n = |\\det(\\mathbf{J})|\\,du_1 \\dots du_n$."
    ),

    # 7. jahn-teller effect (index 21)
    21: (
        "A theorem of quantum chemistry and molecular physics formulated by Hermann Jahn and Edward Teller in 1937. It states that any non-linear "
        "molecular system in an electronically degenerate ground state will undergo spontaneous geometric distortion that lowers its molecular symmetry, "
        "removes the orbital degeneracy, and lowers the overall electronic energy:\n\n"
        "$$\\hat{H} = \\hat{H}_0 + \\sum_k \\left( \\frac{\\partial \\hat{H}}{\\partial Q_k} \\right)_0 Q_k$$\n\n"
        "Prominently observed in octahedral coordination complexes of transition metals with unevenly occupied $e_g$ orbitals, most notably $d^9$ copper(II) "
        "complexes ($[\\text{Cu}(\\text{H}_2\\text{O})_6]^{2+}$), where axial elongation splits the $e_g$ level into $d_{x^2 - y^2}$ and lower-energy $d_{z^2}$."
    ),

    # 8. jensen inequality (index 47)
    47: (
        "A foundational mathematical inequality in convex analysis and probability theory established by Danish mathematician Johan Jensen in 1906. "
        "For any convex function $g: \\mathbb{R} \\to \\mathbb{R}$ and real weights $\\lambda_i \\ge 0$ with $\\sum_{i=1}^n \\lambda_i = 1$:\n\n"
        "$$g\\left( \\sum_{i=1}^n \\lambda_i x_i \\right) \\le \\sum_{i=1}^n \\lambda_i g(x_i)$$\n\n"
        "In probabilistic expectation notation for a random variable $X$:\n\n"
        "$$g(\\mathbb{E}[X]) \\le \\mathbb{E}[g(X)]$$\n\n"
        "(with the inequality reversed if $g$ is strictly concave). Directly implies the arithmetic mean-geometric mean (AM-GM) inequality and Gibbs's entropy inequality in information theory."
    ),

    # 9. joint distribution function (index 61)
    61: (
        "In probability and multivariable statistics, the joint cumulative distribution function (joint CDF) $F_{X, Y}(x, y)$ of continuous random variables $X$ and $Y$, "
        "defined as the probability that $X \\le x$ and $Y \\le y$ simultaneously:\n\n"
        "$$F_{X, Y}(x, y) = \\mathbb{P}(X \\le x, \\, Y \\le y) = \\int_{-\\infty}^x \\int_{-\\infty}^y f_{X, Y}(u, v)\\,du\\,dv$$\n\n"
        "where $f_{X, Y}(u, v) \\ge 0$ is the joint probability density function (joint PDF), satisfying total normalization:\n\n"
        "$$\\int_{-\\infty}^\\infty \\int_{-\\infty}^\\infty f_{X, Y}(x, y)\\,dx\\,dy = 1$$\n\n"
        "The marginal PDF is recovered by integrating out the nuisance variable: $f_X(x) = \\int_{-\\infty}^\\infty f_{X, Y}(x, y)\\,dy$."
    ),

    # 10. jonquière's function (index 68)
    68: (
        "In analytic number theory and special functions, the polylogarithm function $\\text{Li}_s(z)$ (named after Alfred Jonquière), defined for complex $s$ and $|z| < 1$ "
        "by the Dirichlet series:\n\n"
        "$$\\text{Li}_s(z) = \\sum_{k=1}^\\infty \\frac{z^k}{k^s}$$\n\n"
        "Special integer values correspond to fundamental functions: $\\text{Li}_1(z) = -\\ln(1 - z)$, $\\text{Li}_2(z)$ is Euler's dilogarithm (Spence's function), "
        "and $\\text{Li}_3(z)$ is the trilogarithm. At $z = 1$, it evaluates to the Riemann zeta function: $\\text{Li}_s(1) = \\zeta(s)$ for $\\text{Re}(s) > 1$."
    ),

    # 11. jordan algebra (index 69)
    69: (
        "A non-associative, commutative algebra $(\\mathcal{A}, \\circ)$ over a field of characteristic $\\neq 2$, introduced by Pascual Jordan in 1933 to formalize "
        "the quantum mechanical algebra of observables. The Jordan product $a \\circ b$ satisfies the commutativity axiom and the Jordan identity:\n\n"
        "$$a \\circ b = b \\circ a$$\n\n"
        "$$(a^2 \\circ b) \\circ a = a^2 \\circ (b \\circ a)$$\n\n"
        "In quantum mechanics, if $\\mathcal{A}$ is an associative operator algebra, symmetrized product $A \\circ B = \\frac{1}{2}(AB + BA)$ forms a special Jordan algebra "
        "guaranteeing that the product of two Hermitian operators remains Hermitian."
    ),

    # 12. jordan block (index 70)
    70: (
        "In linear algebra, an upper triangular square matrix $\\mathbf{J}_k(\\lambda)$ of size $k \\times k$ consisting of a single scalar eigenvalue $\\lambda$ along the main "
        "diagonal, ones along the superdiagonal, and zeros elsewhere:\n\n"
        "$$\\mathbf{J}_k(\\lambda) = \\begin{bmatrix} "
        "\\lambda & 1 & 0 & \\dots & 0 \\\\[4pt] "
        "0 & \\lambda & 1 & \\dots & 0 \\\\[4pt] "
        "\\vdots & \\vdots & \\ddots & \\ddots & \\vdots \\\\[4pt] "
        "0 & 0 & \\dots & \\lambda & 1 \\\\[4pt] "
        "0 & 0 & \\dots & 0 & \\lambda "
        "\\end{bmatrix} = \\lambda \\mathbf{I}_k + \\mathbf{N}$$\n\n"
        "where $\\mathbf{N}$ is a standard nilpotent shift matrix ($\\mathbf{N}^k = \\mathbf{0}$). A Jordan block has geometric multiplicity $1$ and algebraic multiplicity $k$."
    ),

    # 13. jordan product (index 78)
    78: (
        "In operator theory and quantum mechanics, the symmetrized anti-commutator product of two operators or square matrices $\\mathbf{A}$ and $\\mathbf{B}$:\n\n"
        "$$\\mathbf{A} \\circ \\mathbf{B} = \\frac{1}{2}(\\mathbf{A}\\mathbf{B} + \\mathbf{B}\\mathbf{A})$$\n\n"
        "Because associative matrix multiplication does not preserve self-adjointness for non-commuting observables ($(\\mathbf{A}\\mathbf{B})^\\dagger = \\mathbf{B}^\\dagger \\mathbf{A}^\\dagger = \\mathbf{B}\\mathbf{A} \\neq \\mathbf{A}\\mathbf{B}$), "
        "the Jordan product preserves Hermiticity: $(\\mathbf{A} \\circ \\mathbf{B})^\\dagger = \\mathbf{A} \\circ \\mathbf{B}$."
    ),

    # 14. josephson's effects (index 82)
    82: (
        "Quantum macroscopic tunneling phenomena predicted by Brian Josephson in 1962, occurring when Cooper pairs tunnel through a thin insulating barrier between two superconductors (Josephson junction):\n\n"
        "* **DC Josephson effect**: A constant supercurrent flows with zero applied voltage across the junction:\n"
        "$$I = I_c \\sin(\\Delta\\phi)$$\n"
        "where $I_c$ is the critical current and $\\Delta\\phi$ is phase difference between superconducting macroscopic wavefunctions.\n\n"
        "* **AC Josephson effect**: Applying a constant DC voltage $V$ drives high-frequency oscillation of supercurrent:\n"
        "$$\\frac{d(\\Delta\\phi)}{dt} = \\frac{2eV}{\\hbar} \\implies f = \\frac{2e}{h} V$$\n\n"
        "where $\\frac{2e}{h} = K_J \\approx 483597.9\\,\\text{GHz/V}$ is the Josephson constant, providing the primary voltage standard in metrology."
    ),

    # 15. joule (index 83)
    83: (
        "The SI derived unit of energy, work, and amount of heat, with the symbol $\\text{J}$, named in honour of English physicist James Prescott Joule. "
        "Defined as the work done by a constant force of one newton acting through a displacement of one metre in the direction of the force:\n\n"
        "$$1\\,\\text{J} = 1\\,\\text{N}\\cdot\\text{m} = 1\\,\\text{kg}\\cdot\\text{m}^2\\cdot\\text{s}^{-2}$$\n\n"
        "In electrical terms: $1\\,\\text{J} = 1\\,\\text{W}\\cdot\\text{s} = 1\\,\\text{V}\\cdot\\text{A}\\cdot\\text{s} = 1\\,\\text{C}\\cdot\\text{V}$. "
        "Thermochemical conversions: $1\\,\\text{cal} = 4.184\\,\\text{J}$ and $1\\,\\text{eV} = 1.602176634 \\times 10^{-19}\\,\\text{J}$."
    ),

    # 16. joule heating (index 84)
    84: (
        "Also known as ohmic heating or resistive heating, the physical process by which electrical energy is irreversibly converted into thermal energy "
        "due to resistive collisions between charge carriers (electrons) and the conductor lattice. The thermal power $P$ generated is:\n\n"
        "$$P = I^2 R = \\frac{V^2}{R} = IV, \\quad \\text{SI unit: watt (W)}$$\n\n"
        "Over time $t$, total heat energy produced is $Q = I^2 R t$. Exploited in electric stoves, toasters, and arc furnaces, but represents parasitic transmission loss ($I^2 R$ loss) in electric power grids."
    ),

    # 17. joule's law (index 86)
    86: (
        "1. **Joule's first law of electric heating**: The thermal energy $Q$ generated in an electrical conductor of resistance $R$ carrying a current $I$ for duration $t$ is:\n\n"
        "$$Q = I^2 R t$$\n\n"
        "2. **Joule's second law of thermodynamics**: For an ideal gas, the internal energy $U$ depends exclusively on thermodynamic temperature $T$, being independent of volume $V$ and pressure $P$:\n\n"
        "$$\\left(\\frac{\\partial U}{\\partial V}\\right)_T = 0, \\qquad \\left(\\frac{\\partial U}{\\partial P}\\right)_T = 0$$\n\n"
        "Verified by Joule's free-expansion experiment into an evacuated chamber."
    ),

    # 18. joule-thomson effect (index 88)
    88: (
        "In thermodynamics, the temperature change experienced by a real gas when forced through a porous plug or throttling valve in a steady-state adiabatic expansion "
        "without external shaft work ($Q = 0, W = 0$). The process is strictly isenthalpic (constant enthalpy: $\\Delta H = 0$). The Joule-Thomson coefficient $\\mu_{\\text{JT}}$ is:\n\n"
        "$$\\mu_{\\text{JT}} = \\left( \\frac{\\partial T}{\\partial P} \\right)_H = \\frac{1}{C_p} \\left[ T \\left(\\frac{\\partial V}{\\partial T}\\right)_P - V \\right]$$\n\n"
        "For an ideal gas, $\\mu_{\\text{JT}} \\equiv 0$. For real gases below their Joule-Thomson inversion temperature ($T < T_{\\text{inv}}$), $\\mu_{\\text{JT}} > 0$, causing cooling upon expansion ($\\Delta T < 0$), "
        "which forms the foundational basis of the Linde-Hampson liquefaction of air and industrial cryogenic refrigeration."
    ),

    # 19. junction field-effect transistor, jfet (index 102)
    102: (
        "A three-terminal unipolar semiconductor device (Source, Drain, Gate) where channel current conduction between source and drain is modulated by the reverse-bias electrostatic "
        "depletion region of one or more $pn$ junctions. In the active saturation regime ($V_{\\text{DS}} \\ge V_{\\text{GS}} - V_P$), the drain current $I_D$ is governed by Shockley's quadratic relation:\n\n"
        "$$I_D = I_{\\text{DSS}} \\left( 1 - \\frac{V_{\\text{GS}}}{V_P} \\right)^2$$\n\n"
        "where $I_{\\text{DSS}}$ is the drain saturation current at zero gate-source bias ($V_{\\text{GS}} = 0$) and $V_P$ is the pinch-off voltage. "
        "Because the gate junction is operated in reverse bias ($I_G \\approx 0$), JFETs exhibit extremely high input impedance ($10^9\\text{--}10^{12}\\,\\Omega$)."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(j_entries):
        w = j_entries[idx]['word']
        j_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (J has {len(j_entries)} entries)")

data['J'] = j_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section J Complete Batch.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
