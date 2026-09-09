"""
enrich_section_e_batch_1.py
===========================
Section E Formula Enrichment - Batch 1 (Terms 1 to 45)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

e_entries = data.get('E', [])

UPDATES = {
    # 4. economy
    102: (
        "A mathematical model of an economic system in which, commonly, there are $m$ producers, each with a production set $P_j$ and $n$ consumers, each with a consumption set $C_i$ and an associated ordering $\\le_i$. These sets lie on a Euclidean space, whose dimension corresponds to the number of goods in the economy. There is a total resource level $w$. The producers each produce a vector $y_j \\in P_j$ and the consumers have a demand $x_i \\in C_i$. These $m + n$ elements define a state of the economy. The excess demand is $\\sum x_i - \\sum y_j - w$ and a market equilibrium occurs if excess demand is zero. Individual consumers will try to maximize their preference satisfaction; this leads to the study of equilibria that occur as a market equilibrium together with a pricing of resources such that every producer maximizes profit and every consumer optimizes satisfaction."
    ),

    # 5. eddington limit
    126: (
        "A theoretical limit for the maximum value of the brightness of a star of a given mass, named after British astronomer and physicist Arthur Stanley Eddington and given as:\n\n$$L_{\\text{Edd}} = \\frac{4\\pi G M m_p c}{\\sigma_T}$$\n\nwhere $G$ is the gravitational constant, $M$ is the mass of the luminous object, $m_p$ is the mass of a proton, $c$ is the speed of light, and $\\sigma_T$ is the Thomson scattering cross-section (effective area) of an electron. This limit exists because the outward radiation pressure has to balance, but not exceed, the inward gravitational force. A star emitting radiation at greater than the Eddington limit would blow away its outer layers via radiation pressure."
    ),

    # 6. effective nuclear charge
    161: (
        "The apparent nuclear or net positive charge which an outermost electron actually experiences through attraction in a multi-electron atom as a result of the shielding effect by inner electrons. Its symbol is $Z_{\\text{eff}}$. The effective nuclear charge is given by the expression:\n\n$$Z_{\\text{eff}} = Z - S$$\n\nwhere $Z$ is the atomic number (number of protons in the nucleus) and $S$ is the screening or shielding constant (the average number of shielding electrons between the nucleus and the valence electron)."
    ),

    # 7. efficiency
    172: (
        "1. A measure of the performance or how well a machine or energy-converting device transforms input energy into useful work. It is the percentage ratio of useful work output to total work input:\n\n$$\\text{Efficiency} = \\frac{\\text{Energy Output}}{\\text{Energy Input}} \\times 100\\%$$\n\nFor example, a gear transmission is $97\\%$ efficient when the useful energy output is $97\\%$ of the input, with $3\\%$ lost as heat due to friction. 2. In chemistry, the ratio between useful energy delivered or bound and the energy supplied. Its symbol is $\\eta$."
    ),

    # 8. effort
    179: (
        "The force applied to a machine to move a load, often expressed in mechanics in relation to work and mechanical advantage. In terms of work done by the effort:\n\n$$\\text{Work} = \\text{Effort} \\times \\text{Distance moved by effort}$$\n\nand mechanical advantage is defined as $\\text{M.A.} = \\frac{\\text{Load}}{\\text{Effort}}$."
    ),

    # 9. egoroff's theorem
    192: (
        "Named after the Russian mathematician D. F. Egorov (1869–1931), the foundational measure-theoretic result stating that if a sequence of measurable functions $f_n$ on a set of finite measure $E$ converges almost everywhere to a finite limit function $f$, then for every $\\varepsilon > 0$, there exists a measurable subset $F \\subset E$ with measure $\\mu(F) < \\varepsilon$ such that $f_n$ converges uniformly to $f$ on $E \\setminus F$."
    ),

    # 11. eigenvalue
    202: (
        "In linear algebra, for a square matrix $A$, if there exists a nonzero vector $x$ (the eigenvector) such that:\n\n$$Ax = \\lambda x$$\n\nfor a scalar $\\lambda$, then $\\lambda$ is called an eigenvalue of $A$. The eigenvalues are the roots of the characteristic equation $\\det(A - \\lambda I) = 0$. For a linear operator $T$, it is a scalar $\\lambda$ satisfying $T(x) = \\lambda x$ for some $x \\neq 0$."
    ),

    # 12. eigenvalue equation
    203: (
        "A parameter-dependent equation of the form $A x = \\lambda x$ (or $\\hat{H}\\psi = E\\psi$ in quantum mechanics) that possesses non-trivial (non-vanishing) solutions only for specific values of the parameter $\\lambda$, called eigenvalues. The corresponding non-trivial solutions are eigenvectors or eigenfunctions."
    ),

    # 13. eigenvector
    204: (
        "In linear algebra, a nonzero vector $x$ that, when transformed by a square matrix or linear operator $A$, changes only by a scalar factor $\\lambda$ (the eigenvalue):\n\n$$Ax = \\lambda x$$\n\nmeaning its direction remains unchanged (or reversed if $\\lambda < 0$)."
    ),

    # 14. eigh tcur ve (eight curve)
    205: (
        "A quartic curve (also called the lemniscate-like figure-eight curve) having the Cartesian equation:\n\n$$x^4 = a^2 (x^2 - y^2)$$\n\nwhich has the visual appearance of a figure eight or the infinity symbol $\\infty$ lying on its side."
    ),

    # 15. einstein's equation
    211: (
        "1. Einstein's mass-energy equivalence equation:\n\n$$E = mc^2$$\n\nwhere $E$ is the energy, $m$ is the relativistic or rest mass, and $c$ is the speed of light in vacuum ($c \\approx 3 \\times 10^8\\text{ m/s}$). 2. Einstein's photoelectric equation:\n\n$$E_{\\max} = hf - W_0 = hf - hf_0$$\n\nwhere $E_{\\max} = \\frac{1}{2}mv_{\\max}^2$ is the maximum kinetic energy of emitted photoelectrons, $h$ is Planck's constant, $f$ is incident photon frequency, and $W_0$ is the metal work function ($f_0$ being the threshold frequency). 3. Einstein's Field Equations (EFE) in general relativity: $G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}$."
    ),

    # 16. einstein, albert
    212: (
        "German-born theoretical physicist (1879–1955) and Nobel laureate, widely regarded as one of the greatest physicists of all time. Famous for formulating the Special Theory of Relativity (1905), General Theory of Relativity (1915), the mass-energy equivalence formula $E = mc^2$, and the explanation of the photoelectric effect ($E = hf - W$), for which he received the 1921 Nobel Prize in Physics."
    ),

    # 17. einstein-smoluchowski equation
    213: (
        "The relation discovered independently by Albert Einstein (1905) and Marian Smoluchowski (1906) connecting the microscopic diffusion coefficient $D$ of Brownian particles to thermal energy and mobility:\n\n$$D = \\mu k_B T = \\frac{k_B T}{6\\pi \\eta r}$$\n\nand in jump-diffusion: $D = \\frac{\\lambda^2}{2\\tau}$, where $\\lambda$ is the mean jump distance and $\\tau$ is the characteristic jump time."
    ),

    # 18. eisenstein's criterion
    215: (
        "A criterion for the irreducibility of a polynomial with integer coefficients. For a polynomial $P(x) = a_n x^n + a_{n-1} x^{n-1} + \\dots + a_1 x + a_0$, if there exists a prime $p$ such that $p \\nmid a_n$, $p \\mid a_i$ for all $0 \\le i < n$, and $p^2 \\nmid a_0$, then $P(x)$ is irreducible over the rational numbers $\\mathbb{Q}$. For example, $x^n - p$ is irreducible for every prime $p$ and $n \\ge 1$."
    ),

    # 19. elastance
    226: (
        "The reciprocal of capacitance (the electrostatic stiffness or opposition to storing electric charge). Defined as:\n\n$$S = \\frac{1}{C} = \\frac{V}{Q}$$\n\nIts SI unit is the reciprocal farad ($\\text{F}^{-1}$), sometimes historically referred to as the daraf."
    ),

    # 20. elastic modules (elastic modulus)
    230: (
        "The ratio of the stress applied to a body to the resulting strain in the elastic deformation region:\n\n$$\\text{Modulus of Elasticity} = \\frac{\\text{Stress}}{\\text{Strain}}$$\n\nwhere $\\text{Stress} = \\frac{F}{A}$ (measured in $\\text{N/m}^2$ or $\\text{Pa}$) and $\\text{Strain} = \\frac{\\Delta L}{L}$ is dimensionless. The unit of elastic modulus is the pascal ($\\text{Pa}$ or $\\text{N/m}^2$). Common forms include Young's modulus $E$, shear modulus $G$, and bulk modulus $K$."
    ),

    # 21. electric charge
    246: (
        "A fundamental property of matter that governs electromagnetic interactions. Electric charge $Q$ is related to electric current $I$ and time $t$ by:\n\n$$Q = I \\times t$$\n\nwith the SI unit being the coulomb ($\\text{C} = \\text{A}\\cdot\\text{s}$). The elementary charge carried by a proton is $+e$ and by an electron is $-e$, where $e \\approx 1.602 \\times 10^{-19}\\text{ C}$."
    ),

    # 22. electric constant
    248: (
        "The absolute permittivity of free space (vacuum permittivity), symbolized by $\\varepsilon_0$. It connects electric charge to mechanical force in Coulomb's law:\n\n$$\\varepsilon_0 = \\frac{1}{\\mu_0 c^2} \\approx 8.854 \\times 10^{-12}\\text{ F}\\cdot\\text{m}^{-1}$$\n\n(or $\\text{C}^2\\cdot\\text{N}^{-1}\\cdot\\text{m}^{-2}$)."
    ),

    # 23. electric current density
    250: (
        "A vector quantity $\\mathbf{J}$ representing the electric current per unit cross-sectional area:\n\n$$J = \\frac{I}{A}$$\n\nwith SI unit amperes per square metre ($\\text{A}\\cdot\\text{m}^{-2}$). Microscopically, $\\mathbf{J} = n q \\mathbf{v}_d = \\sigma \\mathbf{E}$, where $n$ is charge carrier density, $q$ is charge, $\\mathbf{v}_d$ is drift velocity, $\\sigma$ is electrical conductivity, and $\\mathbf{E}$ is electric field."
    ),

    # 24. electric displacement
    253: (
        "The electric displacement field $\\mathbf{D}$, defined in a dielectric medium as:\n\n$$\\mathbf{D} = \\varepsilon_0 \\mathbf{E} + \\mathbf{P}$$\n\nwhere $\\varepsilon_0$ is the vacuum permittivity, $\\mathbf{E}$ is the electric field strength, and $\\mathbf{P}$ is the electric polarization density. By Gauss's law for displacement, $\\nabla \\cdot \\mathbf{D} = \\rho_{\\text{free}}$, measuring the charge density of free charges."
    ),

    # 25. electric field
    255: (
        "A vector field around charged particles that exerts an electrostatic force on other charges. The electric field strength $\\mathbf{E}$ at a point is defined as:\n\n$$\\mathbf{E} = \\frac{\\mathbf{F}}{q}$$\n\nwhere $\\mathbf{F}$ is the electric force experienced by a small positive test charge $q$. Measured in newtons per coulomb ($\\text{N/C}$) or volts per metre ($\\text{V/m}$)."
    ),

    # 26. electric field strength
    256: (
        "The magnitude of the electric force exerted per unit positive charge placed at that point:\n\n$$E = \\frac{F}{Q}$$\n\nFor a point charge $Q$ at distance $r$ in vacuum, Coulomb's law gives:\n\n$$E = \\frac{1}{4\\pi \\varepsilon_0} \\frac{Q}{r^2}$$\n\nIts SI units are volts per metre ($\\text{V}\\cdot\\text{m}^{-1}$) or newtons per coulomb ($\\text{N}\\cdot\\text{C}^{-1}$)."
    ),

    # 27. electric flux
    257: (
        "The measure of the distribution of the electric field through a given surface. For a uniform field $\\mathbf{E}$ through area $\\mathbf{A}$:\n\n$$\\Phi_E = \\mathbf{E} \\cdot \\mathbf{A} = E A \\cos\\theta$$\n\nand in general by surface integral $\\Phi_E = \\iint_S \\mathbf{E} \\cdot d\\mathbf{A}$. By Gauss's law, the net electric flux through any closed surface is $\\Phi_E = \\frac{Q_{\\text{enc}}}{\\varepsilon_0}$."
    ),

    # 28. electric polarisation
    264: (
        "The vector field $\\mathbf{P}$ representing the density of permanent or induced electric dipole moments $\\mathbf{p}$ in a dielectric material:\n\n$$\\mathbf{P} = \\frac{\\sum \\mathbf{p}}{\\Delta V}$$\n\nIn linear isotropic dielectrics, $\\mathbf{P} = \\varepsilon_0 \\chi_e \\mathbf{E}$, where $\\chi_e$ is the electric susceptibility. Its SI unit is coulombs per square metre ($\\text{C}\\cdot\\text{m}^{-2}$)."
    ),

    # 29. electric power
    266: (
        "The rate at which electrical energy is transferred by an electric circuit. For direct current (DC):\n\n$$P = IV = I^2 R = \\frac{V^2}{R}$$\n\nwhere $V$ is potential difference, $I$ is current, and $R$ is resistance. In alternating current (AC) circuits, real power is given by:\n\n$$P = V_{\\text{rms}} I_{\\text{rms}} \\cos\\phi$$\n\nwhere $\\cos\\phi$ is the power factor. The SI unit of power is the watt ($\\text{W} = \\text{J/s}$)."
    ),

    # 30. electrical conductance
    275: (
        "A measure of how easily electric current flows through an electrical element. Conductance $G$ is the reciprocal of electrical resistance $R$:\n\n$$G = \\frac{1}{R} = \\frac{I}{V}$$\n\nIts SI unit is the siemens ($\\text{S} = \\Omega^{-1}$)."
    ),

    # 31. electrical conductivity
    276: (
        "The intrinsic material property measuring the ability to conduct electric current, defined as the reciprocal of electrical resistivity $\\rho$:\n\n$$\\sigma = \\frac{1}{\\rho} = \\frac{L}{R A}$$\n\nwhere $R$ is electrical resistance, $A$ is cross-sectional area, and $L$ is length of the conductor. Its SI unit is siemens per metre ($\\text{S}\\cdot\\text{m}^{-1}$)."
    ),

    # 32. electrical energy
    279: (
        "The energy derived from electric potential energy or the flow of electric charge. Given by:\n\n$$E = P \\times t = IVt = I^2 Rt = \\frac{V^2}{R}t$$\n\nFor a single electron moving through potential difference $V$, $E = eV$, where $1\\text{ eV} \\approx 1.602 \\times 10^{-19}\\text{ J}$. In commercial utility metering, energy is billed in kilowatt-hours ($1\\text{ kWh} = 3.6 \\times 10^6\\text{ J}$)."
    ),

    # 34. electron beam
    349: (
        "A stream of electrons emitted from a cathode and accelerated through a potential difference $V$. By conservation of energy, kinetic energy gained equals electrical potential energy lost:\n\n$$\\frac{1}{2} m_e v^2 = eV \\implies v = \\sqrt{\\frac{2eV}{m_e}}$$\n\nwhere $m_e$ is the electron mass, $e$ is electronic charge, and $v$ is velocity."
    ),

    # 36. electron rest mass
    386: (
        "The rest mass of a stationary electron, a fundamental physical constant denoted $m_e$:\n\n$$m_e \\approx 9.1093837 \\times 10^{-31}\\text{ kg} \\approx 0.5109989\\text{ MeV}/c^2$$"
    ),

    # 38. element
    455: (
        "1. In set theory, an object belonging to a set ($x \\in A$). The $p$-elements of a group are those of order $p^\\alpha$ for prime $p$. 2. In calculus, an infinitesimal quantity summed in an integral, such as $dA = f(x)\\,dx$ in $\\int_a^b f(x)\\,dx$. 3. In chemistry, a pure chemical substance consisting of atoms with the same atomic number $Z$."
    ),

    # 40. elementary function
    461: (
        "A function of one variable built up from a finite number of arithmetic operations ($+,-,\\times,\\div$), roots, exponentials, logarithms, trigonometric functions, and their inverse functions through repeated composition. For example: $f(x) = \\ln\\left(\\arctan\\left(\\sqrt{e^{x^2} + 1}\\right)\\right)$."
    ),

    # 41. elementary reduction
    468: (
        "In combinatorial group theory, the replacement of a subword of the form $x x^{-1}$ or $x^{-1} x$ in a free group word by the empty word $\\varepsilon$, or the process of reducing a word to its canonical irreducible form."
    ),

    # 42. eliminant
    480: (
        "The condition or determinant resulting from eliminating variables between simultaneous algebraic equations. For three homogeneous linear equations in two unknowns $a_i x + b_i y + c_i = 0$ ($i=1,2,3$), the eliminant is the determinant of coefficients:\n\n$$\\begin{vmatrix} a_1 & b_1 & c_1 \\\\ a_2 & b_2 & c_2 \\\\ a_3 & b_3 & c_3 \\end{vmatrix} = 0$$"
    ),

    # 43. elli ptic equa tion (elliptic equation)
    484: (
        "A second-order partial differential equation of the general form:\n\n$$a u_{xx} + b u_{xy} + c u_{yy} + d u_x + e u_y + f u = g$$\n\nsatisfying the elliptic discriminant condition $b^2 - 4ac < 0$. The prototypical example is Laplace's equation $\\nabla^2 u = u_{xx} + u_{yy} = 0$."
    ),

    # 44. ellipse
    486: (
        "A plane curve surrounding two focal points $F_1, F_2$ such that the sum of the distances to the two focal points is constant: $PF_1 + PF_2 = 2a$. The standard Cartesian equation of an ellipse centered at the origin is:\n\n$$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1$$\n\nwhere $a$ is the semi-major axis, $b$ is the semi-minor axis, and eccentricity $e = \\sqrt{1 - \\frac{b^2}{a^2}}$."
    ),

    # 45. ellipsoid
    487: (
        "A closed quadric surface that is a three-dimensional analogue of an ellipse. The standard Cartesian equation of an ellipsoid centered at the origin is:\n\n$$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} + \\frac{z^2}{c^2} = 1$$\n\nwhere $a, b, c$ denote the semi-principal axes along the $x, y, z$ directions respectively."
    ),
}

print(f"Applying {len(UPDATES)} enriched formulas to Section E...")
count = 0
for idx, new_def in UPDATES.items():
    if idx < len(e_entries):
        old_def = e_entries[idx]['definition']
        e_entries[idx]['definition'] = new_def
        word = e_entries[idx]['word']
        print(f"  + Enriched [{idx:4d}] {word}")
        count += 1

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSaved dictionary.json ({count} entries updated).")

# Recompile core_dictionary.js
print("Recompiling core_dictionary.js...")
js_content = "const CoreDictionary = " + json.dumps(data, ensure_ascii=False) + ";\n"
js_content += "if (typeof window !== 'undefined') { window.CoreDictionary = CoreDictionary; }\n"
js_content += "if (typeof module !== 'undefined') { module.exports = CoreDictionary; }\n"

with open('core_dictionary.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("core_dictionary.js successfully recompiled!")
