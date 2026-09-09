"""
enrich_section_f_batch_2.py
===========================
Section F Formula Enrichment - Batch 2 (Terms 51 to 102)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

f_entries = data.get('F', [])

UPDATES = {
    # 51. folium
    682: (
        "1. The Folium of Descartes, a planar cubic algebraic curve featuring a single loop in the first quadrant, a node at the origin, and an oblique asymptote. Its Cartesian equation is:\n\n"
        "$$x^3 + y^3 = 3axy$$\n\n"
        "with real asymptote $x + y + a = 0$. In polar coordinates: $r(\\theta) = \\frac{3a\\sin\\theta\\cos\\theta}{\\sin^3\\theta + \\cos^3\\theta}$. 2. In geology and petrology, a thin, leaf-like mineral stratum or lamella characteristic of metamorphic foliation."
    ),

    # 52. force
    735: (
        "Any external vector interaction that alters or tends to alter a body's state of rest or uniform rectilinear motion, or induces mechanical deformation. Formulated in Newton's second law of motion as the time rate of change of linear momentum $\\mathbf{p}$:\n\n"
        "$$\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = m\\mathbf{a}$$\n\n"
        "(for constant mass $m$). The SI derived unit of force is the newton ($\\text{N}$), where $1\\,\\text{N} = 1\\,\\text{kg}\\cdot\\text{m}\\cdot\\text{s}^{-2}$."
    ),

    # 53. force constant
    737: (
        "In physical chemistry and classical mechanics, the proportionality constant $k$ (bond stiffness) in Hooke's law relating restoring force $F$ to infinitesimal displacement $x$ from equilibrium:\n\n"
        "$$F = -kx$$\n\n"
        "For a diatomic molecule modeled as a quantum harmonic oscillator, the fundamental vibrational frequency $\\nu$ is directly governed by the force constant $k$ and reduced mass $\\mu$:\n\n"
        "$$\\nu = \\frac{1}{2\\pi}\\sqrt{\\frac{k}{\\mu}}$$\n\n"
        "measured in units of $\\text{N}\\cdot\\text{m}^{-1}$ or $\\text{dyn}\\cdot\\text{cm}^{-1}$."
    ),

    # 54. force of mortality
    745: (
        "In actuarial mathematics and demography, the instantaneous failure rate or hazard rate $\\mu(x)$ of an individual at age $x$, defined in terms of the survival function $S(x)$:\n\n"
        "$$\\mu(x) = -\\frac{1}{S(x)}\\frac{dS(x)}{dx} = -\\frac{d}{dx}\\ln S(x)$$\n\n"
        "Under Gompertz-Makeham mortality law: $\\mu(x) = A + B c^x$."
    ),

    # 55. formal equivalence
    770: (
        "In symbolic logic and model theory, a semantic relationship between two open formulas $\\varphi(x)$ and $\\psi(x)$ asserting that their universal closures are materially equivalent across all interpretations in a domain:\n\n"
        "$$\\forall x \\, [\\varphi(x) \\iff \\psi(x)]$$\n\n"
        "For example, in arithmetic, the formal algebraic identity $a + b = b + a$ holds under universal quantification."
    ),

    # 56. formal system
    774: (
        "An axiomatic mathematical structure consisting of a formal language alphabet $\\mathcal{L}$, a set of formation rules defining well-formed formulas (wffs), a collection of designated axioms $\\mathcal{A}$, and deductive inference rules $\\mathcal{R}$ (such as *modus ponens*):\n\n"
        "$$\\mathcal{S} = \\langle \\mathcal{L}, \\mathcal{A}, \\mathcal{R} \\rangle$$\n\n"
        "Enables rigorous deduction of theorems through finite syntactic proof sequences independently of intuitive interpretation."
    ),

    # 57. formaldehyde
    775: (
        "Methanal, the simplest aldehyde, a pungent, toxic gas with chemical formula $\\text{HCHO}$ (or $\\text{CH}_2\\text{O}$), molar mass $30.03\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.8153\\,\\text{g}\\cdot\\text{cm}^{-3}$ (at $-20\\,^\\circ\\text{C}$), melting point $-92\\,^\\circ\\text{C}$ ($181\\,\\text{K}$), and boiling point $-19\\,^\\circ\\text{C}$ ($254\\,\\text{K}$). Its $37\\%$ stabilized aqueous solution is formalin, widely utilized as an embalming fluid, biological tissue fixative, and precursor to bakelite and urea-formaldehyde resins."
    ),

    # 58. formation constant
    780: (
        "The thermodynamic equilibrium constant $K_f$ (or stability constant $\\beta_n$) describing the coordination complex formation between a central metal ion $\\text{M}^{m+}$ and ligands $\\text{L}$ in aqueous solution:\n\n"
        "$$\\text{M}^{m+} + n\\text{L} \\rightleftharpoons [\\text{ML}_n]^{m+}, \\quad K_f = \\frac{[\\text{ML}_n^{m+}]}{[\\text{M}^{m+}][\\text{L}]^n}$$\n\n"
        "A large formation constant indicates high thermodynamic stability of the coordination entity."
    ),

    # 59. formation rules
    781: (
        "In formal logic and proof theory, recursive syntactic rules specifying the construction of well-formed formulas (wffs): (1) Any propositional atom or predicate applied to $n$ terms $P(t_1, \\dots, t_n)$ is a wff; (2) If $\\alpha$ is a wff, then negation $\\neg \\alpha$ is a wff; (3) If $\\alpha$ and $\\beta$ are wffs, then binary connectives $(\\alpha \\land \\beta)$, $(\\alpha \\lor \\beta)$, and $(\\alpha \\to \\beta)$ are wffs; (4) If $\\alpha$ is a wff and $x$ is a variable, then quantified formulas $\\forall x\\,\\alpha$ and $\\exists x\\,\\alpha$ are wffs."
    ),

    # 60. formazans
    783: (
        "A class of organic azo-hydrazone compounds characterized by the characteristic conjugated backbone $\\text{R}^1-\\text{N}=\\text{N}-\\text{C}(\\text{R}^3)=\\text{N}-\\text{NH}-\\text{R}^2$, derived from the parent compound $\\text{H}_2\\text{N}-\\text{N}=\\text{CH}-\\text{N}=\\text{NH}$. Readily formed by the biochemical enzymatic reduction of tetrazolium salts (such as MTT or WST-1) in cell viability assays."
    ),

    # 61. formula
    786: (
        "A concise symbolic mathematical or chemical expression conveying a quantitative rule, relationship, or identity. For example, geometric formulas include circle area $A = \\pi r^2$ and circumference $C = 2\\pi r = \\pi D$; in physics, Einstein's mass-energy equivalence $E = mc^2$; and in chemistry, empirical and molecular formulas representing elemental stoichiometry."
    ),

    # 63. formula unit
    788: (
        "The lowest whole-number stoichiometric ratio of ions or constituent atoms represented in an empirical formula for ionic crystals or network covalent lattices lacking discrete molecules. Representative examples include $\\text{NaCl}$ for rock salt ($1:1$ ratio of $\\text{Na}^+$ to $\\text{Cl}^-$), $\\text{K}_2\\text{O}$ ($2:1$), and $\\text{SiO}_2$ ($1:2$ in quartz network lattice)."
    ),

    # 64. formula weight
    789: (
        "The sum of the standard atomic weights (relative atomic masses $A_r$) of all atoms comprising the chemical formula unit of a substance:\n\n"
        "$$\\text{FW} = \\sum_{i} n_i A_{r, i}$$\n\n"
        "Expressed in atomic mass units ($\\text{u}$) or molar mass units ($\\text{g}\\cdot\\text{mol}^{-1}$). Standardly applied to ionic compounds such as sodium chloride ($\\text{NaCl}$, $\\text{FW} = 22.99 + 35.45 = 58.44\\,\\text{g}\\cdot\\text{mol}^{-1}$)."
    ),

    # 66. formyl trichloride
    791: (
        "Chloroform (trichloromethane), a dense, volatile, sweet-smelling trihalomethane liquid with chemical formula $\\text{CHCl}_3$, molar mass $119.38\\,\\text{g}\\cdot\\text{mol}^{-1}$, relative density $1.489\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-63.5\\,^\\circ\\text{C}$ ($209.5\\,\\text{K}$), and boiling point $61.2\\,^\\circ\\text{C}$ ($334.3\\,\\text{K}$). Formed by the chlorination of methane or the haloform reaction with acetone. Extensively utilized as an industrial organic solvent and formerly as an inhalation anaesthetic."
    ),

    # 67. forward difference
    801: (
        "In numerical analysis and finite difference calculus, the discrete operator $\\Delta$ defined for a function $f(x)$ with uniform step size $h$ as:\n\n"
        "$$\\Delta f(x) = f(x + h) - f(x)$$\n\n"
        "The $n$-th forward difference is obtained iteratively:\n\n"
        "$$\\Delta^n f(x) = \\sum_{k=0}^n (-1)^{n-k} \\binom{n}{k} f(x + kh)$$\n\n"
        "For example, $\\Delta^2 f(x) = f(x + 2h) - 2f(x + h) + f(x)$, forming the basis of Newton's forward difference interpolation formula."
    ),

    # 68. four ierc oeff icie nts (fourier coefficients)
    820: (
        "The orthogonal projection amplitudes in the Fourier series expansion of a $2\\pi$-periodic integrable function $f(x)$. In trigonometric form:\n\n"
        "$$a_n = \\frac{1}{\\pi}\\int_{-\\pi}^\\pi f(x)\\cos(nx)\\,dx \\quad (n \\ge 0)$$\n\n"
        "$$b_n = \\frac{1}{\\pi}\\int_{-\\pi}^\\pi f(x)\\sin(nx)\\,dx \\quad (n \\ge 1)$$\n\n"
        "and in complex exponential form:\n\n"
        "$$c_n = \\frac{1}{2\\pi}\\int_{-\\pi}^\\pi f(x)e^{-inx}\\,dx \\quad (n \\in \\mathbb{Z})$$\n\n"
        "where $f(x) \\sim \\sum_{n=-\\infty}^\\infty c_n e^{inx} = \\frac{a_0}{2} + \\sum_{n=1}^\\infty [a_n \\cos(nx) + b_n \\sin(nx)]$."
    ),

    # 69. four squares theorem
    821: (
        "Lagrange's four-square theorem (proved in 1770), stating that every positive natural number $n \\in \\mathbb{N}$ can be represented as the sum of at most four integer squares:\n\n"
        "$$n = a^2 + b^2 + c^2 + d^2$$\n\n"
        "where $a, b, c, d \\in \\mathbb{Z}_{\\ge 0}$. For example, $5 = 2^2 + 1^2 + 0^2 + 0^2$, $15 = 3^2 + 2^2 + 1^2 + 1^2$, and $23 = 3^2 + 3^2 + 2^2 + 1^2$."
    ),

    # 70. four-colour theorem
    825: (
        "The graph-theoretic theorem proved by Kenneth Appel and Wolfgang Haken (1976), asserting that any planar map separated into contiguous regions can be colored using no more than four distinct colors such that no two regions sharing a common boundary line receive the same color:\n\n"
        "$$\\chi(G) \\le 4$$\n\n"
        "for every planar graph $G$. It was the first major mathematical theorem proved with computer-assisted computational verification."
    ),

    # 71. fourier's law of conduction
    834: (
        "The constitutive phenomenological law governing conductive thermal energy transfer formulated by Joseph Fourier (1822). In one dimension:\n\n"
        "$$q_x = -k \\frac{dT}{dx}$$\n\n"
        "and in three-dimensional vector form:\n\n"
        "$$\\mathbf{q} = -k \\nabla T$$\n\n"
        "where $\\mathbf{q}$ is local heat flux density ($\\text{W}\\cdot\\text{m}^{-2}$), $k$ is material thermal conductivity ($\\text{W}\\cdot\\text{m}^{-1}\\cdot\\text{K}^{-1}$), and $\\nabla T$ is the spatial temperature gradient."
    ),

    # 72. fractile
    852: (
        "In descriptive statistics, the cut-off value dividing the total area under a probability distribution or cumulative frequency curve into specified proportions. Common fractiles include quartiles ($Q_1, Q_2, Q_3$ dividing data into quarters at $25\\%$, $50\\%$, and $75\\%$), deciles ($D_1$ to $D_9$ in tenths), and percentiles ($P_1$ to $P_{99}$ in hundredths). For grouped data with class width $w$, the $k$-th quartile is computed as:\n\n"
        "$$Q_k = L + \\left(\\frac{\\frac{k N}{4} - CF}{f}\\right) w$$\n\n"
        "where $L$ is lower class boundary, $CF$ is cumulative frequency before the quartile class, and $f$ is class frequency."
    ),

    # 73. fraction
    853: (
        "A numerical representation of the quotient of two quantities $\\frac{a}{b}$ where $b \\neq 0$ ($a$ is the numerator and $b$ is the denominator). The standard arithmetic field operations for rational fractions are:\n\n"
        "$$\\frac{a}{b} \\pm \\frac{c}{d} = \\frac{ad \\pm bc}{bd}, \\quad \\frac{a}{b} \\times \\frac{c}{d} = \\frac{ac}{bd}, \\quad \\frac{a}{b} \\div \\frac{c}{d} = \\frac{ad}{bc}$$\n\n"
        "2. In petroleum refining and industrial chemistry, a distilled cut of hydrocarbon mixtures collected within a specific boiling range during fractional distillation."
    ),

    # 74. fractional linear transformation
    858: (
        "A Möbius transformation on the extended complex plane $\\widehat{\\mathbb{C}} = \\mathbb{C} \\cup \\{\\infty\\}$, defined as a rational conformal mapping of the form:\n\n"
        "$$f(z) = \\frac{az + b}{cz + d}$$\n\n"
        "where $a, b, c, d \\in \\mathbb{C}$ with non-vanishing determinant $ad - bc \\neq 0$. Möbius transformations form a group under composition isomorphic to the projective linear group $\\operatorname{PGL}(2, \\mathbb{C})$, mapping generalized circles (circles and lines) strictly to generalized circles."
    ),

    # 75. fractional part
    859: (
        "The difference between a real number $x$ and its integer floor part $\\lfloor x \\rfloor$, denoted $\\{x\\}$ or $\\operatorname{frac}(x)$:\n\n"
        "$$\\{x\\} = x - \\lfloor x \\rfloor$$\n\n"
        "Strictly satisfying $0 \\le \\{x\\} < 1$ for all $x \\in \\mathbb{R}$. For example, $\\{3.42\\} = 3.42 - 3 = 0.42$, while for negative values $\\{-3.42\\} = -3.42 - (-4) = 0.58$."
    ),

    # 76. frattini subgroup
    883: (
        "The characteristic subgroup $\\Phi(G)$ of a group $G$, defined as the intersection of all maximal proper subgroups of $G$:\n\n"
        "$$\\Phi(G) = \\bigcap_{M <_{\\max} G} M$$\n\n"
        "(defined as $G$ if $G$ has no maximal subgroups). An element $g \\in G$ belongs to $\\Phi(G)$ if and only if $g$ is a non-generator of $G$ (if $G = \\langle X, g \\rangle$, then $G = \\langle X \\rangle$)."
    ),

    # 77. fredholm alternative
    887: (
        "A fundamental theorem in functional analysis and integral equations established by Ivar Fredholm. For a compact linear operator $K: X \\to X$ on a Banach space and identity operator $I$, exactly one of the following alternatives holds:\n\n"
        "1. The homogeneous equation $(I - K)x = 0$ has only the trivial solution $x = 0$, in which case the inhomogeneous equation $(I - K)x = y$ has a unique solution for every $y \\in X$.\n"
        "2. The homogeneous equation has non-trivial solutions ($\\dim \\ker(I - K) = n < \\infty$), and $(I - K)x = y$ has solutions if and only if $y$ is orthogonal to the kernel of the adjoint operator $\\ker(I - K^*)$."
    ),

    # 78. free group
    898: (
        "In abstract algebra, the free group $F_S$ generated by a set $S$, consisting of all equivalence classes of reduced words formed from elements of $S$ and their formal inverses $s^{-1}$, subject only to trivial cancellations $s s^{-1} = s^{-1} s = e$. It satisfies the universal mapping property: any set map from $S$ into a group $G$ extends uniquely to a group homomorphism $\\bar{\\phi}: F_S \\to G$."
    ),

    # 79. free module
    900: (
        "A module $M$ over a ring $R$ that possesses a basis $\\{e_i\\}_{i \\in I}$ of linearly independent elements that span $M$. Every element $x \\in M$ is uniquely represented as a finite linear combination:\n\n"
        "$$x = \\sum_{i \\in I} r_i e_i \\quad (r_i \\in R)$$\n\n"
        "Every vector space over a field is a free module. Over general rings, submodules of free modules are not necessarily free unless $R$ is a principal ideal domain."
    ),

    # 80. free space propagation model
    907: (
        "In wireless communications and radio frequency engineering, the theoretical attenuation of an electromagnetic wave propagating along an unobstructed line-of-sight path in free space (Friis transmission equation). The path loss $\\text{FSPL}$ is:\n\n"
        "$$\\text{FSPL} = \\left(\\frac{4\\pi d}{\\lambda}\\right)^2 = \\left(\\frac{4\\pi d f}{c}\\right)^2$$\n\n"
        "where $d$ is transmission distance, $\\lambda$ is wavelength, $f$ is frequency, and $c$ is the speed of light."
    ),

    # 81. frenet formulae
    930: (
        "The Frenet-Serret differential formulas describing the kinematic curvature and torsion of a smooth space curve parametrized by arc length $s$, relating the orthonormal moving frame of unit tangent $\\mathbf{T}$, principal normal $\\mathbf{N}$, and binormal $\\mathbf{B} = \\mathbf{T} \\times \\mathbf{N}$:\n\n"
        "$$\\frac{d\\mathbf{T}}{ds} = \\kappa \\mathbf{N}$$\n\n"
        "$$\\frac{d\\mathbf{N}}{ds} = -\\kappa \\mathbf{T} + \\tau \\mathbf{B}$$\n\n"
        "$$\\frac{d\\mathbf{B}}{ds} = -\\tau \\mathbf{N}$$\n\n"
        "where $\\kappa(s) > 0$ is the curvature and $\\tau(s)$ is the torsion of the curve."
    ),

    # 82. frequency
    934: (
        "The number of occurrences of a repeating periodic event per unit time, denoted $f$ or $\\nu$. Measured in hertz ($\\text{Hz}$), where $1\\,\\text{Hz} = 1\\,\\text{s}^{-1}$. Related to period $T$, angular frequency $\\omega$, wave speed $v$, and wavelength $\\lambda$ by:\n\n"
        "$$f = \\frac{1}{T} = \\frac{\\omega}{2\\pi} = \\frac{v}{\\lambda}$$"
    ),

    # 83. fresnel integrals
    952: (
        "Two transcendental special functions $S(x)$ and $C(x)$ occurring extensively in the analysis of near-field wave optics and Fresnel diffraction, defined as:\n\n"
        "$$S(x) = \\int_0^x \\sin\\left(\\frac{\\pi t^2}{2}\\right)dt, \\quad C(x) = \\int_0^x \\cos\\left(\\frac{\\pi t^2}{2}\\right)dt$$\n\n"
        "Their parametric trajectory $(C(t), S(t))$ in the complex plane forms the Euler spiral (clothoid or Cornu spiral), converging as $x \\to \\infty$ to the limit point $(1/2, 1/2)$."
    ),

    # 84. friction factor
    955: (
        "1. In tribology, the dimensionless coefficient of friction $\\mu$, defined as the ratio of limiting frictional force $F_f$ to the normal reaction force $R_N$:\n\n"
        "$$\\mu = \\frac{F_f}{R_N}$$\n\n"
        "2. In fluid dynamics, the Darcy-Weisbach friction factor $f_D$ relating frictional pressure drop $\\Delta p$ along a pipe of diameter $D$ and length $L$ to mean fluid velocity $v$:\n\n"
        "$$\\Delta p = f_D \\frac{L}{D}\\frac{\\rho v^2}{2}$$"
    ),

    # 85. fritz john conditions/theorem
    963: (
        "In mathematical optimization, a necessary optimality criterion for constrained nonlinear programming problems with objective $f(\\mathbf{x})$ and constraints $g_i(\\mathbf{x}) \\le 0, h_j(\\mathbf{x}) = 0$. At a local optimum $\\mathbf{x}^*$, there exist multipliers $\\lambda_0 \\ge 0, \\boldsymbol{\\mu} \\ge \\mathbf{0}, \\boldsymbol{\\lambda}$ (not all simultaneously zero) satisfying:\n\n"
        "$$\\lambda_0 \\nabla f(\\mathbf{x}^*) + \\sum_{i=1}^m \\mu_i \\nabla g_i(\\mathbf{x}^*) + \\sum_{j=1}^p \\lambda_j \\nabla h_j(\\mathbf{x}^*) = \\mathbf{0}$$\n\n"
        "with complementary slackness $\\mu_i g_i(\\mathbf{x}^*) = 0$. When constraint qualification holds, $\\lambda_0 > 0$, yielding the standard Karush-Kuhn-Tucker (KKT) conditions."
    ),

    # 86. frobenius group
    964: (
        "In finite group theory, a transitive permutation group $G$ on a finite set $\\Omega$ such that no non-identity element fixes more than one point, and some non-identity element fixes at least one point. Equivalently, $G$ contains a proper non-trivial subgroup $H$ (the Frobenius complement) such that $H \\cap g H g^{-1} = \\{e\\}$ for all $g \\notin H$. By Frobenius' theorem, the set $N = (G \\setminus \\bigcup_{g} g H g^{-1}) \\cup \\{e\\}$ is a normal subgroup (the Frobenius kernel), forming a semidirect product $G = N \\rtimes H$."
    ),

    # 87. frobenius method
    965: (
        "A power-series method for solving linear second-order ordinary differential equations near a regular singular point $x = x_0$:\n\n"
        "$$y''(x) + \\frac{p(x)}{x - x_0}y'(x) + \\frac{q(x)}{(x - x_0)^2}y(x) = 0$$\n\n"
        "by proposing a Frobenius generalized power series solution:\n\n"
        "$$y(x) = (x - x_0)^r \\sum_{n=0}^\\infty a_n (x - x_0)^n \\quad (a_0 \\neq 0)$$\n\n"
        "where the index parameter $r$ is determined from the roots of the quadratic indicial equation $r(r - 1) + p_0 r + q_0 = 0$."
    ),

    # 88. frobenius norm
    966: (
        "The matrix norm induced by treating an $m \\times n$ matrix $\\mathbf{A} = [a_{ij}]$ as a vector in Euclidean space $\\mathbb{C}^{m \\times n}$, defined as the square root of the sum of the absolute squares of its elements:\n\n"
        "$$\\|\\mathbf{A}\\|_F = \\sqrt{\\sum_{i=1}^m \\sum_{j=1}^n |a_{ij}|^2} = \\sqrt{\\operatorname{Tr}(\\mathbf{A}^* \\mathbf{A})} = \\sqrt{\\sum_{i=1}^{\\min(m, n)} \\sigma_i^2}$$\n\n"
        "where $\\sigma_i$ are the singular values of $\\mathbf{A}$."
    ),

    # 89. frontier
    977: (
        "In general topology, the topological boundary or frontier of a subset $A \\subseteq X$, denoted $\\partial A$ or $\\operatorname{Fr}(A)$, defined as the set of points belonging both to the closure of $A$ and the closure of its complement:\n\n"
        "$$\\operatorname{Fr}(A) = \\overline{A} \\cap \\overline{X \\setminus A} = \\overline{A} \\setminus \\operatorname{int}(A)$$\n\n"
        "For example, in $\\mathbb{R}$, $\\operatorname{Fr}((0, 1)) = \\{0, 1\\}$, while the frontier of the rational numbers $\\mathbb{Q}$ is the entire real line $\\mathbb{R}$."
    ),

    # 90. fréchet differential
    1003: (
        "In functional analysis, the derivative $Df(x)$ of a mapping $f: U \\to Y$ between real or complex normed spaces (where $U \\subseteq X$ is open). $f$ is Fréchet differentiable at $x \\in U$ if there exists a bounded linear operator $T \\in \\mathcal{L}(X, Y)$ such that:\n\n"
        "$$\\lim_{\\|h\\|_X \\to 0} \\frac{\\|f(x + h) - f(x) - T(h)\\|_Y}{\\|h\\|_X} = 0$$\n\n"
        "The operator $T = Df(x)$ is the Fréchet derivative of $f$ at $x$."
    ),

    # 91. fubini's theorem
    1006: (
        "A cornerstone theorem of measure theory and multivariable calculus, formulated by Guido Fubini (1907). It states that if $f(x, y)$ is an integrable function on the product measure space $X \\times Y$ ($\x5cint_{X \\times Y} |f|\\,d(\\mu \\times \\nu) < \\infty$), then the double integral equals the iterated integrals in either order:\n\n"
        "$$\\iint_{X \\times Y} f(x, y)\\,d(\\mu \\times \\nu) = \\int_X \\left(\\int_Y f(x, y)\\,d\\nu(y)\\right)d\\mu(x) = \\int_Y \\left(\\int_X f(x, y)\\,d\\mu(x)\\right)d\\nu(y)$$"
    ),

    # 92. function
    1033: (
        "A fundamental mathematical mapping $f: X \\to Y$ that associates each element $x$ of a set $X$ (the domain) with exactly one element $y = f(x)$ of a set $Y$ (the codomain). The set of all actual outputs $\\{f(x) : x \\in X\\} \\subseteq Y$ is the range (or image). In applied sciences, functional relationships model causal mechanisms, input-output signal transducers, and software subroutines."
    ),

    # 93. functional equations
    1041: (
        "Equations in which the unknown variables represent functions rather than numbers or vectors. Prototypical examples include Cauchy's additive functional equation:\n\n"
        "$$f(x + y) = f(x) + f(y)$$\n\n"
        "(whose only continuous solutions are linear maps $f(x) = cx$), d'Alembert's functional equation $f(x+y) + f(x-y) = 2f(x)f(y)$, and the reflection formula for the Riemann zeta function $\\zeta(s) = 2^s \\pi^{s-1} \\sin\\left(\\frac{\\pi s}{2}\\right)\\Gamma(1-s)\\zeta(1-s)$."
    ),

    # 94. fundamental constants
    1051: (
        "Universal physical quantities whose values are invariant throughout spacetime, forming the bedrock of modern physical theories. Prime examples with exact defined SI values include the speed of light in vacuum ($c = 299792458\\,\\text{m}\\cdot\\text{s}^{-1}$), Planck constant ($h = 6.62607015 \\times 10^{-34}\\,\\text{J}\\cdot\\text{s}$), elementary electric charge ($e = 1.602176634 \\times 10^{-19}\\,\\text{C}$), Boltzmann constant ($k_B = 1.380649 \\times 10^{-23}\\,\\text{J}\\cdot\\text{K}^{-1}$), and the universal gravitational constant ($G \\approx 6.67430 \\times 10^{-11}\\,\\text{m}^3\\cdot\\text{kg}^{-1}\\cdot\\text{s}^{-2}$)."
    ),

    # 95. fundamental form
    1054: (
        "In differential geometry of surfaces, quadratic forms describing intrinsic metric and extrinsic curvature of a smooth parametrized surface $\\mathbf{r}(u, v)$. 1. First fundamental form (metric tensor governing arc length $ds^2$):\n\n"
        "$$I = E\\,du^2 + 2F\\,du\\,dv + G\\,dv^2$$\n\n"
        "where $E = \\mathbf{r}_u \\cdot \\mathbf{r}_u$, $F = \\mathbf{r}_u \\cdot \\mathbf{r}_v$, $G = \\mathbf{r}_v \\cdot \\mathbf{r}_v$. 2. Second fundamental form (curvature):\n\n"
        "$$II = L\\,du^2 + 2M\\,du\\,dv + N\\,dv^2$$\n\n"
        "where $L = \\mathbf{r}_{uu} \\cdot \\mathbf{n}$, $M = \\mathbf{r}_{uv} \\cdot \\mathbf{n}$, $N = \\mathbf{r}_{vv} \\cdot \\mathbf{n}$, classifying surface points as elliptic ($LN - M^2 > 0$), parabolic ($LN - M^2 = 0$), or hyperbolic ($LN - M^2 < 0$)."
    ),

    # 96. fundamental matrix
    1057: (
        "1. In ordinary differential equations, an $n \\times n$ matrix $\\mathbf{\\Phi}(t)$ whose columns form a linearly independent basis of solutions to a homogeneous linear system $\\frac{d\\mathbf{y}}{dt} = \\mathbf{A}(t)\\mathbf{y}$, satisfying $\\det \\mathbf{\\Phi}(t) \\neq 0$. 2. In epipolar computer vision geometry, a $3 \\times 3$ matrix $\\mathbf{F}$ of rank 2 relating matching points $\\mathbf{x} \\leftrightarrow \\mathbf{x}'$ across stereo images by the epipolar constraint $\\mathbf{x}'^T \\mathbf{F} \\mathbf{x} = 0$."
    ),

    # 97. fundamental theorem of algebra
    1063: (
        "The foundational theorem first rigorously proven by Carl Friedrich Gauss, asserting that the field of complex numbers $\\mathbb{C}$ is algebraically closed. Specifically, every non-zero single-variable polynomial $P(z) = a_n z^n + a_{n-1} z^{n-1} + \\dots + a_1 z + a_0$ of degree $n \\ge 1$ with complex coefficients has at least one complex root, and factorizes completely into linear factors over $\\mathbb{C}$:\n\n"
        "$$P(z) = a_n \\prod_{k=1}^n (z - z_k)$$\n\n"
        "counting roots according to their algebraic multiplicities."
    ),

    # 98. fundamental theorem of arithmetic
    1064: (
        "The unique factorization theorem in number theory, stating that every integer $n > 1$ can be expressed as a product of prime numbers in a representation that is unique up to the order of the prime factors:\n\n"
        "$$n = p_1^{a_1} p_2^{a_2} \\dots p_k^{a_k}$$\n\n"
        "where $p_1 < p_2 < \\dots < p_k$ are distinct primes and $a_i \\in \\mathbb{Z}^+$ are positive integer exponents."
    ),

    # 99. fundamental theorem of calculus
    1065: (
        "The foundational dual theorem bridging differential and integral calculus: 1. First Part: if $f$ is continuous on $[a, b]$, then the accumulated area function $F(x) = \\int_a^x f(t)\\,dt$ is differentiable with derivative:\n\n"
        "$$\\frac{d}{dx}\\left(\\int_a^x f(t)\\,dt\\right) = f(x)$$\n\n"
        "2. Second Part: if $F$ is any antiderivative of $f$ ($F'(x) = f(x)$), then the definite integral evaluates as:\n\n"
        "$$\\int_a^b f(x)\\,dx = F(b) - F(a)$$"
    ),

    # 100. fundamental theorem of projectivity
    1066: (
        "In projective geometry, the theorem stating that a projective transformation (projectivity) between two one-dimensional projective spaces (projective lines) is uniquely and completely determined by specifying the images of three distinct collinear points."
    ),

    # 101. furan
    1082: (
        "A five-membered heterocyclic aromatic compound containing four carbon atoms and one oxygen atom in the ring, with molecular formula $\\text{C}_4\\text{H}_4\\text{O}$, molar mass $68.07\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.936\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-85.6\\,^\\circ\\text{C}$ ($187.55\\,\\text{K}$), and boiling point $31.3\\,^\\circ\\text{C}$ ($304.45\\,\\text{K}$). Exhibiting an aromatic sextet ($6\\pi$ electrons from four $p$-electrons on carbon and one oxygen lone pair), it undergoes electrophilic aromatic substitution predominantly at the 2-position ($\\alpha$-position)."
    ),

    # 102. furfural
    1086: (
        "Furan-2-carbaldehyde, an aromatic heterocyclic aldehyde with chemical formula $\\text{C}_5\\text{H}_4\\text{O}_2$ (or $\\text{C}_4\\text{H}_3\\text{O}-\\text{CHO}$), molar mass $96.08\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $1.16\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-37\\,^\\circ\\text{C}$ ($236\\,\\text{K}$), and boiling point $161.7\\,^\\circ\\text{C}$ ($434.8\\,\\text{K}$). Industrially synthesized via acid-catalyzed dehydration of agricultural pentosan biomass (such as corncobs and oat hulls) containing xylose:\n\n"
        "$$\\text{C}_5\\text{H}_{10}\\text{O}_5 \\xrightarrow{\\text{H}^+,\\,\\Delta} \\text{C}_5\\text{H}_4\\text{O}_2 + 3\\text{H}_2\\text{O}$$\n\n"
        "Widely applied as a renewable platform chemical for furfuryl alcohol, furan, and THF resin production."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(f_entries):
        w = f_entries[idx]['word']
        f_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")

data['F'] = f_entries

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section F Batch 2.")
