"""
enrich_section_e_batch_3.py
===========================
Section E Formula Enrichment - Batch 3 (Terms 91 to 140)
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
    # 91. ethanoic anhydride
    1035: (
        "A colourless liquid with a sharp, pungent odour, molecular formula $\\text{C}_4\\text{H}_6\\text{O}_3$ and structural formula $(\\text{CH}_3\\text{CO})_2\\text{O}$, molar mass $102.09\\,\\text{g}\\cdot\\text{mol}^{-1}$, boiling point $139.8\\,^\\circ\\text{C}$ ($412.9\\,\\text{K}$), and melting point $-73.1\\,^\\circ\\text{C}$ ($200.1\\,\\text{K}$). Produced industrially by the carbonylation of methyl acetate or dehydration of acetic acid. Widely used as an acetylating agent to introduce the ethanoyl group ($\\text{CH}_3\\text{CO}-$), notably in synthesizing cellulose acetate and aspirin (acetylsalicylic acid)."
    ),

    # 92. ethanol
    1036: (
        "Ethyl alcohol, a colourless, volatile, flammable primary alcohol with molecular formula $\\text{C}_2\\text{H}_5\\text{OH}$ and structural formula $\\text{CH}_3\\text{CH}_2\\text{OH}$, molar mass $46.07\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.789\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-114.1\\,^\\circ\\text{C}$ ($159.05\\,\\text{K}$), and boiling point $78.37\\,^\\circ\\text{C}$ ($351.52\\,\\text{K}$). Completely miscible with water via hydrogen bonding. Produced biologically by the yeast fermentation of sugars:\n\n"
        "$$\\text{C}_6\\text{H}_{12}\\text{O}_6 \\xrightarrow{\\text{zymase}} 2\\text{C}_2\\text{H}_5\\text{OH} + 2\\text{CO}_2$$\n\n"
        "or synthetically by the acid-catalyzed hydration of ethene:\n\n"
        "$$\\text{C}_2\\text{H}_4 + \\text{H}_2\\text{O} \\xrightarrow{\\text{H}_3\\text{PO}_4} \\text{C}_2\\text{H}_5\\text{OH}$$"
    ),

    # 93. ethanoyl chloride
    1038: (
        "Acetyl chloride, a fuming, pungent liquid acyl chloride with chemical formula $\\text{CH}_3\\text{COCl}$, molar mass $78.50\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $1.104\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-112\\,^\\circ\\text{C}$ ($161\\,\\text{K}$), and boiling point $52\\,^\\circ\\text{C}$ ($325\\,\\text{K}$). Prepared by reacting ethanoic acid with phosphorus pentachloride or thionyl chloride:\n\n"
        "$$\\text{CH}_3\\text{COOH} + \\text{SOCl}_2 \\to \\text{CH}_3\\text{COCl} + \\text{SO}_2 + \\text{HCl}$$\n\n"
        "It undergoes rapid exothermic hydrolysis upon contact with water:\n\n"
        "$$\\text{CH}_3\\text{COCl} + \\text{H}_2\\text{O} \\to \\text{CH}_3\\text{COOH} + \\text{HCl}$$"
    ),

    # 94. ethene
    1040: (
        "Ethylene, the simplest alkene, a colourless flammable gas with molecular formula $\\text{C}_2\\text{H}_4$ and structural formula $\\text{CH}_2=\\text{CH}_2$, molar mass $28.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, melting point $-169.2\\,^\\circ\\text{C}$ ($104\\,\\text{K}$), and boiling point $-103.7\\,^\\circ\\text{C}$ ($169.5\\,\\text{K}$). The $sp^2$-hybridized carbon atoms feature a planar $120^\\circ$ geometry with one $\\sigma$ and one $\\pi$ bond. Produced industrially by steam cracking of petroleum hydrocarbons, it polymerizes via addition polymerisation to polyethene (polyethylene):\n\n"
        "$$n(\\text{CH}_2=\\text{CH}_2) \\to -(-\\text{CH}_2-\\text{CH}_2-)-_n$$\n\n"
        "In plant physiology, ethylene acts as a key gaseous hormone stimulating fruit ripening."
    ),

    # 95. ethoxyethane
    1048: (
        "Diethyl ether, a colourless, volatile, highly flammable liquid ether with molecular formula $\\text{C}_2\\text{H}_5\\text{OC}_2\\text{H}_5$ (or $\\text{C}_4\\text{H}_{10}\\text{O}$), molar mass $74.12\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.7134\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-116.3\\,^\\circ\\text{C}$ ($156.9\\,\\text{K}$), and boiling point $34.6\\,^\\circ\\text{C}$ ($307.8\\,\\text{K}$). Prepared industrially by the acid-catalyzed intermolecular dehydration of ethanol:\n\n"
        "$$2\\text{C}_2\\text{H}_5\\text{OH} \\xrightarrow{140\\,^\\circ\\text{C},\\,\\text{H}_2\\text{SO}_4} \\text{C}_2\\text{H}_5\\text{OC}_2\\text{H}_5 + \\text{H}_2\\text{O}$$"
    ),

    # 96. ethy lami ne (ethylamine)
    1049: (
        "Ethylamine, a colourless, volatile, flammable primary aliphatic amine with chemical formula $\\text{C}_2\\text{H}_5\\text{NH}_2$ or $\\text{CH}_3\\text{CH}_2\\text{NH}_2$, molar mass $45.08\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.689\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-81\\,^\\circ\\text{C}$ ($192\\,\\text{K}$), and boiling point $16.6\\,^\\circ\\text{C}$ ($290\\,\\text{K}$). It is basic ($pK_b = 3.25$) and acts as a nucleophile in organic synthesis and resin manufacturing."
    ),

    # 97. ethyl alcohol
    1051: (
        "Ethanol, a colourless, flammable, volatile liquid alcohol with molecular formula $\\text{C}_2\\text{H}_5\\text{OH}$ and structural formula $\\text{CH}_3\\text{CH}_2\\text{OH}$, molar mass $46.07\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.789\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-114.1\\,^\\circ\\text{C}$ ($159.05\\,\\text{K}$), and boiling point $78.37\\,^\\circ\\text{C}$ ($351.52\\,\\text{K}$). Used globally as a universal solvent, antiseptic, recreational psychoactive beverage component, and alternative biofuel."
    ),

    # 98. ethyl ethanoate
    1053: (
        "Ethyl acetate, an organic ester with molecular formula $\\text{CH}_3\\text{COOCH}_2\\text{CH}_3$ (or $\\text{C}_4\\text{H}_8\\text{O}_2$), molar mass $88.11\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.897\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-83.6\\,^\\circ\\text{C}$ ($190\\,\\text{K}$), and boiling point $77.1\\,^\\circ\\text{C}$ ($350\\,\\text{K}$). Prepared via Fischer esterification of ethanoic acid with ethanol:\n\n"
        "$$\\text{CH}_3\\text{COOH} + \\text{C}_2\\text{H}_5\\text{OH} \\xrightleftharpoons{\\text{H}^+} \\text{CH}_3\\text{COOC}_2\\text{H}_5 + \\text{H}_2\\text{O}$$\n\n"
        "Possesses a sweet, fruity odor and is widely utilized as an industrial solvent for paints, glues, and nail polish removers."
    ),

    # 99. ethylbenzene
    1055: (
        "An aromatic hydrocarbon with chemical formula $\\text{C}_6\\text{H}_5\\text{CH}_2\\text{CH}_3$ (or $\\text{C}_8\\text{H}_{10}$), molar mass $106.17\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $0.867\\,\\text{g}\\cdot\\text{cm}^{-3}$, melting point $-95\\,^\\circ\\text{C}$ ($178\\,\\text{K}$), and boiling point $136\\,^\\circ\\text{C}$ ($409\\,\\text{K}$). Synthesized via acid-catalyzed Friedel-Crafts alkylation of benzene with ethene:\n\n"
        "$$\\text{C}_6\\text{H}_6 + \\text{C}_2\\text{H}_4 \\xrightarrow{\\text{AlCl}_3} \\text{C}_6\\text{H}_5\\text{CH}_2\\text{CH}_3$$\n\n"
        "Nearly all commercial ethylbenzene is catalytic dehydrogenated to produce styrene ($\\text{C}_6\\text{H}_5\\text{CH}=\\text{CH}_2$), the monomer for polystyrene."
    ),

    # 100. ethylene
    1056: (
        "Ethene, the simplest alkene, a colourless flammable gas with molecular formula $\\text{C}_2\\text{H}_4$ and structural formula $\\text{CH}_2=\\text{CH}_2$, molar mass $28.05\\,\\text{g}\\cdot\\text{mol}^{-1}$, melting point $-169.2\\,^\\circ\\text{C}$ ($104\\,\\text{K}$), and boiling point $-103.7\\,^\\circ\\text{C}$ ($169.5\\,\\text{K}$). The fundamental feedstock for the petrochemical industry, consumed in the manufacture of polyethylene polymers, ethylene oxide, ethylene glycol, and styrene."
    ),

    # 101. ethyne
    1059: (
        "Acetylene, the simplest alkyne, a linear unsaturated hydrocarbon with molecular formula $\\text{C}_2\\text{H}_2$ and structural formula $\\text{H}-\\text{C}\\equiv\\text{C}-\\text{H}$, molar mass $26.04\\,\\text{g}\\cdot\\text{mol}^{-1}$, density $1.097\\,\\text{kg}\\cdot\\text{m}^{-3}$, sublimation point $-84\\,^\\circ\\text{C}$ ($189.2\\,\\text{K}$), and triple point $-80.8\\,^\\circ\\text{C}$ at $1.27\\,\\text{atm}$. Prepared by the hydrolysis of calcium carbide:\n\n"
        "$$\\text{CaC}_2 + 2\\text{H}_2\\text{O} \\to \\text{Ca(OH)}_2 + \\text{C}_2\\text{H}_2$$\n\n"
        "Burns in pure oxygen to yield oxy-acetylene flame temperatures exceeding $3300\\,^\\circ\\text{C}$, extensively used in oxy-fuel welding and metal cutting."
    ),

    # 102. euclidean distance
    1075: (
        "The ordinary straight-line distance between two points in Euclidean space $\\mathbb{R}^n$, derived from the Pythagorean theorem. For points $\\mathbf{x} = (x_1, x_2, \\dots, x_n)$ and $\\mathbf{y} = (y_1, y_2, \\dots, y_n)$, the Euclidean distance metric is:\n\n"
        "$$d(\\mathbf{x}, \\mathbf{y}) = \\sqrt{\\sum_{i=1}^n (x_i - y_i)^2} = \\|\\mathbf{x} - \\mathbf{y}\\|_2$$\n\n"
        "In two dimensions, $d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$; in three dimensions, $d = \\sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2 + (z_2 - z_1)^2}$."
    ),

    # 103. euclidean norm
    1078: (
        "The standard $L^2$-norm on Euclidean vector space $\\mathbb{R}^n$, assigning to each vector $\\mathbf{x} = (x_1, x_2, \\dots, x_n)$ its geometric length:\n\n"
        "$$\\|\\mathbf{x}\\|_2 = \\sqrt{\\mathbf{x} \\cdot \\mathbf{x}} = \\sqrt{\\sum_{i=1}^n x_i^2}$$\n\n"
        "It satisfies the three norm axioms: positivity ($\\|\\mathbf{x}\\| \\ge 0$, with equality if and only if $\\mathbf{x} = \\mathbf{0}$), absolute homogeneity ($\\|c\\mathbf{x}\\| = |c|\\,\\|\\mathbf{x}\\|$ for scalar $c$), and the triangle inequality ($\\|\\mathbf{x} + \\mathbf{y}\\| \\le \\|\\mathbf{x}\\| + \\|\\mathbf{y}\\|$)."
    ),

    # 104. euclidean topology
    1080: (
        "The standard topology on $\\mathbb{R}^n$ induced by the Euclidean metric $d(\\mathbf{x}, \\mathbf{y}) = \\sqrt{\\sum_{i=1}^n (x_i - y_i)^2}$. A subset $U \\subseteq \\mathbb{R}^n$ is defined to be open in the Euclidean topology if for every point $\\mathbf{x} \\in U$, there exists an open metric ball $B_r(\\mathbf{x}) = \\{\\mathbf{y} \\in \\mathbb{R}^n : \\|\\mathbf{x} - \\mathbf{y}\\| < r\\} \\subseteq U$ with radius $r > 0$."
    ),

    # 105. euler characteristic
    1092: (
        "A topological invariant $\\chi$ that characterizes the topological structure and genus of a space. For a convex three-dimensional polyhedron, Euler's polyhedron formula states:\n\n"
        "$$\\chi = V - E + F = 2$$\n\n"
        "where $V$ is the number of vertices, $E$ is the number of edges, and $F$ is the number of faces. For example, a cube has $V = 8, E = 12, F = 6$, giving $8 - 12 + 6 = 2$. More generally, for a closed orientable surface of genus $g$, the Euler characteristic is $\\chi = 2 - 2g$."
    ),

    # 106. euler phi function
    1096: (
        "Euler's totient function, denoted $\\varphi(n)$, which counts the number of positive integers $1 \\le k \\le n$ that are coprime to $n$ ($\\gcd(k, n) = 1$). It is multiplicative (if $\\gcd(m, n) = 1$, then $\\varphi(mn) = \\varphi(m)\\varphi(n)$). For prime powers, $\\varphi(p^k) = p^k - p^{k-1} = p^{k-1}(p - 1)$. By Euler's product formula:\n\n"
        "$$\\varphi(n) = n \\prod_{p \\mid n} \\left(1 - \\frac{1}{p}\\right)$$\n\n"
        "It forms the cornerstone of Euler's totient theorem: if $\\gcd(a, n) = 1$, then $a^{\\varphi(n)} \\equiv 1 \\pmod n$."
    ),

    # 107. euler summation formula
    1098: (
        "The Euler-Maclaurin summation formula, providing an asymptotic relationship between a finite discrete sum and an integral of a smooth function $f(x)$:\n\n"
        "$$\\sum_{i=a}^b f(i) = \\int_a^b f(x)\\,dx + \\frac{f(a) + f(b)}{2} + \\sum_{k=1}^m \\frac{B_{2k}}{(2k)!} \\left[f^{(2k-1)}(b) - f^{(2k-1)}(a)\\right] + R_m$$\n\n"
        "where $B_{2k}$ are the Bernoulli numbers and $R_m$ is an integral remainder term. Extensively used in numerical analysis, analytic number theory, and asymptotic expansions."
    ),

    # 108. euler's constant
    1100: (
        "The Euler-Mascheroni constant, denoted $\\gamma$, defined as the limiting difference between the harmonic series and the natural logarithm:\n\n"
        "$$\\gamma = \\lim_{n \\to \\infty} \\left(\\sum_{k=1}^n \\frac{1}{k} - \\ln n\\right) \\approx 0.5772156649\\dots$$\n\n"
        "It arises in gamma functions, Bessel functions, and the asymptotic distribution of prime numbers."
    ),

    # 109. euler's equation
    1101: (
        "1. In differential equations, the Cauchy-Euler equidistant linear differential equation:\n\n"
        "$$a_n x^n \\frac{d^n y}{dx^n} + a_{n-1} x^{n-1} \\frac{d^{n-1} y}{dx^{n-1}} + \\dots + a_1 x \\frac{dy}{dx} + a_0 y = f(x)$$\n\n"
        "which is transformed into a constant-coefficient linear equation via substitution $x = e^t$ (for $x > 0$). 2. In fluid dynamics, Euler's equation of inviscid fluid motion:\n\n"
        "$$\\rho \\left(\\frac{\\partial \\mathbf{v}}{\\partial t} + \\mathbf{v} \\cdot \\nabla \\mathbf{v}\\right) = -\\nabla p + \\rho \\mathbf{g}$$"
    ),

    # 110. euler's equations of motion
    1102: (
        "The system of three non-linear coupled differential equations governing the rotational dynamics of a rigid body expressed in the body-fixed principal axes frame:\n\n"
        "$$I_1 \\dot{\\omega}_1 + (I_3 - I_2)\\omega_2 \\omega_3 = M_1$$\n\n"
        "$$I_2 \\dot{\\omega}_2 + (I_1 - I_3)\\omega_3 \\omega_1 = M_2$$\n\n"
        "$$I_3 \\dot{\\omega}_3 + (I_2 - I_1)\\omega_1 \\omega_2 = M_3$$\n\n"
        "where $I_1, I_2, I_3$ are the principal moments of inertia, $\\omega_1, \\omega_2, \\omega_3$ are angular velocity components, and $M_1, M_2, M_3$ are the applied external torque components."
    ),

    # 111. euler's formula for polyhedral
    1103: (
        "The foundational topological relation for any simply connected (genus-0) convex polyhedron:\n\n"
        "$$V - E + F = 2$$\n\n"
        "where $V$ is the number of vertices, $E$ is the number of edges, and $F$ is the number of faces. For example, an octahedron has $V = 6, E = 12, F = 8$, satisfying $6 - 12 + 8 = 2$. The invariant $V - E + F = \\chi$ is known as the Euler characteristic."
    ),

    # 112. euler's laws of motion
    1104: (
        "Extensions of Newton's laws from point particles to continuous rigid and deformable bodies: (1) First law (balance of linear momentum):\n\n"
        "$$\\mathbf{F} = \\frac{d\\mathbf{p}}{dt} = m \\mathbf{a}_{\\text{cm}}$$\n\n"
        "where net external force equals the rate of change of total linear momentum; and (2) Second law (balance of angular momentum):\n\n"
        "$$\\boldsymbol{\\tau} = \\frac{d\\mathbf{L}}{dt}$$\n\n"
        "stating that net external torque about a fixed point equals the rate of change of angular momentum."
    ),

    # 113. euler's method
    1105: (
        "A foundational first-order numerical procedure for solving ordinary differential equations with given initial value $\\frac{dy}{dx} = f(x, y), y(x_0) = y_0$. Using a step size $h$, the iterative step is given by:\n\n"
        "$$y_{n+1} = y_n + h f(x_n, y_n)$$\n\n"
        "$$x_{n+1} = x_n + h$$\n\n"
        "The local truncation error per step is $O(h^2)$, resulting in a global truncation error of $O(h)$."
    ),

    # 114. euler's number
    1106: (
        "The mathematical constant $e$, base of the natural logarithm, defined analytically as:\n\n"
        "$$e = \\lim_{n \\to \\infty} \\left(1 + \\frac{1}{n}\\right)^n = \\sum_{k=0}^\\infty \\frac{1}{k!} = 1 + 1 + \\frac{1}{2} + \\frac{1}{6} + \\dots \\approx 2.7182818284\\dots$$\n\n"
        "It is transcendental and represents the unique real base for which the derivative of $f(x) = e^x$ is identical to itself: $\\frac{d}{dx}(e^x) = e^x$."
    ),

    # 115. euler-bernoulli law
    1108: (
        "The fundamental law in structural mechanics (Euler-Bernoulli beam theory) stating that the internal bending moment $M(x)$ in an elastic beam is proportional to the curvature of the beam's neutral axis:\n\n"
        "$$M = EI \\kappa = EI \\frac{d^2 w}{dx^2}$$\n\n"
        "where $E$ is Young's modulus of elasticity, $I$ is the second moment of area (areal moment of inertia) of the beam cross-section, and $w(x)$ is the transverse deflection."
    ),

    # 116. euler-lagrange equations
    1109: (
        "The fundamental second-order partial differential equation in the calculus of variations and Lagrangian mechanics. For a functional $J[y] = \\int_a^b L(x, y, y')\\,dx$ to attain a stationary value (extremum), the function $y(x)$ must satisfy:\n\n"
        "$$\\frac{\\partial L}{\\partial y} - \\frac{d}{dx}\\left(\\frac{\\partial L}{\\partial y'}\\right) = 0$$\n\n"
        "In classical mechanics with Lagrangian $L = T - V$ and generalized coordinates $q_i$, it takes the form $\\frac{d}{dt}\\left(\\frac{\\partial L}{\\partial \\dot{q}_i}\\right) - \\frac{\\partial L}{\\partial q_i} = 0$."
    ),

    # 117. euler-riemann zeta function
    1110: (
        "A central special function in analytic number theory, denoted $\\zeta(s)$, defined for complex variable $s = \\sigma + it$ with $\\operatorname{Re}(s) > 1$ by the Dirichlet series:\n\n"
        "$$\\zeta(s) = \\sum_{n=1}^\\infty \\frac{1}{n^s}$$\n\n"
        "and related to prime numbers via Euler's product formula:\n\n"
        "$$\\zeta(s) = \\prod_{p \\text{ prime}} \\frac{1}{1 - p^{-s}}$$\n\n"
        "Analytically continued to a meromorphic function on the entire complex plane $\\mathbb{C}$ with a single simple pole at $s = 1$. The Riemann Hypothesis conjectures that all non-trivial zeros lie on the critical line $\\operatorname{Re}(s) = \\frac{1}{2}$."
    ),

    # 118. eulerian strain rate
    1116: (
        "In continuum mechanics, the symmetric part of the spatial velocity gradient tensor $\\mathbf{L} = \\nabla \\mathbf{v}$, defining the rate of deformation (strain rate tensor) $\\mathbf{D}$:\n\n"
        "$$\\mathbf{D} = \\frac{1}{2}\\left(\\mathbf{L} + \\mathbf{L}^T\\right)$$\n\n"
        "where $D_{ij} = \\frac{1}{2}\\left(\\frac{\\partial v_i}{\\partial x_j} + \\frac{\\partial v_j}{\\partial x_i}\\right)$. The anti-symmetric part $\\mathbf{W} = \\frac{1}{2}(\\mathbf{L} - \\mathbf{L}^T)$ represents the spin or vorticity tensor."
    ),

    # 119. evaluate
    1141: (
        "To compute the exact or approximate numerical value of a mathematical expression, function, or integral by substituting specific numerical values for its variables. For example, evaluating $f(x) = x^2 - 4x + 7$ at $x = 3$ yields $f(3) = 3^2 - 4(3) + 7 = 4$."
    ),

    # 120. exact
    1175: (
        "1. Strictly accurate, without rounding or numerical approximation (e.g., $1/3$ is exact, whereas $0.333$ is an approximation). 2. In differential equations, an exact differential equation has the form $M(x, y)\\,dx + N(x, y)\\,dy = 0$ where there exists a potential function $F(x, y)$ such that $dF = M\\,dx + N\\,dy = 0$. By Schwarz's theorem, this holds if and only if $\\frac{\\partial M}{\\partial y} = \\frac{\\partial N}{\\partial x}$. 3. In differential geometry, a differential $k$-form $\\omega$ is exact if $\\omega = d\\eta$ for some $(k-1)$-form $\\eta$."
    ),

    # 121. exchangeable cation percentage
    1191: (
        "In soil chemistry, the proportion of the soil's cation exchange capacity (CEC) satisfied by a specific exchangeable cation $M^{n+}$:\n\n"
        "$$\\text{ECP} = \\frac{\\text{Exchangeable } M^{n+}\\,(\\text{meq}/100\\,\\text{g soil})}{\\text{Cation Exchange Capacity } (\\text{meq}/100\\,\\text{g soil})} \\times 100\\%$$"
    ),

    # 122. exchangeable sodium percentage
    1194: (
        "In agricultural soil science, the degree of saturation of the soil exchange complex with sodium ions ($\\text{Na}^+$):\n\n"
        "$$\\text{ESP} = \\frac{[\\text{Na}^+]}{\\text{CEC}} \\times 100\\%$$\n\n"
        "where $[\\text{Na}^+]$ is exchangeable sodium in $\\text{meq}/100\\,\\text{g}$ and $\\text{CEC}$ is total cation exchange capacity. Soils with $\\text{ESP} > 15\\%$ are classified as sodic, exhibiting clay dispersion and degraded permeability."
    ),

    # 124. exothermic reaction
    1257: (
        "A chemical or physical reaction that releases net thermal energy to its surroundings, characterized by a negative standard change in enthalpy:\n\n"
        "$$\\Delta H < 0$$\n\n"
        "Because enthalpy of reactants exceeds enthalpy of products ($H_{\\text{reactants}} > H_{\\text{products}}$), heat is liberated ($\text{Reactants} \\to \\text{Products} + \\text{Heat}$). Examples include hydrocarbon combustion ($2\\text{C}_2\\text{H}_6 + 7\\text{O}_2 \\to 4\\text{CO}_2 + 6\\text{H}_2\\text{O}, \\Delta H_c^\\circ = -1560.7\\,\\text{kJ}\\cdot\\text{mol}^{-1}$), acid-base neutralizations, and cellular respiration."
    ),

    # 125. expected outcome
    1273: (
        "The probability-weighted average outcome over infinitely many repetitions of a random variable $X$. For a discrete random variable with outcomes $x_i$ and probabilities $p_i = P(X = x_i)$, the expected outcome is:\n\n"
        "$$\\mathbb{E}[X] = \\sum_{i=1}^n x_i p_i$$\n\n"
        "For a fair six-sided die where $p_i = 1/6$ for $x_i \\in \\{1, 2, 3, 4, 5, 6\\}$, the expected outcome is $\\mathbb{E}[X] = \\frac{1 + 2 + 3 + 4 + 5 + 6}{6} = 3.5$."
    ),

    # 126. expected value
    1275: (
        "The first central moment and mean $\\mu$ of a probability distribution, denoted $\\mathbb{E}[X]$ or $E(X)$. For a discrete random variable, $\\mathbb{E}[X] = \\sum_i x_i P(X = x_i)$; for a continuous random variable with probability density function $f(x)$:\n\n"
        "$$\\mathbb{E}[X] = \\int_{-\infty}^\\infty x f(x)\\,dx$$\n\n"
        "By linearity of expectation, $\\mathbb{E}[aX + bY + c] = a\\mathbb{E}[X] + b\\mathbb{E}[Y] + c$ for any constants $a, b, c$."
    ),

    # 128. exponent
    1297: (
        "The mathematical index $n$ indicating the power to which a base $x$ is raised ($x^n$). Standard algebraic laws of exponents include:\n\n"
        "$$x^a \\cdot x^b = x^{a+b}, \\quad \\frac{x^a}{x^b} = x^{a-b}, \\quad (x^a)^b = x^{ab}$$\n\n"
        "$$x^{-n} = \\frac{1}{x^n}, \\quad x^{1/n} = \\sqrt[n]{x}, \\quad x^0 = 1 \\quad (x \\neq 0)$$"
    ),

    # 129. exponential
    1298: (
        "A mathematical term describing functions, equations, or curves where an independent variable appears in the exponent, such as $y = a^x$ or $y = e^{kx}$. It exhibits growth (or decay) proportional to its current value: $\\frac{dy}{dx} = ky$."
    ),

    # 130. exponential decay
    1299: (
        "The reduction of a quantity at a rate proportional to its current value over time, modeled by the differential equation $\\frac{dN}{dt} = -\\lambda N$ and solved by:\n\n"
        "$$N(t) = N_0 e^{-\\lambda t} = N_0 \\left(\\frac{1}{2}\\right)^{t / t_{1/2}}$$\n\n"
        "where $N_0$ is the initial quantity, $\\lambda > 0$ is the decay constant, and $t_{1/2} = \\frac{\\ln 2}{\\lambda}$ is the half-life. Observed in radioactive decay, RC circuit discharge, and first-order chemical reaction kinetics."
    ),

    # 131. exponential distribution
    1300: (
        "A continuous probability distribution describing the time between Poisson point process events, with probability density function (PDF):\n\n"
        "$$f(x; \\lambda) = \\begin{cases} \\lambda e^{-\\lambda x}, & x \\ge 0 \\\\ 0, & x < 0 \\end{cases}$$\n\n"
        "where $\\lambda > 0$ is the rate parameter. Possesses mean $\\mathbb{E}[X] = \\frac{1}{\\lambda}$, variance $\\operatorname{Var}(X) = \\frac{1}{\\lambda^2}$, and the unique memoryless property $P(X > s + t \\mid X > s) = P(X > t)$."
    ),

    # 132. exponential function
    1301: (
        "The fundamental mathematical function $f(x) = e^x$ or $\\exp(x)$, where $e \\approx 2.71828$ is Euler's number. Defined as the unique non-trivial function equal to its own derivative with $f(0) = 1$:\n\n"
        "$$\\frac{d}{dx}(e^x) = e^x, \\quad \\int e^x\\,dx = e^x + C$$\n\n"
        "Represented globally by the infinite power series $e^x = \\sum_{n=0}^\\infty \\frac{x^n}{n!}$."
    ),

    # 133. exponential series
    1304: (
        "The Maclaurin power series expansion for the exponential function, which converges absolutely for every complex number $z \\in \\mathbb{C}$:\n\n"
        "$$e^z = \\sum_{n=0}^\\infty \\frac{z^n}{n!} = 1 + z + \\frac{z^2}{2!} + \\frac{z^3}{3!} + \\frac{z^4}{4!} + \\dots$$\n\n"
        "with infinite radius of convergence ($R = \\infty$)."
    ),

    # 135. exterior product
    1346: (
        "The alternating multilinear product (wedge product $\\wedge$) in exterior algebra (Grassmann algebra). For a differential $p$-form $\\alpha$ and a $q$-form $\\beta$, the exterior product satisfies graded commutativity:\n\n"
        "$$\\alpha \\wedge \\beta = (-1)^{pq} (\\beta \\wedge \\alpha)$$\n\n"
        "For 1-forms and vectors, $\\mathbf{u} \\wedge \\mathbf{v} = -(\\mathbf{v} \\wedge \\mathbf{u})$, and $\\mathbf{v} \\wedge \\mathbf{v} = 0$. The magnitude $\|\mathbf{u} \\wedge \\mathbf{v}\\|$ corresponds to the area of the parallelogram spanned by $\\mathbf{u}$ and $\\mathbf{v}$."
    ),

    # 138. external work
    1356: (
        "In thermodynamics, the work $W$ performed by a system expanding quasi-statically against an external pressure $p_{\\text{ext}}$ as its volume changes from $V_1$ to $V_2$:\n\n"
        "$$W = \\int_{V_1}^{V_2} p_{\\text{ext}}\\,dV$$\n\n"
        "Graphically represented as the area beneath the process path on a $p$-$V$ pressure-volume indicator diagram. For a cyclic closed system, the net external work done per cycle equals the area enclosed by the cycle curve."
    ),

    # 139. extinction coefficient
    1359: (
        "The molar attenuation coefficient (or molar absorptivity $\\varepsilon$) in the Beer-Lambert law, quantifying how strongly a chemical solute absorbs light at a given wavelength $\\lambda$:\n\n"
        "$$A = \\varepsilon b c = -\\log_{10}\\left(\\frac{I}{I_0}\\right)$$\n\n"
        "where $A$ is dimensionless optical absorbance, $\\varepsilon$ is the molar extinction coefficient (typically in $\\text{L}\\cdot\\text{mol}^{-1}\\cdot\\text{cm}^{-1}$), $b$ is optical path length in $\\text{cm}$, and $c$ is molar concentration in $\\text{mol}\\cdot\\text{L}^{-1}$."
    ),

    # 140. extreme point
    1385: (
        "In convex analysis, a point $\\mathbf{x}$ in a convex set $C$ that does not lie in the interior of any line segment connecting two distinct points of $C$. Formally, $\\mathbf{x} \\in C$ is an extreme point if:\n\n"
        "$$\\mathbf{x} = t \\mathbf{y} + (1 - t)\\mathbf{z} \\quad (\\mathbf{y}, \\mathbf{z} \\in C,\\, 0 < t < 1) \\implies \\mathbf{x} = \\mathbf{y} = \\mathbf{z}$$\n\n"
        "By the Krein-Milman theorem, every compact convex subset of a locally convex space is the closed convex hull of its extreme points."
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

print(f"\nSuccessfully enriched {count} terms in Section E Batch 3.")
