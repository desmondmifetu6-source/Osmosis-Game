"""
enrich_section_e_batch_2.py
===========================
Section E Formula Enrichment - Batch 2 (Terms 46 to 90)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

e_entries = data.get('E', [])

UPDATES = {
    # 46. elliptic curve
    490: (
        "The set of solutions to a non-singular cubic equation in two variables, whose complex solutions geometrically form a torus (a donut-shaped surface). In algebraic geometry and cryptography, an elliptic curve over a field $K$ is typically expressed in Weierstrass form:\n\n"
        "$$y^2 + a_1 xy + a_3 y = x^3 + a_2 x^2 + a_4 x + a_6$$\n\n"
        "which simplifies over fields of characteristic not equal to 2 or 3 to the short Weierstrass equation:\n\n"
        "$$y^2 = x^3 + ax + b$$\n\n"
        "with non-zero discriminant $\\Delta = -16(4a^3 + 27b^2) \\neq 0$ ensuring smoothness."
    ),

    # 47. elliptic function
    491: (
        "In complex analysis, a doubly periodic meromorphic function $f: \\mathbb{C} \\to \\mathbb{C} \\cup \\{\\infty\\}$. While a singly periodic function like sine has a single period $\\omega = 2\\pi$ satisfying $\\sin(z + 2\\pi) = \\sin(z)$, a doubly periodic function has two fundamental periods $\\omega_1, \\omega_2 \\in \\mathbb{C}$ whose ratio $\\tau = \\omega_2 / \\omega_1$ is not real ($\x5ctau \\notin \\mathbb{R}$), satisfying:\n\n"
        "$$f(z + \\omega_1) = f(z + \\omega_2) = f(z)$$\n\n"
        "for all $z$. Prototypical examples include the Weierstrass $\\wp$-function and Jacobi elliptic functions, which arise naturally by inverting elliptic integrals."
    ),

    # 48. elliptic integral
    493: (
        "A definite or indefinite integral of the general form:\n\n"
        "$$I = \\int R(x, y)\\,dx$$\n\n"
        "where $R(x, y)$ is a rational function of $x$ and $y$, and $y^2 = P(x)$ is a cubic or quartic polynomial in $x$ with no repeated roots. Such integrals cannot generally be expressed in terms of elementary functions. They are categorized into Legendre canonical forms of the first, second, and third kinds. When the limits span a full period (e.g., $x \\in [0, 1]$), the integral is complete; otherwise, it is an incomplete elliptic integral. Named 'elliptic' because they first arose in computing the arc length of an ellipse."
    ),

    # 49. elliptic paraboloid
    494: (
        "A quadric surface whose sections parallel to one coordinate plane are ellipses, while sections parallel to the other two planes are parabolas (vertical cross-sections are parabolas and horizontal cross-sections are ellipses). In standard Cartesian coordinates, its canonical equation is:\n\n"
        "$$\\frac{z}{c} = \\frac{x^2}{a^2} + \\frac{y^2}{b^2}$$\n\n"
        "where $a, b > 0$ dictate curvature along the principal planes. For $a = b$, it is a circular paraboloid of revolution, opening upward for $c > 0$ and downward for $c < 0$. This geometry underlies parabolic dish reflectors, satellite antennas, and the equilibrium surface of rotating liquids in liquid-mirror telescopes."
    ),

    # 50. emissivity
    553: (
        "The quantitative measure of a surface's effectiveness in emitting thermal radiation, defined as the ratio of radiant flux emitted by the surface to that emitted by an ideal blackbody at the same thermodynamic temperature $T$:\n\n"
        "$$\\varepsilon = \\frac{E(T)}{E_{\\text{blackbody}}(T)}$$\n\n"
        "Its symbol is $\\varepsilon$, with values ranging strictly between $0$ (ideal reflector) and $1$ (ideal blackbody). Emissivity varies with material composition, surface roughness, temperature, wavelength (spectral emissivity $\\varepsilon_\\lambda$), and emission angle."
    ),

    # 51. empirical formula
    565: (
        "The chemical formula showing the simplest whole-number ratio of atoms of each element in a compound, as opposed to the actual molecular formula or spatial arrangement. For example, the empirical formula for hydrogen peroxide (molecular formula $\\text{H}_2\\text{O}_2$) is $\\text{HO}$, representing a $1:1$ ratio of $\\text{H}$ to $\\text{O}$. For ethanoic acid (molecular formula $\\text{C}_2\\text{H}_4\\text{O}_2$, structural $\\text{CH}_3\\text{COOH}$), the empirical formula is $\\text{CH}_2\\text{O}$. Empirical formulas are calculated directly from experimental percentage elemental composition data, and serve as the standard formulation for giant ionic lattices (such as $\\text{CaCl}_2$) and network solids (such as $\\text{SiO}_2$)."
    ),

    # 52. encephalisation/encephalization quotient, eq
    588: (
        "A relative brain size metric defined as the ratio of observed brain mass $M_{\\text{brain}}$ of a species to the expected brain mass $E(M_{\\text{brain}})$ predicted for an average animal of the same body mass $M_{\\text{body}}$:\n\n"
        "$$\\text{EQ} = \\frac{M_{\\text{brain}}}{E(M_{\\text{brain}})}$$\n\n"
        "The allometric expected brain mass is typically calculated using the power law:\n\n"
        "$$E(M_{\\text{brain}}) = 0.12\\,M_{\\text{body}}^{2/3}$$\n\n"
        "(or exponent $3/4$ in specific mammalian taxa). EQ is used in comparative biology and evolutionary anthropology to assess encephalization and cognitive capabilities beyond basic somatic maintenance."
    ),

    # 53. endothermic reaction
    657: (
        "A chemical or physical transformation that absorbs thermal energy from its surroundings, characterized by a positive standard enthalpy of reaction:\n\n"
        "$$\\Delta H > 0$$\n\n"
        "Because heat is absorbed, the enthalpy of products exceeds that of reactants ($H_{\\text{products}} > H_{\\text{reactants}}$). Standard Gibbs free energy relates to enthalpy by $\\Delta G^\\circ = \\Delta H^\\circ - T\\Delta S^\\circ$. Examples include photosynthesis, thermal decomposition of calcium carbonate ($\\text{CaCO}_3 \\to \\text{CaO} + \\text{CO}_2$), and dissolution of ammonium chloride ($\\text{NH}_4\\text{Cl}$) in water."
    ),

    # 54. endow
    661: (
        "In mathematics, to equip an underlying set with additional mathematical structure—such as an operation, a topology, an ordering, or a distance metric—so that the combined system behaves as a unified mathematical object. For example, a metric space $(S, d)$ consists of a set $S$ endowed with a metric function $d: S \\times S \\to \\mathbb{R}_{\\ge 0}$."
    ),

    # 58. enthalpy
    726: (
        "A state function and fundamental thermodynamic potential denoted by $H$ and defined as the sum of internal energy $U$ and the product of pressure $p$ and volume $V$:\n\n"
        "$$H = U + pV$$\n\n"
        "Under constant-pressure (isobaric) conditions with only expansion work, the enthalpy change equals the heat exchanged:\n\n"
        "$$\\Delta H = q_p$$\n\n"
        "In endothermic processes $\\Delta H > 0$, while in exothermic processes $\\Delta H < 0$. Specific enthalpy is defined on a per-unit-mass basis as $h = \\frac{H}{m} = u + pv$."
    ),

    # 59. entire surd
    728: (
        "A surd in which all terms are irrational and which has no rational factor other than $\\pm 1$. In other words, the entire expression remains under the radical sign. Examples include $\\sqrt{3}$, $\\sqrt{7}$, $\\sqrt{10}$, and $\\sqrt[3]{50}$ (as opposed to mixed surds like $2\\sqrt{3} = \\sqrt{12}$)."
    ),

    # 60. entropy
    736: (
        "1. In classical thermodynamics, a state function $S$ quantifying the irreversibility and unavailable energy of a system, defined along a reversible path by Clausius as:\n\n"
        "$$\\Delta S = \\int \\frac{dq_{\\text{rev}}}{T}$$\n\n"
        "with SI units $\\text{J}\\cdot\\text{K}^{-1}$. The second law of thermodynamics mandates that for any isolated system, $\\Delta S_{\\text{isolated}} \\ge 0$. 2. In statistical mechanics, Boltzmann's entropy formula relates entropy to the number of accessible microstates $\\Omega$:\n\n"
        "$$S = k_B \\ln \\Omega$$\n\n"
        "where $k_B = 1.380649 \\times 10^{-23}\\,\\text{J}\\cdot\\text{K}^{-1}$. 3. In information theory, the Shannon entropy of a discrete random variable $X$ with outcomes $x_i$ and probability distribution $P(x_i)$ is:\n\n"
        "$$H(X) = -\\sum_{i} P(x_i) \\log_2 P(x_i)$$"
    ),

    # 61. epitrochoid
    844: (
        "A roulette planar curve traced by a point rigidly attached at distance $c$ from the center of a circle of radius $b$ that rolls without slipping along the exterior of a fixed circle of radius $a$. Its parametric equations are:\n\n"
        "$$x(t) = (a + b)\\cos(t) - c\\cos\\left(\\frac{a + b}{b}t\\right)$$\n\n"
        "$$y(t) = (a + b)\\sin(t) - c\\sin\\left(\\frac{a + b}{b}t\\right)$$\n\n"
        "When $c = b$, the curve reduces to an epicycloid; when $c < b$, it traces an epitrochoid (such as the combustion chamber contour of a Wankel rotary engine)."
    ),

    # 63. epoxyethane
    852: (
        "A colourless, toxic, highly flammable gas with molecular formula $\\text{C}_2\\text{H}_4\\text{O}$ (ethylene oxide), molar mass $44.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.882\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-111.3\\,^\\circ\\text{C}$ ($161.85\\,\\text{K}$), and boiling point $10.7\\,^\\circ\\text{C}$ ($283.85\\,\\text{K}$). It is the simplest cyclic ether (three-membered oxirane ring), produced industrially by the direct catalytic oxidation of ethene over silver:\n\n"
        "$$2\\text{C}_2\\text{H}_4 + \\text{O}_2 \\xrightarrow{\\text{Ag}} 2\\text{C}_2\\text{H}_4\\text{O}$$\n\n"
        "It serves as a prime chemical intermediate for manufacturing ethylene glycol (ethane-1,2-diol), ethoxylates, and as a gaseous sterilizing agent in healthcare."
    ),

    # 64. equal fraction
    862: (
        "The theorem of equal fractions in arithmetic and proportion: if two or more ratios are equal, such that:\n\n"
        "$$\\frac{a_1}{b_1} = \\frac{a_2}{b_2} = \\dots = \\frac{a_n}{b_n} = k$$\n\n"
        "then for any set of real multipliers $l_1, l_2, \\dots, l_n$ with $\\sum_{i=1}^n l_i b_i \\neq 0$, the weighted combination equals the original common ratio:\n\n"
        "$$\\frac{l_1 a_1 + l_2 a_2 + \\dots + l_n a_n}{l_1 b_1 + l_2 b_2 + \\dots + l_n b_n} = k$$"
    ),

    # 65. equality
    866: (
        "A fundamental binary relation on mathematical objects asserting that two expressions denote the exact same mathematical entity, written $a = b$. Equality satisfies three fundamental equivalence properties: reflexivity ($a = a$), symmetry ($a = b \\implies b = a$), and transitivity ($a = b$ and $b = c \\implies a = c$). It also preserves algebraic operations: if $a = b$, then $a + c = b + c$ and $ac = bc$ for any scalar $c$."
    ),

    # 66. equality of matrices
    867: (
        "Two matrices $A = [a_{ij}]$ and $B = [b_{ij}]$ are defined to be equal ($A = B$) if and only if they share identical orders ($m \\times n$) and each corresponding entry is equal ($a_{ij} = b_{ij}$ for all $1 \\le i \\le m$ and $1 \\le j \\le n$). For example, if $\\begin{pmatrix} x & 3 \\\\ 6 & y \\end{pmatrix} = \\begin{pmatrix} 2 & a \\\\ t & 5 \\end{pmatrix}$, then by element-wise comparison $x = 2$, $a = 3$, $t = 6$, and $y = 5$."
    ),

    # 68. equation
    871: (
        "A formal mathematical statement asserting that two expressions joined by an equals sign ($=$) have the same value. Equations are fundamentally classified into: (1) identities, which hold true for all valid values in the domain of the variables (e.g., $x^2 - 1 = (x - 1)(x + 1)$ or $\\cos^2\\theta + \\sin^2\\theta = 1$); and (2) conditional equations, which hold true only for specific values of the variable(s) called roots or solutions (e.g., $x^2 - 1 = 3 \\implies x = \\pm 2$). In chemistry, a balanced equation represents the conservation of mass and atoms in a chemical transformation."
    ),

    # 69. equation of state
    872: (
        "A constitutive equation relating thermodynamic state variables—most notably pressure ($p$), volume ($V$), absolute temperature ($T$), and amount of substance ($n$)—for a homogeneous substance. The ideal gas law serves as the baseline equation of state:\n\n"
        "$$pV = nRT$$\n\n"
        "while real gases exhibiting intermolecular forces and finite molecular volume are described by relations such as the van der Waals equation of state:\n\n"
        "$$\\left(p + \\frac{a n^2}{V^2}\\right)(V - nb) = nRT$$"
    ),

    # 71. equation ofa circle
    874: (
        "The equation describing the set of all points $(x, y)$ in a plane equidistant from a fixed center $C(h, k)$ by radius $r$. The standard (center-radius) form is:\n\n"
        "$$(x - h)^2 + (y - k)^2 = r^2$$\n\n"
        "For example, a circle centered at $(2, -4)$ with radius $5$ has the equation $(x - 2)^2 + (y + 4)^2 = 25$. Expanding yields the general equation of a circle:\n\n"
        "$$x^2 + y^2 + 2gx + 2fy + c = 0$$\n\n"
        "with center $(-g, -f)$ and radius $r = \\sqrt{g^2 + f^2 - c}$."
    ),

    # 72. equation ofa parabola
    875: (
        "The Cartesian equation representing the locus of points equidistant from a fixed focus point and a directrix line. In standard form with vertex $(h, k)$ and focal length $p$:\n\n"
        "$$(y - k)^2 = 4p(x - h)$$\n\n"
        "when the parabola has a horizontal axis of symmetry (directrix $x = h - p$), opening rightward for $p > 0$ and leftward for $p < 0$. When the axis of symmetry is vertical (directrix $y = k - p$), the equation is:\n\n"
        "$$(x - h)^2 = 4p(y - k)$$\n\n"
        "opening upward for $p > 0$ and downward for $p < 0$."
    ),

    # 73. equations of motion
    876: (
        "The standard kinematic formulas relating displacement ($s$), initial velocity ($u$), final velocity ($v$), constant acceleration ($a$), and elapsed time ($t$) for linear motion under uniform acceleration:\n\n"
        "$$v = u + at$$\n\n"
        "$$s = ut + \\frac{1}{2}at^2$$\n\n"
        "$$v^2 = u^2 + 2as$$\n\n"
        "with the auxiliary relation $s = \\left(\\frac{u + v}{2}\\right)t$."
    ),

    # 74. equilibrant
    893: (
        "A single force which, when applied to a system of forces acting on a rigid body, establishes static equilibrium by exactly balancing the resultant vector sum and resultant torque. For concurrent forces $\\mathbf{F}_1, \\mathbf{F}_2, \\dots, \\mathbf{F}_n$, the equilibrant force $\\mathbf{F}_E$ is equal in magnitude and directly opposite in direction to the resultant force:\n\n"
        "$$\\mathbf{F}_E = -\\sum_{i=1}^n \\mathbf{F}_i$$\n\n"
        "so that $\\sum \\mathbf{F} = \\mathbf{0}$."
    ),

    # 75. equilibrium constant
    897: (
        "The numerical value of the reaction quotient for a reversible chemical reaction when dynamic chemical equilibrium is reached at a specific temperature. For a general reaction $a\\text{A} + b\\text{B} \\rightleftharpoons c\\text{C} + d\\text{D}$, the equilibrium constant in terms of molar concentrations is:\n\n"
        "$$K_c = \\frac{[\\text{C}]^c [\\text{D}]^d}{[\\text{A}]^a [\\text{B}]^b}$$\n\n"
        "and in terms of partial pressures for gases is $K_p = \\frac{p_{\\text{C}}^c p_{\\text{D}}^d}{p_{\\text{A}}^a p_{\\text{B}}^b} = K_c(RT)^{\\Delta n_g}$. The equilibrium constant relates to the standard Gibbs free energy change via $\\Delta G^\\circ = -RT \\ln K_{\\text{eq}}$."
    ),

    # 76. equilibrium point
    901: (
        "A constant or stationary solution $\\mathbf{y}^*$ to an autonomous system of ordinary differential equations $\\frac{d\\mathbf{y}}{dt} = \\mathbf{f}(\\mathbf{y})$, defined such that the rate of change vanishes:\n\n"
        "$$\\mathbf{f}(\\mathbf{y}^*) = \\mathbf{0}$$\n\n"
        "The local stability of the equilibrium point is determined by linearizing the system around $\\mathbf{y}^*$ and computing the eigenvalues of the Jacobian matrix $J = \\nabla \\mathbf{f}(\\mathbf{y}^*)$."
    ),

    # 77. equinumerous
    912: (
        "Two sets $A$ and $B$ are said to be equinumerous (or equipollent / having identical cardinality, denoted $A \\approx B$ or $|A| = |B|$) if there exists a bijective function (one-to-one and onto) $f: A \\to B$. By the Cantor-Bernstein-Schröder theorem, if $|A| \\le |B|$ and $|B| \\le |A|$, then $|A| = |B|$."
    ),

    # 78. equivalent
    928: (
        "1. In chemistry, the amount of a substance that supplies or reacts with one mole of hydrogen ions ($\\text{H}^+$) in an acid-base neutralization or one mole of electrons ($e^-$) in a redox reaction: $\\text{Equivalent Weight} = \\frac{\\text{Molar Mass}}{n}$. 2. In mathematics, sharing an equivalence relation (denoted $\\equiv$ or $\\sim$) satisfying reflexivity, symmetry, and transitivity. 3. In matrix algebra, two $m \\times n$ matrices $A$ and $B$ are equivalent if there exist non-singular invertible matrices $P$ and $Q$ such that $A = PBQ$. 4. In logic, two propositions $P$ and $Q$ are logically equivalent ($P \\iff Q$) if they share identical truth values under all interpretations."
    ),

    # 79. equivalent equations
    933: (
        "Equations that have exactly the same solution set over a specified domain. For example, $2x + 4 = 8$ and $x = 2$ are equivalent equations because the unique value satisfying both is $x = 2$."
    ),

    # 80. equivalent norms
    937: (
        "Two norms $\\|\\cdot\\|_a$ and $\\|\\cdot\\|_b$ on a real or complex vector space $V$ are topologically equivalent if there exist positive real constants $c_1, c_2 > 0$ such that for all vectors $\\mathbf{x} \\in V$:\n\n"
        "$$c_1 \\|\\mathbf{x}\\|_a \\le \\|\\mathbf{x}\\|_b \\le c_2 \\|\\mathbf{x}\\|_a$$\n\n"
        "Equivalent norms induce the exact same open sets, convergence of sequences, and topology. On any finite-dimensional vector space, all norms are equivalent."
    ),

    # 81. error
    976: (
        "The quantitative discrepancy between an observed, measured, or computed value $x$ and the true value $x_0$. 1. Absolute error: $\\Delta x = |x - x_0|$. 2. Relative error: $\\delta_x = \\frac{|x - x_0|}{|x_0|}$. 3. Percentage error: $\\text{PE} = \\frac{|x - x_0|}{|x_0|} \\times 100\\%$. In numerical computation, total computational error is the combined effect of algorithmic truncation error and machine floating-point round-off error."
    ),

    # 82. essentially bounded
    1014: (
        "A measurable function $f: X \\to \\mathbb{R}$ on a measure space $(X, \\Sigma, \\mu)$ is essentially bounded if there exists a finite real constant $C \\ge 0$ such that the set $\\{x \\in X : |f(x)| > C\\}$ has measure zero. The essential supremum of $|f|$ is defined as:\n\n"
        "$$\\|f\\|_{L^\\infty} = \\operatorname{ess\\,sup}_{x \\in X} |f(x)| = \\inf\\{C \\ge 0 : \\mu(\\{x : |f(x)| > C\\}) = 0\}$$"
    ),

    # 83. estimate of mean
    1017: (
        "For grouped frequency distributions where individual raw data points are unavailable, the sample mean $\\bar{x}$ is estimated using the midpoint $x_i$ and corresponding frequency $f_i$ of each class interval:\n\n"
        "$$\\bar{x} \\approx \\frac{\\sum f_i x_i}{\\sum f_i}$$\n\n"
        "where $\\sum f_i = N$ is the total frequency."
    ),

    # 84. ethanal
    1026: (
        "A volatile aldehyde (acetaldehyde) with molecular formula $\\text{C}_2\\text{H}_4\\text{O}$ and structural formula $\\text{CH}_3\\text{CHO}$, molar mass $44.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.788\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-123.5\\,^\\circ\\text{C}$ ($150\\,\\text{K}$), and boiling point $20.8\\,^\\circ\\text{C}$ ($293.95\\,\\text{K}$). Formed by the gentle oxidation of ethanol:\n\n"
        "$$\\text{CH}_3\\text{CH}_2\\text{OH} + [\\text{O}] \\xrightarrow{\\text{Cr}_2\\text{O}_7^{2-}/\\text{H}^+} \\text{CH}_3\\text{CHO} + \\text{H}_2\\text{O}$$\n\n"
        "or through the Wacker process by catalytic palladium-copper oxidation of ethylene."
    ),

    # 85. ethanal trimer
    1027: (
        "Paraldehyde, a cyclic trimer of acetaldehyde with chemical formula $\\text{C}_6\\text{H}_{12}\\text{O}_3$ (2,4,6-trimethyl-1,3,5-trioxane), molar mass $132.16\\,\\text{g}\\cdot\\text{mol}^{-1}$, melting point $12\\,^\\circ\\text{C}$ ($285\\,\\text{K}$), and boiling point $124\\,^\\circ\\text{C}$ ($397\\,\\text{K}$). Formed by treating acetaldehyde with traces of concentrated sulfuric acid:\n\n"
        "$$3\\text{CH}_3\\text{CHO} \\xrightarrow{\\text{H}_2\\text{SO}_4} \\text{C}_6\\text{H}_{12}\\text{O}_3$$"
    ),

    # 86. ethane
    1029: (
        "A colourless, odourless alkane gas with molecular formula $\\text{C}_2\\text{H}_6$, structural formula $\\text{CH}_3-\\text{CH}_3$, molar mass $30.07\\,\\text{g}\\cdot\\text{mol}^{-1}$, melting point $-183\\,^\\circ\\text{C}$ ($90.4\\,\\text{K}$), and boiling point $-89\\,^\\circ\\text{C}$ ($184.6\\,\\text{K}$). The second member of the alkane homologous series ($C_n H_{2n+2}$), undergoing complete combustion according to:\n\n"
        "$$2\\text{C}_2\\text{H}_6 + 7\\text{O}_2 \\to 4\\text{CO}_2 + 6\\text{H}_2\\text{O} \\quad (\\Delta H_c^\\circ = -1560.7\\,\\text{kJ}\\cdot\\text{mol}^{-1})$$"
    ),

    # 87. ethane-1,2-diol
    1030: (
        "Ethylene glycol, a colourless, viscous, sweet-tasting hygroscopic dihydric alcohol with molecular formula $\\text{C}_2\\text{H}_6\\text{O}_2$ and structural formula $\\text{HO}-\\text{CH}_2-\\text{CH}_2-\\text{OH}$, molar mass $62.07\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $1.1132\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-12.9\\,^\\circ\\text{C}$ ($260\\,\\text{K}$), and boiling point $197.3\\,^\\circ\\text{C}$ ($470.5\\,\\text{K}$). Produced industrially by the hydrolysis of epoxyethane:\n\n"
        "$$\\text{C}_2\\text{H}_4\\text{O} + \\text{H}_2\\text{O} \\to \\text{HO}-\\text{CH}_2-\\text{CH}_2-\\text{OH}$$\n\n"
        "Widely used as an automotive antifreeze (due to substantial freezing-point depression) and as a monomer in polyethylene terephthalate (PET) synthesis."
    ),

    # 88. ethanedioic acid
    1031: (
        "Oxalic acid, a poisonous dicarboxylic acid with molecular formula $\\text{H}_2\\text{C}_2\\text{O}_4$ or $(\\text{COOH})_2$, typically crystallized as the dihydrate $(\\text{COOH})_2 \\cdot 2\\text{H}_2\\text{O}$, with molar mass $90.03\\,\\text{g}\\cdot\\text{mol}^{-1}$ (anhydrous) and $126.07\\,\\text{g}\\cdot\\text{mol}^{-1}$ (dihydrate), melting point $189\\text{--}191\\,^\\circ\\text{C}$. Ionizes in two steps with $pK_{a1} = 1.25$ and $pK_{a2} = 4.14$. Its conjugate base, the oxalate ion ($\\text{C}_2\\text{O}_4^{2-}$), functions as a bidentate chelating agent for transition metal ions and a primary reducing agent in redox titrations with permanganate:\n\n"
        "$$5\\text{C}_2\\text{O}_4^{2-} + 2\\text{MnO}_4^- + 16\\text{H}^+ \\to 10\\text{CO}_2 + 2\\text{Mn}^{2+} + 8\\text{H}_2\\text{O}$$"
    ),

    # 89. ethanenitrile
    1032: (
        "Acetonitrile, a colourless polar aprotic liquid with chemical formula $\\text{CH}_3\\text{CN}$, molar mass $41.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.786\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-45\\,^\\circ\\text{C}$ ($228\\,\\text{K}$), and boiling point $82\\,^\\circ\\text{C}$ ($355\\,\\text{K}$). Exhibiting a large dipole moment of $\\mu = 3.92\\,\\text{D}$ and dielectric constant $\\varepsilon_r \\approx 37.5$, it is an essential solvent in high-performance liquid chromatography (HPLC) and non-aqueous electrochemistry."
    ),

    # 90. ethanoic acid
    1034: (
        "Acetic acid, a clear monocarboxylic acid with chemical formula $\\text{CH}_3\\text{COOH}$ (or $\\text{C}_2\\text{H}_4\\text{O}_2$), molar mass $60.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $1.049\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $16.6\\,^\\circ\\text{C}$ ($289.8\\,\\text{K}$), and boiling point $118.1\\,^\\circ\\text{C}$ ($391.3\\,\\text{K}$). In dilute aqueous solution ($4\\text{--}8\\%$) it forms household vinegar. It is a weak acid with dissociation equilibrium:\n\n"
        "$$\\text{CH}_3\\text{COOH} + \\text{H}_2\\text{O} \\rightleftharpoons \\text{CH}_3\\text{COO}^- + \\text{H}_3\\text{O}^+ \\quad (pK_a = 4.76)$$"
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(e_entries):
        w = e_entries[idx]['word']
        e_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")

data['E'] = e_entries

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section E Batch 2.")
