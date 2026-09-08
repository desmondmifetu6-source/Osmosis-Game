"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION A (BATCH 3 & FINAL)
=====================================================================
Enriches all remaining mathematical, physical, and chemical formulas
for Section A (Items 111-219) using KaTeX LaTeX typesetting.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_A3_DEFINITIONS = {
    "ampere's law": (
        "A fundamental law of electromagnetism relating the integrated magnetic field around a closed loop to the electric current passing through the loop: "
        "$$\\oint \\vec{B} \\cdot d\\vec{l} = \\mu_0 I_{\\text{enc}}$$ "
        "where $\\vec{B}$ is the magnetic flux density, $d\\vec{l}$ is an infinitesimal element of the closed path, $\\mu_0$ is the permeability of free space "
        "($4\\pi \\times 10^{-7}\\text{ T}\\cdot\\text{m/A}$), and $I_{\\text{enc}}$ is the enclosed net electric current. "
        "In the differential Biot-Savart form, the magnetic field contribution from a current element $I\\,d\\vec{l}$ is: "
        "$$d\\vec{B} = \\frac{\\mu_0 I \\, d\\vec{l} \\times \\hat{r}}{4\\pi r^2} \\implies dB = \\frac{\\mu_0 I \\sin\\theta \\, dl}{4\\pi r^2}$$"
    ),
    "amplitude": (
        "1. The maximum displacement or distance moved by a point on a vibrating body or wave from its equilibrium (mean) position. "
        "For a sinusoidal wave described by: "
        "$$y(t) = A \\sin(\\omega t + \\phi)$$ "
        "where $A$ is the amplitude, $\\omega = 2\\pi f$ is angular frequency, and $\\phi$ is the phase constant. "
        "The energy transported by a wave is directly proportional to the square of its amplitude ($E \\propto A^2$). "
        "2. In complex analysis, also known as the argument ($\\arg z$), the angle $\\theta$ formed by a complex number $z = x + iy$ with the positive real axis."
    ),
    "analyser": (
        "An optical device (such as a Nicol prism or Polaroid sheet) placed in the optical path to detect and determine the plane of polarization of light. "
        "By Malus's Law, when completely plane-polarized light of initial intensity $I_0$ passes through an analyzer whose transmission axis is oriented at an angle $\\theta$ "
        "relative to the plane of polarization, the transmitted intensity $I$ is given by: "
        "$$I = I_0 \\cos^2\\theta$$ "
        "Extinction ($I = 0$) occurs when the polarizer and analyzer are crossed at $\\theta = 90^\\circ$."
    ),
    "angle between two vectors": (
        "For two non-zero vectors $\\vec{p}$ and $\\vec{q}$, the angle $\\theta$ ($0 \\le \\theta \\le \\pi$) between them is determined from their scalar (dot) product: "
        "$$\\vec{p} \\cdot \\vec{q} = |\\vec{p}| |\\vec{q}| \\cos\\theta \\implies \\cos\\theta = \\frac{\\vec{p} \\cdot \\vec{q}}{|\\vec{p}| |\\vec{q}|}$$ "
        "Therefore, the angle is: "
        "$$\\theta = \\arccos\\left(\\frac{\\vec{p} \\cdot \\vec{q}}{|\\vec{p}| |\\vec{q}|}\\right) = \\arccos\\left(\\frac{p_x q_x + p_y q_y + p_z q_z}{\\sqrt{p_x^2 + p_y^2 + p_z^2}\\sqrt{q_x^2 + q_y^2 + q_z^2}}\\right)$$"
    ),
    "angle of deviation": (
        "The angle $D$ through which an incident ray of light is deviated upon passing through an optical prism. "
        "For a prism with refracting angle $A$, the deviation is $D = (i_1 + i_2) - A$. "
        "At the position of minimum deviation ($D = D_m$), the light ray passes symmetrically through the prism ($i_1 = i_2 = i$ and $r_1 = r_2 = r = A/2$), "
        "giving $D_m = 2i - A$. The refractive index $n$ of the prism material is given by the prism formula: "
        "$$n = \\frac{\\sin\\left(\\frac{A + D_m}{2}\\right)}{\\sin\\left(\\frac{A}{2}\\right)}$$"
    ),
    "angle of friction": (
        "The angle $\\lambda$ of an inclined plane to the horizontal at which an object placed on the plane is on the verge of sliding down under gravity. "
        "It is related to the coefficient of static friction $\\mu_s$ by: "
        "$$\\tan\\lambda = \\mu_s \\implies \\lambda = \\arctan(\\mu_s)$$"
    ),
    "angular acceleration": (
        "The time rate of change of angular velocity, denoted by the Greek letter $\\alpha$. Measured in radians per second squared ($\\text{rad/s}^2$). "
        "Average angular acceleration over a time interval $\\Delta t$ is: "
        "$$\\alpha_{\\text{avg}} = \\frac{\\omega_2 - \\omega_1}{\\Delta t} = \\frac{\\Delta\\omega}{\\Delta t}$$ "
        "Instantaneous angular acceleration is the first derivative of angular velocity and second derivative of angular position: "
        "$$\\alpha = \\frac{d\\omega}{dt} = \\frac{d^2\\theta}{dt^2}$$ "
        "By Newton's rotational second law, torque $\\tau$ is related to angular acceleration by $\\tau = I\\alpha$, where $I$ is moment of inertia."
    ),
    "angular magnification": (
        "The ratio of the angle $\\theta_i$ subtended at the observer's eye by the magnified virtual image to the angle $\\theta_o$ subtended by the object at the unaided eye: "
        "$$M_\\theta = \\frac{\\theta_i}{\\theta_o}$$ "
        "For a simple magnifying glass viewing an object at the near point ($D = 25\\text{ cm}$), the angular magnification is $M = 1 + \\frac{D}{f}$."
    ),
    "angular momentum": (
        "A vector measure of the rotational momentum of a system about a reference axis or origin, denoted by $\\vec{L}$. "
        "For a single particle of mass $m$ and linear velocity $\\vec{v}$ at position vector $\\vec{r}$: "
        "$$\\vec{L} = \\vec{r} \\times \\vec{p} = \\vec{r} \\times (m\\vec{v})$$ "
        "For a circular orbit of radius $r$ where $\\vec{r} \\perp \\vec{v}$, its magnitude is: "
        "$$L = mvr$$ "
        "For a rigid body rotating with angular velocity $\\vec{\\omega}$ about a principal axis of moment of inertia $I$: "
        "$$\\vec{L} = I\\vec{\\omega}$$ "
        "By the Principle of Conservation of Angular Momentum, if the net external torque is zero ($\\sum \\vec{\\tau} = 0$), then $\\vec{L}$ remains constant."
    ),
    "angular speed": (
        "The scalar magnitude of angular velocity, representing the rate of rotation about an axis: "
        "$$\\omega = \\frac{\\Delta\\theta}{\\Delta t} = \\frac{2\\pi}{T} = 2\\pi f$$ "
        "where $\\theta$ is angular displacement in radians, $T$ is the period of revolution, and $f$ is rotational frequency in Hertz."
    ),
    "angular velocity": (
        "The vector rate of change of angular displacement with respect to time, denoted by $\\vec{\\omega}$. "
        "Its SI unit is radians per second ($\\text{rad/s}$ or $\\text{rad s}^{-1}$). "
        "Mathematically defined as: "
        "$$\\vec{\\omega} = \\frac{d\\theta}{dt}\\hat{n}$$ "
        "where $\\hat{n}$ is the unit vector along the axis of rotation given by the right-hand rule. "
        "The linear tangential velocity $\\vec{v}$ of a rotating particle at radius $\\vec{r}$ is: "
        "$$\\vec{v} = \\vec{\\omega} \\times \\vec{r} \\implies v = r\\omega$$"
    ),
    "annihilation": (
        "In subatomic physics, a high-energy process in which a subatomic particle collides with its corresponding antiparticle, converting their entire rest mass into energy "
        "in accordance with Einstein's mass-energy equivalence principle: "
        "$$E = mc^2$$ "
        "In electron-positron annihilation, an electron ($e^-$) and a positron ($e^+$) annihilate at low kinetic energy to produce two gamma-ray photons: "
        "$$e^- + e^+ \\longrightarrow 2\\gamma$$ "
        "Each gamma photon carries energy $E_\\gamma = m_e c^2 = 0.511\\text{ MeV}$, giving a total energy release of $1.022\\text{ MeV}$."
    ),
    "antiaromaticity": (
        "A property of cyclic, planar, completely conjugated systems containing $4n$ $\\pi$-electrons (where $n \\ge 1$ is an integer), in contrast to Hückel's $(4n + 2)$ aromatic rule. "
        "Antiaromatic compounds (such as cyclobuta-1,3-diene with $4\\pi$ electrons) are exceptionally thermodynamically unstable and chemically reactive."
    ),
    "antiderivative": (
        "A differentiable function $F(x)$ whose derivative equals the original function $f(x)$ on an open interval: "
        "$$F'(x) = f(x) \\iff \\int f(x) \\, dx = F(x) + C$$ "
        "where $C$ is an arbitrary constant of integration. For example, an antiderivative of $x^n$ (for $n \\neq -1$) is: "
        "$$\\int x^n \\, dx = \\frac{x^{n+1}}{n+1} + C$$"
    ),
    "apollonius' theorem": (
        "In plane Euclidean geometry, a theorem relating the lengths of the sides of any triangle to the length of a median. "
        "In $\\triangle ABC$, if $M$ is the midpoint of side $BC$ such that $AM = m$ is the median, and $BM = MC = c/2$, then: "
        "$$AB^2 + AC^2 = 2AM^2 + 2BM^2 \\implies a^2 + b^2 = 2m^2 + 2\\left(\\frac{c}{2}\\right)^2$$"
    ),
    "arc length": (
        "The measure of the distance along a curved path between two points. "
        "1. For a circular arc of radius $r$ subtending an angle $\\theta$ (in radians) at the center: "
        "$$s = r\\theta$$ "
        "2. For a smooth plane curve $y = f(x)$ between $x = a$ and $x = b$, the arc length is given by the definite integral: "
        "$$L = \\int_a^b \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$"
    ),
    "archimedes' principle": (
        "A foundational law of fluid statics stating that any body completely or partially submerged in a fluid experiences an upward buoyant force ($F_b$, or upthrust) "
        "equal in magnitude to the weight of the fluid displaced by the body: "
        "$$F_b = m_f g = \\rho_f V_{\\text{disp}} g$$ "
        "where $\\rho_f$ is fluid density, $V_{\\text{disp}}$ is displaced fluid volume, and $g$ is acceleration due to gravity. "
        "The apparent weight of the submerged object is: "
        "$$W_{\\text{apparent}} = W_{\\text{actual}} - F_b$$ "
        "A body floats when its buoyant force equals its total weight ($F_b = W$), meaning its average density is less than or equal to that of the fluid."
    ),
    "area ofsu rfac eof revolution": (
        "The surface area $S$ generated by rotating the arc of a smooth curve $y = f(x) \\ge 0$ (for $a \\le x \\le b$) through $2\\pi$ radians ($360^\\circ$) about the $x$-axis: "
        "$$S = 2\\pi \\int_a^b y \\sqrt{1 + \\left(\\frac{dy}{dx}\\right)^2} dx$$ "
        "For rotation about the $y$-axis: "
        "$$S = 2\\pi \\int_c^d x \\sqrt{1 + \\left(\\frac{dx}{dy}\\right)^2} dy$$"
    ),
    "area under a curve": (
        "In integral calculus, the net geometric area bounded by a continuous curve $y = f(x)$, the $x$-axis, and the vertical boundary lines $x = a$ and $x = b$: "
        "$$A = \\int_a^b f(x) \\, dx$$ "
        "The area enclosed between two continuous curves $y_1 = f(x)$ and $y_2 = g(x)$ where $f(x) \\ge g(x)$ between intersection points $x_1$ and $x_2$ is: "
        "$$A = \\int_{x_1}^{x_2} [f(x) - g(x)] \\, dx$$"
    ),
    "argument ofa complex number": (
        "For a non-zero complex number $z = x + iy = r(\\cos\\theta + i\\sin\\theta) = r e^{i\\theta}$, the argument $\\arg(z)$ is the oriented angle $\\theta$ "
        "made with the positive real axis in the Argand plane: "
        "$$\\tan\\theta = \\frac{y}{x} \\implies \\theta = \\arctan\\left(\\frac{y}{x}\\right)$$ "
        "The principal argument $\\operatorname{Arg}(z)$ is conventionally restricted to the interval $(-\\pi, \\pi]$. The modulus $|z|$ is given by: "
        "$$|z| = r = \\sqrt{x^2 + y^2}$$"
    ),
    "arithmetic progression": (
        "A sequence of numbers in which the difference between any two consecutive terms is a constant known as the common difference $d$. "
        "The $n$-th term $u_n$ of an arithmetic progression with first term $a$ is given by: "
        "$$u_n = a + (n - 1)d$$ "
        "where $d = u_n - u_{n-1}$."
    ),
    "arithmetic series": (
        "The indicated sum of the terms of an arithmetic progression. For a series with $n$ terms, first term $a$, and common difference $d$, the sum $S_n$ is: "
        "$$S_n = \\frac{n}{2}(a + l) = \\frac{n}{2}\\left[2a + (n - 1)d\\right]$$ "
        "where $l = u_n = a + (n - 1)d$ is the last term."
    ),
    "arithmetic-geometric mean iteration": (
        "An algorithm that computes the arithmetic-geometric mean (AGM) of two positive real numbers $a_0 = a$ and $b_0 = b$ via coupled recurrence relations: "
        "$$a_{n+1} = \\frac{a_n + b_n}{2} \\quad (\\text{arithmetic mean})$$ "
        "$$b_{n+1} = \\sqrt{a_n b_n} \\quad (\\text{geometric mean})$$ "
        "Both sequences converge quadratically to a common limit, $\\operatorname{AGM}(a, b)$, fundamental in computing complete elliptic integrals and digits of $\\pi$."
    ),
    "aromaticity": (
        "A chemical property of cyclic, planar, conjugated unsaturated molecules possessing enhanced thermodynamic stability due to electron delocalization. "
        "By Hückel's Rule, a monocyclic planar ring exhibits aromatic stability if it possesses $(4n + 2)$ $\\pi$-electrons: "
        "$$N_\\pi = 4n + 2 \\quad (n = 0, 1, 2, 3, \\dots)$$ "
        "Benzene ($\\text{C}_6\\text{H}_6$) has $6$ $\\pi$-electrons ($n = 1$) and exhibits complete resonance delocalization."
    ),
    "arrhenius equation": (
        "A fundamental formula in chemical kinetics proposed by Svante Arrhenius, modeling the temperature dependence of reaction rate constants: "
        "$$k = A \\exp\\left(-\\frac{E_a}{RT}\\right) \\quad \\text{or in logarithmic form} \\quad \\ln k = \\ln A - \\frac{E_a}{RT}$$ "
        "where $k$ is the rate constant, $A$ is the pre-exponential frequency factor, $E_a$ is activation energy (in $\\text{J/mol}$), "
        "$R$ is the universal gas constant ($8.314\\text{ J}\\cdot\\text{mol}^{-1}\\text{K}^{-1}$), and $T$ is absolute temperature in Kelvins. "
        "An Arrhenius plot of $\\ln k$ versus $1/T$ yields a straight line with slope $m = -\\frac{E_a}{R}$."
    ),
    "asymptote": (
        "A straight line $L$ associated with a curve $y = f(x)$ such that the perpendicular distance between the curve and the line approaches zero as points on the curve diverge to infinity: "
        "$$\\lim_{x \\to \\infty} |f(x) - (mx + c)| = 0$$ "
        "1. Vertical asymptote at $x = a$ if $\\lim_{x \\to a} f(x) = \\pm \\infty$. "
        "2. Horizontal asymptote at $y = b$ if $\\lim_{x \\to \\pm \\infty} f(x) = b$. "
        "3. Oblique (slant) asymptote $y = mx + c$ if $\\lim_{x \\to \\pm \\infty} \\frac{f(x)}{x} = m$ and $\\lim_{x \\to \\pm \\infty} [f(x) - mx] = c$."
    ),
    "atomic mass constant": (
        "A physical constant defined as one-twelfth of the rest mass of an unbound carbon-12 atom at ground state, denoted by $m_u$: "
        "$$m_u = \\frac{1}{12} m({}^{12}\\text{C}) = 1.66053907 \\times 10^{-27}\\text{ kg} = 931.494\\text{ MeV/}c^2$$ "
        "It defines the unified atomic mass unit ($\\text{u}$, or Dalton $\\text{Da}$)."
    ),
    "atomic weight": (
        "The dimensionless relative atomic mass ($A_r$) of an element, defined as the weighted average mass of its naturally occurring isotopes relative to 1/12 of the mass of a carbon-12 atom: "
        "$$A_r = \\frac{\\sum_{i} (m_i \\times p_i)}{100}$$ "
        "where $m_i$ is the isotopic mass of isotope $i$ and $p_i$ is its natural percentage abundance. "
        "For chlorine with ${}^{35}\\text{Cl}$ (75.77%, $34.97\\text{ u}$) and ${}^{37}\\text{Cl}$ (24.23%, $36.97\\text{ u}$): "
        "$$A_r(\\text{Cl}) = \\frac{(35 \\times 75) + (37 \\times 25)}{100} = 35.5$$"
    ),
    "auxiliary equation": (
        "In differential equations, the algebraic characteristic equation obtained by replacing derivatives in a homogeneous linear differential equation with powers of a variable $r$: "
        "$$a \\frac{d^2y}{dx^2} + b \\frac{dy}{dx} + cy = 0 \\implies ar^2 + br + c = 0$$ "
        "The nature of the roots $r_1, r_2$ governs the complementary function: "
        "1. Real distinct roots: $y = C_1 e^{r_1 x} + C_2 e^{r_2 x}$. "
        "2. Repeated real root $r$: $y = (C_1 + C_2 x) e^{rx}$. "
        "3. Complex conjugate roots $\\alpha \\pm i\\beta$: $y = e^{\\alpha x}(C_1 \\cos\\beta x + C_2 \\sin\\beta x)$."
    ),
    "average deviation": (
        "In statistics, the mean absolute deviation (MAD) measuring dispersion in a dataset of $N$ observations: "
        "$$\\text{MAD} = \\frac{1}{N} \\sum_{i=1}^N |X_i - \\bar{X}|$$ "
        "where $X_i$ are individual data points and $\\bar{X} = \\frac{1}{N}\\sum X_i$ is the arithmetic mean."
    ),
    "avogadro's number": (
        "The fundamental physical constant representing the number of constituent particles (atoms, molecules, or ions) in one mole of substance, denoted by $N_A$: "
        "$$N_A = 6.02214076 \\times 10^{23}\\text{ mol}^{-1}$$ "
        "It connects the macroscopic molar mass of a substance to its microscopic atomic mass: $M = m \\cdot N_A$."
    ),
    "axiomatic probability": (
        "The mathematical foundation of probability theory formulated by Andrey Kolmogorov via three fundamental axioms on a sample space $\\Omega$: "
        "1. Non-negativity: For every event $A$, $P(A) \\ge 0$. "
        "2. Normalization: The probability of the sample space is unity, $P(\\Omega) = 1$. "
        "3. Countable additivity: For any sequence of mutually exclusive (pairwise disjoint) events $A_1, A_2, A_3, \\dots$: "
        "$$P\\left(\\bigcup_{i=1}^\\infty A_i\\right) = \\sum_{i=1}^\\infty P(A_i)$$"
    ),
    "azimuthal quantum number": (
        "The secondary (orbital angular momentum) quantum number of an electron orbital, denoted by $l$. "
        "For a principal quantum number $n$, $l$ takes integer values: "
        "$$l \\in \\{0, 1, 2, \\dots, n - 1\\}$$ "
        "Values $l = 0, 1, 2, 3$ correspond to $s, p, d, f$ orbitals. The magnitude of the orbital angular momentum is quantized as: "
        "$$L = \\sqrt{l(l+1)}\\,\\hbar$$ "
        "where $\\hbar = \\frac{h}{2\\pi}$ is the reduced Planck constant."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    a_entries = data.get('A', [])
    word_map = {item.get('word', '').strip().lower(): item for item in a_entries}

    for target_word, new_def in BATCH_A3_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section A: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_A3_DEFINITIONS)} definitions in Section A.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
