"""
enrich_section_i_batch_1.py
===========================
Section I Formula Enrichment - Batch 1 (Candidates 1 to 15)
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

i_entries = data.get('I', [])

UPDATES = {
    # 1. ideal gas (index 39)
    39: (
        "A theoretical gas composed of randomly moving point particles that interact solely through perfectly elastic collisions, "
        "obeying the ideal gas equation of state at all temperatures and pressures:\n\n"
        "$$PV = nRT = N k_B T$$\n\n"
        "where $P$ is pressure, $V$ is volume, $n$ is amount of substance in moles, $R = 8.314462618\\,\\text{J}\\cdot\\text{mol}^{-1}\\cdot\\text{K}^{-1}$ "
        "is the universal gas constant, $T$ is absolute thermodynamic temperature, $N$ is the number of particles, and $k_B = 1.380649 \\times 10^{-23}\\,\\text{J/K}$ "
        "is the Boltzmann constant. Real gases approach ideal behavior at low pressures and high temperatures."
    ),

    # 2. ideal gas law (index 40)
    40: (
        "The fundamental equation of state of a hypothetical ideal gas, combining Boyle's law ($PV = \\text{const}$), Charles's law "
        "($V/T = \\text{const}$), and Avogadro's law ($V/n = \\text{const}$):\n\n"
        "$$PV = nRT$$\n\n"
        "Expressed in terms of mass density $\\rho = \\frac{m}{V}$ and molar mass $M$ as $P = \\frac{\\rho RT}{M}$. The law implies that "
        "internal energy $U$ depends strictly on temperature ($U = c_V n T$) and provides the baseline for non-ideal real gas models such as the van der Waals equation."
    ),

    # 3. idempotent (index 44)
    44: (
        "1. In linear algebra and ring theory, an element or matrix $\\mathbf{A}$ that equals its own square under multiplication:\n\n"
        "$$\\mathbf{A}^2 = \\mathbf{A}$$\n\n"
        "Every idempotent matrix represents an oblique or orthogonal projection onto its column space $\\text{col}(\\mathbf{A})$, "
        "and its eigenvalues are restricted strictly to $0$ and $1$ ($\\lambda \\in \\{0, 1\\}$). "
        "2. In abstract algebra, an operation $*$ is idempotent if $x * x = x$ for all elements $x$. For example, set union and intersection "
        "are idempotent: $S \\cup S = S$ and $S \\cap S = S$. A ring in which every element is idempotent ($x^2 = x$) is a Boolean ring."
    ),

    # 4. identical equation (index 46)
    46: (
        "An algebraic equality (identity) that holds true for every permissible numerical value assigned to its variables, distinguished "
        "from a conditional equation which holds only for specific solution roots. Frequently denoted with the identity sign $\\equiv$:\n\n"
        "$$(x^2 - a^2) \\equiv (x - a)(x + a), \\qquad (x + y)^2 \\equiv x^2 + 2xy + y^2$$\n\n"
        "Prominent trigonometric examples include the Pythagorean identity $\\sin^2 \\theta + \\cos^2 \\theta \\equiv 1$ and Euler's formula $e^{i\\theta} \\equiv \\cos \\theta + i\\sin \\theta$."
    ),

    # 5. identity (index 51)
    51: (
        "1. In mathematics, an equality relation $A \\equiv B$ valid for all possible values of the variables involved, such as the trigonometric identity:\n\n"
        "$$\\sin^2 \\theta + \\cos^2 \\theta = 1$$\n\n"
        "2. In algebra, an identity element $e$ of an algebraic structure $(G, *)$ satisfying $a * e = e * a = a$ for all $a \\in G$. "
        "3. In logic and philosophy, the binary reflexive relation of numerical identity $\\forall x, \\, x = x$, formalizing that an object is identical strictly to itself."
    ),

    # 6. identity element (index 52)
    52: (
        "For a set $S$ equipped with a binary operation $*: S \\times S \\to S$, a distinguished neutral element $e \\in S$ such that for every $x \\in S$:\n\n"
        "$$x * e = e * x = x$$\n\n"
        "In an additive group or ring $(R, +)$, the identity element is the additive zero ($0$), where $x + 0 = 0 + x = x$. In a multiplicative "
        "monoid, group, or field $(F, \\cdot)$, the identity element is unity ($1$), where $x \\times 1 = 1 \\times x = x$. In any group, the identity element is unique."
    ),

    # 7. identity function (index 53)
    53: (
        "A mathematical function $\\text{id}_X: X \\to X$ that maps every element of its domain set $X$ to itself:\n\n"
        "$$\\text{id}_X(x) = x \\quad \\forall x \\in X$$\n\n"
        "In function composition, $\\text{id}_X$ acts as the neutral two-sided identity: for any function $f: X \\to Y$, $f \\circ \\text{id}_X = f$ "
        "and $\\text{id}_Y \\circ f = f$. On real numbers $\\mathbb{R}$, its Cartesian graph is the $45^\\circ$ bisector line $y = x$ passing through the origin."
    ),

    # 8. identity matrix (index 54)
    54: (
        "The $n \\times n$ square diagonal matrix $\\mathbf{I}_n$ whose main diagonal entries are all $1$ and all off-diagonal entries are $0$, "
        "defined via the Kronecker delta as $(\\mathbf{I}_n)_{ij} = \\delta_{ij}$:\n\n"
        "$$\\mathbf{I}_n = \\begin{bmatrix} 1 & 0 & 0 & \\dots & 0 \\\\[4pt] 0 & 1 & 0 & \\dots & 0 \\\\[4pt] 0 & 0 & 1 & \\dots & 0 \\\\[4pt] \\vdots & \\vdots & \\vdots & \\ddots & \\vdots \\\\[4pt] 0 & 0 & 0 & \\dots & 1 \\end{bmatrix}$$\n\n"
        "It serves as the multiplicative identity in matrix algebra: for any compatible matrix $\\mathbf{A}$, $\\mathbf{A}\\mathbf{I} = \\mathbf{I}\\mathbf{A} = \\mathbf{A}$. "
        "For an invertible matrix $\\mathbf{A}$, $\\mathbf{A}\\mathbf{A}^{-1} = \\mathbf{A}^{-1}\\mathbf{A} = \\mathbf{I}$."
    ),

    # 9. identity property of addition (index 56)
    56: (
        "A foundational axiom of arithmetic and ring theory stating that the sum of any real or complex number $n$ and zero is equal to $n$:\n\n"
        "$$n + 0 = 0 + n = n$$\n\n"
        "Zero is the unique additive identity element in $\\mathbb{Z}, \\mathbb{Q}, \\mathbb{R}$, and $\\mathbb{C}$."
    ),

    # 10. identity property of multiplication (index 57)
    57: (
        "A foundational axiom of arithmetic and field theory asserting that the product of any real or complex number $n$ and the number one is equal to $n$:\n\n"
        "$$n \\times 1 = 1 \\times n = n$$\n\n"
        "One ($1$) is the unique multiplicative identity element in $\\mathbb{Z}, \\mathbb{Q}, \\mathbb{R}$, and $\\mathbb{C}$."
    ),

    # 11. identity theorem (index 59)
    59: (
        "In complex analysis, a rigidity theorem stating that if two holomorphic (analytic) functions $f$ and $g$ defined on a connected open region "
        "$\\Omega \\subseteq \\mathbb{C}$ agree on a subset $S \\subset \\Omega$ that has an accumulation point (limit point) in $\\Omega$:\n\n"
        "$$f(z) = g(z) \\; \\forall z \\in S, \\; z_0 \\in S' \\cap \\Omega \\implies f(z) = g(z) \\; \\forall z \\in \\Omega$$\n\n"
        "A direct consequence is that the zeros of a non-constant holomorphic function are strictly isolated, and analytic continuation from any arc or cluster is unique."
    ),

    # 12. imaginary number (index 74)
    74: (
        "A complex number whose square is a non-positive real number, expressed in standard form as $z = bi$ where $b \\in \\mathbb{R}$ ($b \\neq 0$) "
        "and $i$ is the imaginary unit satisfying:\n\n"
        "$$i = \\sqrt{-1}, \\quad i^2 = -1$$\n\n"
        "For example, $\\sqrt{-9} = 3i$ and $\\sqrt{-3} = i\\sqrt{3}$. On the complex plane (Argand diagram), pure imaginary numbers lie "
        "exclusively along the vertical imaginary axis."
    ),

    # 13. implicit (index 141)
    141: (
        "In calculus, a relation between independent variable(s) $x$ and dependent variable $y$ defined by an equation of the form:\n\n"
        "$$F(x, y) = 0$$\n\n"
        "in which $y$ is not explicitly isolated as $y = f(x)$. For example, the equation of the unit circle $x^2 + y^2 - 1 = 0$ or the folium of "
        "Descartes $x^3 + y^3 - 3axy = 0$ define $y$ implicitly as functions of $x$."
    ),

    # 14. implicit differentiation (index 142)
    142: (
        "A differentiation technique applied to calculate the derivative $\\frac{dy}{dx}$ of an implicitly defined curve $F(x, y) = 0$ using the chain rule "
        "without first explicitly solving for $y$ in terms of $x$:\n\n"
        "$$\\frac{d}{dx}[F(x, y)] = \\frac{\\partial F}{\\partial x} + \\frac{\\partial F}{\\partial y}\\frac{dy}{dx} = 0 \\implies \\frac{dy}{dx} = -\\frac{F_x}{F_y} \\quad (F_y \\neq 0)$$\n\n"
        "For example, differentiating $x^2 + y^2 = r^2$ with respect to $x$ gives $2x + 2y\\frac{dy}{dx} = 0 \\implies \\frac{dy}{dx} = -\\frac{x}{y}$."
    ),

    # 15. implicit function theorem (index 143)
    143: (
        "A central theorem in multivariable differential calculus stating that for a continuously differentiable function $\\mathbf{F}: \\mathbb{R}^{n+m} \\to \\mathbb{R}^m$ "
        "satisfying $\\mathbf{F}(\\mathbf{a}, \\mathbf{b}) = \\mathbf{0}$, if the Jacobian determinant with respect to $\\mathbf{y}$ is non-zero at $(\\mathbf{a}, \\mathbf{b})$:\n\n"
        "$$\\det\\left( \\frac{\\partial \\mathbf{F}}{\\partial \\mathbf{y}}(\\mathbf{a}, \\mathbf{b}) \\right) \\neq 0$$\n\n"
        "then there exists an open neighborhood $U$ of $\\mathbf{a}$ and a unique $C^1$ function $\\mathbf{g}: U \\to \\mathbb{R}^m$ such that $\\mathbf{b} = \\mathbf{g}(\\mathbf{a})$ "
        "and $\\mathbf{F}(\\mathbf{x}, \\mathbf{g}(\\mathbf{x})) = \\mathbf{0}$ for all $\\mathbf{x} \\in U$. The Jacobian matrix of $\\mathbf{g}$ is given by "
        "$\\mathbf{J}_{\\mathbf{g}}(\\mathbf{x}) = -\\left[\\frac{\\partial \\mathbf{F}}{\\partial \\mathbf{y}}(\\mathbf{x}, \\mathbf{g}(\\mathbf{x}))\\right]^{-1} "
        "\\left[\\frac{\\partial \\mathbf{F}}{\\partial \\mathbf{x}}(\\mathbf{x}, \\mathbf{g}(\\mathbf{x}))\\right]$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(i_entries):
        w = i_entries[idx]['word']
        i_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (I has {len(i_entries)} entries)")

data['I'] = i_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section I Batch 1.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
