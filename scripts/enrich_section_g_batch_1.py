"""
enrich_section_g_batch_1.py
===========================
Section G Formula Enrichment - Batch 1 (Candidates 1 to 40)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

g_entries = data.get('G', [])

UPDATES = {
    # 1. g2 (Candidate 1, index 10)
    10: (
        "In categorical data analysis and statistics, the likelihood-ratio goodness-of-fit test statistic "
        "(deviance), denoted $G^2$. It evaluates whether observed contingency frequencies $O_i$ differ "
        "significantly from model-expected frequencies $E_i$:\n\n"
        "$$G^2 = 2 \\sum_{i=1}^k O_i \\ln\\left(\\frac{O_i}{E_i}\\right)$$\n\n"
        "Under the null hypothesis that the fitted log-linear model is correct, $G^2$ asymptotically follows a "
        "chi-squared distribution $\\chi^2(\\text{df})$ as the sample size $N \\to \\infty$. It serves as a "
        "direct likelihood-ratio counterpart to Pearson's chi-squared test statistic $X^2 = \\sum \\frac{(O_i - E_i)^2}{E_i}$."
    ),

    # 2. gadolinium (Candidate 2, index 16)
    16: (
        "A rare silvery-white metallic chemical element belonging to the lanthanide series of the Periodic Table "
        "(symbol $\\text{Gd}$, atomic number $64$, relative atomic mass $157.25$). Ground-state electron configuration: "
        "$[\\text{Xe}]\\,4f^7 5d^1 6s^2$. Melting point $1313\\,^\\circ\\text{C}$ ($1586\\,\\text{K}$), boiling point "
        "$3273\\,^\\circ\\text{C}$ ($3546\\,\\text{K}$), and density $7.90\\,\\text{g/cm}^3$. With seven unpaired $4f$ "
        "electrons, $\\text{Gd}^{3+}$ possesses the highest electronic magnetic moment among stable ions ($7.94\\,\\mu_B$), "
        "making gadolinium strongly ferromagnetic below its Curie temperature $T_C = 292\\,\\text{K}$ ($19\\,^\\circ\\text{C}$) "
        "and exceptionally paramagnetic above it. Widely used as a paramagnetic contrast agent in magnetic resonance imaging (MRI)."
    ),

    # 3. gain (Candidate 3, index 18)
    18: (
        "A measure of the ability of a two-port electronic circuit (such as an amplifier) to increase the amplitude or power "
        "of a signal from input to output. Voltage gain $A_v$ and current gain $A_i$ are dimensionless linear ratios:\n\n"
        "$$A_v = \\frac{V_{\\text{out}}}{V_{\\text{in}}}, \\quad A_i = \\frac{I_{\\text{out}}}{I_{\\text{in}}}$$\n\n"
        "Power gain $A_p$ is expressed as $A_p = \\frac{P_{\\text{out}}}{P_{\\text{in}}}$. On a logarithmic decibel ($\\text{dB}$) scale:\n\n"
        "$$G_{\\text{dB}} = 10 \\log_{10}\\left(\\frac{P_{\\text{out}}}{P_{\\text{in}}}\\right) = 20 \\log_{10}\\left(\\frac{V_{\\text{out}}}{V_{\\text{in}}}\\right)$$\n\n"
        "where input and output impedances are matched."
    ),

    # 4. galactose (Candidate 4, index 35)
    35: (
        "A hexose monosaccharide and aldohexose stereoisomer of glucose (C-4 epimer), with molecular formula "
        "$\\text{C}_6\\text{H}_{12}\\text{O}_6$, molar mass $180.16\\,\\text{g/mol}$, density $1.723\\,\\text{g/cm}^3$, and melting "
        "point $167\\,^\\circ\\text{C}$ ($440\\,\\text{K}$). It condenses with D-glucose via a $\\beta(1\\to 4)$-glycosidic bond "
        "to form the disaccharide lactose:\n\n"
        "$$\\text{C}_6\\text{H}_{12}\\text{O}_6 \\text{ (galactose)} + \\text{C}_6\\text{H}_{12}\\text{O}_6 \\text{ (glucose)} "
        "\\xrightarrow{\\text{synthase}} \\text{C}_{12}\\text{H}_{22}\\text{O}_{11} \\text{ (lactose)} + \\text{H}_2\\text{O}$$\n\n"
        "Crucial in human metabolism, where it is converted to glucose-6-phosphate via the Leloir pathway."
    ),

    # 5. galilean telescope (Candidate 5, index 45)
    45: (
        "A refracting optical telescope designed by Galileo Galilei in 1609, consisting of a convergent (convex) objective lens "
        "of long positive focal length $f_o > 0$ and a divergent (concave) eyepiece lens of short negative focal length $f_e < 0$. "
        "The separation distance between the lenses equals the algebraic sum of their focal lengths:\n\n"
        "$$L = f_o + f_e = f_o - |f_e|$$\n\n"
        "The angular magnification $M$ is positive, producing an upright (erect) virtual image without requiring an erecting prism:\n\n"
        "$$M = -\\frac{f_o}{f_e} = +\\frac{f_o}{|f_e|}$$\n\n"
        "Though compact, it suffers from a narrow field of view and lack of an accessible real exit pupil."
    ),

    # 6. galilean transformation (Candidate 6, index 46)
    46: (
        "The coordinate transformation in Newtonian mechanics relating the space-time coordinates of an event observed in an inertial "
        "reference frame $S$ with coordinates $(x, y, z, t)$ to an inertial frame $S'$ moving with uniform velocity $v$ along their common $x$-axis:\n\n"
        "$$x' = x - vt, \\quad y' = y, \\quad z' = z, \\quad t' = t$$\n\n"
        "Assuming absolute time ($t' = t$), Newton's laws of motion remain invariant under Galilean transformations (Galilean relativity). "
        "For velocities approaching the speed of light $c$, it is superseded by the Lorentz transformation of special relativity."
    ),

    # 7. gallic acid (Candidate 7, index 52)
    52: (
        "A trihydroxybenzoic acid (3,4,5-trihydroxybenzoic acid), an organic aromatic compound with molecular formula "
        "$\\text{C}_6\\text{H}_2(\\text{OH})_3\\text{COOH}$ (or $\\text{C}_7\\text{H}_6\\text{O}_5$), molar mass $170.12\\,\\text{g/mol}$, "
        "density $1.70\\,\\text{g/cm}^3$, and melting point $250\\,^\\circ\\text{C}$ ($523\\,\\text{K}$, decomposes). Found in gallnuts, "
        "sumac, witch hazel, and oak bark. Thermal decarboxylation yields pyrogallol (1,2,3-trihydroxybenzene) and carbon dioxide:\n\n"
        "$$\\text{C}_6\\text{H}_2(\\text{OH})_3\\text{COOH} \\xrightarrow{\\Delta} \\text{C}_6\\text{H}_3(\\text{OH})_3 + \\text{CO}_2$$\n\n"
        "Acts as a powerful antioxidant, astringent, and precursor in the historical synthesis of iron gall ink."
    ),

    # 8. gallium arsenide (Candidate 8, index 55)
    55: (
        "A III-V binary direct-bandgap semiconductor compound composed of equal parts gallium and arsenic (chemical formula $\\text{GaAs}$, "
        "molar mass $144.645\\,\\text{g/mol}$, melting point $1238\\,^\\circ\\text{C}$ / $1511\\,\\text{K}$). Crystallises in the zincblende "
        "lattice structure. It features a direct bandgap of $E_g \\approx 1.424\\,\\text{eV}$ at $300\\,\\text{K}$ and an electron mobility "
        "($\\mu_e \\approx 8500\\,\\text{cm}^2\\cdot\\text{V}^{-1}\\cdot\\text{s}^{-1}$) nearly six times higher than silicon, enabling ultra-fast "
        "switching in monolithic microwave integrated circuits (MMICs), high-efficiency multi-junction solar cells, laser diodes, and photodetectors."
    ),

    # 9. gamma distribution (Candidate 9, index 81)
    81: (
        "A continuous two-parameter probability distribution family on $(0, \\infty)$. Parametrized by shape parameter $\\alpha > 0$ (or $k$) "
        "and rate parameter $\\beta > 0$ (where $\\theta = 1/\\beta$ is the scale parameter), its probability density function (PDF) is:\n\n"
        "$$f(x; \\alpha, \\beta) = \\frac{\\beta^\\alpha}{\\Gamma(\\alpha)} x^{\\alpha - 1} e^{-\\beta x} \\quad \\text{for } x > 0$$\n\n"
        "where $\\Gamma(\\alpha)$ is the Euler gamma function. Its population mean and variance are given by:\n\n"
        "$$\\mu = \\mathbb{E}[X] = \\frac{\\alpha}{\\beta} = k\\theta, \\quad \\sigma^2 = \\operatorname{Var}(X) = \\frac{\\alpha}{\\beta^2} = k\\theta^2$$\n\n"
        "Special cases include the exponential distribution (when $\\alpha = 1$) and the chi-squared distribution $\\chi^2(k)$ (when $\\alpha = k/2, \\beta = 1/2$)."
    ),

    # 10. gamma function (Candidate 10, index 83)
    83: (
        "A fundamental transcendental special function extending the factorial to complex numbers. For $\\operatorname{Re}(z) > 0$, "
        "it is defined via the Euler integral of the second kind:\n\n"
        "$$\\Gamma(z) = \\int_0^\\infty t^{z-1} e^{-t} \\, dt$$\n\n"
        "Satisfies the foundational functional recurrence $\\Gamma(z + 1) = z\\Gamma(z)$, giving for any positive integer $n$:\n\n"
        "$$\\Gamma(n + 1) = n!$$\n\n"
        "Gauss's infinite limit product representation is:\n\n"
        "$$\\Gamma(z) = \\lim_{n \\to \\infty} \\frac{n! \\, n^z}{z(z+1)(z+2)\\cdots(z+n)}$$\n\n"
        "Weierstrass's Hadamard canonical product is:\n\n"
        "$$\\frac{1}{\\Gamma(z)} = z e^{\\gamma z} \\prod_{n=1}^\\infty \\left(1 + \\frac{z}{n}\\right) e^{-z/n}$$\n\n"
        "where $\\gamma \\approx 0.577215$ is the Euler-Mascheroni constant. Also satisfies Euler's reflection formula:\n\n"
        "$$\\Gamma(z)\\Gamma(1 - z) = \\frac{\\pi}{\\sin(\\pi z)} \\implies \\Gamma\\left(\\frac{1}{2}\\right) = \\sqrt{\\pi}$$"
    ),

    # 11. gamma radiation (Candidate 11, index 85)
    85: (
        "High-energy, highly penetrating electromagnetic radiation originating from transitions within excited atomic nuclei during radioactive decay "
        "or nuclear reactions. Occupies the highest frequency band of the electromagnetic spectrum, with wavelengths $\\lambda < 10^{-11}\\,\\text{m}$ "
        "($< 10\\,\\text{pm}$) and photon energies $E$ exceeding $100\\,\\text{keV}$:\n\n"
        "$$E = h\\nu = \\frac{hc}{\\lambda} \\ge 100\\,\\text{keV}$$\n\n"
        "where $h = 6.626 \\times 10^{-34}\\,\\text{J}\\cdot\\text{s}$ and $c = 3.0 \\times 10^8\\,\\text{m/s}$. Emitted by radioisotopes such as "
        "Cobalt-60 ($^{60}_{27}\\text{Co}$) and Caesium-137 ($^{137}_{55}\\text{Cs}$). Attenuation through matter obeys the Beer-Lambert exponential law:\n\n"
        "$$I = I_0 e^{-\\mu x}$$\n\n"
        "where $\\mu$ is the linear attenuation coefficient and $x$ is absorber thickness. Widely used in radiotherapy, industrial radiography, and food irradiation."
    ),

    # 12. gamma-aminobutyric acid (Candidate 12, index 86)
    86: (
        "4-Aminobutanoic acid (GABA), the chief inhibitory neurotransmitter in the developmentally mature mammalian central nervous system. "
        "Molecular formula $\\text{C}_4\\text{H}_9\\text{NO}_2$, molar mass $103.12\\,\\text{g/mol}$, density $1.11\\,\\text{g/cm}^3$, melting point "
        "$203.7\\,^\\circ\\text{C}$ ($477\\,\\text{K}$). Biosynthesized from L-glutamate via decarboxylation catalyzed by glutamate decarboxylase (GAD) "
        "with pyridoxal phosphate (PLP):\n\n"
        "$$\\text{HOOC-CH}_2\\text{-CH}_2\\text{-CH(NH}_2\\text{)-COOH} \\xrightarrow{\\text{GAD}} "
        "\\text{H}_2\\text{N-CH}_2\\text{-CH}_2\\text{-CH}_2\\text{-COOH} + \\text{CO}_2$$\n\n"
        "Acts on ionotropic $\\text{GABA}_A$ and $\\text{GABA}_C$ ligand-gated chloride channels (inducing hyperpolarizing $\\text{Cl}^-$ influx) "
        "and metabotropic $\\text{GABA}_B$ G-protein coupled receptors."
    ),

    # 13. gap series (Candidate 13, index 103)
    103: (
        "A power series with lacunary structure (a lacunary power series) in which the indices of non-zero terms exhibit growing gaps:\n\n"
        "$$f(z) = \\sum_{k=0}^\\infty c_k z^{n_k}$$\n\n"
        "where the strictly increasing sequence of exponents $n_k$ satisfies Hadamard's gap condition:\n\n"
        "$$\\frac{n_{k+1}}{n_k} \\ge \\lambda > 1$$\n\n"
        "By Hadamard's lacunary value theorem, if such a series has radius of convergence $R = 1$, the boundary of its disk of convergence "
        "$|z| = 1$ constitutes a natural boundary across which the analytic function $f(z)$ cannot be analytically continued."
    ),

    # 14. gas (Candidate 14, index 109)
    109: (
        "One of the fundamental classical states of matter, characterized by particles that are widely separated, in constant random thermal motion, "
        "and lacking fixed shape or definite volume. Under the kinetic molecular theory, the average translational kinetic energy per molecule depends solely on absolute temperature $T$:\n\n"
        "$$\\langle E_k \\rangle = \\frac{1}{2} m \\langle v^2 \\rangle = \\frac{3}{2} k_B T$$\n\n"
        "where $k_B = 1.3806 \\times 10^{-23}\\,\\text{J/K}$ is Boltzmann's constant. The root-mean-square speed of gas molecules of molar mass $M$ is:\n\n"
        "$$v_{\\text{rms}} = \\sqrt{\\frac{3RT}{M}}$$\n\n"
        "At low pressures and high temperatures, real gases closely follow the ideal gas equation $PV = nRT$."
    ),

    # 15. gas chromatography (Candidate 15, index 112)
    112: (
        "An analytical separation technique for volatilized compounds partitioning between a mobile inert gas phase (e.g. $\\text{He}$, $\\text{N}_2$, $\\text{H}_2$) "
        "and a stationary liquid or solid phase. The retention factor (capacity factor) $k'$ of an analyte with retention time $t_R$ and dead time $t_M$ is:\n\n"
        "$$k' = \\frac{t_R - t_M}{t_M}$$\n\n"
        "Chromatographic peak efficiency is quantified by the number of theoretical plates $N$:\n\n"
        "$$N = 16\\left(\\frac{t_R}{W}\\right)^2 = 5.545\\left(\\frac{t_R}{W_{1/2}}\\right)^2$$\n\n"
        "where $W$ is peak width at baseline and $W_{1/2}$ is width at half-height. Separation resolution between adjacent peaks is "
        "$R_s = \\frac{2(t_{R2} - t_{R1})}{W_1 + W_2}$."
    ),

    # 16. gas constant (Candidate 16, index 114)
    114: (
        "The universal physical constant of proportionality $R$ appearing in the ideal gas law and across chemical thermodynamics:\n\n"
        "$$PV = nRT$$\n\n"
        "It equals the product of Avogadro's constant $N_A$ and the Boltzmann constant $k_B$ ($R = N_A k_B$). Standard CODATA values:\n\n"
        "$$R = 8.314462618\\,\\text{J}\\cdot\\text{K}^{-1}\\cdot\\text{mol}^{-1}$$\n\n"
        "$$R = 0.0820574\\,\\text{L}\\cdot\\text{atm}\\cdot\\text{K}^{-1}\\cdot\\text{mol}^{-1} = 1.9872\\,\\text{cal}\\cdot\\text{K}^{-1}\\cdot\\text{mol}^{-1} = 8.3145 \\times 10^7\\,\\text{erg}\\cdot\\text{K}^{-1}\\cdot\\text{mol}^{-1}$$\n\n"
        "Dictates gas expansion work, molar heat capacities ($C_{p,m} - C_{v,m} = R$), and chemical equilibrium constants via $\\Delta G^\\circ = -RT \\ln K$."
    ),

    # 17. gas laws (Candidate 17, index 122)
    122: (
        "Empirical physical laws describing the thermodynamic relationships among pressure $P$, volume $V$, absolute temperature $T$, and amount of substance $n$:\n\n"
        "1. **Boyle's Law** ($T, n = \\text{const}$): $P V = k_1 \\iff P_1 V_1 = P_2 V_2$\n\n"
        "2. **Charles's Law** ($P, n = \\text{const}$): $\\frac{V}{T} = k_2 \\iff \\frac{V_1}{T_1} = \\frac{V_2}{T_2}$\n\n"
        "3. **Gay-Lussac's (Pressure) Law** ($V, n = \\text{const}$): $\\frac{P}{T} = k_3 \\iff \\frac{P_1}{T_1} = \\frac{P_2}{T_2}$\n\n"
        "4. **Combined Gas Law** ($n = \\text{const}$):\n\n"
        "$$\\frac{P_1 V_1}{T_1} = \\frac{P_2 V_2}{T_2} = \\text{constant}$$\n\n"
        "Combined with Avogadro's law ($V \\propto n$), they unify into the ideal gas equation of state $PV = nRT$."
    ),

    # 18. gast herm omet er (gas thermometer) (Candidate 18, index 138)
    138: (
        "A precision primary thermometer in which temperature is measured via the pressure or volume variations of an ideal gas (such as helium or hydrogen). "
        "In a constant-volume gas thermometer, the Celsius temperature $t$ on the gas scale is defined from measured pressures at temperature $t$ ($P_t$), "
        "the ice point ($P_0$), and the steam point ($P_{100}$):\n\n"
        "$$t = \\frac{P_t - P_0}{P_{100} - P_0} \\times 100\\,^\\circ\\text{C}$$\n\n"
        "On the thermodynamic Kelvin scale, the absolute temperature $T$ is defined in the limit of zero filling pressure $P_3 \\to 0$ relative to the water triple point ($T_{\\text{tp}} = 273.16\\,\\text{K}$):\n\n"
        "$$T = 273.16 \\lim_{P_3 \\to 0} \\left(\\frac{P}{P_3}\\right) \\,\\text{K}$$"
    ),

    # 19. gateaux differential (Candidate 19, index 152)
    152: (
        "In functional analysis, a generalization of directional derivatives to infinite-dimensional topological vector spaces. Let $X, Y$ be locally convex "
        "topological vector spaces, $U \\subseteq X$ open, and $f: U \\to Y$. The Gateaux differential (directional derivative) of $f$ at $x \\in U$ in direction $h \\in X$ is:\n\n"
        "$$d f(x; h) = \\lim_{t \\to 0} \\frac{f(x + th) - f(x)}{t} = \\left. \\frac{d}{dt} f(x + th) \\right|_{t=0}$$\n\n"
        "If this limit exists for all $h \\in X$ and the mapping $h \\mapsto df(x; h)$ is continuous and linear, $f$ is Gateaux differentiable at $x$, and the operator "
        "$T = f'(x) \\in \\mathcal{L}(X, Y)$ is the Gateaux derivative, representing the gradient $\\nabla f(x)$ in Hilbert spaces."
    ),

    # 20. gattermann reaction (Candidate 20, index 158)
    158: (
        "An organic substitution and formylation reaction named after Ludwig Gattermann. 1. **Gattermann Formylation**: Synthesis of aromatic aldehydes by reacting "
        "an activated aromatic ring (such as phenol or pyrrole) with hydrogen cyanide ($\\text{HCN}$) and hydrogen chloride ($\\text{HCl}$) in the presence of a Lewis acid "
        "catalyst ($\\text{AlCl}_3$ or $\\text{ZnCl}_2$), followed by hydrolysis of the intermediate aldimine:\n\n"
        "$$\\text{Ar-H} + \\text{HCN} + \\text{HCl} \\xrightarrow{\\text{AlCl}_3} \\text{Ar-CH=NH}_2^+\\text{Cl}^- \\xrightarrow{\\text{H}_2\\text{O}} \\text{Ar-CHO} + \\text{NH}_4\\text{Cl}$$\n\n"
        "2. **Gattermann Diazonium Reaction**: Preparation of aryl halides from diazonium salts using copper powder as catalyst instead of copper(I) salts (Sandmeyer):\n\n"
        "$$\\text{Ar-N}_2^+\\text{Cl}^- \\xrightarrow{\\text{Cu, HCl}} \\text{Ar-Cl} + \\text{N}_2 \\uparrow$$"
    ),

    # 21. gauge (Candidate 21, index 159)
    159: (
        "1. A standardized instrument or scale for measuring physical dimensions, pressure, wire thickness, or railway track width. "
        "2. In abstract algebra, a **gauge** (or valuation norm) on an integral domain $R$ is a function $g: R \\setminus \\{0\\} \\to \\mathbb{N}_0$ satisfying:\n\n"
        "$$g(ab) \\ge g(a) \\quad \\forall a, b \\in R \\setminus \\{0\\}$$\n\n"
        "and enabling Euclidean division: for any $b \\in R$ and $a \\in R \\setminus \\{0\\}$, there exist $q, r \\in R$ such that $b = qa + r$ with either $r = 0$ or $g(r) < g(a)$. "
        "For polynomial rings $K[x]$, the polynomial degree $\\deg(p)$ serves as the canonical gauge function."
    ),

    # 22. gauge function (Candidate 22, index 161)
    161: (
        "In convex analysis and functional analysis, the **Minkowski functional** (or gauge) associated with an absorbing convex subset $C$ of a real vector space $X$. "
        "It is defined for each $x \\in X$ by:\n\n"
        "$$p_C(x) = \\inf \\{ t > 0 : x \\in tC \\}$$\n\n"
        "The gauge $p_C$ is sublinear (subadditive and positively homogeneous):\n\n"
        "$$p_C(x + y) \\le p_C(x) + p_C(y), \\quad p_C(\\lambda x) = \\lambda p_C(x) \\; (\\lambda \\ge 0)$$\n\n"
        "If $C$ is symmetric ($C = -C$) and bounded, $p_C(x)$ defines a genuine seminorm or norm on $X$, establishing a duality between convex bodies and support functions."
    ),

    # 23. gauss' hypergeometric equation (Candidate 23, index 169)
    169: (
        "A canonical second-order linear ordinary differential equation with three regular singular points (at $x = 0, 1, \\infty$):\n\n"
        "$$x(1 - x) \\frac{d^2 y}{dx^2} + \\left[ c - (a + b + 1)x \\right] \\frac{dy}{dx} - ab y = 0$$\n\n"
        "where $a, b, c$ are complex parameters ($c \\notin \\{0, -1, -2, \\dots\\}$). A fundamental solution valid for $|x| < 1$ is the Gaussian hypergeometric series:\n\n"
        "$$_2F_1(a, b; c; x) = \\sum_{n=0}^\\infty \\frac{(a)_n (b)_n}{(c)_n} \\frac{x^n}{n!}$$\n\n"
        "where $(q)_n = q(q+1)\\cdots(q+n-1)$ is the rising factorial (Pochhammer symbol). Many elementary and special functions (Legendre, Bessel, Chebyshev) are reducible to $_2F_1$."
    ),

    # 24. gauss' law (Candidate 24, index 170)
    170: (
        "One of the four foundational Maxwell equations governing classical electromagnetism, formulating how electric charges generate electric fields. "
        "In integral form, it states that the net electric flux $\\Phi_E$ through any closed Gaussian surface $\\partial V$ equals the net enclosed charge $Q_{\\text{enc}}$ divided by the electric permittivity $\\varepsilon_0$:\n\n"
        "$$\\Phi_E = \\oint_{\\partial V} \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{\\text{enc}}}{\\varepsilon_0} = \\frac{1}{\\varepsilon_0} \\iiint_V \\rho \\, dV$$\n\n"
        "Applying the divergence theorem yields the local differential form:\n\n"
        "$$\\nabla \\cdot \\mathbf{E} = \\frac{\\rho}{\\varepsilon_0}$$\n\n"
        "where $\\rho$ is the volume charge density and $\\varepsilon_0 = 8.854 \\times 10^{-12}\\,\\text{F/m}$ is vacuum permittivity. By spherical symmetry, it directly implies Coulomb's inverse-square law."
    ),

    # 25. gauss' test (Candidate 25, index 172)
    172: (
        "A sensitive convergence test for positive series $\\sum u_n$ when d'Alembert's ratio test and Raabe's test are inconclusive (limit equals $1$). "
        "If the ratio of consecutive terms can be expanded asymptotically as:\n\n"
        "$$\\frac{u_n}{u_{n+1}} = 1 + \\frac{L}{n} + \\frac{\\theta_n}{n^{1 + \\varepsilon}} = 1 + \\frac{L}{n} + \\mathcal{O}\\left(\\frac{1}{n^{1+\\varepsilon}}\\right)$$\n\n"
        "where $\\varepsilon > 0$ and $|\\theta_n|$ is bounded, then:\n\n"
        "1. $\\sum u_n$ **converges** if $L > 1$.\n"
        "2. $\\sum u_n$ **diverges** if $L \\le 1$.\n\n"
        "Gauss's test resolves the delicate edge case $L = 1$, where Raabe's test fails."
    ),

    # 26. gauss-markov least squares theorem (Candidate 26, index 174)
    174: (
        "A central theorem in linear regression and econometrics. For the linear regression model $\\mathbf{y} = \\mathbf{X}\\boldsymbol{\\beta} + \\boldsymbol{\\varepsilon}$, "
        "satisfying the classical Gauss-Markov conditions:\n\n"
        "$$\\mathbb{E}[\\boldsymbol{\\varepsilon} \\mid \\mathbf{X}] = \\mathbf{0}, \\quad \\operatorname{Var}(\\boldsymbol{\\varepsilon} \\mid \\mathbf{X}) = \\sigma^2 \\mathbf{I}_n$$\n\n"
        "(homoscedasticity and zero autocorrelation), the ordinary least squares (OLS) estimator:\n\n"
        "$$\\hat{\\boldsymbol{\\beta}}_{\\text{OLS}} = (\\mathbf{X}^T \\mathbf{X})^{-1} \\mathbf{X}^T \\mathbf{y}$$\n\n"
        "is the **BLUE** (**Best Linear Unbiased Estimator**), possessing the minimum sampling variance among all possible linear unbiased estimators of $\\boldsymbol{\\beta}$."
    ),

    # 27. gauss-seidel iteration (Candidate 27, index 175)
    175: (
        "An iterative numerical algorithm for solving a square system of $n$ linear algebraic equations $\\mathbf{A}\\mathbf{x} = \\mathbf{b}$. "
        "Unlike the Jacobi method, Gauss-Seidel updates unknown components immediately in-place during the current iteration step $k+1$:\n\n"
        "$$x_i^{(k+1)} = \\frac{1}{a_{ii}} \\left( b_i - \\sum_{j=1}^{i-1} a_{ij} x_j^{(k+1)} - \\sum_{j=i+1}^n a_{ij} x_j^{(k)} \\right), \\quad i = 1, 2, \\dots, n$$\n\n"
        "In matrix decomposition form with $\\mathbf{A} = \\mathbf{D} - \\mathbf{L} - \\mathbf{U}$ (diagonal, strictly lower, and strictly upper triangular matrices):\n\n"
        "$$\\mathbf{x}^{(k+1)} = (\\mathbf{D} - \\mathbf{L})^{-1} \\mathbf{U} \\mathbf{x}^{(k)} + (\\mathbf{D} - \\mathbf{L})^{-1} \\mathbf{b}$$\n\n"
        "Convergence is guaranteed if $\\mathbf{A}$ is strictly diagonally dominant or symmetric positive-definite."
    ),

    # 28. gaussian distribution (Candidate 28, index 177)
    177: (
        "The normal (Gaussian) distribution, the most ubiquitous continuous probability distribution in probability and statistics. "
        "Parametrized by mean $\\mu \\in \\mathbb{R}$ and variance $\\sigma^2 > 0$, its probability density function (PDF) is given by:\n\n"
        "$$f(x; \\mu, \\sigma^2) = \\frac{1}{\\sigma \\sqrt{2\\pi}} \\exp\\left( -\\frac{(x - \\mu)^2}{2\\sigma^2} \\right), \\quad x \\in \\mathbb{R}$$\n\n"
        "It is symmetric about $\\mu$, bell-shaped, with inflection points at $x = \\mu \\pm \\sigma$. The standardized variable $Z = \\frac{X - \\mu}{\\sigma}$ "
        "follows the standard normal distribution $\\mathcal{N}(0, 1)$. By the Central Limit Theorem, the sum of independent random variables with finite variance converges asymptotically to a Gaussian distribution."
    ),

    # 29. gaussian domain (Candidate 29, index 178)
    178: (
        "1. A unique factorization domain (UFD), historically termed a Gaussian domain in honour of Carl Friedrich Gauss's arithmetic of Gaussian integers. "
        "2. The ring of **Gaussian integers**, denoted $\\mathbb{Z}[i] = \\{a + bi : a, b \\in \\mathbb{Z}\\}$ where $i^2 = -1$. Equipped with the multiplicative norm:\n\n"
        "$$N(a + bi) = a^2 + b^2$$\n\n"
        "$\\mathbb{Z}[i]$ is a Euclidean domain, hence a Principal Ideal Domain (PID) and a UFD. For example, the rational prime $5$ factors into irreducibles as "
        "$5 = (1 + 2i)(1 - 2i)$ and is therefore reducible in $\\mathbb{Z}[i]$, whereas $3$ is prime in $\\mathbb{Z}[i]$ because $a^2 + b^2 = 3$ has no integer solutions."
    ),

    # 30. gaussian function (Candidate 30, index 181)
    181: (
        "A symmetric bell-shaped mathematical function defined in its general one-dimensional form by:\n\n"
        "$$f(x) = a \\exp\\left( -\\frac{(x - b)^2}{2c^2} \\right)$$\n\n"
        "where $a$ is peak height, $b$ is the center position, and $c$ controls Gaussian width (standard deviation). The canonical Gaussian function is $y = e^{-x^2}$. "
        "Its definite integral over the entire real line is evaluated via the famous Poisson polar-coordinate trick:\n\n"
        "$$\\int_{-\\infty}^\\infty e^{-x^2} \\, dx = \\sqrt{\\pi}$$\n\n"
        "Crucial in heat conduction kernels, quantum harmonic oscillator ground states, and signal filtering."
    ),

    # 31. gaussian plane (Candidate 31, index 183)
    183: (
        "The complex plane (also known as the Argand diagram), a geometric representation of complex numbers $z \\in \\mathbb{C}$ as points or position vectors "
        "$(x, y)$ in a two-dimensional Cartesian coordinate system. The horizontal axis represents the real part $\\operatorname{Re}(z) = x$, while the vertical "
        "axis represents the imaginary part $\\operatorname{Im}(z) = y$:\n\n"
        "$$z = x + iy = r(\\cos\\theta + i\\sin\\theta) = r e^{i\\theta}$$\n\n"
        "where the modulus (distance from origin) is $r = |z| = \\sqrt{x^2 + y^2}$, and the argument (phase angle) is $\\theta = \\operatorname{arg}(z) = \\operatorname{atan2}(y, x)$."
    ),

    # 32. gaussian unit (Candidate 32, index 184)
    184: (
        "A mixed metric system of physical units (CGS-Gaussian system) combining electrostatic units (esu) for electric charge/potential and electromagnetic units (emu) "
        "for magnetic fields. In Gaussian units, vacuum permittivity $\\varepsilon_0$ and permeability $\\mu_0$ are dimensionless and set to $\\varepsilon_0 = 1, \\mu_0 = 1$, "
        "causing the speed of light $c$ to appear explicitly in Maxwell's equations. Conversion factors to SI:\n\n"
        "$$1\\,\\text{statC (statcoulomb)} = \\frac{1}{10 c}\\,\\text{C} \\approx 3.33564 \\times 10^{-10}\\,\\text{C}$$\n\n"
        "$$1\\,\\text{statV (statvolt)} = 10^{-8} c\\,\\text{V} \\approx 299.7925\\,\\text{V}$$\n\n"
        "$$1\\,\\text{statF (statfarad)} = \\frac{1}{10^9 c^2}\\,\\text{F} \\approx 1.11265\\,\\text{pF}$$\n\n"
        "$$1\\,\\text{G (gauss)} = 10^{-4}\\,\\text{T (tesla)}$$"
    ),

    # 33. gay-lussac's law (Candidate 33, index 185)
    185: (
        "1. **Law of Combining Volumes** (Joseph Louis Gay-Lussac, 1808): When gases react chemically at constant temperature and pressure, the volumes of reacting gases "
        "and gaseous products stand in simple whole-number integer ratios. For example, in the formation of steam:\n\n"
        "$$2\\text{H}_{2(g)} + \\text{O}_{2(g)} \\to 2\\text{H}_2\\text{O}_{(g)} \\quad (\\text{ratio } 2 : 1 : 2)$$\n\n"
        "2. **Pressure-Temperature Law** (Amontons' Law): For a fixed mass of gas at constant volume, pressure $P$ is directly proportional to absolute Kelvin temperature $T$:\n\n"
        "$$\\frac{P}{T} = \\text{constant} \\iff \\frac{P_1}{T_1} = \\frac{P_2}{T_2}$$"
    ),

    # 34. gaylussite (Candidate 34, index 187)
    187: (
        "A translucent yellowish-white hydrous sodium calcium double carbonate evaporite mineral named after Joseph Louis Gay-Lussac. "
        "Chemical formula $\\text{Na}_2\\text{Ca}(\\text{CO}_3)_2 \\cdot 5\\text{H}_2\\text{O}$, molar mass $296.16\\,\\text{g/mol}$, density $1.99\\,\\text{g/cm}^3$, "
        "and Mohs hardness $2.5$. Crystallizes in the monoclinic crystal system (space group $I2/a$). Unstable in dry air, dehydrating to chalconatronite "
        "or decomposing in freshwater through calcium carbonate precipitation:\n\n"
        "$$\\text{Na}_2\\text{Ca}(\\text{CO}_3)_2 \\cdot 5\\text{H}_2\\text{O}_{(s)} \\xrightarrow{\\text{excess } \\text{H}_2\\text{O}} "
        "\\text{CaCO}_{3(s)} + 2\\text{Na}^+_{(aq)} + \\text{CO}_3^{2-}_{(aq)} + 5\\text{H}_2\\text{O}_{(l)}$$"
    ),

    # 35. geiger-nuttall law (Candidate 35, index 194)
    194: (
        "An empirical relationship established by Hans Geiger and John Mitchell Nuttall in 1911 (later explained quantum mechanically by George Gamow via quantum tunneling) "
        "relating the radioactive alpha-decay constant $\\lambda$ to the kinetic energy $E_\\alpha$ of emitted alpha particles:\n\n"
        "$$\\ln \\lambda = -a_1 \\frac{Z}{\\sqrt{E_\\alpha}} + a_2 \\quad \\text{or} \\quad \\log_{10} T_{1/2} = A + \\frac{B}{\\sqrt{E_\\alpha}}$$\n\n"
        "where $Z$ is the atomic number of the daughter nucleus, $E_\\alpha$ is the alpha particle kinetic energy, $\\lambda = \\frac{\\ln 2}{T_{1/2}}$ is the decay constant, "
        "and $a_1, a_2$ are empirical constants. It demonstrates that a small increase in alpha energy results in an exponentially shorter radioactive half-life $T_{1/2}$."
    ),

    # 36. gel filtration chromatography (Candidate 36, index 198)
    198: (
        "A size-exclusion chromatography (SEC) method using porous polymeric beads (e.g. Sephadex, agarose, polyacrylamide) to separate biological macromolecules "
        "such as proteins, enzymes, and nucleic acids based on hydrodynamic volume (Stokes radius $R_h$). The total column volume $V_t$ is the sum of void volume $V_0$ "
        "and internal pore volume $V_i$ ($V_t = V_0 + V_i$). The distribution coefficient $K_{\\text{av}}$ is given by:\n\n"
        "$$K_{\\text{av}} = \\frac{V_e - V_0}{V_t - V_0}$$\n\n"
        "where $V_e$ is analyte elution volume. Large molecules unable to enter pores elute first at $V_e = V_0$ ($K_{\\text{av}} = 0$), while small molecules permeate all pores and elute last ($K_{\\text{av}} \\approx 1$)."
    ),

    # 37. gelfand transform (Candidate 37, index 202)
    202: (
        "In functional analysis, a canonical representation of a commutative Banach algebra $\\mathcal{A}$ over $\\mathbb{C}$ as an algebra of continuous functions. "
        "Let $\\Delta(\\mathcal{A})$ denote the Gelfand spectrum (the compact Hausdorff space of all non-zero multiplicative linear functionals / maximal ideals of $\\mathcal{A}$ "
        "endowed with the weak-* topology). The Gelfand transform is the algebra homomorphism $\\mathcal{A} \\to C(\\Delta(\\mathcal{A}))$ mapping each $x \\in \\mathcal{A}$ to $\\hat{x}$ defined by:\n\n"
        "$$\\hat{x}(\\varphi) = \\varphi(x), \\quad \\varphi \\in \\Delta(\\mathcal{A})$$\n\n"
        "By the Gelfand-Naimark theorem, if $\\mathcal{A}$ is a commutative $C^*$-algebra, the Gelfand transform is an isometric $*$-isomorphism:\n\n"
        "$$\\|\\hat{x}\\|_{\\infty} = \\|x\\| = r(x)$$\n\n"
        "where $r(x) = \\lim_{n\\to\\infty} \\|x^n\\|^{1/n}$ is the spectral radius."
    ),

    # 38. gelfond-schneider theorem (Candidate 38, index 203)
    203: (
        "A major theorem in transcendental number theory proved independently by Aleksandr Gelfond (1934) and Theodor Schneider (1935), solving Hilbert's seventh problem. "
        "It asserts that if $\\alpha$ and $\\beta$ are algebraic numbers in $\\mathbb{C}$ such that $\\alpha \\notin \\{0, 1\\}$ and $\\beta$ is irrational, then any value of $\\alpha^\\beta$ is transcendental:\n\n"
        "$$\\alpha, \\beta \\in \\overline{\\mathbb{Q}}, \\; \\alpha \\neq 0, 1, \\; \\beta \\notin \\mathbb{Q} \\implies \\alpha^\\beta \\text{ is transcendental}$$\n\n"
        "Prime examples include the Gelfond-Schneider constant $2^{\\sqrt{2}}$ and Gelfond's constant $e^\\pi = (e^{i\\pi})^{-i} = (-1)^{-i}$."
    ),

    # 39. generalisation (Candidate 39, index 244)
    244: (
        "1. In mathematics and logic, the inductive or deductive abstraction from specific instances to broader principles valid for an entire set or universe of discourse $S$. "
        "In predicate calculus, universal generalisation is formalized with the universal quantifier $\\forall$:\n\n"
        "$$P(x) \\text{ for arbitrary } x \\in S \\implies \\forall x \\in S, \\, P(x)$$\n\n"
        "In arithmetic and algebra, generalizing arithmetic relations $3 + 5 = 5 + 3$ yields the commutative ring axiom $a + b = b + a$, and generalizing numerical summations "
        "leads to formula expressions such as $\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$. "
        "2. In psychology and behavioural neuroscience, stimulus generalization is the phenomenon where a conditioned response (CR) is elicited by stimuli resembling the original conditioned stimulus (CS)."
    ),

    # 40. generalised eigenvalue problem (Candidate 40, index 247)
    247: (
        "In numerical linear algebra, the problem of finding non-zero vectors $\\mathbf{x} \\in \\mathbb{C}^n$ (eigenvectors) and scalars $\\lambda \\in \\mathbb{C}$ (eigenvalues) satisfying:\n\n"
        "$$\\mathbf{A}\\mathbf{x} = \\lambda \\mathbf{B}\\mathbf{x}$$\n\n"
        "where $\\mathbf{A}$ and $\\mathbf{B}$ are given $n \\times n$ matrices. Non-trivial solutions exist if and only if the matrix determinant of the matrix pencil vanishes:\n\n"
        "$$\\det(\\mathbf{A} - \\lambda \\mathbf{B}) = 0$$\n\n"
        "When $\\mathbf{B} = \\mathbf{I}$ (the identity matrix), it reduces to the standard eigenvalue problem $\\mathbf{A}\\mathbf{x} = \\lambda \\mathbf{x}$. "
        "Arises naturally in structural vibration analysis, where $\\mathbf{A} = \\mathbf{K}$ is the stiffness matrix and $\\mathbf{B} = \\mathbf{M}$ is the positive-definite mass matrix: $\\mathbf{K}\\mathbf{x} = \\omega^2 \\mathbf{M}\\mathbf{x}$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(g_entries):
        w = g_entries[idx]['word']
        g_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (G has {len(g_entries)} entries)")

data['G'] = g_entries

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section G Batch 1.")
