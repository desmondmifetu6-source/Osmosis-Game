"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION D (BATCH 1)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section D
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_D1_DEFINITIONS = {
    "1,2-dibromoethane": (
        "A volatile organobromine liquid with molecular formula $\\text{C}_2\\text{H}_4\\text{Br}_2$, density $2.17\\text{ g/cm}^3$, "
        "melting point $9 - 10^\\circ\\text{C}$ ($282 - 283\\text{ K}$), and boiling point $131 - 132^\\circ\\text{C}$ ($404 - 405\\text{ K}$). "
        "It is synthesized by the electrophilic addition of bromine to ethene: "
        "$$\\text{CH}_2=\\text{CH}_2 + \\text{Br}_2 \\to \\text{BrCH}_2\\text{CH}_2\\text{Br}$$ "
        "Historically used as a lead scavenger additive in leaded fuels and as an agricultural pesticide."
    ),
    "d'alembert's ratio test": (
        "A criterion for the convergence of an infinite series $\\sum a_k$ of positive terms based on the limit of successive ratios: "
        "$$L = \\lim_{k \\to \\infty} \\left| \\frac{a_{k+1}}{a_k} \\right|$$ "
        "If $L < 1$, the series converges absolutely; if $L > 1$, the series diverges; and if $L = 1$, the test is inconclusive."
    ),
    "dalton's law": (
        "The fundamental gas law stating that the total pressure $P_{\\text{total}}$ of a mixture of non-reacting ideal gases equals the sum of the partial pressures of its individual components: "
        "$$P_{\\text{total}} = P_A + P_B + P_C + \\dots = \\sum_{i} P_i$$"
    ),
    "darcy's law": (
        "A constitutive equation describing the flow of a fluid through a porous medium under a hydraulic pressure gradient: "
        "$$Q = -\\frac{k A}{\\mu} \\frac{\\Delta P}{L}$$ "
        "where $Q$ is volumetric flow rate ($\\text{m}^3/\\text{s}$), $k$ is intrinsic permeability ($\\text{m}^2$), $A$ is cross-sectional area, "
        "$\\mu$ is dynamic viscosity ($\\text{Pa}\\cdot\\text{s}$), and $\\Delta P / L$ is the pressure drop per unit length."
    ),
    "daughter element": (
        "The nuclide produced by the radioactive decay or nuclear fission of a parent radionuclide. "
        "For example, in the uranium decay series: "
        "$${}^{238}\\text{U} \\to {}^{234}\\text{Th} \\to {}^{234}\\text{Pa} \\dots \\to {}^{206}\\text{Pb}$$ "
        "where thorium-234 is the daughter of uranium-238."
    ),
    "de broglie equation": (
        "The fundamental relationship of wave-particle duality stating that any moving matter has an associated matter wave whose wavelength $\\lambda$ is: "
        "$$\\lambda = \\frac{h}{p} = \\frac{h}{mv}$$ "
        "and frequency $\\nu = \\frac{E}{h}$, where $h$ is Planck's constant, $p$ is momentum, $m$ is mass, and $v$ is velocity."
    ),
    "de broglie wavelength": (
        "The quantum mechanical wavelength associated with a particle of mass $m$ moving with velocity $v$: "
        "$$\\lambda = \\frac{h}{mv}$$ "
        "where $h \\approx 6.626 \\times 10^{-34}\\text{ J}\\cdot\\text{s}$ is Planck's constant."
    ),
    "de moivre's theorem": (
        "A foundational formula in complex analysis relating complex powers to trigonometry for any integer $n$: "
        "$$(\\cos\\theta + i\\sin\\theta)^n = \\cos(n\\theta) + i\\sin(n\\theta)$$ "
        "or equivalently in Euler's form $(e^{i\\theta})^n = e^{i n\\theta}$, where $i = \\sqrt{-1}$."
    ),
    "de morgan's laws": (
        "Duality laws in Boolean algebra and set theory: "
        "1. In set theory: "
        "$$(A \\cup B)' = A' \\cap B', \\quad (A \\cap B)' = A' \\cup B'$$ "
        "2. In propositional logic: "
        "$$\\neg(P \\lor Q) \\equiv \\neg P \\land \\neg Q, \\quad \\neg(P \\land Q) \\equiv \\neg P \\lor \\neg Q$$"
    ),
    "debye temperature": (
        "A characteristic temperature $\\theta_D$ used in the Debye model of solid-state specific heats, defined by: "
        "$$k_B \\theta_D = h \\nu_D \\implies \\theta_D = \\frac{h \\nu_D}{k_B}$$ "
        "where $\\nu_D$ is the Debye cutoff frequency, $h$ is Planck's constant, and $k_B$ is the Boltzmann constant."
    ),
    "debye theory of specific heat": (
        "A theoretical model for the phonon contribution to specific heat in solids, predicting that at low temperatures ($T \\ll \\theta_D$), "
        "heat capacity follows the Debye $T^3$ law: "
        "$$C_V \\propto T^3$$ "
        "where the cutoff temperature $\\theta_D = \\frac{h\\nu_D}{k_B}$."
    ),
    "debye-hückel theory": (
        "A thermodynamic model explaining non-ideal behaviour in dilute electrolyte solutions due to electrostatic interactions: "
        "$$\\ln \\gamma_i = -A z_i^2 \\sqrt{I}$$ "
        "where $\\gamma_i$ is the activity coefficient, $z_i$ is ionic charge, and $I = \\frac{1}{2}\\sum c_i z_i^2$ is the ionic strength."
    ),
    "decane": (
        "A saturated straight-chain alkane hydrocarbon with molecular formula $\\text{C}_{10}\\text{H}_{22}$, density $730\\text{ kg/m}^3$, "
        "melting point $-29^\\circ\\text{C}$ ($242.7\\text{ K}$), and boiling point $174^\\circ\\text{C}$ ($447\\text{ K}$). "
        "It possesses 75 constitutional isomers and is a component of gasoline."
    ),
    "decay chain": (
        "A successive series of radioactive decays in which an unstable parent radioisotope transforms through intermediate daughters: "
        "$${}^{238}\\text{U} \\xrightarrow{\\alpha} {}^{234}\\text{Th} \\xrightarrow{\\beta^-} {}^{234}\\text{Pa} \\dots \\xrightarrow{\\alpha} {}^{206}\\text{Pb}$$ "
        "terminating at a stable isotope."
    ),
    "decay constant": (
        "The fractional rate of nuclear decay per unit time, denoted by $\\lambda$: "
        "$$\\lambda = \\frac{\\ln 2}{t_{1/2}} \\approx \\frac{0.693}{t_{1/2}}$$ "
        "where $t_{1/2}$ is the radioactive half-life. Activity is governed by $A = \\lambda N$ with SI unit reciprocal seconds ($\\text{s}^{-1}$ or $\\text{Bq}$)."
    ),
    "decay product": (
        "A nuclide resulting from the radioactive decay of a parent nuclide. "
        "For example, radon-222 decays via $\\alpha$-emission to polonium-218: "
        "$${}^{222}\\text{Rn} \\to {}^{218}\\text{Po} + \\alpha$$"
    ),
    "decile": (
        "Any of the nine numerical values that divide an ordered dataset into ten equal frequency intervals. "
        "The $k$-th decile $D_k$ ($k=1, \\dots, 9$) corresponds to the $(10k)$-th percentile: "
        "$$D_k = L_1 + \\left( \\frac{\\frac{k N}{10} - \\sum f_1}{f_d} \\right) c$$ "
        "where $L_1$ is the lower boundary of the decile class, $N$ is total frequency, and $c$ is class width."
    ),
    "decomposition": (
        "1. In mathematics, factoring an object into simpler components, such as prime factorisation $48 = 2^4 \\times 3$ or vector decomposition $\\mathbf{v} = v_x \\mathbf{i} + v_y \\mathbf{j}$. "
        "2. In chemistry, a reaction where a single compound breaks down into two or more simpler elements or compounds: "
        "$$\\text{AB} \\to \\text{A} + \\text{B}$$ "
        "3. In biology, the biochemical breakdown of dead organic matter by decomposers."
    ),
    "dedekind cut": (
        "A partition of the set of rational numbers $\\mathbb{Q}$ into two non-empty subsets $(A, B)$ such that every element of $A$ is strictly less than every element of $B$, and $A$ contains no greatest rational. "
        "For example, $\\sqrt{2}$ is constructed as: "
        "$$A = \\{x \\in \\mathbb{Q} \\mid x < 0 \\text{ or } x^2 < 2\\}, \\quad B = \\{x \\in \\mathbb{Q} \\mid x > 0 \\text{ and } x^2 > 2\\}$$"
    ),
    "dedekind-peano axioms": (
        "The axiomatic foundation for natural numbers $\\mathbb{N}$: "
        "(i) $0 \\in \\mathbb{N}$. "
        "(ii) Every $n \\in \\mathbb{N}$ has a unique successor $S(n) = n'$. "
        "(iii) $0$ is not the successor of any natural number: $\\forall n, \\, n' \\ne 0$. "
        "(iv) The successor function is injective: $n' = m' \\implies n = m$. "
        "(v) Mathematical induction: if $P(0)$ holds and $\\forall k, \\, P(k) \\implies P(k')$, then $P(n)$ holds for all $n \\in \\mathbb{N}$."
    ),
    "defect": (
        "1. In solid-state physics, any crystallographic imperfection disrupting regular lattice periodicity. "
        "2. In spherical geometry, the spherical defect $D$ of a spherical triangle with sides $a, b, c$ is: "
        "$$D = 2\\pi - (a + b + c)$$"
    ),
    "deferred approach to the limit": (
        "Richardson extrapolation for accelerating the convergence of numerical approximations $F(h)$: "
        "$$E(h) = \\frac{F(h/r) - r^n F(h)}{1 - r^n}$$ "
        "where $r$ is grid ratio and $n$ is the order of truncation error."
    ),
    "deficient number": (
        "A positive integer $n$ whose sum of all positive divisors $\\sigma(n)$ is strictly less than $2n$: "
        "$$\\sigma(n) < 2n$$ "
        "The deficiency is $d(n) = 2n - \\sigma(n)$. For example, for $21$: divisors are $1, 3, 7, 21$ with sum $32 < 42$, yielding deficiency $10$."
    ),
    "definite integral": (
        "The integral of a function $f(x)$ between specified lower and upper integration limits $[a, b]$, representing net signed area: "
        "$$\\int_a^b f(x) \\, dx = F(b) - F(a)$$ "
        "where $F'(x) = f(x)$ by the Fundamental Theorem of Calculus. For example: "
        "$$\\int_1^3 (2x + 3) \\, dx = [x^2 + 3x]_1^3 = (9 + 9) - (1 + 3) = 14$$"
    ),
    "deflection": (
        "1. In mechanics, the angular displacement or rebound of an object striking a surface, where incidental angle equals reflection angle: $\\alpha = \\beta$. "
        "2. In electromagnetic fields, the magnetic deflection experienced by a charged particle governed by the Lorentz force: "
        "$$\\mathbf{F} = q(\\mathbf{E} + \\mathbf{v} \\times \\mathbf{B})$$"
    ),
    "deformation": (
        "The transformation of the metric shape or volume of a continuous body under mechanical stress: "
        "$$\\mathbf{u} = \\mathbf{x} - \\mathbf{X}$$ "
        "characterized by the infinitesimal strain tensor $\\varepsilon_{ij} = \\frac{1}{2}\\left( \\frac{\\partial u_i}{\\partial x_j} + \\frac{\\partial u_j}{\\partial x_i} \\right)$."
    ),
    "degree ofa polynomial": (
        "The highest exponent of the indeterminate variable in a non-zero single-variable polynomial. "
        "For example, in $P(x) = x^3 + 4x^2 - 6x - 7$, the degree is $3$."
    ),
    "dehydration": (
        "An elimination reaction resulting in the loss of water ($\\text{H}_2\\text{O}$) from a molecule. "
        "For example, the acid-catalyzed dehydration of ethanol to ethene: "
        "$$\\text{CH}_3\\text{CH}_2\\text{OH} \\xrightarrow{\\text{conc. } \\text{H}_2\\text{SO}_4, \\, 170^\\circ\\text{C}} \\text{CH}_2=\\text{CH}_2 + \\text{H}_2\\text{O}$$ "
        "or methanoic acid to carbon monoxide: $\\text{HCOOH} \\to \\text{CO} + \\text{H}_2\\text{O}$."
    ),
    "delocalisation": (
        "The distribution of valence electron density across multiple adjacent atoms rather than being localized in a single bond. "
        "In benzene ($\\text{C}_6\\text{H}_6$), the six $\\pi$-electrons are delocalized uniformly over the planar hexagonal carbon ring."
    ),
    "delta function": (
        "The Dirac delta distribution $\\delta(x)$, which is zero everywhere except at $x = 0$, defined rigorously by its sifting property: "
        "$$\\int_{-\\infty}^\\infty \\delta(x) \\, dx = 1, \\quad \\int_{-\\infty}^\\infty f(x) \\delta(x - x_0) \\, dx = f(x_0)$$"
    ),
    "density": (
        "1. In physics, volumetric mass density defined as mass per unit volume: "
        "$$\\rho = \\frac{m}{V}$$ "
        "with SI unit $\\text{kg}\\cdot\\text{m}^{-3}$ (or $\\text{g/cm}^3$). "
        "2. In statistics, probability density function $f(x)$ where $\\int_{-\\infty}^\\infty f(x) \\, dx = 1$."
    ),
    "density function": (
        "A probability density function (PDF) $f(x)$ for a continuous random variable $X$ such that: "
        "$$P(a \\le X \\le b) = \\int_a^b f(x) \\, dx, \\quad \\text{with } \\int_{-\\infty}^\\infty f(x) \\, dx = 1$$"
    ),
    "dental formula": (
        "A standardized representation of the dentition of mammalian jaws in quadrant form: "
        "Human permanent teeth: "
        "$$\\frac{\\text{I}2}{\\text{I}2} \\, \\frac{\\text{C}1}{\\text{C}1} \\, \\frac{\\text{PM}2}{\\text{PM}2} \\, \\frac{\\text{M}3}{\\text{M}3} \\times 2 = 32$$ "
        "Deciduous teeth: $\\frac{\\text{I}2}{\\text{I}2} \\frac{\\text{C}1}{\\text{C}1} \\frac{\\text{PM}0}{\\text{PM}0} \\frac{\\text{M}2}{\\text{M}2} \\times 2 = 20$."
    ),
    "deontic logic": (
        "A branch of modal logic dealing with obligation ($O$), permission ($P$), and prohibition ($F$): "
        "$$PA \\equiv \\neg O \\neg A, \\quad FA \\equiv O \\neg A$$"
    ),
    "dependent equations": (
        "A system of equations where at least one equation can be derived algebraically as a linear combination of the others: "
        "$$c_1 E_1 + c_2 E_2 + \\dots + c_k E_k = 0$$ "
        "implying the equations do not provide independent constraints."
    ),
    "dependent event": (
        "In probability theory, two events $A$ and $B$ where the occurrence of $A$ alters the conditional probability of $B$: "
        "$$P(A \\cap B) = P(A) \\cdot P(B \\mid A), \\quad \\text{where } P(B \\mid A) \\ne P(B)$$"
    ),
    "dependent variable": (
        "A variable whose values depend systematically on changes in one or more independent variables. "
        "In the relation $y = f(x) = 2x + 3$, $y$ is the dependent variable and $x$ is the independent variable."
    ),
    "depleted": (
        "Nuclear material with an isotopic abundance of a specific fissile isotope lower than natural abundance, "
        "such as depleted uranium (DU) containing $< 0.3\\%\\ {}^{235}\\text{U}$ compared to $0.72\\%$ in natural uranium."
    ),
    "depreciation": (
        "The reduction in the financial book value of a capital asset over time $n$ at annual depreciation rate $d$: "
        "$$A = P\\left(1 - \\frac{d}{100}\\right)^n$$ "
        "where $P$ is initial cost, $d$ is rate percentage, and $A$ is depreciated value."
    ),
    "derivative": (
        "The instantaneous rate of change of a differentiable function $f(x)$ with respect to independent variable $x$: "
        "$$f'(x) = \\frac{dy}{dx} = \\lim_{\\Delta x \\to 0} \\frac{f(x + \\Delta x) - f(x)}{\\Delta x}$$"
    ),
    "derived quantity": (
        "A physical quantity defined through mathematical combinations of base SI quantities: "
        "Force ($F = ma$, $\\text{N} = \\text{kg}\\cdot\\text{m}\\cdot\\text{s}^{-2}$), "
        "Pressure ($P = F/A$, $\\text{Pa} = \\text{N/m}^2$), "
        "Work ($W = F \\cdot d$, $\\text{J} = \\text{N}\\cdot\\text{m}$), "
        "Charge ($Q = I \\cdot t$, $\\text{C} = \\text{A}\\cdot\\text{s}$), "
        "Power ($P = W/t$, $\\text{W} = \\text{J/s}$)."
    ),
    "derived unit": (
        "An SI unit formed by algebraic multiplication or division of base units: "
        "$$\\text{Hz} = \\text{s}^{-1}, \\quad \\text{N} = \\text{kg}\\cdot\\text{m}\\cdot\\text{s}^{-2}, \\quad \\text{J} = \\text{N}\\cdot\\text{m}, \\quad \\text{Pa} = \\text{N/m}^2, \\quad \\Omega = \\text{V/A}$$"
    ),
    "descartes' rule of signs": (
        "A theorem stating that the number of positive real roots of a polynomial $P(x)$ equals the number of sign variations between consecutive non-zero coefficients, or is less than it by an even integer: "
        "$$P(x) = a_n x^n + a_{n-1}x^{n-1} + \\dots + a_0$$"
    ),
    "descent methods": (
        "An iterative numerical optimization algorithm that generates a sequence $\\{\\mathbf{x}_k\\}$ minimizing objective function $f$: "
        "$$\\mathbf{x}_{k+1} = \\mathbf{x}_k + \\alpha_k \\mathbf{g}_k$$ "
        "where $\\mathbf{g}_k$ is a descent direction ($f'(\\mathbf{x}_k)^T \\mathbf{g}_k < 0$) and $\\alpha_k > 0$ is step size."
    ),
    "determinant": (
        "A scalar attribute of a square matrix $A$. "
        "For a $2 \\times 2$ matrix: "
        "$$\\det \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} = ad - bc$$ "
        "For a $3 \\times 3$ matrix: "
        "$$\\det \\begin{pmatrix} a & b & c \\\\ d & e & f \\\\ g & h & i \\end{pmatrix} = a(ei - fh) - b(di - fg) + c(dh - eg)$$"
    ),
    "deuterium oxide": (
        "Heavy water with chemical formula $\\text{D}_2\\text{O}$ (or ${}^2\\text{H}_2\\text{O}$), "
        "composed of the hydrogen isotope deuterium (${}^2\\text{H}$). "
        "It has a density approximately $11\\%$ greater than protium water and is used as a neutron moderator in nuclear reactors."
    ),
    "deviation": (
        "The signed difference between an individual observed data value $x_i$ and a reference value, usually the arithmetic mean $\\mu$: "
        "$$\\text{deviation} = x_i - \\mu$$"
    ),
    "deviatoric": (
        "The traceless component of a second-order tensor $\\mathbf{T}$, defined by subtracting its isotropic spherical part: "
        "$$\\mathbf{T}_{\\text{dev}} = \\mathbf{T} - \\frac{1}{3} \\operatorname{tr}(\\mathbf{T}) \\mathbf{I}$$"
    ),
    "devil's curve": (
        "A quartic plane curve defined in Cartesian coordinates by: "
        "$$y^4 - a^2 y^2 = x^4 - b^2 x^2$$ "
        "and in polar coordinates by: "
        "$$r^2(\\sin^2\\theta - \\cos^2\\theta) = a^2\\sin^2\\theta - b^2\\cos^2\\theta$$"
    ),
    "dextronic acid": (
        "Gluconic acid, a non-volatile organic polyhydroxy acid with chemical formula $\\text{C}_6\\text{H}_{12}\\text{O}_7$ "
        "and melting point $131^\\circ\\text{C}$ ($404\\text{ K}$), produced by oxidation of the aldehyde group on C-1 of D-glucose."
    ),
    "diagonal matrix": (
        "A square matrix whose off-diagonal entries are all zero: "
        "$$A = \\operatorname{diag}(d_1, d_2, \\dots, d_n) = \\begin{pmatrix} d_1 & 0 & \\dots & 0 \\\\ 0 & d_2 & \\dots & 0 \\\\ \\vdots & \\vdots & \\ddots & \\vdots \\\\ 0 & 0 & \\dots & d_n \\end{pmatrix}$$"
    ),
    "diazo compound": (
        "An organic compound containing a terminal diazonio functional group ($-\\text{N}^+\\equiv\\text{N}$) with general structure: "
        "$$R_2\\text{C}=\\text{N}^+=\\text{N}^- \\longleftrightarrow R_2\\text{C}^--\\text{N}^+\\equiv\\text{N}$$"
    ),
    "dichlorine oxide": (
        "A brownish-yellow gas with molecular formula $\\text{Cl}_2\\text{O}$, melting point $-120.6^\\circ\\text{C}$ ($153\\text{ K}$), "
        "and boiling point $2.2^\\circ\\text{C}$ ($275\\text{ K}$). It is prepared by reacting dry chlorine gas with yellow mercury(II) oxide: "
        "$$2\\text{Cl}_2 + 2\\text{HgO} \\to \\text{HgCl}_2\\cdot\\text{HgO} + \\text{Cl}_2\\text{O}$$"
    ),
    "dichlorodiphenyltrichloroethane": (
        "DDT, a synthetic organochlorine insecticide with chemical formula $\\text{C}_{14}\\text{H}_9\\text{Cl}_5$, "
        "melting point $108.5^\\circ\\text{C}$ ($381.65\\text{ K}$), and IUPAC name 1,1,1-trichloro-2,2-bis(4-chlorophenyl)ethane."
    ),
    "dichloromethane": (
        "A volatile organochlorine solvent with chemical formula $\\text{CH}_2\\text{Cl}_2$, density $1.33\\text{ g/cm}^3$, "
        "melting point $-96.7^\\circ\\text{C}$ ($176\\text{ K}$), and boiling point $39.6^\\circ\\text{C}$ ($313\\text{ K}$)."
    ),
    "dielectric constant": (
        "The relative permittivity $\\varepsilon_r$ of a dielectric material: "
        "$$\\varepsilon_r = \\frac{\\varepsilon}{\\varepsilon_0} = \\frac{C}{C_0}$$ "
        "representing the ratio of capacitance $C$ with the dielectric to capacitance $C_0$ in vacuum."
    ),
    "difference": (
        "1. In arithmetic, the result of subtracting one quantity from another: $a - b$. "
        "2. In set theory, relative complement $A \\setminus B = \\{x \\in A \\mid x \\notin B\\}$. "
        "3. Symmetric difference: $A \\, \\Delta \\, B = (A \\setminus B) \\cup (B \\setminus A)$."
    ),
    "difference equation": (
        "An equation relating successive values in a sequence through forward difference operators: "
        "$$\\Delta u(n) = u(n+1) - u(n), \\quad \\Delta^2 u(n) = u(n+2) - 2u(n+1) + u(n)$$"
    ),
    "difference of two squares": (
        "An algebraic identity factoring the difference between two quadratic terms: "
        "$$a^2 - b^2 = (a - b)(a + b)$$ "
        "For example, $x^2 - 9 = (x - 3)(x + 3)$."
    ),
    "difference quotient": (
        "The slope of the secant line passing through $(x, f(x))$ and $(x + h, f(x + h))$: "
        "$$\\frac{\\Delta y}{\\Delta x} = \\frac{f(x + h) - f(x)}{h}$$ "
        "Central difference quotient: $\\frac{f(x + \\Delta x) - f(x - \\Delta x)}{2\\Delta x}$."
    ),
    "difference sequence": (
        "A sequence formed by taking consecutive differences of a sequence $\\{x_k\\}$: "
        "$$\\Delta x_k = x_{k+1} - x_k, \\quad \\Delta^m x_k = \\Delta^{m-1}x_{k+1} - \\Delta^{m-1}x_k$$"
    ),
    "differential": (
        "1. For a single-variable differentiable function $y = F(x)$, the differential is $dF = F'(x) \\, dx = \\frac{dF}{dx} \\, dx$. "
        "2. For multivariable functions $F(x_1, \\dots, x_n)$, total differential is: "
        "$$dF = \\sum_{i=1}^n \\frac{\\partial F}{\\partial x_i} \\, dx_i$$"
    ),
    "differential coefficient": (
        "The limiting ratio of the increment in a function to the increment in the independent variable: "
        "$$\\frac{dy}{dx} = y' = \\lim_{\\Delta x \\to 0} \\frac{\\Delta y}{\\Delta x}$$"
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    d_entries = data.get('D', [])
    word_map = {item.get('word', '').strip().lower(): item for item in d_entries}

    for target_word, new_def in BATCH_D1_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section D: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_D1_DEFINITIONS)} definitions in Section D Batch 1.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    print("Rebuilding core_dictionary.js index...")
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
