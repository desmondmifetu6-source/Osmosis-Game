"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION D (BATCH 2)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section D
Items 71-139: differential equation through dulong and petit's law
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_D2_DEFINITIONS = {
    "differential equation": (
        "A mathematical equation for an unknown function of one or several variables that relates the values of "
        "the function itself and its derivatives of various orders. For example, given $y = x^2 + 2x^{-3}$, then "
        "$$\\frac{dy}{dx} = 2x + 2$$ "
        "The order is the order of its highest derivative; the degree is the highest power of that derivative. "
        "Differential equations play an essential role in engineering, physics, economics and other disciplines."
    ),
    "differentiation": (
        "1. A mathematical process of obtaining the gradient of the tangent to a curve $f(x)$ at any point $x$. "
        "Key formulae: (i) algebraic: $\\frac{d}{dx}(x^n) = nx^{n-1}$; "
        "(ii) trigonometric: $\\frac{d}{dx}(\\sin x) = \\cos x$; "
        "(iii) exponential: $\\frac{d}{dx}(e^x) = e^x$. "
        "Rules: sum $D(af+bg) = aDf+bDg$, product $D(fg)=fDg+gDf$, "
        "quotient $D(f/g)=(gDf-fDg)/g^2$, chain rule $D(f(g(x))) = Df(g(x))\\cdot Dg(x)$. "
        "2. In biology, the process by which cells become increasingly specialised, giving rise to complex structures."
    ),
    "diffusion equation": (
        "The partial differential equation $$\\nabla^2 u = c^2 \\frac{\\partial u}{\\partial t}$$ "
        "where $\\nabla^2$ is the Laplacian in one, two or three dimensions. Generally solved using Fourier series. "
        "The solution describes the distribution of temperature in a region as a function of space and time."
    ),
    "digamma function": (
        "The logarithmic derivative of the gamma function, denoted $\\psi(z)$ and defined as "
        "$$\\psi(z) = \\frac{\\Gamma'(z)}{\\Gamma(z)}$$"
    ),
    "dihydric": (
        "Describing alcohols containing two hydroxyl groups ($\\text{-OH}$). "
        "The simplest and most important dihydric alcohol is ethylene glycol. "
        "Dihydric alcohols are dihydroxy derivatives of alkanes with the general formula $C_nH_{2n+2}O_2$. "
        "Compare monohydric (one $\\text{-OH}$ group, e.g. ethanol $\\text{CH}_3\\text{CH}_2\\text{OH}$) and "
        "trihydric (three $\\text{-OH}$ groups, e.g. glycerol $\\text{CH}_2\\text{OH-CHOH-CH}_2\\text{OH}$)."
    ),
    "dilogarithm": (
        "In the theory of polylogarithms, the function $$\\text{Li}_n(z) = \\sum_{k=1}^{\\infty} \\frac{z^k}{k^n}$$ "
        "defined for integer $n \\geq 2$ and $z$ in the unit disk; $\\text{Li}_2(z)$ is the dilogarithm and "
        "$\\text{Li}_3(z)$ the trilogarithm."
    ),
    "dimension ofa matrix": (
        "The number of rows and the number of columns of a matrix. "
        "A matrix with 3 rows and 2 columns has dimension $3 \\times 2$."
    ),
    "dimensional analysis": (
        "A method of checking the validity of an equation by analysing its dimensions. "
        "Every physical quantity is some combination of mass ($M$), length ($L$), time ($T$), "
        "electric charge ($Q$) and temperature ($\\Theta$). "
        "For example, speed has dimension $LT^{-1}$. "
        "Dimensional analysis is routinely used to check derived equations and establish the form of empirical relationships."
    ),
    "dimensionality": (
        "The combination of basic dimensions associated with a physically significant quantity. "
        "Momentum has dimensions $MLT^{-1}$ and energy has dimensions $ML^2T^{-2}$. "
        "Equations describing physical quantities can be checked by ensuring they have the correct dimensions. "
        "Dimensionless quantities are significant as they are entirely independent of the conventions "
        "used to define mass, length and time."
    ),
    "dimethylformamide": (
        "A colourless organic liquid with chemical formula $(\\text{CH}_3)_2\\text{NC(O)H}$, "
        "relative density 0.944, melting point $-61\\,^\\circ\\text{C}$ (212 K) and boiling point "
        "$153\\,^\\circ\\text{C}$ (426 K). Widely used as a polar aprotic solvent for organic reactions "
        "and is miscible with water and most organic liquids."
    ),
    "dinitrogen oxide": (
        "A colourless gas with chemical formula $\\text{N}_2\\text{O}$, density $1.97\\,\\text{g dm}^{-3}$, "
        "melting point $-90.8\\,^\\circ\\text{C}$ (182 K) and boiling point $-88.5\\,^\\circ\\text{C}$ (184 K). "
        "Prepared by controlled heating of ammonium nitrate to 250 °C (523 K). "
        "Decomposes above 520 °C (793 K) to nitrogen and oxygen. Used as an anaesthetic gas and aerosol propellant."
    ),
    "diol": (
        "An organic compound containing two hydroxyl ($\\text{-OH}$) groups. "
        "Example: ethane-1,2-diol (ethylene glycol), formula $\\text{C}_2\\text{H}_6\\text{O}_2$, "
        "widely used as a solvent and antifreeze. Vicinal diols have $\\text{-OH}$ groups on adjacent atoms, "
        "e.g. 1,2-ethanediol $\\text{HO-(CH}_2)_2\\text{-OH}$; gem diols bear both groups on the same carbon "
        "and are very unstable."
    ),
    "diophantine equation": (
        "An indeterminate polynomial equation to be solved in integers only. "
        "Linear diophantine equations take the form $$a_1x_1 + a_2x_2 + \\cdots + a_nx_n = c$$ "
        "where $c, a_1, \\ldots, a_n$ are integers and integer solutions are sought for $x_1, \\ldots, x_n$. "
        "An exponential example is the Ramanujan-Nagell equation: $$2^n - 7 = x^2$$"
    ),
    "dioxane": (
        "A colourless, toxic heterocyclic organic compound with a six-membered ring containing four "
        "$\\text{CH}_2$ groups and two oxygen atoms at opposite corners. Chemical formula $\\text{C}_4\\text{H}_8\\text{O}_2$, "
        "density $1.033\\,\\text{g/cm}^3$, melting point $11.8\\,^\\circ\\text{C}$ (285.95 K) and boiling point "
        "$101.1\\,^\\circ\\text{C}$ (374.25 K). Used as a solvent and stabiliser for trichloroethane."
    ),
    "dioxin": (
        "A family of highly toxic chlorinated aromatic hydrocarbons whose basic structure consists of two benzene "
        "rings connected by a pair of oxygen atoms. The most widely studied is 2,3,7,8-tetrachlorodibenzo-$p$-dioxin "
        "(2,3,7,8-TCDD), which is extremely stable chemically. Considered human carcinogens; formed as by-products "
        "of industrial incineration and other processes."
    ),
    "diphosphane": (
        "A yellow liquid with chemical formula $\\text{P}_2\\text{H}_4$, melting point $-99\\,^\\circ\\text{C}$ (174 K) "
        "and boiling point $52\\,^\\circ\\text{C}$ (325 K), spontaneously flammable in air. "
        "Obtained by hydrolysis of calcium phosphide. Many apparent examples of spontaneous flammability of "
        "phosphine ($\\text{PH}_3$) are due to trace impurities of $\\text{P}_2\\text{H}_4$."
    ),
    "dirac constant": (
        "A constant with symbol $\\hbar$, used in quantum mechanics, equal to Planck's constant divided by $2\\pi$: "
        "$$\\hbar = \\frac{h}{2\\pi} \\approx 1.0546 \\times 10^{-34}\\,\\text{J s}$$ "
        "The energy of a photon with angular frequency $\\omega = 2\\pi\\nu$ is $E = \\hbar\\omega$."
    ),
    "dirac delta function": (
        "The function $\\delta(x)$, introduced by Paul Dirac, that is zero for all $x \\neq 0$ "
        "and satisfies $$\\int_{-\\infty}^{\\infty} \\delta(x)\\,dx = 1$$ "
        "Fundamental in signal processing, quantum mechanics and the theory of distributions."
    ),
    "dirac equation": (
        "A relativistic wave equation formulated by Paul Dirac in 1928, combining quantum mechanics with "
        "special relativity for spin-$\\tfrac{1}{2}$ particles such as electrons: "
        "$$i\\hbar\\,\\frac{\\partial\\phi}{\\partial t} = \\frac{\\hbar c}{i}"
        "\\left(\\alpha_1\\frac{\\partial\\phi}{\\partial x_1} + \\alpha_2\\frac{\\partial\\phi}{\\partial x_2} + "
        "\\alpha_3\\frac{\\partial\\phi}{\\partial x_3}\\right) + \\alpha_4 mc^2\\phi$$ "
        "where $\\hbar$ is the reduced Planck constant, $c$ the speed of light, $\\phi$ the wavefunction, "
        "$m$ the particle mass and $\\alpha_i$ are the Dirac matrices. It demands the existence of antiparticles."
    ),
    "direct product": (
        "An algebraic operation constructing a new group $G \\times H$ from two groups $G$ and $H$, "
        "with order $|G \\times H| = |G| \\cdot |H|$. "
        "The direct product of vector spaces of dimensions $m$ and $n$ is a vector space of dimension $m + n$."
    ),
    "direct sum": (
        "The decomposition of a vector space $V$ into subspaces such that every element has a unique representation "
        "as a finite sum of elements, one from each subspace. For subspaces $U$ and $W$ of $V$: "
        "$$V = U \\oplus W \\iff V = U + W \\text{ and } U \\cap W = \\{0\\}$$"
    ),
    "direct variation": (
        "A relationship in which one variable is proportional to another. If $x$ varies directly as $y$, "
        "then $x = ky$ where $k$ is a constant of proportionality."
    ),
    "directed set": (
        "A partially ordered set with a transitive and reflexive relation $\\geq$ such that for every pair of "
        "elements $a, b$ in the set, there exists a third element $c$ with $a \\geq c$ and $c \\geq b$."
    ),
    "direction field": (
        "A geometrical interpretation of a differential equation. For an equation of the form "
        "$p = \\dfrac{dy}{dx} = f(x, y)$, the lineal elements are the triples $(x, y, p)$, "
        "forming a field of slope indicators across the $xy$-plane."
    ),
    "directional derivative": (
        "The limit of divided differences of a function $f$ in a given direction $\\mathbf{h}$: "
        "$$f'(\\mathbf{x}, \\mathbf{h}) = \\lim_{t \\to 0} \\frac{f(\\mathbf{x}+t\\mathbf{h}) - f(\\mathbf{x})}{t}$$ "
        "for $\\mathbf{x}$ in $n$-space."
    ),
    "directrix": (
        "A fixed line used with a focus and eccentricity $e$ to define a conic section as the locus of points "
        "whose distance from the focus divided by distance from the directrix equals $e$. "
        "If $e = 1$: parabola; $e < 1$: ellipse; $e > 1$: hyperbola."
    ),
    "dirichlet series": (
        "Any series of the form $$\\sum_{n=1}^{\\infty} a_n n^{-s}$$ where $s$ is complex and $\\{a_n\\}$ is a "
        "complex sequence. Of great importance in number theory; the most important case is the Riemann zeta "
        "function $\\zeta(s) = \\sum_{n=1}^{\\infty} n^{-s}$."
    ),
    "dirichlet's kernel": (
        "The collection of functions in Fourier analysis defined as "
        "$$D_n(t) = \\frac{1}{2} + \\sum_{k=1}^{n}\\cos(kt) = \\frac{\\sin\\!\\left((n+\\tfrac{1}{2})t\\right)}{2\\sin(t/2)}$$ "
        "for $t$ not a multiple of $2\\pi$."
    ),
    "dirichlet's test": (
        "1. A convergence test: if $\\{a_n\\}$ has bounded partial sums and $\\{b_n\\}$ is strictly decreasing "
        "to zero, then $\\sum a_nb_n$ converges. The alternating series test is a special case. "
        "2. A uniform convergence test: if partial sums of $\\sum a_n(z)$ are uniformly bounded on compact $K$ "
        "and $\\{b_n(z)\\}$ converges uniformly to zero, then $\\sum a_n(z)b_n(z)$ converges uniformly in $K$."
    ),
    "dirichlet's theorem": (
        "In number theory: for any two positive coprime integers $a$ and $d$, there are infinitely many primes "
        "of the form $a + nd$ where $n \\geq 0$; equivalently, there are infinitely many primes congruent to "
        "$a \\pmod{d}$. Named after Johann Peter Gustav Lejeune Dirichlet (1805-1859)."
    ),
    "discrete fourier transform, dft": (
        "Converts a finite list of $N$ equally spaced samples $\\{x_n\\}$ into the list of coefficients of "
        "complex sinusoids: $$X_k = \\sum_{n=0}^{N-1} x_n\\,e^{-i2\\pi kn/N}$$ "
        "Widely used in digital signal processing for revealing periodicities and the relative strengths "
        "of periodic components in data."
    ),
    "discriminant": (
        "A quantity that determines the nature of the roots of a quadratic $ax^2 + bx + c = 0$. "
        "The discriminant is $\\Delta = b^2 - 4ac$. "
        "If $\\Delta > 0$: two distinct real roots; if $\\Delta = 0$: one repeated real root; "
        "if $\\Delta < 0$: two complex conjugate roots."
    ),
    "disintegration constant": (
        "The probability of radioactive decay of an atomic nucleus per unit time, denoted $\\lambda$. "
        "The decay law is $$N(t) = N_0\\,e^{-\\lambda t}$$ and the activity (rate of decay) is $A = \\lambda N$."
    ),
    "disintegration energy": (
        "The energy released in a nuclear or particle reaction (the Q-value): "
        "$$Q = (m_{\\text{reactants}} - m_{\\text{products}})c^2$$ "
        "Disjoint sets $A$ and $B$ satisfy $A \\cap B = \\emptyset$."
    ),
    "dissociation constant": (
        "An equilibrium constant measuring the tendency of a complex $A_xB_y$ to dissociate. "
        "For the reaction $A_xB_y \\rightleftharpoons xA + yB$: "
        "$$K_d = \\frac{[A]^x[B]^y}{[A_xB_y]}$$ "
        "It is the inverse of the association constant."
    ),
    "distance between two points": (
        "The distance between points $A(x_1, y_1)$ and $B(x_2, y_2)$ is defined as "
        "$$AB = \\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$$ "
        "For example, $A(3,4)$ and $B(6,8)$: $AB = \\sqrt{9+16} = \\sqrt{25} = 5$."
    ),
    "distance from a point toa line": (
        "The perpendicular distance from point $P(x_1, y_1)$ to the line $ax + by + c = 0$ is "
        "$$d = \\frac{|ax_1 + by_1 + c|}{\\sqrt{a^2 + b^2}}$$"
    ),
    "distributive law": (
        "An axiom stating that one operation distributes over another. "
        "For arithmetic multiplication over addition: $a(b + c) = ab + ac$. "
        "A fundamental axiom of ring theory and field theory."
    ),
    "distributive property": (
        "A trait allowing one operation to be distributed over another. "
        "Over addition: $a(b + c) = ab + ac$ (e.g. $2(5+3) = 10+6 = 16$). "
        "Over subtraction: $a(b - c) = ab - ac$ (e.g. $2(5-3) = 10-6 = 4$)."
    ),
    "disulfur dichloride": (
        "An orange-red liquid with chemical formula $\\text{S}_2\\text{Cl}_2$, density $1.688\\,\\text{g/cm}^3$, "
        "melting point $-80\\,^\\circ\\text{C}$ (193 K) and boiling point $137\\,^\\circ\\text{C}$ (410 K). "
        "Prepared by passing chlorine over molten sulfur. Vapour-phase molecules have Cl-S-S-Cl chains; "
        "can form higher chlorosulfanes $\\text{Cl-(S)}_n\\text{-Cl}$ ($n < 100$), used in vulcanisation."
    ),
    "divergence": (
        "1. The branching of a neuron's terminal axon to connect with many target cells. "
        "2. The simultaneous outward movement of both eyes. "
        "3. In vector calculus, the divergence of a vector field $\\mathbf{F}$ is the scalar: "
        "$$\\nabla \\cdot \\mathbf{F} = \\frac{\\partial F_x}{\\partial x} + \\frac{\\partial F_y}{\\partial y} + "
        "\\frac{\\partial F_z}{\\partial z}$$"
    ),
    "divergence theorem": (
        "States that the outward flux of a vector field through a closed surface equals the volume integral "
        "of the divergence over the enclosed region: "
        "$$\\iiint_V (\\nabla \\cdot \\mathbf{F})\\,dV = \\oiint_S (\\mathbf{F} \\cdot \\hat{n})\\,dS$$ "
        "Gauss' law of electric fields is a particular case. Widely used in electrostatics and fluid dynamics."
    ),
    "division algorithm": (
        "1. The theorem that for any integers $a$ and $b$ there exist unique integers $q$ and $r$ such that "
        "$$a = qb + r, \\quad 0 \\leq r < |b|$$ "
        "2. Any systematic process for computing the quotient of two numbers."
    ),
    "division of fractions property": (
        "Division by a fraction equals multiplication by its reciprocal: "
        "$$\\frac{a}{b} \\div \\frac{c}{d} = \\frac{a}{b} \\times \\frac{d}{c} = \\frac{ad}{bc}$$ "
        "For example, $\\frac{15}{3} \\div \\frac{3}{5} = \\frac{15}{3} \\times \\frac{5}{3} = 25$."
    ),
    "division ring": (
        "A ring in which every non-zero element $a$ has a multiplicative inverse $a^{-1}$ satisfying "
        "$aa^{-1} = e = a^{-1}a$, where $e$ is the identity element."
    ),
    "dodecene": (
        "A straight-chain alkene with molecular formula $\\text{CH}_3(\\text{CH}_2)_9\\text{CH=CH}_2$, "
        "molar mass $168.32\\,\\text{g mol}^{-1}$, density $0.758\\,\\text{g/cm}^3$, "
        "melting point $-35.2\\,^\\circ\\text{C}$ and boiling point $213.8\\,^\\circ\\text{C}$. "
        "Obtained from petroleum and used in making dodecylbenzene."
    ),
    "dominated convergence theorem": (
        "A theorem of Lebesgue integration: if $\\{f_n\\}$ is a sequence of integrable functions converging "
        "almost everywhere to $f$, and there exists an integrable $g$ such that $|f_n| \\leq g$ for all $n$, "
        "then $f$ is integrable and $$\\int f\\,d\\mu = \\lim_{n \\to \\infty}\\int f_n\\,d\\mu$$"
    ),
    "doppler effect": (
        "The apparent change in observed frequency or wavelength of waves due to relative motion between source "
        "and observer. For sound: $$f_o = f_s \\cdot \\frac{V \\pm V_o}{V \\mp V_s}$$ "
        "where $V$ is the speed of sound, $V_o$ and $V_s$ are the speeds of observer and source. "
        "For light (wavelength shift): $\\Delta\\lambda = \\frac{v}{c}\\lambda$. "
        "Named after Austrian physicist Christian Doppler (1842)."
    ),
    "dot product": (
        "For vectors $\\mathbf{U}$ and $\\mathbf{V}$, the dot product is defined algebraically as "
        "$\\mathbf{U} \\cdot \\mathbf{V} = U_1V_1 + U_2V_2 + U_3V_3$ "
        "or geometrically as $\\mathbf{U} \\cdot \\mathbf{V} = |\\mathbf{U}||\\mathbf{V}|\\cos\\theta$, "
        "where $\\theta$ is the angle between the vectors."
    ),
    "double angle formulae": (
        "Trigonometric identities expressing a function at twice an angle: "
        "$\\sin(2x) = 2\\sin x\\cos x$, "
        "$\\cos(2x) = \\cos^2x - \\sin^2x = 2\\cos^2x - 1 = 1 - 2\\sin^2x$, "
        "$\\tan(2x) = \\dfrac{2\\tan x}{1-\\tan^2x}$. "
        "Hyperbolic analogues: $\\sinh(2x) = 2\\sinh x\\cosh x$, "
        "$\\cosh(2x) = 2\\cosh^2x - 1$, $\\tanh(2x) = \\dfrac{2\\tanh x}{1-\\tanh^2x}$."
    ),
    "double beta decay": (
        "The simultaneous decay of two neutrons into two protons, emitting two beta particles and two antineutrinos: "
        "$$2n \\to 2p + 2e^- + 2\\bar{\\nu}_e$$ "
        "Elements undergoing this process include germanium-76, selenium-82 and uranium-238."
    ),
    "double bond": (
        "A chemical bond containing two shared pairs of electrons between adjacent atoms, as in "
        "alkenes ($\\text{-C=C-}$) and carbonyl groups ($\\text{-C=O}$). "
        "Double bonds are stronger and shorter than single bonds. Also found in azo ($\\text{N=N}$), "
        "imine ($\\text{C=N}$) and sulfoxide ($\\text{S=O}$) groups."
    ),
    "double decomposition": (
        "A reaction in which two compounds exchange partners (metathesis). Example: "
        "$$\\text{KCl} + \\text{AgNO}_3 \\to \\text{KNO}_3 + \\text{AgCl}$$ "
        "Alkene metathesis is catalysed by Schrock catalysts (Mo-based) and Grubbs catalysts (Ru-based); "
        "Schrock and Grubbs shared the 2005 Nobel Prize in Chemistry for this work."
    ),
    "double refraction": (
        "The property of certain anisotropic crystals (e.g. calcite) of splitting light into two refracted rays. "
        "The birefringence magnitude is $\\Delta n = n_e - n_o$, where $n_e$ and $n_o$ are the extraordinary "
        "and ordinary refractive indices, respectively."
    ),
    "doubly periodic function": (
        "A function $f(z)$ of a complex variable with two distinct complex periods $\\omega_1$ and $\\omega_2$ "
        "(whose ratio is not real) satisfying $f(z) = f(z+\\omega_1) = f(z+\\omega_2)$ for all $z$. "
        "Such functions are periodic in both the real and imaginary directions."
    ),
    "doubly stochastic matrix": (
        "A square matrix $A = (a_{ij})$ with $a_{ij} \\geq 0$ whose rows and columns each sum to unity: "
        "$$\\sum_j a_{ij} = 1 = \\sum_i a_{ij}$$"
    ),
    "drag": (
        "The resistive force on a body moving through a fluid. For a sphere moving at terminal velocity in "
        "streamlined flow, Stokes' law gives $$F = 6\\pi r\\eta v$$ "
        "where $r$ is the sphere radius, $\\eta$ the fluid viscosity and $v$ the speed. "
        "Drag increases with speed and is lower for streamlined objects."
    ),
    "drift speed": (
        "The mean speed of charge carriers through a conductor in an applied electric field. "
        "For a conductor of cross-sectional area $A$ with carrier density $n$, charge $e$ and drift speed $v$: "
        "$$I = nAve$$"
    ),
    "dulong and petit's law": (
        "Formulated in 1819 by Pierre Dulong and Alexis Petit, it states that the molar heat capacity of a "
        "solid element is approximately $$C_m \\approx 3R \\approx 25\\,\\text{J mol}^{-1}\\text{K}^{-1}$$ "
        "where $R$ is the gas constant. Applies with fair accuracy at normal temperatures to elements with "
        "simple crystal structures."
    ),
}


def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    d_entries = data.get('D', [])
    word_map = {item.get('word', '').strip().lower(): item for item in d_entries}

    for target_word, new_def in BATCH_D2_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  \u2713 Updated: [{target_word}]")
        else:
            print(f"  \u26a0\ufe0f  Not found in Section D: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_D2_DEFINITIONS)} definitions in Section D Batch 2.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    print("Rebuilding core_dictionary.js index...")
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n\u2705 Successfully updated dictionary.json and rebuilt core_dictionary.js!")


if __name__ == '__main__':
    apply_enrichment()
