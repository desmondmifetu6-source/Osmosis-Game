"""
enrich_section_k_batch_1.py
===========================
Section K Formula Enrichment - Batch 1 (Candidates 1 to 20)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
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
    # 1. k (index 0)
    0: (
        "1. In the SI metric system, the symbol $\\text{k}$ for the prefix kilo-, denoting a scaling factor of one thousand ($10^3 = 1000$). "
        "For example, $1\\,\\text{kg} = 10^3\\,\\text{g} = 1000\\,\\text{grams}$. "
        "2. In vector calculus, the standard unit Cartesian basis vector pointing along the positive $z$-axis, denoted $\\mathbf{k}$ or $\\hat{\\mathbf{k}}$, "
        "with Cartesian coordinates $(0, 0, 1)$ such that $\\|\\hat{\\mathbf{k}}\\| = 1$. "
        "3. In statistical mechanics and thermodynamics, the Boltzmann constant $k_B$ (or $k$), defined as the ratio of molar gas constant $R$ to Avogadro's number $N_A$:\n\n"
        "$$k_B = \\frac{R}{N_A} = 1.380649 \\times 10^{-23}\\,\\text{J}\\cdot\\text{K}^{-1}$$"
    ),

    # 2. k (index 1)
    1: (
        "1. The symbol $\\text{K}$ for the kelvin, the SI base unit of absolute thermodynamic temperature. "
        "2. In mathematics, the symbol $K(k)$ for the complete elliptic integral of the first kind with elliptic modulus $k \\in [0, 1)$:\n\n"
        "$$K(k) = \\int_0^{\\pi/2} \\frac{d\\theta}{\\sqrt{1 - k^2 \\sin^2 \\theta}} = \\frac{\\pi}{2} \\sum_{n=0}^\\infty \\left( \\frac{(2n)!}{2^{2n}(n!)^2} \\right)^2 k^{2n}$$\n\n"
        "which governs the exact period of a large-amplitude simple pendulum of length $L$: $T = 4\\sqrt{\\frac{L}{g}}K\\left(\\sin\\frac{\\theta_0}{2}\\right)$. "
        "3. In computing, the historical binary prefix kilo- (symbol $\\text{K}$) representing $2^{10} = 1024\\,\\text{bytes}$, formally standardized by the IEC as the kibibyte ($\\text{KiB}$)."
    ),

    # 3. k-ar dating (index 2)
    2: (
        "In geochronology, an absolute radiometric dating method based on the branched radioactive decay of potassium-40 ($^{40}\\text{K}$) "
        "into the radiogenic stable noble gas argon-40 ($^{40}\\text{Ar}$) via electron capture and positron emission with total half-life $t_{1/2} \\approx 1.248 \\times 10^9\\,\\text{years}$. "
        "The age $t$ of a geological rock or mineral sample is calculated from the accumulation equation:\n\n"
        "$$t = \\frac{1}{\\lambda} \\ln\\left( 1 + \\frac{^{40}\\text{Ar}^*}{^{40}\\text{K}} \\left(\\frac{\\lambda}{\\lambda_e}\\right) \\right)$$\n\n"
        "where $\\lambda = 5.543 \\times 10^{-10}\\,\\text{yr}^{-1}$ is total decay constant, and $\\lambda_e = 0.581 \\times 10^{-10}\\,\\text{yr}^{-1}$ is the decay constant for decay to argon. "
        "Routinely dates volcanic rocks and hominid fossil strata spanning from $10^5$ to $4.5 \\times 10^9$ years old."
    ),

    # 4. kainic acid (index 5)
    5: (
        "A naturally occurring heterocyclic pyrrolidine dicarboxylic acid and potent neuroexcitatory amino acid analogue of L-glutamic acid, "
        "isolated from the red marine alga *Digenea simplex*. Molecular formula $\\text{C}_{10}\\text{H}_{15}\\text{NO}_4$, molar mass $213.23\\,\\text{g/mol}$, "
        "density $1.22\\,\\text{g/cm}^3$, and melting point $250\\text{--}252\\,^\\circ\\text{C}$ ($523\\text{--}525\\,\\text{K}$). "
        "Acts as a selective agonist at ionotropic kainate receptors in the central nervous system, widely used in neuropharmacology to induce experimental temporal lobe epilepsy and excitotoxic neuronal injury models."
    ),

    # 5. kainite (index 6)
    6: (
        "A naturally occurring hydrated evaporite sulfate-chloride mineral of magnesium and potassium with chemical formula:\n\n"
        "$$\\text{MgSO}_4 \\cdot \\text{KCl} \\cdot 3\\text{H}_2\\text{O} \\quad \\text{or} \\quad \\text{KMg(SO}_4\\text{)Cl} \\cdot 3\\text{H}_2\\text{O}$$\n\n"
        "Mohs hardness $2.5\\text{--}3.0$, density $2.13\\,\\text{g/cm}^3$. Crystallizes in the monoclinic crystal system. "
        "Forms naturally in marine salt and potash evaporite beds; serves as an important industrial source of potassium and magnesium fertilizers."
    ),

    # 6. kakutani fixed point theorem (index 9)
    9: (
        "A cornerstone theorem of mathematical economics and topology proved by Shizuo Kakutani in 1941, generalizing Brouwer's fixed-point theorem to set-valued correspondences. "
        "It states that if $S$ is a non-empty, compact, convex subset of Euclidean space $\\mathbb{R}^n$, and $\\Phi: S \\rightrightarrows S$ is a set-valued correspondence "
        "with a closed graph such that $\\Phi(x)$ is non-empty and convex for all $x \\in S$:\n\n"
        "$$\\exists x^* \\in S \\quad \\text{such that} \\quad x^* \\in \\Phi(x^*)$$\n\n"
        "Serves as the foundational mathematical tool in John Nash's 1950 proof of the existence of mixed-strategy Nash equilibria in non-cooperative finite games, "
        "and Arrow and Debreu's proof of competitive general economic equilibrium."
    ),

    # 7. kantorovitch inequality (index 15)
    15: (
        "In numerical analysis and optimization theory, an inequality established by Leonid Kantorovich (1948) providing an upper bound on Cauchy-Schwarz error for positive-definite operators. "
        "For any symmetric positive-definite real matrix $\\mathbf{P}$ with smallest eigenvalue $m > 0$ and largest eigenvalue $M \\ge m$, and any non-zero vector $\\mathbf{x} \\in \\mathbb{R}^n$:\n\n"
        "$$\\frac{(\\mathbf{x}^T \\mathbf{P} \\mathbf{x})(\\mathbf{x}^T \\mathbf{P}^{-1} \\mathbf{x})}{(\\mathbf{x}^T \\mathbf{x})^2} \\le \\frac{(m + M)^2}{4mM} = \\frac{(\\kappa + 1)^2}{4\\kappa}$$\n\n"
        "where $\\kappa = \\frac{M}{m}$ is the matrix spectral condition number. Governs the linear convergence rate of the method of steepest descent for quadratic optimization: "
        "$\\|\\mathbf{x}_{k+1} - \\mathbf{x}^*\\|_P \\le \\left(\\frac{\\kappa - 1}{\\kappa + 1}\\right)\\|\\mathbf{x}_k - \\mathbf{x}^*\\|_P$."
    ),

    # 8. kaolinite (index 17)
    17: (
        "A layered dioctahedral 1:1 aluminosilicate clay mineral with the idealized stoichiometric chemical formula:\n\n"
        "$$\\text{Al}_2\\text{Si}_2\\text{O}_5(\\text{OH})_4$$\n\n"
        "Density $2.6\\,\\text{g/cm}^3$, Mohs hardness $2.0\\text{--}2.5$. Its crystal structure consists of alternating sheets of tetrahedral silicon dioxide ($\\text{SiO}_4$) "
        "and octahedral aluminum hydroxide ($\\text{Al(OH)}_6$) linked by strong interlayer hydrogen bonds. Forms through the hydrothermal weathering of feldspar rocks ($2\\text{KAlSi}_3\\text{O}_8 + 2\\text{H}_2\\text{CO}_3 + 9\\text{H}_2\\text{O} \\to \\text{Al}_2\\text{Si}_2\\text{O}_5(\\text{OH})_4 + 4\\text{H}_4\\text{SiO}_4 + 2\\text{K}^+ + 2\\text{HCO}_3^-$). "
        "Primary constituent of kaolin (china clay), widely used in porcelain, ceramics, and coated paper."
    ),

    # 9. karush-kuhn-tucker theorem (index 23)
    23: (
        "In non-linear mathematical optimization, the Karush-Kuhn-Tucker (KKT) conditions provide first-order necessary conditions for a local optimum in a continuously differentiable "
        "constrained non-linear problem: $\\min_{\\mathbf{x}} f(\\mathbf{x})$ subject to inequality constraints $g_i(\\mathbf{x}) \\le 0$ ($i=1,\\dots,m$) and equality constraints $h_j(\\mathbf{x}) = 0$ ($j=1,\\dots,p$). "
        "Under a constraint qualification (such as Slater's condition or LICQ), there exist Lagrange multiplier vectors $\\boldsymbol{\\mu} \\ge \\mathbf{0}$ and $\\boldsymbol{\\lambda}$ such that:\n\n"
        "$$\\nabla f(\\mathbf{x}^*) + \\sum_{i=1}^m \\mu_i \\nabla g_i(\\mathbf{x}^*) + \\sum_{j=1}^p \\lambda_j \\nabla h_j(\\mathbf{x}^*) = \\mathbf{0}$$\n\n"
        "$$g_i(\\mathbf{x}^*) \\le 0, \\qquad h_j(\\mathbf{x}^*) = 0$$\n\n"
        "$$\\mu_i \\ge 0, \\qquad \\mu_i g_i(\\mathbf{x}^*) = 0 \\quad (\\text{complementary slackness})$$"
    ),

    # 10. kater's pendulum (index 33)
    33: (
        "A reversible compound pendulum invented by British physicist Henry Kater in 1817 for precision absolute determinations of the local acceleration due to gravity $g$. "
        "Constructed with two opposing parallel knife-edge pivot axes $K_1$ and $K_2$ and adjustable sliding counterweights. When the positions of the weights are adjusted such that the "
        "oscillation periods about both knife edges are identical ($T_1 = T_2 = T$), the separation distance $L$ between the knife edges precisely equals the length of an equivalent simple pendulum:\n\n"
        "$$T = 2\\pi \\sqrt{\\frac{L}{g}} \\implies g = \\frac{4\\pi^2 L}{T^2}$$\n\n"
        "This reversible design completely eliminates errors stemming from measuring the unknown moment of inertia or center of gravity of the pendulum rod."
    ),

    # 11. kekulé structure (index 40)
    40: (
        "A historical structural representation of the benzene ring proposed by Friedrich August Kekulé in 1865, depicting benzene as a planar hexagonal ring of six carbon atoms "
        "with alternating alternating single ($\\text{C}\\text{---}\\text{C}$) and double ($\\text{C}\\text{=}\\text{C}$) covalent bonds, with each carbon bearing one hydrogen atom:\n\n"
        "$$\\text{C}_6\\text{H}_6$$\n\n"
        "In modern resonance and valence-bond theory, Kekulé's two structures are canonical contributing resonance hybrids with equal weights, whose continuous quantum superposition "
        "delocalizes six cyclic $\\pi$-electrons across the ring, giving all $\\text{C}\\text{---}\\text{C}$ bonds an identical intermediate bond length of $1.397\\,\\text{\\AA}$ ($139.7\\,\\text{pm}$) "
        "and conferring aromatic resonance stabilization energy ($\\approx 150\\,\\text{kJ/mol}$)."
    ),

    # 12. kelvin (index 42)
    42: (
        "The SI base unit of thermodynamic temperature (symbol $\\text{K}$), named after Lord Kelvin. Since the 2019 SI redefinition, the kelvin is defined by taking the fixed numerical value "
        "of the Boltzmann constant $k_B$ to be exactly $1.380649 \\times 10^{-23}\\,\\text{J}\\cdot\\text{K}^{-1}$. Absolute zero is $0\\,\\text{K}$, at which thermodynamic entropy and molecular kinetic motion "
        "reach quantum ground states. Related to the Celsius scale by an additive offset of $273.15$:\n\n"
        "$$T(\\text{K}) = T(^\\circ\\text{C}) + 273.15, \\qquad \\Delta T(1\\,\\text{K}) = \\Delta T(1\\,^\\circ\\text{C})$$"
    ),

    # 13. kelvin scale (index 44)
    44: (
        "An absolute thermodynamic temperature scale that begins at absolute zero ($0\\,\\text{K} = -273.15\\,^\\circ\\text{C}$), eliminating negative temperature values for classical thermodynamic systems. "
        "Key reference transition benchmarks:\n\n"
        "* **Absolute Zero**: $0\\,\\text{K} = -273.15\\,^\\circ\\text{C}$\n"
        "* **Freezing point of water ($1\\,\\text{atm}$)**: $273.15\\,\\text{K} = 0.00\\,^\\circ\\text{C}$\n"
        "* **Triple point of pure water**: $273.16\\,\\text{K} = 0.01\\,^\\circ\\text{C}$\n"
        "* **Boiling point of water ($1\\,\\text{atm}$)**: $373.13\\,\\text{K} = 99.98\\,^\\circ\\text{C}$\n\n"
        "The ideal gas law $PV = nRT$ requires thermodynamic temperature strictly on the Kelvin scale."
    ),

    # 14. kelvin's circulation theorem (index 45)
    45: (
        "A fundamental theorem in theoretical fluid dynamics published by William Thomson (Lord Kelvin) in 1869. It states that for an inviscid, barotropic ideal fluid subjected to "
        "conservative body forces (such as gravity), the fluid circulation $\\Gamma$ around any closed material loop $C(t)$ moving with the fluid remains constant in time:\n\n"
        "$$\\frac{D\\Gamma}{Dt} = 0, \\quad \\text{where } \\Gamma = \\oint_{C(t)} \\mathbf{u} \\cdot d\\mathbf{r} = \\iint_{S(t)} (\\nabla \\times \\mathbf{u}) \\cdot d\\mathbf{A}$$\n\n"
        "A direct consequence is that if a fluid begins irrotational ($\\boldsymbol{\\omega} = \\nabla \\times \\mathbf{u} = \\mathbf{0}$), it remains irrotational along fluid streamlines, "
        "precluding the creation or destruction of vortex lines within the fluid interior."
    ),

    # 15. kendell method (index 48)
    48: (
        "In non-parametric statistics, Kendall's rank correlation coefficient $\\tau$ (devised by Maurice Kendall in 1938), measuring the ordinal association between two ranked variables $X$ and $Y$ "
        "across $n$ paired observations $(x_1, y_1), \\dots, (x_n, y_n)$. Defined as the difference between the number of concordant pairs $C$ and discordant pairs $D$, normalized by total pairs $\\binom{n}{2}$:\n\n"
        "$$\\tau = \\frac{C - D}{\\frac{1}{2}n(n - 1)} = \\frac{2(C - D)}{n(n - 1)}$$\n\n"
        "The coefficient takes values in $[-1, +1]$: $\\tau = +1$ indicates identical rank order, $\\tau = -1$ indicates perfect inverse rank agreement, and $\\tau = 0$ indicates independence."
    ),

    # 16. kepler's laws of planetary motion (index 50)
    50: (
        "Three astronomical laws formulated by Johannes Kepler (1609, 1619) describing heliocentric orbital mechanics:\n\n"
        "1. **Law of Ellipses**: The orbit of each planet is an ellipse with the Sun located at one of the two foci:\n"
        "$$\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1, \\quad r(\\theta) = \\frac{a(1 - e^2)}{1 + e\\cos\\theta}$$\n\n"
        "2. **Law of Equal Areas**: The line segment (radius vector $\\mathbf{r}$) joining a planet to the Sun sweeps out equal orbital areas $\\Delta A$ in equal intervals of time $\\Delta t$, representing conservation of orbital angular momentum $\\mathbf{L}$:\n"
        "$$\\frac{dA}{dt} = \\frac{1}{2} r^2 \\frac{d\\theta}{dt} = \\frac{L}{2m} = \\text{constant}$$\n\n"
        "3. **Law of Harmonies**: The square of the orbital period $T$ of a planet is directly proportional to the cube of the semi-major axis $a$ of its orbit:\n"
        "$$T^2 = \\left( \\frac{4\\pi^2}{G(M_\\odot + m)} \\right) a^3 \\implies \\frac{T^2}{a^3} = \\text{constant}$$"
    ),

    # 17. ketenes (index 63)
    63: (
        "A class of highly reactive unsaturated organic compounds containing the cumulated carbonyl-alkene functional group $\\text{R}_1\\text{R}_2\\text{C}=\\text{C}=\\text{O}$. "
        "The simplest member is ethenone (ketene itself), with molecular formula $\\text{CH}_2=\\text{C}=\\text{O}$, boiling point $-56\\,^\\circ\\text{C}$ ($217\\,\\text{K}$), "
        "prepared industrially by the gas-phase thermal pyrolysis of acetone at $700\\,^\\circ\\text{C}$:\n\n"
        "$$\\text{CH}_3\\text{COCH}_3 \\xrightarrow{\\Delta} \\text{CH}_2\\text{=C=O} + \\text{CH}_4$$\n\n"
        "The central carbon is sp-hybridized and electrophilic, readily undergoing $[2+2]$ cycloaddition with alkenes and nucleophilic addition with water to produce ethanoic acid: "
        "$\\text{CH}_2\\text{=C=O} + \\text{H}_2\\text{O} \\to \\text{CH}_3\\text{COOH}$."
    ),

    # 18. keto-enol tautomerism (index 65)
    65: (
        "A chemical equilibrium between a carbonyl compound containing an $\\alpha$-hydrogen (the keto form, $-\\text{CH}_2-\\text{C}(=\\text{O})-$) "
        "and its constitutional isomer possessing an enolic alkene-alcohol structure (the enol form, $-\\text{CH}=\\text{C}(\\text{OH})-$):\n\n"
        "$$\\text{R}-\\text{CH}_2-\\text{C}(=\\text{O})-\\text{R}' \\rightleftharpoons \\text{R}-\\text{CH}=\\text{C}(\\text{OH})-\\text{R}'$$\n\n"
        "The tautomerization is catalyzed by both acids (via resonance-stabilized oxocarbenium intermediates) and bases (via delocalized enolate anions). "
        "For simple aldehydes and ketones (e.g. acetone), the keto tautomer is thermodynamically favored ($> 99.99\\%$), whereas in $\\beta$-dicarbonyls (such as ethyl acetoacetate or acetylacetone), "
        "the enol form is strongly stabilized ($> 80\\%$) by internal intramolecular hydrogen bonding and conjugated resonance."
    ),

    # 19. ketone (index 70)
    70: (
        "An organic compound containing a carbonyl group ($\\text{C=O}$) bonded covalently to two distinct carbon alkyl or aryl substituent radicals: $\\text{R}^1\\text{COR}^2$. "
        "General molecular formula: $\\text{C}_n\\text{H}_{2n}\\text{O}$ (for aliphatic ketones). Produced by the oxidation of secondary alcohols using acidified potassium dichromate:\n\n"
        "$$\\text{R}^1\\text{CH}(\\text{OH})\\text{R}^2 + [\\text{O}] \\xrightarrow{\\text{Cr}_2\\text{O}_7^{2-}/\\text{H}^+} \\text{R}^1\\text{C}(=\\text{O})\\text{R}^2 + \\text{H}_2\\text{O}$$\n\n"
        "The carbonyl carbon is $sp^2$-hybridized with trigonal planar geometry ($120^\\circ$ bond angles). The simplest aliphatic ketone is propanone (acetone, $\\text{CH}_3\\text{COCH}_3$, boiling point $56\\,^\\circ\\text{C}$)."
    ),

    # 20. kilowatt-hour (index 122)
    122: (
        "A non-SI composite metric unit of energy commonly used as a commercial billing unit by electrical utility providers (Board of Trade Unit). "
        "Symbol $\\text{kWh}$, representing the energy delivered by a constant power output of one kilowatt ($1000\\,\\text{W}$) over a duration of one hour ($3600\\,\\text{s}$):\n\n"
        "$$1\\,\\text{kWh} = 1000\\,\\text{W} \\times 3600\\,\\text{s} = 3.6 \\times 10^6\\,\\text{J} = 3.6\\,\\text{MJ}$$\n\n"
        "Total electrical energy consumed $E$ in $\\text{kWh}$ from power rating $P$ (in watts) and operating time $t$ (in hours) is $E = \\frac{P \\times t}{1000}$."
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

print(f"\nSuccessfully enriched {count} terms in Section K Batch 1.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
