"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION C (BATCH 1)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section C
(Items 1-100) using KaTeX LaTeX typesetting.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_C1_DEFINITIONS = {
    "cahn-hilliard model": (
        "A non-linear fourth-order partial differential equation in mathematical physics describing the process of spontaneous phase separation (spinodal decomposition) "
        "in a binary fluid mixture: "
        "$$\\frac{\\partial c}{\\partial t} = D \\nabla^2 \\mu = D \\nabla^2 \\left(c^3 - c - \\gamma \\nabla^2 c\\right)$$"
        "where $c(\\vec{r}, t)$ is the conserved scalar concentration order parameter (with $c = \\pm 1$ representing pure domains), "
        "$D$ is the diffusion mobility coefficient, and $\\mu = \\frac{\\delta F}{\\delta c} = c^3 - c - \\gamma \\nabla^2 c$ is the chemical potential."
    ),
    "canonical equations of motion": (
        "In Hamiltonian mechanics, the symmetric first-order differential equations governing the time evolution of a dynamical system in phase space: "
        "$$\\dot{q}_i = \\frac{\\partial H}{\\partial p_i} \\quad \\text{and} \\quad \\dot{p}_i = -\\frac{\\partial H}{\\partial q_i}$$ "
        "where $q_i$ are generalized coordinates, $p_i = \\frac{\\partial L}{\\partial \\dot{q}_i}$ are conjugate momenta, and $H(q, p, t) = \\sum p_i \\dot{q}_i - L$ is the Hamiltonian function representing total mechanical energy."
    ),
    "cantor-bernstein theorem": (
        "A fundamental theorem in set theory stating that if there exist injective mappings $f: A \\to B$ and $g: B \\to A$ between two sets $A$ and $B$, "
        "then there exists a bijective mapping between them, establishing that both sets have identical cardinality: "
        "$$|A| \\le |B| \\quad \\text{and} \\quad |B| \\le |A| \\implies |A| = |B|$$"
    ),
    "capacitance": (
        "The ability of a system of electrical conductors and dielectrics to store electric charge per unit potential difference: "
        "$$C = \\frac{Q}{V}$$ "
        "where $Q$ is the stored charge in coulombs and $V$ is electric potential difference in volts. Its SI unit is the farad ($\\text{F}$). "
        "For an ideal parallel-plate capacitor with plate area $A$ separated by distance $d$: "
        "$$C = \\frac{\\varepsilon_0 \\varepsilon_r A}{d}$$ "
        "where $\\varepsilon_0 \\approx 8.854 \\times 10^{-12}\\text{ F/m}$ is permittivity of free space and $\\varepsilon_r$ is relative permittivity (dielectric constant)."
    ),
    "capacitive reactance": (
        "The opposition to the flow of alternating current caused by a capacitor's capacitance, denoted by $X_C$: "
        "$$X_C = \\frac{1}{\\omega C} = \\frac{1}{2\\pi f C}$$ "
        "where $X_C$ is measured in ohms ($\\Omega$), $f$ is frequency in Hertz, and $C$ is capacitance in farads. "
        "By Ohm's Law for capacitive AC circuits: $V_C = I_C X_C$. "
        "For capacitors in parallel: $C_{\\text{total}} = C_1 + C_2 + \\dots + C_n$. "
        "For capacitors in series: $\\frac{1}{C_{\\text{total}}} = \\frac{1}{C_1} + \\frac{1}{C_2} + \\dots + \\frac{1}{C_n}$."
    ),
    "cardano's formula": (
        "The algebraic solution for the roots of a reduced cubic equation $y^3 + py + q = 0$, published by Gerolamo Cardano (1545): "
        "$$y = \\sqrt[3]{-\\frac{q}{2} + \\sqrt{\\Delta}} + \\sqrt[3]{-\\frac{q}{2} - \\sqrt{\\Delta}}$$ "
        "where the cubic discriminant $\\Delta$ is given by: "
        "$$\\Delta = \\left(\\frac{q}{2}\\right)^2 + \\left(\\frac{p}{3}\\right)^3$$ "
        "If $\\Delta > 0$, there is one real root and two complex conjugate roots; if $\\Delta = 0$, there are multiple real roots; "
        "and if $\\Delta < 0$ (casus irreducibilis), there are three distinct real roots."
    ),
    "cardioid": (
        "A heart-shaped plane curve traced by a fixed point on the perimeter of a circle of radius $a$ rolling without slipping around an equal fixed circle of radius $a$. "
        "In polar coordinates, its equation is: "
        "$$r = 2a(1 \\pm \\cos\\theta) \\quad \\text{or} \\quad r = 2a(1 \\pm \\sin\\theta)$$ "
        "In Cartesian coordinates: "
        "$$(x^2 + y^2 - 2ax)^2 = 4a^2(x^2 + y^2)$$"
    ),
    "carmichael number": (
        "A composite positive integer $n$ that satisfies Fermat's Little Theorem congruence for all integers $b$ coprime to $n$: "
        "$$b^{n-1} \\equiv 1 \\pmod n \\quad \\text{for all } \\gcd(b, n) = 1$$ "
        "Also known as absolute pseudoprimes. By Korselt's criterion, a composite integer $n$ is a Carmichael number if and only if $n$ is square-free "
        "and for every prime divisor $p$ of $n$, $(p - 1)$ divides $(n - 1)$. The smallest Carmichael number is $561 = 3 \\times 11 \\times 17$."
    ),
    "cartesian distance": (
        "The straight-line Euclidean distance between two points in Cartesian coordinate space. "
        "In 2-dimensional space between points $P(x_1, y_1)$ and $Q(x_2, y_2)$: "
        "$$d(P, Q) = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$ "
        "In $n$-dimensional Euclidean space $\\mathbb{R}^n$ between vectors $\\vec{p}$ and $\\vec{q}$: "
        "$$d(\\vec{p}, \\vec{q}) = \\sqrt{\\sum_{i=1}^n (p_i - q_i)^2}$$"
    ),
    "cartesian product": (
        "1. For two sets $A$ and $B$, the set of all ordered pairs $(a, b)$ where $a \\in A$ and $b \\in B$: "
        "$$A \\times B = \\{(a, b) : a \\in A \\text{ and } b \\in B\\}$$ "
        "The cardinality satisfies $|A \\times B| = |A| \\times |B|$. "
        "2. For two 3-dimensional Cartesian vectors $\\vec{a}$ and $\\vec{b}$, their vector cross product is: "
        "$$\\vec{a} \\times \\vec{b} = \\begin{vmatrix} \\hat{i} & \\hat{j} & \\hat{k} \\\\ a_x & a_y & a_z \\\\ b_x & b_y & b_z \\end{vmatrix} = (a_y b_z - a_z b_y)\\hat{i} + (a_z b_x - a_x b_z)\\hat{j} + (a_x b_y - a_y b_x)\\hat{k}$$ "
        "with magnitude $|\\vec{a} \\times \\vec{b}| = |\\vec{a}| |\\vec{b}| \\sin\\theta$."
    ),
    "catalan numbers": (
        "A sequence of positive integers $C_n$ appearing in combinatorial counting problems, defined by the formula: "
        "$$C_n = \\frac{1}{n + 1} \\binom{2n}{n} = \\frac{(2n)!}{(n + 1)! \\, n!} \\quad (n \\ge 0)$$ "
        "The first several terms are $1, 1, 2, 5, 14, 42, 132, 429, 1430$. "
        "Catalan numbers enumerate the number of correct bracket pairings of $n$ pairs of parentheses, full binary trees with $n+1$ leaves, "
        "and triangulations of a convex polygon with $n+2$ vertices."
    ),
    "catalan's constant": (
        "A mathematical constant, denoted by $G$ or $K$, appearing in combinatorics and definite integrals, defined as the sum of the alternating Dirichlet beta series: "
        "$$K = \\sum_{n=0}^{\\infty} \\frac{(-1)^n}{(2n + 1)^2} = 1 - \\frac{1}{9} + \\frac{1}{25} - \\frac{1}{49} + \\dots \\approx 0.91596559$$"
    ),
    "cauchy condensation test": (
        "A convergence test for an infinite series $\\sum_{n=1}^\\infty a_n$ of non-negative, monotonically decreasing terms ($a_1 \\ge a_2 \\ge \\dots \\ge 0$): "
        "$$\\sum_{n=1}^{\\infty} a_n \\text{ converges} \\iff \\sum_{k=0}^{\\infty} 2^k a_{2^k} \\text{ converges}$$ "
        "For example, applying this test to the $p$-series $\\sum \\frac{1}{n^p}$ yields $\\sum 2^k \\frac{1}{(2^k)^p} = \\sum (2^{1-p})^k$, which converges if and only if $p > 1$."
    ),
    "cauchy integral formula": (
        "A central theorem in complex analysis stating that if a function $f(z)$ is holomorphic (analytic) within and on a simple closed positively oriented contour $C$, "
        "then for every point $z_0$ inside $C$: "
        "$$f(z_0) = \\frac{1}{2\\pi i} \\oint_C \\frac{f(z)}{z - z_0} \\, dz$$ "
        "Higher derivatives of $f$ are given by: "
        "$$f^{(n)}(z_0) = \\frac{n!}{2\\pi i} \\oint_C \\frac{f(z)}{(z - z_0)^{n+1}} \\, dz$$"
    ),
    "cauchy product": (
        "The discrete convolution product of two infinite series $\\sum_{n=0}^\\infty a_n$ and $\\sum_{n=0}^\\infty b_n$, defined as $\\sum_{n=0}^\\infty c_n$ where: "
        "$$c_n = \\sum_{k=0}^{n} a_k b_{n-k} = a_0 b_n + a_1 b_{n-1} + \\dots + a_n b_0$$ "
        "By Mertens' theorem, if both series converge and at least one converges absolutely, their Cauchy product converges to the product of their sums: "
        "$$\\sum_{n=0}^{\\infty} c_n = \\left(\\sum_{n=0}^{\\infty} a_n\\right) \\left(\\sum_{n=0}^{\\infty} b_n\\right)$$"
    ),
    "cauchy's inequality": (
        "The fundamental Cauchy-Schwarz inequality for sequences of real numbers: "
        "$$\\left(\\sum_{i=1}^n a_i b_i\\right)^2 \\le \\left(\\sum_{i=1}^n a_i^2\\right) \\left(\\sum_{i=1}^n b_i^2\\right)$$ "
        "Equality holds if and only if the sequences are proportional ($a_i = \\lambda b_i$). In vector dot-product notation: "
        "$$|\\vec{a} \\cdot \\vec{b}| \\le \\|\\vec{a}\\| \\|\\vec{b}\\|$$"
    ),
    "cauchy's integral theorem": (
        "A foundational theorem of complex analysis stating that if a function $f(z)$ is analytic throughout a simply connected domain $D$, "
        "then its contour integral around any closed rectifiable path $C$ in $D$ is zero: "
        "$$\\oint_C f(z) \\, dz = 0$$"
    ),
    "cauchy's mean-value theorem": (
        "Also known as the Extended Mean Value Theorem, stating that if real-valued functions $f$ and $g$ are continuous on $[a, b]$ "
        "and differentiable on $(a, b)$, then there exists at least one $c \\in (a, b)$ such that: "
        "$$[f(b) - f(a)] g'(c) = [g(b) - g(a)] f'(c) \\iff \\frac{f'(c)}{g'(c)} = \\frac{f(b) - f(a)}{g(b) - g(a)}$$ "
        "provided $g'(c) \\neq 0$ and $g(b) \\neq g(a)$. This theorem forms the basis of L'Hôpital's Rule."
    ),
    "cauchy's ratio test": (
        "D'Alembert's ratio test for the absolute convergence of a complex or real series $\\sum_{n=1}^\\infty a_n$ with non-zero terms: "
        "$$L = \\lim_{n \\to \\infty} \\left| \\frac{a_{n+1}}{a_n} \\right|$$ "
        "1. If $L < 1$, the series converges absolutely. "
        "2. If $L > 1$ (or $L = \\infty$), the series diverges. "
        "3. If $L = 1$, the test is inconclusive."
    ),
    "cauchy's residue theorem": (
        "A powerful integration theorem stating that if $f(z)$ is analytic in a simply connected domain $D$ except for a finite set of isolated singularities $z_1, z_2, \\dots, z_k$, "
        "then the contour integral along a positively oriented simple closed path $C$ enclosing the singularities is: "
        "$$\\oint_C f(z) \\, dz = 2\\pi i \\sum_{k=1}^n \\operatorname{Res}(f, z_k)$$ "
        "where $\\operatorname{Res}(f, z_k)$ is the residue of $f(z)$ at pole $z_k$ (the coefficient $b_1$ in its Laurent series expansion)."
    ),
    "cauchy's root test": (
        "A convergence test for an infinite series $\\sum_{n=1}^\\infty a_n$, by calculating: "
        "$$L = \\limsup_{n \\to \\infty} \\sqrt[n]{|a_n|}$$ "
        "1. If $L < 1$, the series converges absolutely. "
        "2. If $L > 1$, the series diverges. "
        "3. If $L = 1$, the test is inconclusive. "
        "For a power series $\\sum a_n (z - z_0)^n$, its radius of convergence is $R = \\frac{1}{L}$ (Cauchy-Hadamard theorem)."
    ),
    "cauchy-riemann equationscauchy-schwarz inequality": (
        "1. The Cauchy-Riemann equations are the necessary and sufficient conditions for a complex function $f(z) = u(x, y) + i v(x, y)$ to be complex differentiable (holomorphic): "
        "$$\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y} \\quad \\text{and} \\quad \\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$$ "
        "2. The Cauchy-Schwarz inequality for any vectors $x, y$ in an inner product space states: "
        "$$|\\langle x, y \\rangle|^2 \\le \\langle x, x \\rangle \\langle y, y \\rangle \\iff |\\langle x, y \\rangle| \\le \\|x\\| \\|y\\|$$"
    ),
    "cayley-hamilton theorem": (
        "A fundamental linear algebra theorem stating that every square $n \\times n$ matrix $A$ over a commutative ring satisfies its own characteristic polynomial: "
        "$$p(\\lambda) = \\det(\\lambda I - A) = \\lambda^n + c_{n-1} \\lambda^{n-1} + \\dots + c_1 \\lambda + c_0 = 0$$ "
        "Substituting matrix $A$ yields: "
        "$$p(A) = A^n + c_{n-1} A^{n-1} + \\dots + c_1 A + c_0 I = \\mathbf{0}$$ "
        "This allows higher powers of $A$ and matrix inverses $A^{-1}$ to be expressed as linear combinations of lower powers of $A$."
    ),
    "celsius temperature": (
        "A scale of temperature defined relative to the Kelvin thermodynamic temperature scale: "
        "$$\\theta(^\\circ\\text{C}) = T(\\text{K}) - 273.15$$ "
        "where $0^\\circ\\text{C}$ is defined as $273.15\\text{ K}$ (the freezing point of pure water at $1\\text{ atm}$) "
        "and $100^\\circ\\text{C}$ is $373.15\\text{ K}$ (the normal boiling point of water). A temperature difference of $1^\\circ\\text{C}$ equals $1\\text{ K}$."
    ),
    "central limit theorem": (
        "A foundational probability theorem stating that given a sequence of independent, identically distributed (i.i.d.) random variables $X_1, X_2, \\dots, X_n$ "
        "with finite mean $\\mu$ and finite variance $\\sigma^2$, the normalized sample mean converges in distribution to a standard normal distribution $\\mathcal{N}(0, 1)$ as $n \\to \\infty$: "
        "$$Z_n = \\frac{\\bar{X}_n - \\mu}{\\sigma / \\sqrt{n}} = \\frac{\\sum_{i=1}^n X_i - n\\mu}{\\sigma \\sqrt{n}} \\xrightarrow{d} \\mathcal{N}(0, 1)$$"
    ),
    "centre of mass": (
        "1. The unique position vector $\\vec{R}_{\\text{cm}}$ representing the weighted mean position of a discrete system of particles with masses $m_i$ and positions $\\vec{r}_i$: "
        "$$\\vec{R}_{\\text{cm}} = \\frac{\\sum_{i=1}^n m_i \\vec{r}_i}{\\sum_{i=1}^n m_i} = \\frac{1}{M} \\sum_{i=1}^n m_i \\vec{r}_i$$ "
        "2. For a continuous body with mass density $\\rho(\\vec{r})$ over volume $V$: "
        "$$\\vec{R}_{\\text{cm}} = \\frac{1}{M} \\int_V \\vec{r} \\, \\rho(\\vec{r}) \\, dV$$"
    ),
    "centripetal acceleration": (
        "The radial acceleration directed toward the center of curvature experienced by any body traveling in a circular path of radius $r$ at tangential speed $v$: "
        "$$a_c = \\frac{v^2}{r} = \\omega^2 r = \\frac{4\\pi^2 r}{T^2}$$ "
        "where $\\omega = \\frac{v}{r}$ is angular speed and $T$ is the period of revolution."
    ),
    "centripetal force": (
        "The net inward radial force required to keep a body of mass $m$ moving in a circular path of radius $r$ at speed $v$: "
        "$$F_c = m a_c = \\frac{m v^2}{r} = m \\omega^2 r$$ "
        "Centripetal force is not an independent physical force, but rather the net resultant of real forces (such as tension, gravity, or friction) directed toward the center."
    ),
    "ceva's theorem": (
        "A theorem in Euclidean plane geometry concerning concurrent lines in a triangle. "
        "In $\\triangle ABC$, if points $D, E, F$ lie on sides $BC, CA, AB$ respectively, the lines $AD, BE, CF$ are concurrent at a common point if and only if: "
        "$$\\frac{AF}{FB} \\cdot \\frac{BD}{DC} \\cdot \\frac{CE}{EA} = 1$$"
    ),
    "chain rule": (
        "A fundamental formula for computing the derivative of the composite of two or more differentiable functions. "
        "If $y = f(u)$ and $u = g(x)$, then: "
        "$$\\frac{dy}{dx} = \\frac{dy}{du} \\cdot \\frac{du}{dx} = f'(g(x)) \\cdot g'(x)$$ "
        "For multivariable functions where $z = f(u, v)$ with $u = u(x, y)$ and $v = v(x, y)$: "
        "$$\\frac{\\partial z}{\\partial x} = \\frac{\\partial z}{\\partial u} \\frac{\\partial u}{\\partial x} + \\frac{\\partial z}{\\partial v} \\frac{\\partial v}{\\partial x}$$"
    ),
    "characteristic equation": (
        "For an $n \\times n$ square matrix $A$, the algebraic polynomial equation obtained by setting the characteristic polynomial equal to zero: "
        "$$\\det(A - \\lambda I) = 0$$ "
        "The roots $\\lambda_1, \\lambda_2, \\dots, \\lambda_n$ of this equation are the eigenvalues (characteristic values) of the matrix."
    ),
    "charles' law": (
        "An experimental gas law discovered by Jacques Charles (1787), stating that for a fixed mass of an ideal gas at constant pressure, "
        "volume $V$ is directly proportional to absolute temperature $T$: "
        "$$V \\propto T \\iff \\frac{V}{T} = \\text{constant} \\iff \\frac{V_1}{T_1} = \\frac{V_2}{T_2}$$ "
        "Extrapolating the linear volume-temperature isobar to zero volume identifies absolute zero at $-273.15^\\circ\\text{C}$."
    ),
    "chebyshev polynomials of the first kind": (
        "A family of orthogonal polynomials $T_n(x)$ on the interval $[-1, 1]$, defined by: "
        "$$T_n(x) = \\cos(n \\arccos x)$$ "
        "Satisfying the recurrence relation: "
        "$$T_{n+1}(x) = 2x T_n(x) - T_{n-1}(x) \\quad (T_0(x) = 1, T_1(x) = x)$$ "
        "The first several polynomials are $T_0 = 1$, $T_1 = x$, $T_2 = 2x^2 - 1$, $T_3 = 4x^3 - 3x$, and $T_4 = 8x^4 - 8x^2 + 1$."
    ),
    "chebyshev's inequality": (
        "A fundamental probabilistic bound stating that for any random variable $X$ with finite mean $\\mu$ and finite standard deviation $\\sigma$, "
        "the probability of deviation by $k$ or more standard deviations is bounded by: "
        "$$P(|X - \\mu| \\ge k\\sigma) \\le \\frac{1}{k^2} \\quad (k > 0)$$ "
        "Equivalently, at least $1 - \\frac{1}{k^2}$ of the distribution's values fall within $k$ standard deviations of the mean."
    ),
    "chemical potential": (
        "The partial molar Gibbs free energy of a thermodynamic component, measuring how total Gibbs free energy changes with the quantity of substance: "
        "$$\\mu_i = \\left(\\frac{\\partial G}{\\partial n_i}\\right)_{T, P, n_{j \\neq i}}$$ "
        "For chemical equilibrium or phase equilibrium across a multi-component system, the chemical potential of each species must be equal in all phases: "
        "$$\\mu_i^{(\\alpha)} = \\mu_i^{(\\beta)}$$"
    ),
    "chinese remainder theorem": (
        "A foundational result in number theory stating that if $m_1, m_2, \\dots, m_k$ are pairwise coprime positive integers, "
        "then for any given integers $a_1, a_2, \\dots, a_k$, the system of simultaneous congruences: "
        "$$x \\equiv a_1 \\pmod{m_1}, \\quad x \\equiv a_2 \\pmod{m_2}, \\quad \\dots, \\quad x \\equiv a_k \\pmod{m_k}$$ "
        "has a unique integer solution modulo the product $M = m_1 m_2 \\cdots m_k$."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    c_entries = data.get('C', [])
    word_map = {item.get('word', '').strip().lower(): item for item in c_entries}

    for target_word, new_def in BATCH_C1_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section C: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_C1_DEFINITIONS)} definitions in Section C.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
