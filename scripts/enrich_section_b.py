"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION B
=====================================================================
Enriches all mathematical, physical, and chemical formulas for Section B
terms using KaTeX LaTeX typesetting as specified in the Desmond Manual
Engineering Guide.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_B_DEFINITIONS = {
    "balmer series": (
        "The spectral emission series of atomic hydrogen corresponding to electron transitions from higher energy levels ($n \\ge 3$) "
        "to the second principal energy level ($n = 2$), appearing in the visible spectrum at four distinct wavelengths: "
        "$410\\text{ nm}$ (violet), $434\\text{ nm}$ (blue), $486\\text{ nm}$ (cyan), and $656\\text{ nm}$ (red, $H_\\alpha$). "
        "The wavelengths are given by the empirical Balmer-Rydberg formula: "
        "$$\\frac{1}{\\lambda} = R_H \\left(\\frac{1}{2^2} - \\frac{1}{n^2}\\right) = R_H \\left(\\frac{1}{4} - \\frac{1}{n^2}\\right) \\quad (n = 3, 4, 5, \\dots)$$ "
        "where $R_H \\approx 1.097373 \\times 10^7\\text{ m}^{-1}$ is the Rydberg constant for hydrogen."
    ),
    "base ionisation constant": (
        "The equilibrium constant $K_b$ describing the ionization of a weak base in aqueous solution. "
        "For a generic base $\\text{B}$ in water: "
        "$$\\text{B}(\\text{aq}) + \\text{H}_2\\text{O}(\\text{l}) \\rightleftharpoons \\text{BH}^+(\\text{aq}) + \\text{OH}^-(\\text{aq})$$ "
        "The base ionization constant is defined as: "
        "$$K_b = \\frac{[\\text{BH}^+][\\text{OH}^-]}{[\\text{B}]}$$ "
        "Water is omitted because its concentration is essentially constant. The base strength is expressed logarithmically as: "
        "$$\\text{p}K_b = -\\log_{10} K_b$$ "
        "where a smaller $\\text{p}K_b$ denotes a stronger base. For any conjugate acid-base pair, $K_a \\times K_b = K_w = 10^{-14}$ at $25^\\circ\\text{C}$."
    ),
    "bayes' theorem": (
        "A foundational probability theorem named after Reverend Thomas Bayes (1702–1761) that determines the posterior probability of an event "
        "based on prior knowledge of conditions related to the event: "
        "$$P(A \\mid B) = \\frac{P(B \\mid A) \\, P(A)}{P(B)}$$ "
        "In the partitioned form with mutually exclusive hypotheses $A_1, A_2, \\dots, A_n$: "
        "$$P(A_k \\mid B) = \\frac{P(B \\mid A_k) \\, P(A_k)}{\\sum_{i=1}^n P(B \\mid A_i) \\, P(A_i)}$$ "
        "where $P(A)$ is the prior probability, $P(B \\mid A)$ is the likelihood, and $P(A \\mid B)$ is the posterior probability."
    ),
    "beat frequency": (
        "The frequency of the periodic fluctuation in acoustic intensity (amplitude modulation) heard when two sound waves of slightly different frequencies "
        "$f_1$ and $f_2$ interfere with each other: "
        "$$f_{\\text{beat}} = |f_1 - f_2|$$ "
        "The combined wave oscillates with carrier frequency $f_{\\text{avg}} = \\frac{f_1 + f_2}{2}$ while its envelope beats at frequency $f_{\\text{beat}}$."
    ),
    "beer's law": (
        "Also known as the Beer-Lambert law, stating that the absorbance $A$ of monochromatic light passing through an absorbing solution "
        "is directly proportional to the path length $l$ and the molar concentration $c$: "
        "$$A = \\varepsilon c l$$ "
        "where $A = -\\log_{10}\\left(\\frac{I}{I_0}\\right) = \\log_{10}\\left(\\frac{I_0}{I}\\right)$, $\\varepsilon$ is the molar absorptivity "
        "(in $\\text{L}\\cdot\\text{mol}^{-1}\\text{cm}^{-1}$), $c$ is concentration in $\\text{mol/L}$, and $l$ is the cuvette path length in $\\text{cm}$."
    ),
    "bell curve": (
        "The symmetric, bell-shaped probability density function of the Gaussian normal distribution, completely characterized by its mean $\\mu$ and standard deviation $\\sigma$: "
        "$$f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} \\exp\\left(-\\frac{(x - \\mu)^2}{2\\sigma^2}\\right)$$ "
        "By the Empirical Rule: approximately 68.27% of values fall within $\\mu \\pm 1\\sigma$, 95.45% within $\\mu \\pm 2\\sigma$, and 99.73% within $\\mu \\pm 3\\sigma$."
    ),
    "bernoulli equation": (
        "In differential calculus, a non-linear first-order ordinary differential equation of the form: "
        "$$\\frac{dy}{dx} + P(x)y = Q(x)y^n \\quad (n \\neq 0, 1)$$ "
        "Solved by substituting the transformation $v = y^{1-n}$, which transforms the non-linear equation into a standard linear first-order differential equation: "
        "$$\\frac{dv}{dx} + (1 - n)P(x)v = (1 - n)Q(x)$$"
    ),
    "bernoulli number": (
        "A sequence of rational numbers $B_m$ arising in number theory, defined via the generating function: "
        "$$\\frac{t}{e^t - 1} = \\sum_{m=0}^{\\infty} B_m \\frac{t^m}{m!}$$ "
        "The first several values are $B_0 = 1$, $B_1 = -\\frac{1}{2}$, $B_2 = \\frac{1}{6}$, $B_4 = -\\frac{1}{30}$, $B_6 = \\frac{1}{42}$, with $B_m = 0$ for all odd $m > 1$. "
        "Bernoulli numbers yield exact values for the Riemann zeta function at positive even integers: "
        "$$\\zeta(2k) = \\frac{(-1)^{k-1} (2\\pi)^{2k} B_{2k}}{2(2k)!}$$"
    ),
    "bernoulli trial": (
        "A random experiment with exactly two mutually exclusive outcomes, conventionally termed 'success' (with probability $p$) and 'failure' (with probability $q = 1 - p$). "
        "In $n$ independent Bernoulli trials, the probability of obtaining exactly $k$ successes is given by the binomial distribution: "
        "$$P(X = k) = \\binom{n}{k} p^k (1 - p)^{n-k} \\quad (k = 0, 1, \\dots, n)$$"
    ),
    "bernoulli's theorem": (
        "A fundamental principle in fluid dynamics stating that for an incompressible, inviscid fluid undergoing steady streamline flow, "
        "the sum of pressure energy, kinetic energy per unit volume, and potential energy per unit volume is constant along a streamline: "
        "$$P + \\frac{1}{2}\\rho v^2 + \\rho gh = \\text{constant}$$ "
        "where $P$ is static fluid pressure, $\\rho$ is fluid density, $v$ is flow speed, $g$ is gravitational acceleration, and $h$ is elevation. "
        "It implies that an increase in fluid velocity occurs simultaneously with a decrease in static pressure (the Venturi effect)."
    ),
    "bernstein polynomials": (
        "A sequence of polynomials approximating a continuous function $f(x)$ on the closed interval $[0, 1]$, defined by Sergei Bernstein: "
        "$$B_n(f)(x) = \\sum_{k=0}^{n} f\\left(\\frac{k}{n}\\right) \\binom{n}{k} x^k (1 - x)^{n-k}$$ "
        "As $n \\to \\infty$, $B_n(f)(x)$ converges uniformly to $f(x)$ on $[0, 1]$, providing a constructive proof of the Stone-Weierstrass Approximation Theorem."
    ),
    "bessel function": (
        "Canonical solutions $J_\\alpha(x)$ and $Y_\\alpha(x)$ to Bessel's second-order differential equation: "
        "$$x^2 \\frac{d^2y}{dx^2} + x \\frac{dy}{dx} + (x^2 - \\alpha^2)y = 0$$ "
        "The Bessel function of the first kind of integer order $n$ is defined by the power series: "
        "$$J_n(x) = \\sum_{m=0}^{\\infty} \\frac{(-1)^m}{m! \\, (m + n)!} \\left(\\frac{x}{2}\\right)^{2m + n}$$ "
        "Bessel functions describe wave propagation in cylindrical geometries, circular drum vibrations, and optical Airy diffraction patterns."
    ),
    "bessel inequality": (
        "In inner product spaces and Fourier analysis, an inequality stating that for an orthonormal sequence $(e_n)$ in a Hilbert space $H$ "
        "and any vector $x \\in H$: "
        "$$\\sum_{n=1}^{\\infty} |\\langle x, e_n \\rangle|^2 \\le \\|x\\|^2$$ "
        "For Fourier series on $[0, 2\\pi]$, this implies: "
        "$$\\sum_{n=-\\infty}^{\\infty} |c_n|^2 \\le \\frac{1}{2\\pi} \\int_0^{2\\pi} |f(x)|^2 dx$$ "
        "When the orthonormal set is complete, the inequality becomes an equality (Parseval's identity)."
    ),
    "beta decay": (
        "A radioactive decay process mediated by the weak nuclear force, in which an unstable nucleus transforms by emitting a beta particle. "
        "1. Beta-minus ($\\beta^-$) decay: A neutron decays into a proton, emitting an electron and an electron antineutrino: "
        "$${}_Z^A\\text{X} \\longrightarrow {}_{Z+1}^A\\text{Y} + e^- + \\bar{\\nu}_e \\quad (n \\to p + e^- + \\bar{\\nu}_e)$$ "
        "2. Beta-plus ($\\beta^+$, positron emission) decay: A proton transforms into a neutron, emitting a positron and an electron neutrino: "
        "$${}_Z^A\\text{X} \\longrightarrow {}_{Z-1}^A\\text{Y} + e^+ + \\nu_e \\quad (p \\to n + e^+ + \\nu_e)$$ "
        "The mass number $A$ remains constant while atomic number $Z$ changes by $\\pm 1$."
    ),
    "beta distribution": (
        "A continuous probability distribution defined on the interval $[0, 1]$, parameterized by shape parameters $\\alpha > 0$ and $\\beta > 0$: "
        "$$f(x; \\alpha, \\beta) = \\frac{1}{\\text{B}(\\alpha, \\beta)} x^{\\alpha - 1} (1 - x)^{\\beta - 1} \\quad (0 \\le x \\le 1)$$ "
        "where $\\text{B}(\\alpha, \\beta)$ is the beta function. Widely used as the conjugate prior distribution for Bernoulli and binomial proportions in Bayesian statistics."
    ),
    "beta function": (
        "A special function in calculus, also called the Euler integral of the first kind, defined for $\\text{Re}(p) > 0, \\text{Re}(q) > 0$ by: "
        "$$\\text{B}(p, q) = \\int_0^1 x^{p-1} (1 - x)^{q-1} \\, dx$$ "
        "It is fundamentally related to the Gamma function $\\Gamma(z)$ by: "
        "$$\\text{B}(p, q) = \\frac{\\Gamma(p) \\, \\Gamma(q)}{\\Gamma(p + q)}$$"
    ),
    "bezout's lemma": (
        "A fundamental theorem in elementary number theory stating that for any non-zero integers $a$ and $b$, their greatest common divisor $d = \\gcd(a, b)$ "
        "can be expressed as a linear combination of $a$ and $b$ with integer coefficients $x, y \\in \\mathbb{Z}$: "
        "$$ax + by = \\gcd(a, b)$$ "
        "The integers $x$ and $y$ (Bézout coefficients) can be computed using the Extended Euclidean Algorithm."
    ),
    "bieberbach's conjecture": (
        "A celebrated conjecture in complex analysis proposed by Ludwig Bieberbach (1916) and proved by Louis de Branges (1984), "
        "stating that if $f(z) = z + \\sum_{n=2}^\\infty a_n z^n$ is an univalent (injective holomorphic) function on the open unit disk $|z| < 1$, "
        "then for every $n \\ge 2$: "
        "$$|a_n| \\le n$$ "
        "with equality holding if and only if $f$ is a rotation of the Koebe function $f(z) = \\frac{z}{(1 - e^{i\\theta} z)^2}$."
    ),
    "binomial coefficients": (
        "The positive integer coefficients appearing in the algebraic expansion of powers of a binomial $(a + b)^n$: "
        "$$\\binom{n}{r} = {}^n\\text{C}_r = \\frac{n!}{r!(n - r)!}$$ "
        "representing the number of ways to choose an unordered subset of $r$ elements from a fixed set of $n$ elements. "
        "Satisfies Pascal's identity: $\\binom{n}{r} = \\binom{n-1}{r-1} + \\binom{n-1}{r}$."
    ),
    "binomial distribution": (
        "The discrete probability distribution of the number of successes $k$ in $n$ independent Bernoulli trials with constant success probability $p$: "
        "$$P(X = k) = \\binom{n}{k} p^k (1 - p)^{n-k} \\quad (k = 0, 1, 2, \\dots, n)$$ "
        "Its mean is $\\mu = np$ and its variance is $\\sigma^2 = np(1 - p) = npq$."
    ),
    "binomial theorem": (
        "A fundamental algebraic theorem describing the algebraic expansion of powers of a binomial expression $(a + b)^n$: "
        "$$(a + b)^n = \\sum_{k=0}^{n} \\binom{n}{k} a^{n-k} b^k = a^n + \\binom{n}{1} a^{n-1}b + \\binom{n}{2} a^{n-2}b^2 + \\dots + b^n$$ "
        "For any real power $\\alpha \\in \\mathbb{R}$ where $|x| < 1$, Newton's generalized binomial series states: "
        "$$(1 + x)^\\alpha = 1 + \\alpha x + \\frac{\\alpha(\\alpha - 1)}{2!} x^2 + \\frac{\\alpha(\\alpha - 1)(\\alpha - 2)}{3!} x^3 + \\dots = \\sum_{k=0}^{\\infty} \\binom{\\alpha}{k} x^k$$"
    ),
    "biot-savart law": (
        "An inverse-square equation in classical electromagnetism relating magnetic field $\\vec{B}$ to steady electric current $I$. "
        "The differential magnetic field $d\\vec{B}$ contributed by an infinitesimal current-carrying element $d\\vec{l}$ at displacement vector $\\vec{r}$ is: "
        "$$d\\vec{B} = \\frac{\\mu_0 I}{4\\pi} \\frac{d\\vec{l} \\times \\hat{r}}{r^2} = \\frac{\\mu_0 I}{4\\pi} \\frac{d\\vec{l} \\times \\vec{r}}{r^3}$$ "
        "For an infinitely long straight wire carrying current $I$, integration yields the circular magnetic field at radial distance $r$: "
        "$$B = \\frac{\\mu_0 I}{2\\pi r}$$"
    ),
    "bloch's theorem": (
        "A quantum mechanical theorem stating that energy eigenstates for an electron in a spatially periodic crystal potential $V(\\vec{r} + \\vec{R}) = V(\\vec{r})$ "
        "can be written in the form of plane waves modulated by a periodic function (Bloch wave function): "
        "$$\\psi_{\\vec{k}}(\\vec{r}) = e^{i\\vec{k} \\cdot \\vec{r}} u_{\\vec{k}}(\\vec{r})$$ "
        "where $\\vec{k}$ is the crystal wave vector and $u_{\\vec{k}}(\\vec{r})$ satisfies $u_{\\vec{k}}(\\vec{r} + \\vec{R}) = u_{\\vec{k}}(\\vec{r})$ for all Bravais lattice vectors $\\vec{R}$."
    ),
    "bohr model": (
        "The atomic model of hydrogen proposed by Niels Bohr (1913), postulating that electrons orbit the nucleus in discrete, stable, non-radiating circular orbits. "
        "The orbital energy levels are quantized according to: "
        "$$E_n = -\\frac{13.6\\text{ eV}}{n^2} \\quad (n = 1, 2, 3, \\dots)$$ "
        "A transition between levels $E_2$ and $E_1$ emits or absorbs a photon of energy: "
        "$$\\Delta E = E_2 - E_1 = hf = \\frac{hc}{\\lambda}$$ "
        "where $h = 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ and $c = 3.0 \\times 10^8\\text{ m/s}$."
    ),
    "bohr radius": (
        "A physical constant representing the most probable radius of the ground-state electron orbit in the Bohr model of the hydrogen atom, denoted by $a_0$: "
        "$$a_0 = \\frac{4\\pi \\varepsilon_0 \\hbar^2}{m_e e^2} \\approx 5.29177 \\times 10^{-11}\\text{ m} = 0.529\\text{ \\AA}$$ "
        "where $\\varepsilon_0$ is electric permittivity, $\\hbar = \\frac{h}{2\\pi}$, $m_e$ is electron rest mass, and $e$ is elementary charge."
    ),
    "bohr's theory": (
        "Bohr's quantum hypothesis that the orbital angular momentum $L$ of an electron moving in a circle of radius $r$ with velocity $v$ "
        "is quantized in integer multiples of $\\hbar = \\frac{h}{2\\pi}$: "
        "$$L = mvr = \\frac{nh}{2\\pi} = n\\hbar \\quad (n = 1, 2, 3, \\dots)$$ "
        "Equating the centripetal force to the electrostatic Coulomb attraction: "
        "$$\\frac{m v^2}{r} = \\frac{1}{4\\pi\\varepsilon_0} \\frac{e^2}{r^2}$$ "
        "yields quantized radii $r_n = n^2 a_0$."
    ),
    "boltzmann constant": (
        "The fundamental physical constant relating absolute temperature $T$ to microscopic kinetic energy per degree of freedom, denoted by $k$ or $k_B$: "
        "$$k_B = \\frac{R}{N_A} = 1.380649 \\times 10^{-23}\\text{ J/K}$$ "
        "where $R = 8.314\\text{ J}\\cdot\\text{mol}^{-1}\\text{K}^{-1}$ is the molar gas constant and $N_A = 6.022 \\times 10^{23}\\text{ mol}^{-1}$ is Avogadro's number."
    ),
    "boltzmann formula": (
        "A foundational formula in statistical thermodynamics connecting macroscopic thermodynamic entropy $S$ to microscopic statistical multiplicity $W$: "
        "$$S = k_B \\ln W$$ "
        "where $k_B$ is the Boltzmann constant and $W$ is the thermodynamic probability (the number of microscopic microstates corresponding to the macrostate)."
    ),
    "boyle's law": (
        "An experimental gas law stating that for a fixed mass of an ideal gas kept at constant temperature, the absolute pressure $P$ is inversely proportional to its volume $V$: "
        "$$P \\propto \\frac{1}{V} \\iff PV = \\text{constant} \\iff P_1 V_1 = P_2 V_2$$ "
        "A plot of $P$ versus $V$ at constant temperature produces a set of rectangular hyperbolas known as isotherms."
    ),
    "bragg's law": (
        "A foundational law in X-ray crystallography formulated by W. H. Bragg and W. L. Bragg (1913), describing the condition for constructive interference "
        "of X-rays reflected from parallel lattice planes of a crystal spaced distance $d$ apart: "
        "$$2d \\sin\\theta = n\\lambda$$ "
        "where $\\theta$ is the glancing (Bragg) angle between the incident beam and the crystal plane, $\\lambda$ is X-ray wavelength, and $n \\in \\{1, 2, 3, \\dots\\}$ is the order of reflection."
    ),
    "brewster's law": (
        "An optical law stating that light reflected from a transparent dielectric medium is completely plane-polarized when the reflected ray is perpendicular "
        "to the refracted ray ($\\theta_r + \\theta_B = 90^\\circ$). The Brewster polarizing angle $\\theta_B$ is given by: "
        "$$\\tan\\theta_B = \\frac{n_2}{n_1} = n$$ "
        "where $n_1$ and $n_2$ are the refractive indices of the surrounding medium and the reflecting substance."
    ),
    "bulk modulus": (
        "An elastic modulus measuring a substance's resistance to uniform volumetric compression under hydrostatic pressure, denoted by $K$: "
        "$$K = -V \\frac{dP}{dV} = -V \\left(\\frac{\\partial P}{\\partial V}\\right)_T$$ "
        "where $P$ is pressure, $V$ is volume, and the negative sign ensures $K > 0$ since volume decreases as pressure increases. "
        "Its SI unit is the pascal ($\\text{Pa}$ or $\\text{N/m}^2$). The reciprocal of bulk modulus is compressibility: $\\beta = \\frac{1}{K}$."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    b_entries = data.get('B', [])
    word_map = {item.get('word', '').strip().lower(): item for item in b_entries}

    for target_word, new_def in BATCH_B_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section B: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_B_DEFINITIONS)} definitions in Section B.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
