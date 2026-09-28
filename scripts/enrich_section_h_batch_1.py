"""
enrich_section_h_batch_1.py
===========================
Section H Formula Enrichment - Batch 1 (Candidates 1 to 15)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
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

h_entries = data.get('H', [])

UPDATES = {
    # 1. haar measure (Candidate 1, index 3)
    3: (
        "Introduced by Hungarian mathematician Alfréd Haar in 1933, a non-zero, regular Borel measure $\\mu$ on the "
        "$\\sigma$-algebra $\\mathcal{B}(G)$ of a locally compact topological group $G$ that assigns finite measure to "
        "compact subsets and is invariant under group operations. The measure is left-invariant if:\n\n"
        "$$\\mu(gA) = \\mu(A) \\quad \\forall g \\in G, \\; A \\in \\mathcal{B}(G)$$\n\n"
        "and right-invariant if $\\mu(Ag) = \\mu(A)$. On abelian (commutative) or compact groups, every left-invariant Haar "
        "measure is also right-invariant (unimodular). Haar measure is unique up to a positive multiplicative scalar constant. "
        "On $\\mathbb{R}^n$ under addition, Haar measure coincides with standard Lebesgue measure $\\lambda$."
    ),

    # 2. hadamard design (Candidate 2, index 18)
    18: (
        "Named after French mathematician Jacques Hadamard, a symmetric balanced incomplete block design (BIBD) with "
        "parameters $(v, k, \\lambda) = (4\\lambda + 3, 2\\lambda + 1, \\lambda)$ for some positive integer $\\lambda$. "
        "It consists of $v = 4\\lambda + 3$ varieties (points) and an equal number of blocks $b = 4\\lambda + 3$, where "
        "each block contains $k = 2\\lambda + 1$ points, and every pair of distinct points occurs together in exactly "
        "$\\lambda$ blocks. Every Hadamard design is structurally equivalent to a Hadamard matrix of order $4(\\lambda + 1)$."
    ),

    # 3. hadamard matrix (Candidate 3, index 20)
    20: (
        "An $n \\times n$ square matrix $\\mathbf{H}$ whose entries are exclusively $+1$ or $-1$ and whose mutually orthogonal "
        "column and row vectors satisfy:\n\n"
        "$$\\mathbf{H}\\mathbf{H}^T = n \\mathbf{I}_n$$\n\n"
        "Consequently, its matrix inverse is simply its transpose scaled by $\\frac{1}{n}$:\n\n"
        "$$\\mathbf{H}^{-1} = \\frac{1}{n}\\mathbf{H}^T$$\n\n"
        "The order $n$ of any Hadamard matrix must be $1$, $2$, or a multiple of $4$ ($n \\equiv 0 \\pmod 4$). Hadamard matrices "
        "maximize the determinant among all matrices with entries in $[-1, 1]$ (Hadamard's maximal determinant problem) "
        "and are widely used in error-correcting codes (Reed-Muller codes), signal processing, and orthogonal spectroscopy."
    ),

    # 4. hadamard product (Candidate 4, index 21)
    21: (
        "Also known as the Schur product or entrywise product, a binary operation that takes two matrices $\\mathbf{A}$ "
        "and $\\mathbf{B}$ of the identical dimensions $m \\times n$ and produces another matrix $\\mathbf{C} = \\mathbf{A} \\circ \\mathbf{B}$ "
        "of the same size, where each element is the scalar product of corresponding entries:\n\n"
        "$$(\\mathbf{A} \\circ \\mathbf{B})_{ij} = a_{ij} b_{ij} \\quad \\text{for } 1 \\le i \\le m, \\; 1 \\le j \\le n$$\n\n"
        "Unlike standard matrix multiplication, the Hadamard product is strictly commutative: $\\mathbf{A} \\circ \\mathbf{B} = \\mathbf{B} \\circ \\mathbf{A}$. "
        "By the Schur product theorem, the Hadamard product of two positive semi-definite matrices is also positive semi-definite."
    ),

    # 5. hahn decomposition (Candidate 5, index 60)
    60: (
        "A foundational theorem in measure theory stating that given a measurable space $(X, \\Sigma)$ and a signed measure "
        "$\\nu$, there exists a measurable partition of $X$ into a positive set $P$ and a negative set $N$ such that:\n\n"
        "$$X = P \\cup N, \\quad P \\cap N = \\emptyset$$\n\n"
        "where for every measurable subset $E \\in \\Sigma$, $\\nu(E \\cap P) \\ge 0$ and $\\nu(E \\cap N) \\le 0$. "
        "The Hahn decomposition is essentially unique up to $\\nu$-null sets and provides the analytical basis for the "
        "Jordan decomposition theorem, decomposing $\\nu = \\nu^+ - \\nu^-$ into mutually singular positive measures."
    ),

    # 6. hahn-banach theorem (Candidate 6, index 62)
    62: (
        "A core theorem of functional analysis proved by Hans Hahn (1927) and Stefan Banach (1929). In its analytical form, "
        "if $p: V \\to \\mathbb{R}$ is a sublinear functional on a real vector space $V$, and $f: U \\to \\mathbb{R}$ is a linear "
        "functional defined on a linear subspace $U \\subseteq V$ bounded by $p$ ($f(x) \\le p(x)$ for all $x \\in U$), then there "
        "exists a linear extension $F: V \\to \\mathbb{R}$ such that:\n\n"
        "$$F(x) = f(x) \\; \\forall x \\in U \\quad \\text{and} \\quad F(x) \\le p(x) \\; \\forall x \\in V$$\n\n"
        "In normed spaces, it guarantees that every bounded linear functional on a subspace can be extended to the whole space "
        "preserving its operator norm: $\\|F\\| = \\|f\\|$. Geometrically, it implies that convex sets can be separated by hyperplanes."
    ),

    # 7. hairy ball theorem (Candidate 7, index 73)
    73: (
        "A celebrated theorem of algebraic topology proved by Henri Poincaré (1885) and Luitzen Brouwer (1912), stating that there "
        "is no non-vanishing continuous tangent vector field on even-dimensional spheres $S^{2k}$. For the 2-sphere $S^2$ in $\\mathbb{R}^3$:\n\n"
        "$$\\mathbf{v} \\in C(S^2, \\mathbb{R}^3), \\; \\mathbf{v}(x) \\cdot x = 0 \\; \\forall x \\in S^2 \\implies \\exists x_0 \\in S^2 \\text{ such that } \\mathbf{v}(x_0) = \\mathbf{0}$$\n\n"
        "In meteorological terms, viewing the Earth as $S^2$, horizontal wind forms a tangent vector field; hence at any given moment "
        "there must be at least one point on Earth where the horizontal wind speed is exactly zero (such as the calm eye of a cyclone)."
    ),

    # 8. half-angle formula (Candidate 8, index 79)
    79: (
        "A set of trigonometric identities derived from the double-angle formulas that express trigonometric functions of half an angle "
        "$\\frac{x}{2}$ in terms of the cosine of the full angle $x$:\n\n"
        "$$\\sin\\left(\\frac{x}{2}\\right) = \\pm \\sqrt{\\frac{1 - \\cos x}{2}}$$\n\n"
        "$$\\cos\\left(\\frac{x}{2}\\right) = \\pm \\sqrt{\\frac{1 + \\cos x}{2}}$$\n\n"
        "$$\\tan\\left(\\frac{x}{2}\\right) = \\pm \\sqrt{\\frac{1 - \\cos x}{1 + \\cos x}} = \\frac{1 - \\cos x}{\\sin x} = \\frac{\\sin x}{1 + \\cos x}$$\n\n"
        "where the sign ($+$ or $-$) is determined by the quadrant in which the angle $\\frac{x}{2}$ terminates."
    ),

    # 9. half-equation (Candidate 9, index 84)
    84: (
        "In electrochemistry and redox stoichiometry, a representation of either the oxidation or the reduction component of a "
        "complete oxidation-reduction reaction, explicitly showing the transfer of electrons $e^-$:\n\n"
        "$$\\text{Oxidation (anode): } \\text{Zn}_{(s)} \\longrightarrow \\text{Zn}^{2+}_{(aq)} + 2e^-$$\n\n"
        "$$\\text{Reduction (cathode): } \\text{Cu}^{2+}_{(aq)} + 2e^- \\longrightarrow \\text{Cu}_{(s)}$$\n\n"
        "Summing the two balanced half-equations cancels the shared electrons to yield the overall net ionic cell equation:\n\n"
        "$$\\text{Zn}_{(s)} + \\text{Cu}^{2+}_{(aq)} \\longrightarrow \\text{Zn}^{2+}_{(aq)} + \\text{Cu}_{(s)}$$"
    ),

    # 10. half-plane (Candidate 10, index 91)
    91: (
        "A planar geometric region consisting of all points $(x, y) \\in \\mathbb{R}^2$ lying on one side of an infinite straight "
        "dividing line $ax + by = c$. A closed half-plane includes the boundary line and is defined by a non-strict inequality:\n\n"
        "$$ax + by \\ge c \\quad \\text{or} \\quad ax + by \\le c$$\n\n"
        "An open half-plane excludes the boundary line and is defined by strict inequality: $ax + by > c$ or $ax + by < c$. "
        "In linear programming, the feasible region of constraints represents the intersection of multiple closed half-planes."
    ),

    # 11. half-space (Candidate 11, index 93)
    93: (
        "In $n$-dimensional Euclidean space $\\mathbb{R}^n$, either of the two regions into which space is divided by an affine "
        "hyperplane $H = \\{\\mathbf{x} \\in \\mathbb{R}^n : \\mathbf{a}^T \\mathbf{x} = c\\}$ where $\\mathbf{a} \\neq \\mathbf{0}$. "
        "A closed half-space is defined by:\n\n"
        "$$\\mathcal{H}_{\\ge} = \\{\\mathbf{x} \\in \\mathbb{R}^n : \\mathbf{a}^T \\mathbf{x} \\ge c\\}$$\n\n"
        "and an open half-space is defined by $\\mathcal{H}_{>} = \\{\\mathbf{x} \\in \\mathbb{R}^n : \\mathbf{a}^T \\mathbf{x} > c\\}$. "
        "Half-spaces are convex sets; any convex polyhedron in $\\mathbb{R}^n$ is the finite intersection of closed half-spaces."
    ),

    # 12. hall effect (Candidate 12, index 103)
    103: (
        "The generation of a transverse potential difference (the Hall voltage $V_H$) across an electrical conductor or semiconductor "
        "carrying a longitudinal electric current $I$ placed in a perpendicular magnetic field $\\mathbf{B}$. Discovered by Edwin Hall in 1879, "
        "the Lorentz force $\\mathbf{F} = q(\\mathbf{v}_d \\times \\mathbf{B})$ deflects charge carriers to one lateral face until an opposing "
        "transverse electrostatic field $\\mathbf{E}_H$ balances the magnetic force. The Hall voltage across a sample of thickness $d$ is:\n\n"
        "$$V_H = \\frac{I B}{n q d} = R_H \\frac{I B}{d}$$\n\n"
        "where $n$ is charge carrier volume density, $q$ is carrier charge, and $R_H = \\frac{1}{nq}$ is the Hall coefficient. "
        "The sign of $V_H$ determines whether conduction is dominated by electrons ($R_H < 0$) or holes ($R_H > 0$)."
    ),

    # 13. hall effect thruster (Candidate 13, index 104)
    104: (
        "A type of ion thruster used for spacecraft propulsion that utilizes an annular magnetic field to trap electrons in a closed drift "
        "($\\mathbf{E} \\times \\mathbf{B}$ Hall current). Propellant gas (typically xenon, $\\text{Xe}$) injected at the anode is ionized by "
        "electron impact to produce $\\text{Xe}^+$ ions. The axial electric field accelerates the ions through the electrostatic potential "
        "drop $\\Delta V$ to high exhaust velocities:\n\n"
        "$$v_e = \\sqrt{\\frac{2 q \\Delta V}{m_i}}$$\n\n"
        "producing specific impulse $I_{\\text{sp}} = \\frac{v_e}{g_0} \\approx 1,500\\text{--}3,000\\,\\text{s}$. A hollow cathode external "
        "to the channel neutralizes the exiting ion plume to prevent spacecraft charging."
    ),

    # 14. ham sandwich theorem (Candidate 14, index 138)
    138: (
        "A fundamental theorem in measure theory and topology (a corollary of the Borsuk-Ulam theorem), asserting that given $n$ "
        "measurable sets (objects) in $n$-dimensional Euclidean space $\\mathbb{R}^n$ with finite non-zero measures, there exists at least "
        "one $(n-1)$-dimensional affine hyperplane that simultaneously bisects the measure of all $n$ sets:\n\n"
        "$$\\mu_i(A_i \\cap H^+) = \\mu_i(A_i \\cap H^-) = \\frac{1}{2}\\mu_i(A_i) \\quad \\text{for } i = 1, 2, \\dots, n$$\n\n"
        "In $\\mathbb{R}^3$ ($n=3$), it demonstrates that a sandwich consisting of two pieces of bread and a slice of ham of arbitrary "
        "shapes and positions can always be bisected in half with a single planar knife cut."
    ),

    # 15. hamilton's equations of motion (Candidate 15, index 142)
    142: (
        "In analytical mechanics, a formulation of classical mechanics where the state of a dynamical system is described by canonical "
        "coordinates $q_i$ and conjugate momenta $p_i = \\frac{\\partial L}{\\partial \\dot{q}_i}$ in phase space. The equations of motion "
        "form a symmetric set of $2n$ first-order differential equations governed by the Hamiltonian function $H(q, p, t)$:\n\n"
        "$$\\dot{q}_i = \\frac{\\partial H}{\\partial p_i}, \\qquad \\dot{p}_i = -\\frac{\\partial H}{\\partial q_i} \\quad (i = 1, \\dots, n)$$\n\n"
        "where $H = \\sum_{i} p_i \\dot{q}_i - L$ is obtained via Legendre transformation of the Lagrangian $L$. For time-independent "
        "potentials in conservative systems, $H$ equals total mechanical energy $E = T + V$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(h_entries):
        w = h_entries[idx]['word']
        h_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (H has {len(h_entries)} entries)")

data['H'] = h_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section H Batch 1.")

# Rebuild core_dictionary.js using the dedicated engine script
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
    print(res.stdout[-300:] if len(res.stdout) > 300 else res.stdout)
else:
    print("Error during rebuild:")
    print(res.stderr)
