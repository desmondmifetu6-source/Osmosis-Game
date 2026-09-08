"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION A (BATCH 1)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section A
terms using KaTeX LaTeX typesetting as specified in the Desmond Manual
Engineering Guide.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Add scripts directory to path for clean_and_enrich_formulas module
sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_A1_DEFINITIONS = {
    "abbe numb er": (
        "The reciprocal of the dispersive power of a substance, which is a measure of light dispersion in an optical medium. "
        "It is used to classify optically transparent materials. It is given by a function of the refractive index of a material "
        "at the Fraunhofer spectral lines $f$ (486.1 nm), $d$ (587.6 nm) and $c$ (656.3 nm) wavelengths. Its symbol is $V$ and expressed as: "
        "$$V = \\frac{n_d - 1}{n_f - n_c}$$ "
        "where $n_d$, $n_f$ and $n_c$ are the refractive indices for the Fraunhofer spectral lines $d$ (587.6 nm), $f$ (486.1 nm) and $c$ (656.3 nm). "
        "A material with a high Abbe number produces less chromatic aberration than one with a low number. "
        "Abbe numbers range from around 20 for very dense flint glass, around 30 for polycarbonate plastics, and up to 58 for crown glass."
    ),
    "abc conjecture": (
        "A conjecture in number theory stated in terms of three positive integers, $a, b$ and $c$, which have no common factor and satisfy: "
        "$$a + b = c$$ "
        "If $d$ denotes the product of the distinct prime factors of $abc$, the conjecture essentially states that $d$ cannot be much smaller than $c$. "
        "It was proposed in 1985 by Joseph Oesterlé of the University of Paris and David Masser of the University of Basel. "
        "It is considered one of the most important unsolved problems in number theory."
    ),
    "abel test": (
        "An infinite series test used in testing its convergence. The test states that if $\\sum a_n$ is a convergent series "
        "and $\{b_n\}$ is a sequence of real numbers that is monotonic and bounded (i.e. $b_{n+1} \\le b_n$ for all $n$), "
        "then the series: "
        "$$\\sum_{n=1}^{\\infty} a_n b_n$$ "
        "is also convergent."
    ),
    "abel test for uniform convergence": (
        "A uniform convergence test for infinite series of functions, stating that if $\{a_n(z)\}$ is a sequence of real-valued functions "
        "that is uniformly bounded and monotonic for every $z$ in a compact set $K$, and $\\sum b_n(z)$ converges uniformly on $K$, "
        "then the series: "
        "$$\\sum_{n=1}^{\\infty} a_n(z) b_n(z)$$"
        "is uniformly convergent on $K$."
    ),
    "abel's partial summation formula": (
        "The formula of summability theory that for two arbitrary sequences $\{a_n\}$ and $\{b_n\}$, with $A_n = \\sum_{k=1}^n a_k$: "
        "$$\\sum_{k=m}^{n} a_k b_k = A_n b_{n+1} - A_{m-1} b_m + \\sum_{k=m}^{n} A_k (b_k - b_{k+1})$$"
    ),
    "abelian group": (
        "A group in which the binary operation is commutative, that is, the result of applying the group operation to two group elements "
        "does not depend on their order. Named after Norwegian mathematician Niels Henrik Abel (1802–1829). "
        "Therefore, for all elements $a$ and $b$ in the group: "
        "$$a \\cdot b = b \\cdot a \\quad \\text{or} \\quad a + b = b + a$$ "
        "Abelian groups generalise the arithmetic of addition of integers."
    ),
    "abelian theorem": (
        "A theorem stating that the convergence of a series or integral implies summability with respect to some summability method. "
        "Named after Norwegian mathematician Niels Henrik Abel (1802–1829). Abel's theorem states that if a power series in $z$ converges "
        "to $f(z)$ for $|z| < 1$ and to $a$ for $z = 1$, then $\\lim_{z \\to 1^-} f(z) = a$. "
        "In other words, if a power series converges for $z = a$, it converges absolutely for $|z| < |a|$. "
        "It also states that if three series with $n$-th terms $a_n$, $b_n$ and: "
        "$$c_n = a_0 b_n + a_1 b_{n-1} + \\dots + a_n b_0$$ "
        "respectively converge, then the third series equals the product of the first two series."
    ),
    "absolute": (
        "1. Denoting a number or measurement that does not depend on a standard reference value, or relating to a scale that has absolute zero "
        "as its lowest temperature, which is $0\\text{ K}$, equivalent to $-273.15^\\circ\\text{C}$. It is the point at which all molecular motion ceases. "
        "2. In mathematics, the absolute value or numerical value denotes the distance of a number from zero without regard to its sign: "
        "$$|x| = \\begin{cases} x & \\text{if } x \\ge 0 \\\\ -x & \\text{if } x < 0 \\end{cases}$$ "
        "For example, $|-3| = |3| = 3$. "
        "3. True for all values of a variable in an algebraic expression (e.g. an absolute inequality). "
        "4. Relating to or using basic units of length, time, mass, and charge."
    ),
    "absolute alcohol": (
        "A volatile, flammable, colourless chemical compound with molecular formula $\\text{C}_2\\text{H}_6\\text{O}$ (or $\\text{C}_2\\text{H}_5\\text{OH}$), "
        "density $0.789\\text{ g/cm}^3$ (at $25^\\circ\\text{C}$), molar mass $46.07\\text{ g/mol}$, melting point $-114^\\circ\\text{C}$ ($159\\text{ K}$) "
        "and boiling point $78.3^\\circ\\text{C}$ ($351.5\\text{ K}$), containing not more than 1% water. Used in chemical synthesis and alcoholic beverages."
    ),
    "absolute continuity": (
        "1. For a real-valued function $f(x)$ on an interval $[a,b]$, the property that for every $\\varepsilon > 0$, there exists $\\delta > 0$ "
        "such that for any finite collection of disjoint sub-intervals $(a_j, b_j) \\subset [a,b]$, if: "
        "$$\\sum_{j} (b_j - a_j) < \\delta \\implies \\sum_{j} |f(b_j) - f(a_j)| < \\varepsilon$$ "
        "2. For two measures $\\mu$ and $\\nu$, absolute continuity of $\\mu$ with respect to $\\nu$ (written $\\mu \\ll \\nu$) means that whenever "
        "$E$ is a $\\nu$-measurable set with $\\nu(E) = 0$, then $\\mu(E) = 0$."
    ),
    "absolute convergence": (
        "A series $\\sum_{n=1}^{\\infty} a_n$ is said to converge absolutely (or be absolutely convergent) if the series of absolute values: "
        "$$\\sum_{n=1}^{\\infty} |a_n| < \\infty$$ "
        "converges. If a series is absolutely convergent, then the sum is independent of the order in which terms are rearranged. "
        "By the ratio test, a series converges absolutely if: "
        "$$\\lim_{n \\to \\infty} \\left| \\frac{a_{n+1}}{a_n} \\right| < 1$$ "
        "and diverges if the limit is greater than 1. For an improper integral, $\\int_{a}^{\\infty} f(x)dx$ converges absolutely if $\\int_{a}^{\\infty} |f(x)|dx < \\infty$."
    ),
    "absolute entropy": (
        "The increase in the entropy of a substance as it moves from a perfectly ordered crystalline form at $0\\text{ K}$ ($-273.15^\\circ\\text{C}$), "
        "where by the Third Law of Thermodynamics its entropy is zero, to the temperature in question: "
        "$$S = \\int_0^T \\frac{C_p}{T} dT$$ "
        "Entropy is a measure of molecular randomness. For example, at $20^\\circ\\text{C}$ ($293\\text{ K}$), liquid water has an absolute entropy of "
        "$70\\text{ J mol}^{-1}\\text{K}^{-1}$ and water vapour has an absolute entropy of $189\\text{ J mol}^{-1}\\text{K}^{-1}$."
    ),
    "absolute temperature": (
        "The temperature measured on a thermodynamic scale where zero represents absolute zero ($-273.15^\\circ\\text{C}$), independent of the properties "
        "of any particular thermometric substance. In SI units, absolute temperature is measured in Kelvins ($\\text{K}$), related to Celsius ($^\\circ\\text{C}$) by: "
        "$$T(\\text{K}) = \\theta(^\\circ\\text{C}) + 273.15$$"
    ),
    "absolute value": (
        "1. Also known as numerical value or modulus, the magnitude of a real number without regard to its sign: "
        "$$|x| = \\begin{cases} x & \\text{if } x \\ge 0 \\\\ -x & \\text{if } x < 0 \\end{cases}$$ "
        "For example, $|-3| = |3| = 3$. "
        "2. For a complex number $z = x + iy$, its absolute value (modulus) is the Euclidean distance from the origin in the complex plane: "
        "$$|z| = \\sqrt{x^2 + y^2}$$"
    ),
    "absolute value function": (
        "A mathematical function that maps a real number to its non-negative magnitude, defined by: "
        "$$f(x) = |x| = \\begin{cases} x & \\text{if } x \\ge 0 \\\\ -x & \\text{if } x < 0 \\end{cases}$$ "
        "Its graph forms a V-shape with its vertex at the origin $(0,0)$."
    ),
    "absolute zero": (
        "The lowest temperature theoretically possible, at which entropy reaches its minimum and molecular kinetic energy ceases. "
        "It corresponds to $0\\text{ K}$ on the Kelvin thermodynamic scale, precisely $-273.15^\\circ\\text{C}$ ($-459.67^\\circ\\text{F}$). "
        "By the Third Law of Thermodynamics, absolute zero cannot be attained in a finite number of steps, though temperatures within nanokelvins "
        "($1\\text{ nK} = 10^{-9}\\text{ K}$) have been reached in laboratory optical lattices."
    ),
    "absorbance": (
        "In optics and spectroscopy, a logarithmic measure of the capacity of a substance to absorb radiant energy at a specific wavelength $\\lambda$. "
        "It is defined by the Beer-Lambert relation: "
        "$$A_\\lambda = -\\log_{10}\\left(\\frac{I}{I_0}\\right) = \\log_{10}\\left(\\frac{I_0}{I}\\right)$$ "
        "where $I_0$ is the intensity of the incident radiation and $I$ is the intensity of the transmitted radiation."
    ),
    "absorbing state": (
        "A state in a Markov chain from which the probability of transition to any other state is zero. "
        "Mathematically, state $i$ is an absorbing state if its transition probability satisfies: "
        "$$P_{ii} = 1 \\quad \\text{and} \\quad P_{ij} = 0 \\quad \\text{for all } j \\neq i$$"
    ),
    "absorptance": (
        "A measure of the ability of a body to absorb radiant energy, denoted by $\\alpha$. It is defined as the ratio of radiant or luminous flux "
        "absorbed by the body ($\\Phi_{\\text{abs}}$) to the incident flux ($\\Phi_{\\text{inc}}$): "
        "$$\\alpha = \\frac{\\Phi_{\\text{abs}}}{\\Phi_{\\text{inc}}}$$ "
        "For a black body, $\\alpha = 1$."
    ),
    "absorption coefficient": (
        "1. In spectroscopy, a parameter quantifying how strongly a chemical species attenuates light at a given wavelength, defined by the Beer-Lambert law: "
        "$$I = I_0 e^{-\\alpha x} \\quad \\text{or} \\quad A = \\varepsilon c l$$ "
        "where $\\varepsilon$ is the molar absorption coefficient (with dimensions $\\text{L mol}^{-1}\\text{cm}^{-1}$), $c$ is molar concentration, and $l$ is optical path length. "
        "2. In acoustics, the fraction of sound energy absorbed by a surface relative to total incident energy."
    ),
    "absorption law": (
        "Fundamental algebraic identities in Boolean algebra and lattice theory stating that for any elements $A$ and $B$: "
        "$$A \\cap (A \\cup B) = A$$ "
        "$$A \\cup (A \\cap B) = A$$ "
        "These identities state that a smaller set absorbs a larger set containing it under dual operations."
    ),
    "absorptive power": (
        "The measure of light attenuation through a solution of absorbing solute, governed by the Beer-Lambert Law: "
        "$$A = \\varepsilon b c$$ "
        "where $A = \\log_{10}(P_0 / P)$ is absorbance, $\\varepsilon$ is the molar absorptivity (in $\\text{L mol}^{-1}\\text{cm}^{-1}$), "
        "$b$ is the path length of the cuvette (in $\\text{cm}$), and $c$ is the concentration (in $\\text{mol L}^{-1}$)."
    ),
    "acceleration": (
        "The rate of change of velocity of an object with respect to time. It is a vector quantity with SI unit $\\text{m/s}^2$ (or $\\text{ms}^{-2}$). "
        "Average acceleration over a time interval $\\Delta t$ is given by: "
        "$$a_{\\text{avg}} = \\frac{v - v_0}{\\Delta t} = \\frac{\\Delta v}{\\Delta t}$$ "
        "Instantaneous acceleration is the limit of average acceleration as the time interval approaches zero, given by the derivative of velocity: "
        "$$a = \\lim_{\\Delta t \\to 0} \\frac{\\Delta v}{\\Delta t} = \\frac{dv}{dt} = \\frac{d^2s}{dt^2}$$ "
        "Graphically, acceleration represents the gradient (slope) of a velocity-time graph."
    ),
    "acceleration due to gravity": (
        "The acceleration experienced by a body falling freely in a gravitational field in the absence of air resistance, denoted by $g$. "
        "Near the Earth's surface, $g \\approx 9.81\\text{ ms}^{-2}$. From kinematic equations for free fall from rest: "
        "$$s = \\frac{1}{2}gt^2$$ "
        "When plotting distance $s$ against $t^2$, the resulting graph is a straight line through the origin with slope $m = \\frac{1}{2}g$. "
        "Therefore, the acceleration due to gravity is equal to twice the slope: "
        "$$g = 2m$$"
    ),
    "acid dissociation constant": (
        "A quantitative measure of the strength of an acid in solution, denoted by $K_a$. "
        "For the dissociation equilibrium of a generic weak acid $\\text{HA}$ in aqueous solution: "
        "$$\\text{HA} \\rightleftharpoons \\text{A}^- + \\text{H}^+ \\quad (\\text{or } \\text{HA} + \\text{H}_2\\text{O} \\rightleftharpoons \\text{A}^- + \\text{H}_3\\text{O}^+)$$ "
        "The acid dissociation constant is defined as: "
        "$$K_a = \\frac{[\\text{H}^+][\\text{A}^-]}{[\\text{HA}]}$$ "
        "The logarithmic constant is given by $\\text{p}K_a = -\\log_{10} K_a$, where lower $\\text{p}K_a$ values indicate a stronger acid."
    ),
    "acoustic impedance": (
        "The ratio of acoustic sound pressure $p$ on a surface to the volume acoustic flux $U$ through that surface, denoted by $Z$. "
        "For a plane acoustic wave propagating through a medium of density $\\rho$ at acoustic velocity $c$: "
        "$$Z = \\rho c$$ "
        "Its SI unit is the acoustic ohm (or $\\text{Pa}\\cdot\\text{s/m}^3$), or specific acoustic impedance in rayls ($\\text{kg}\\cdot\\text{m}^{-2}\\text{s}^{-1}$)."
    ),
    "action": (
        "1. In physics, a numerical value describing how a physical system has changed over time, defined as the integral of the Lagrangian $L = T - V$ "
        "(kinetic energy minus potential energy) over time along the system's path between times $t_1$ and $t_2$: "
        "$$S = \\int_{t_1}^{t_2} L(q, \\dot{q}, t) \\, dt$$ "
        "By Hamilton's Principle of Least Action, the path actually taken by the system makes this action stationary ($\\delta S = 0$). "
        "The SI unit of action is joule-second ($\\text{J}\\cdot\\text{s}$). "
        "2. In mathematics, a group action of a group $G$ on a set $S$ is a homomorphism from $G$ to the symmetric group of permutations of $S$."
    ),
    "activity": (
        "1. In nuclear physics, the rate of nuclear disintegrations occurring in a radioactive sample, denoted by $A$: "
        "$$A = -\\frac{dN}{dt} = \\lambda N$$ "
        "where $N$ is the number of radioactive nuclei and $\\lambda$ is the decay constant. The SI unit of activity is the becquerel ($\\text{Bq}$), "
        "where $1\\text{ Bq} = 1\\text{ decay/second}$. "
        "2. In chemical thermodynamics, the effective concentration of a species under non-ideal conditions, denoted by $a = \\gamma c$, "
        "where $\\gamma$ is the activity coefficient."
    ),
    "addition formula": (
        "1. In trigonometry, fundamental identities expressing trigonometric functions of the sum or difference of two angles: "
        "$$\\sin(A + B) = \\sin A \\cos B + \\cos A \\sin B$$ "
        "$$\\sin(A - B) = \\sin A \\cos B - \\cos A \\sin B$$ "
        "$$\\cos(A + B) = \\cos A \\cos B - \\sin A \\sin B$$ "
        "$$\\cos(A - B) = \\cos A \\cos B + \\sin A \\sin B$$ "
        "$$\\tan(A + B) = \\frac{\\tan A + \\tan B}{1 - \\tan A \\tan B}$$ "
        "$$\\tan(A - B) = \\frac{\\tan A - \\tan B}{1 + \\tan A \\tan B}$$ "
        "2. In calculus and functional analysis, any relation giving $f(x + y)$ in terms of $f(x)$ and $f(y)$."
    ),
    "addition law of probability": (
        "A fundamental probability theorem stating that for any two events $A$ and $B$, the probability of their union is: "
        "$$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$$ "
        "If $A$ and $B$ are mutually exclusive (disjoint) events, $P(A \\cap B) = 0$, simplifying to: "
        "$$P(A \\cup B) = P(A) + P(B)$$"
    ),
    "addition of fractions": (
        "Fractions can only be combined by addition when converted to a common denominator: "
        "$$\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}$$ "
        "For example, finding the lowest common denominator for fractions with denominators 2, 3 and 15 (which is 30): "
        "$$\\frac{1}{2} + \\frac{1}{3} + \\frac{1}{15} = \\frac{15}{30} + \\frac{10}{30} + \\frac{2}{30} = \\frac{15 + 10 + 2}{30} = \\frac{27}{30} = \\frac{9}{10}$$"
    ),
    "addition of matrices": (
        "Two matrices $A$ and $B$ can be added if and only if they have identical dimensions (same number of rows and columns). "
        "Addition is performed component-wise: "
        "$$\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} + \\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} = \\begin{pmatrix} a+e & b+f \\\\ c+g & d+h \\end{pmatrix}$$ "
        "Matrix addition is commutative ($A + B = B + A$) and associative ($(A + B) + C = A + (B + C)$)."
    ),
    "addition of vectors": (
        "The operation of combining two or more vectors into a single resultant vector. "
        "By the triangle rule (head-to-tail method), placing the tail of vector $\\vec{b}$ at the head of vector $\\vec{a}$ gives the resultant: "
        "$$\\vec{AC} = \\vec{AB} + \\vec{BC}$$ "
        "In Cartesian coordinate components, vector addition is performed component-wise: "
        "$$\\vec{a} + \\vec{b} = (a_x + b_x)\\hat{i} + (a_y + b_y)\\hat{j} + (a_z + b_z)\\hat{k}$$ "
        "Vector addition is both commutative ($\\vec{a} + \\vec{b} = \\vec{b} + \\vec{a}$) and associative."
    ),
    "additive function": (
        "A mathematical function preserving the addition operation: "
        "$$f(x + y) = f(x) + f(y)$$ "
        "For example, $f(x) = cx$ is additive since $c(x + y) = cx + cy$. "
        "In contrast, non-linear functions such as $g(x) = \\sqrt{x}$ or $h(x) = x^2$ are not additive since $\\sqrt{x + y} \\neq \\sqrt{x} + \\sqrt{y}$."
    ),
    "additive identity": (
        "An identity element under addition. For any number or algebraic structure under addition, the element $0$ satisfies: "
        "$$x + 0 = 0 + x = x$$ "
        "for all elements $x$."
    ),
    "additive inverse": (
        "The element that yields the additive identity ($0$) when added to a given element $x$: "
        "$$x + (-x) = 0$$ "
        "The additive inverse of $x$ is denoted $-x$ (the negative or opposite of $x$)."
    ),
    "adiabatic": (
        "A thermodynamic process that occurs without heat transfer between a system and its surroundings ($Q = 0$). "
        "By the First Law of Thermodynamics ($\\Delta U = Q - W$), the change in internal energy equals the work done on the system: "
        "$$\\Delta U = -W$$ "
        "For an ideal gas undergoing a reversible adiabatic process: "
        "$$PV^\\gamma = \\text{constant} \\quad \\text{and} \\quad TV^{\\gamma - 1} = \\text{constant}$$ "
        "where $\\gamma = C_p / C_v$ is the heat capacity ratio (adiabatic index)."
    ),
    "adjoint": (
        "1. For an $n \\times n$ square matrix $A$, the classical adjoint (also called the adjugate matrix, $\\operatorname{adj}(A)$) "
        "is the transpose of its cofactor matrix $C$: "
        "$$\\operatorname{adj}(A) = C^T$$ "
        "For a $2 \\times 2$ matrix $A = \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$, its adjugate is: "
        "$$\\operatorname{adj}(A) = \\begin{pmatrix} d & -b \\\\ -c & a \\end{pmatrix}$$ "
        "and satisfies $A \\cdot \\operatorname{adj}(A) = \\det(A) I$. "
        "2. In functional analysis, the Hermitian adjoint $A^*$ of an operator $A$ on a Hilbert space satisfies $\\langle Ax, y \\rangle = \\langle x, A^*y \\rangle$."
    ),
    "airy function": (
        "The special functions $\\text{Ai}(x)$ and $\\text{Bi}(x)$, which are linearly independent solutions to the second-order Airy differential equation: "
        "$$\\frac{d^2y}{dx^2} - xy = 0$$ "
        "The Airy function of the first kind is defined by the improper integral: "
        "$$\\text{Ai}(x) = \\frac{1}{\\pi} \\int_0^{\\infty} \\cos\\left(\\frac{t^3}{3} + xt\\right) dt$$ "
        "Airy functions frequently appear in wave physics, optics (caustics and rainbow diffraction), and quantum mechanics (WKB approximation turning points)."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    a_entries = data.get('A', [])

    # Map words for fast lookup
    word_map = {item.get('word', '').strip().lower(): item for item in a_entries}

    for target_word, new_def in BATCH_A1_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section A: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_A1_DEFINITIONS)} definitions in Section A.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
