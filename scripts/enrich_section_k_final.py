"""
enrich_section_k_final.py
=========================
Section K Formula Enrichment - Final Batch (Candidates 21 to 41)
Completing Section K formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys
import os
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_PATH = os.path.join(BASE_DIR, 'dictionary.json')

with open(DICT_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

k_entries = data.get('K', [])

UPDATES = {
    # 21. kinematic equation (index 130)
    130: (
        "In classical Newtonian kinematics, four fundamental equations relating displacement $s$, initial velocity $u$, final velocity $v$, "
        "constant linear acceleration $a$, and elapsed time $t$ for motion in a straight line:\n\n"
        "$$v = u + at$$\n\n"
        "$$s = \\frac{u + v}{2}t$$\n\n"
        "$$s = ut + \\frac{1}{2}at^2$$\n\n"
        "$$v^2 = u^2 + 2as$$\n\n"
        "Valid strictly when acceleration is uniform ($a = \\text{const}$). Derived by integrating constant acceleration $a = \\frac{dv}{dt} = \\frac{d^2s}{dt^2}$."
    ),

    # 22. kinematic viscosity (index 131)
    131: (
        "In fluid dynamics, the ratio of dynamic (shear) viscosity $\\mu$ of a fluid to its mass density $\\rho$, denoted $\\nu$:\n\n"
        "$$\\nu = \\frac{\\mu}{\\rho}, \\quad \\text{SI unit: } \\text{m}^2\\cdot\\text{s}^{-1}$$\n\n"
        "In CGS units, $1\\,\\text{stokes (St)} = 1\\,\\text{cm}^2/\\text{s} = 10^{-4}\\,\\text{m}^2/\\text{s}$. Kinematic viscosity represents the diffusivity "
        "of momentum in a moving fluid, appearing as the characteristic diffusion coefficient in the Navier-Stokes equations and governing the Reynolds number "
        "$\\text{Re} = \\frac{u L}{\\nu}$."
    ),

    # 23. kinetic energy (index 139)
    139: (
        "The scalar physical work an object can do by virtue of its translational or rotational motion. In classical mechanics for a particle of mass $m$ "
        "moving at speed $v \\ll c$:\n\n"
        "$$E_k = \\frac{1}{2}mv^2 = \\frac{p^2}{2m}, \\quad \\text{SI unit: joule (J)}$$\n\n"
        "where $p = mv$ is linear momentum. For a rigid body rotating with angular velocity $\\omega$ about an axis with moment of inertia $I$, rotational kinetic energy "
        "is $E_{k,\\text{rot}} = \\frac{1}{2}I\\omega^2$. By the work-energy theorem, net work done equals the change in kinetic energy: $W_{\\text{net}} = \\Delta E_k$."
    ),

    # 24. kinetic temperature (index 144)
    144: (
        "In statistical mechanics and kinetic theory of gases, the absolute thermodynamic temperature $T$ defined directly in terms of the mean translational "
        "kinetic energy of gas particles having three degrees of translational freedom:\n\n"
        "$$\\langle E_k \\rangle = \\frac{1}{2}m\\langle v^2 \\rangle = \\frac{3}{2}k_B T \\implies T = \\frac{m\\langle v^2 \\rangle}{3k_B}$$\n\n"
        "where $k_B = 1.380649 \\times 10^{-23}\\,\\text{J/K}$ is the Boltzmann constant, and $\\sqrt{\\langle v^2 \\rangle} = v_{\\text{rms}} = \\sqrt{\\frac{3k_B T}{m}}$ "
        "is root-mean-square molecular speed. At thermal equilibrium, kinetic temperature strictly coincides with thermodynamic temperature."
    ),

    # 25. kirchoff's law of thermal radiation (index 159)
    159: (
        "A law of radiative transfer established by Gustav Kirchhoff in 1859 stating that for an arbitrary body in thermodynamic equilibrium with its radiation field, "
        "the spectral directional emissivity $\\varepsilon(\\lambda, T)$ equals its spectral directional absorptivity $\\alpha(\\lambda, T)$ at every wavelength $\\lambda$ and temperature $T$:\n\n"
        "$$\\varepsilon(\\lambda, T) = \\alpha(\\lambda, T) \\quad \\text{or} \\quad \\frac{e(\\lambda, T)}{\\alpha(\\lambda, T)} = e_{\\text{blackbody}}(\\lambda, T)$$\n\n"
        "Consequently, good absorbers of radiation at a given wavelength are equally good emitters at that same wavelength, and an ideal blackbody ($\\alpha = 1$) is the most efficient emitter possible ($\\varepsilon = 1$)."
    ),

    # 26. kirchoff's laws (index 160)
    160: (
        "Two foundational circuit laws formulated by Gustav Kirchhoff in 1845 for electric network analysis:\n\n"
        "1. **Kirchhoff's Current Law (KCL / Junction Rule)**: The algebraic sum of all electric currents entering any circuit node or junction is zero, representing conservation of electric charge:\n"
        "$$\\sum_{k=1}^n I_k = 0 \\implies \\sum I_{\\text{in}} = \\sum I_{\\text{out}}$$\n\n"
        "2. **Kirchhoff's Voltage Law (KVL / Loop Rule)**: The algebraic sum of all electromotive forces (emfs) and potential drops around any closed conducting loop is zero, representing conservation of energy:\n"
        "$$\\sum_{k=1}^m V_k = 0 \\implies \\sum \\mathcal{E} = \\sum I R$$"
    ),

    # 27. kleiber's law (index 166)
    166: (
        "An allometric scaling law in comparative physiology formulated by Max Kleiber in 1932. It demonstrates that the basal metabolic rate $R$ (or $B$) "
        "of an animal scales to the $\\frac{3}{4}$-power of its total body mass $M$ across organisms ranging from unicellular microbes to blue whales:\n\n"
        "$$R = R_0 M^{3/4} = R_0 M^{0.75}$$\n\n"
        "Because mass-specific metabolic rate scales as $\\frac{R}{M} \\propto M^{-1/4}$, larger animals exhibit significantly lower metabolic rates per gram of body tissue than smaller animals. "
        "West, Brown, and Enquist (WBE model) explained this $\\frac{3}{4}$ exponent based on the fractal geometry of internal branching nutrient distribution networks."
    ),

    # 28. klein four-group (index 168)
    168: (
        "In abstract algebra, the smallest non-cyclic group (denoted $V$ or $V_4$, for *Vierergruppe*, introduced by Felix Klein in 1884). "
        "An abelian group of order $4$ isomorphic to the direct product $\\mathbb{Z}_2 \\times \\mathbb{Z}_2$:\n\n"
        "$$V_4 = \\{e, a, b, c\\}$$\n\n"
        "Every non-identity element has order $2$ (involution): $a^2 = b^2 = c^2 = e$, with group multiplication table satisfying $ab = c$, $bc = a$, and $ca = b$. "
        "Forms the symmetry group of a non-square rectangle or rhombus in Euclidean geometry."
    ),

    # 29. klein-gordon equation (index 170)
    170: (
        "In relativistic quantum mechanics, the second-order wave equation governing spin-$0$ scalar bosons (such as pions and the Higgs boson), "
        "formulated by Oskar Klein and Walter Gordon in 1926 from the relativistic energy-momentum relation $E^2 = p^2c^2 + m^2c^4$:\n\n"
        "$$\\left( \\frac{1}{c^2} \\frac{\\partial^2}{\\partial t^2} - \\nabla^2 + \\frac{m^2 c^2}{\\hbar^2} \\right) \\psi = 0$$\n\n"
        "In covariant 4-vector notation using the d'Alembertian operator $\\square = \\partial_\\mu \\partial^\\mu$:\n\n"
        "$$(\\square + \\mu^2)\\psi = 0, \\quad \\text{where } \\mu = \\frac{mc}{\\hbar}$$"
    ),

    # 30. knapsack problem (index 177)
    177: (
        "In combinatorial optimization and theoretical computer science, an NP-complete integer programming problem where given a set of $n$ items, "
        "each with weight $w_i$ and value $c_i$, and a knapsack of maximum weight capacity $W$, the objective is to maximize total packed value:\n\n"
        "$$\\max \\sum_{i=1}^n c_i x_i \\quad \\text{subject to} \\quad \\sum_{i=1}^n w_i x_i \\le W, \\quad x_i \\in \\{0, 1\\}$$\n\n"
        "Solvable in pseudo-polynomial time $\\mathcal{O}(nW)$ using dynamic programming. Forms the foundation of Merkle-Hellman knapsack cryptosystems and resource-allocation scheduling."
    ),

    # 31. kohlrausch equation (index 196)
    196: (
        "An empirical relationship established by Friedrich Kohlrausch in 1876 describing the concentration dependence of molar conductivity $\\Lambda_m$ "
        "for strong electrolytes in dilute aqueous solutions:\n\n"
        "$$\\Lambda_m = \\Lambda_m^\\circ - K \\sqrt{c}$$\n\n"
        "where $\\Lambda_m^\\circ$ is limiting molar conductivity at infinite dilution, $c$ is electrolyte concentration, and $K$ is Kohlrausch's coefficient, "
        "which depends on solution stoichiometry, dielectric constant, and solvent viscosity as explained by the Debye-Hückel-Onsager conductance theory."
    ),

    # 32. kohlrausch's law (index 197)
    197: (
        "The law of independent migration of ions established by Friedrich Kohlrausch in 1875. It states that at infinite dilution, where interionic "
        "attractions vanish, the limiting molar conductivity $\\Lambda_m^\\circ$ of any electrolyte is the sum of the individual contributions of its constituent cations and anions:\n\n"
        "$$\\Lambda_m^\\circ = \\nu_+ \\lambda_+^\\circ + \\nu_- \\lambda_-^\\circ$$\n\n"
        "where $\\nu_+$ and $\\nu_-$ are the numbers of cations and anions per formula unit, and $\\lambda_+^\\circ$ and $\\lambda_-^\\circ$ are limiting ionic conductivities. "
        "Allows determination of $\\Lambda_m^\\circ$ for weak electrolytes (e.g. $\\text{CH}_3\\text{COOH}$) from strong electrolyte data."
    ),

    # 33. kolmogorov-smirnoff test (index 201)
    201: (
        "In non-parametric statistics, the Kolmogorov-Smirnov test ($K\\text{--}S$ test) evaluates whether an empirical sample distribution $F_n(x)$ "
        "agrees with a hypothesized continuous reference cumulative distribution $F_0(x)$. The one-sample test statistic $D_n$ is the supremum distance:\n\n"
        "$$D_n = \\sup_{x} |F_n(x) - F_0(x)|$$\n\n"
        "Because $D_n$ is an exact distribution-free statistic under the null hypothesis $H_0: F = F_0$, critical values depend solely on sample size $n$ rather than the hypothesized distribution."
    ),

    # 34. kramers' degeneracy theorem (index 210)
    210: (
        "In quantum mechanics, a theorem proved by Hendrik Kramers in 1930 stating that for any time-reversal-invariant electronic system possessing an "
        "odd number of half-integer spin fermions (total spin $J = n + \\frac{1}{2}$), every energy eigenstate is at least doubly degenerate (Kramers doublet):\n\n"
        "$$\\hat{\\mathcal{T}}^2 |\\psi\\rangle = (-1)^{2J} |\\psi\\rangle = -|\\psi\\rangle \\implies \\langle \\psi | \\hat{\\mathcal{T}}\\psi \\rangle = 0$$\n\n"
        "This Kramers degeneracy cannot be lifted by any static electric or crystal field; it requires breaking time-reversal symmetry with an external magnetic field $\\mathbf{B}$ (Zeeman effect)."
    ),

    # 35. kramers' law (index 211)
    211: (
        "In stellar astrophysics, an empirical formula derived by Hendrik Kramers in 1923 for the mean Rosseland radiative opacity $\\kappa$ of ionized stellar plasma "
        "dominated by free-free (bremsstrahlung) and bound-free absorption transitions:\n\n"
        "$$\\kappa \\propto \\rho T^{-7/2} = \\kappa_0 \\rho T^{-3.5}$$\n\n"
        "where $\\rho$ is stellar mass density and $T$ is local core temperature. Indicates that opacity decreases rapidly at high temperatures, governing energy transport "
        "in radiative zones of stars with masses $M \\lesssim 1.5\\,M_\\odot$."
    ),

    # 36. krein-milman theorem (index 214)
    214: (
        "A foundational theorem in functional analysis proved by Mark Krein and David Milman in 1940. It states that any non-empty, compact, convex subset $K$ "
        "of a locally convex topological vector space $X$ is equal to the closed convex hull of its extreme points $\\text{ext}(K)$:\n\n"
        "$$K = \\overline{\\text{conv}}(\\text{ext}(K))$$\n\n"
        "Combined with the Banach-Alaoglu theorem, it guarantees that unit balls in dual Banach spaces have abundant extreme points, providing essential representation tools in harmonic analysis and operator algebras."
    ),

    # 37. kronecker delta (index 216)
    216: (
        "A piecewise discrete mathematical function of two integer indices $j$ and $k$, named after Leopold Kronecker. Defined as:\n\n"
        "$$\\delta_{jk} = \\begin{cases} 1 & \\text{if } j = k \\\\[4pt] 0 & \\text{if } j \\neq k \\end{cases}$$\n\n"
        "In matrix algebra, $\\delta_{jk}$ represents the $(j, k)$-th entry of the identity matrix $\\mathbf{I}_n$. In tensor calculus, it acts as the index-substitution operator: "
        "$\\sum_k a_k \\delta_{jk} = a_j$. Relates to the continuous Dirac delta function by $\\delta(x - x_0)$ in distributional limits."
    ),

    # 38. kruskal-wallis test (index 219)
    219: (
        "A non-parametric one-way analysis of variance by ranks (devised by William Kruskal and W. Allen Wallis in 1952) used to test whether $k$ independent samples "
        "originate from the same distribution. Pooling all $N = \\sum n_j$ observations and assigning overall ranks $R_i$, the test statistic $H$ is:\n\n"
        "$$H = \\frac{12}{N(N + 1)} \\sum_{j=1}^k \\frac{R_j^2}{n_j} - 3(N + 1)$$\n\n"
        "where $n_j$ is sample size of group $j$ and $R_j$ is the sum of ranks in group $j$. Under the null hypothesis, $H$ asymptotically follows a chi-squared distribution $\\chi^2(k - 1)$."
    ),

    # 39. krypton (index 221)
    221: (
        "A chemical element belonging to Group 18 (noble gases) of the Periodic Table with chemical symbol $\\text{Kr}$, atomic number $36$, "
        "relative atomic mass $83.798$, density $3.749\\,\\text{g/L}$ at STP, melting point $-157.36\\,^\\circ\\text{C}$ ($115.79\\,\\text{K}$), and boiling point $-153.22\\,^\\circ\\text{C}$ ($119.93\\,\\text{K}$). "
        "Electron configuration: $[\\text{Ar}]\\,3d^{10} 4s^2 4p^6$. Discovered in 1898 by Sir William Ramsay and Morris Travers. "
        "Between 1960 and 1983, the international meter was formally defined as $1,650,763.73$ vacuum wavelengths of the orange-red spectral emission line of krypton-86 ($^{86}\\text{Kr}$)."
    ),

    # 40. kurtosis (index 229)
    229: (
        "In descriptive statistics, a normalized measure of the 'tailedness' of the probability distribution of a real-valued random variable $X$. "
        "The standardized fourth central moment (Pearson's kurtosis $\\beta_2$) is:\n\n"
        "$$\\beta_2 = \\frac{\\mu_4}{\\sigma^4} = \\frac{\\mathbb{E}[(X - \\mu)^4]}{(\\mathbb{E}[(X - \\mu)^2])^2}$$\n\n"
        "Excess kurtosis is defined relative to the standard normal distribution as $\\gamma_2 = \\beta_2 - 3$. A distribution with $\\gamma_2 = 0$ is "
        "mesokurtic; $\\gamma_2 > 0$ is leptokurtic (fat-tailed, higher peak); and $\\gamma_2 < 0$ is platykurtic (thin-tailed, flatter peak)."
    ),

    # 41. kyanite (index 233)
    233: (
        "A typically blue aluminosilicate mineral with chemical formula:\n\n"
        "$$\\text{Al}_2\\text{SiO}_5 \\quad \\text{or} \\quad \\text{Al}_2\\text{O}_3 \\cdot \\text{SiO}_2$$\n\n"
        "A high-pressure polymorph of aluminum silicate (alongside andalusite and sillimanite). Famous for extreme mechanical anisotropy: "
        "Mohs hardness varies from $4.5\\text{--}5.0$ parallel to the length of the crystal bladed axis, up to $6.5\\text{--}7.0$ across the blades. "
        "Used as a geological geobarometer in metamorphic facies and industrially in high-temperature refractory spark plugs and ceramics."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(k_entries):
        w = k_entries[idx]['word']
        k_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (K has {len(k_entries)} entries)")

data['K'] = k_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section K Final.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
