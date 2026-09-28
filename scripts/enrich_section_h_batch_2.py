"""
enrich_section_h_batch_2.py
===========================
Section H Formula Enrichment - Batch 2 (Candidates 16 to 29)
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

h_entries = data.get('H', [])

UPDATES = {
    # 16. hamiltonian function (index 147)
    147: (
        "In analytical mechanics and mathematical physics, a function $H(q, p, t)$ that expresses the total energy of a dynamical "
        "system in terms of generalized coordinates $q_i$ and their conjugate generalized momenta $p_i$. It is defined via Legendre "
        "transformation of the Lagrangian $L(q, \\dot{q}, t)$:\n\n"
        "$$H(q, p, t) = \\sum_{i=1}^n p_i \\dot{q}_i - L(q, \\dot{q}, t), \\quad \\text{where } p_i = \\frac{\\partial L}{\\partial \\dot{q}_i}$$\n\n"
        "For natural scleronomic systems with conservative forces where potentials are velocity-independent, the Hamiltonian represents "
        "the sum of kinetic energy $T$ and potential energy $V$: $H = T + V$. In quantum mechanics, promoting $q$ and $p$ to Hermitian "
        "operators yields the Hamiltonian operator $\\hat{H}$, governing time evolution via the Schrödinger equation $i\\hbar \\frac{\\partial}{\\partial t}|\\psi\\rangle = \\hat{H}|\\psi\\rangle$."
    ),

    # 17. hammett constant (index 152)
    152: (
        "In physical organic chemistry, an empirical parameter $\\sigma$ introduced by Louis Plack Hammett in 1937 that quantifies the "
        "electronic electron-donating or electron-withdrawing effect of a meta- or para-substituent on a benzene ring relative to hydrogen. "
        "It is defined from the ionization equilibrium constants of substituted benzoic acids ($K$) versus unsubstituted benzoic acid ($K_0$) "
        "in water at $25\\,^\\circ\\text{C}$:\n\n"
        "$$\\sigma = \\log_{10}\\left(\\frac{K}{K_0}\\right) = \\text{p}K_{a0} - \\text{p}K_a$$\n\n"
        "Electron-withdrawing groups (e.g., $-\\text{NO}_2$, $-\\text{CN}$) stabilize the conjugate benzoate anion, yielding $\\sigma > 0$. "
        "Electron-donating groups (e.g., $-\\text{OCH}_3$, $-\\text{NH}_2$) destabilize the anion, giving $\\sigma < 0$. Under the Hammett equation "
        "$\\log_{10}(k/k_0) = \\rho \\sigma$, reaction constant $\\rho$ measures susceptibility to polar substituent effects."
    ),

    # 18. hardy-weinberg theorem (index 206)
    206: (
        "A foundational principle of population genetics formulated independently by G. H. Hardy and Wilhelm Weinberg in 1908. It states "
        "that both allele and genotype frequencies in a sexually reproducing population remain constant from generation to generation in the "
        "absence of evolutionary influences (natural selection, mutation, migration, genetic drift, and non-random mating). For a biallelic locus "
        "with alleles $A$ and $a$ having frequencies $p$ and $q$ ($p + q = 1$), the expected diploid genotype frequencies at equilibrium satisfy:\n\n"
        "$$p^2 + 2pq + q^2 = 1$$\n\n"
        "where $p^2 = f(AA)$ is the homozygous dominant frequency, $2pq = f(Aa)$ is the heterozygous frequency, and $q^2 = f(aa)$ is the "
        "homozygous recessive frequency."
    ),

    # 19. harmonic (index 212)
    212: (
        "1. In acoustics and wave physics, a sinusoidal component of a periodic complex wave having a frequency that is an exact integer "
        "multiple of the fundamental frequency $f_0$. The fundamental frequency is the 1st harmonic ($f_1 = f_0$). The 2nd harmonic ($f_2 = 2f_0$) "
        "corresponds to the 1st overtone; the $n$-th harmonic has frequency $f_n = n f_0$. For a standing wave on a string or open pipe of length $L$ "
        "with wave speed $v$:\n\n"
        "$$f_n = n \\frac{v}{2L} \\quad (n = 1, 2, 3, \\dots)$$\n\n"
        "For a pipe closed at one end, only odd harmonics are generated: $f_n = (2n - 1)\\frac{v}{4L}$. "
        "2. In mathematics, of or relating to numbers whose reciprocals form an arithmetic progression, or functions satisfying Laplace's equation."
    ),

    # 20. harmonic function (index 216)
    216: (
        "In mathematical analysis, a twice continuously differentiable real-valued function $u: U \\to \\mathbb{R}$ defined on an open "
        "subset $U \\subseteq \\mathbb{R}^n$ that satisfies Laplace's equation everywhere on $U$:\n\n"
        "$$\\nabla^2 u = \\Delta u = \\sum_{i=1}^n \\frac{\\partial^2 u}{\\partial x_i^2} = 0$$\n\n"
        "In two dimensions ($n=2$): $\\frac{\\partial^2 u}{\\partial x^2} + \\frac{\\partial^2 u}{\\partial y^2} = 0$. By the Cauchy-Riemann equations, "
        "the real and imaginary parts of any complex analytic function $f(z) = u(x, y) + iv(x, y)$ are harmonic conjugate functions. "
        "Harmonic functions satisfy the mean-value property and the maximum principle, and model steady-state heat conduction, electrostatics, and potential fluid flow."
    ),

    # 21. harmonic points (index 221)
    221: (
        "A set of four collinear points $P, Q, R, S$ on a line whose cross-ratio $(P, Q; R, S)$ equals $-1$:\n\n"
        "$$(P, Q; R, S) = \\frac{PR}{QR} \\bigg/ \\frac{PS}{QS} = -1$$\n\n"
        "This condition occurs when points $R$ and $S$ divide the directed line segment $PQ$ internally and externally in the same numerical ratio: "
        "$\\frac{PR}{RQ} = -\\frac{PS}{SQ}$. In projective geometry, harmonic points form a harmonic tetrad (or harmonic quadruple), preserved under all projective transformations."
    ),

    # 22. harmonic ratio (index 222)
    222: (
        "A cross-ratio of four collinear points whose value equals $-1$. If points $P, Q, R, S$ lie on a line such that $(P, S; Q, R) = -1$, "
        "their directed distances satisfy the relation:\n\n"
        "$$\\frac{1}{PQ} + \\frac{1}{PS} = \\frac{2}{PR}$$\n\n"
        "establishing that the lengths $PQ$, $PR$, and $PS$ form a harmonic progression. If $R$ is the midpoint of segment $QS$, the conjugate harmonic point $P$ lies at infinity."
    ),

    # 23. harmonic sequence (index 223)
    223: (
        "A mathematical progression of numbers formed by taking the reciprocals of an arithmetic progression. It has the general form:\n\n"
        "$$\\frac{1}{a}, \\; \\frac{1}{a + d}, \\; \\frac{1}{a + 2d}, \\; \\dots, \\; \\frac{1}{a + (n-1)d}$$\n\n"
        "where $a \\neq 0$ and $d$ is the common difference. The harmonic mean $H$ of two positive numbers $a$ and $b$ is given by:\n\n"
        "$$H = \\frac{2}{\\frac{1}{a} + \\frac{1}{b}} = \\frac{2ab}{a + b}$$\n\n"
        "satisfying the inequality $H \\le G \\le A$ (harmonic mean $\\le$ geometric mean $\\le$ arithmetic mean)."
    ),

    # 24. harmonic series (index 224)
    224: (
        "The infinite series formed by the sum of the reciprocals of the positive integers:\n\n"
        "$$\\sum_{n=1}^\\infty \\frac{1}{n} = 1 + \\frac{1}{2} + \\frac{1}{3} + \\frac{1}{4} + \\dots + \\frac{1}{n} + \\dots$$\n\n"
        "Although its $n$-th term approaches zero ($\\lim_{n\\to\\infty} \\frac{1}{n} = 0$), the series diverges slowly to infinity. "
        "Its $n$-th partial sum $H_n = \\sum_{k=1}^n \\frac{1}{k}$ grows asymptotically as $H_n = \\ln n + \\gamma + \\mathcal{O}\\left(\\frac{1}{n}\\right)$, "
        "where $\\gamma \\approx 0.5772156649$ is the Euler-Mascheroni constant."
    ),

    # 25. hartree (index 227)
    227: (
        "The atomic unit of energy (symbol $E_{\\text{h}}$), named after Douglas Hartree. Defined as $\\frac{\\hbar^2}{m_e a_0^2}$ where $\\hbar$ "
        "is the reduced Planck constant, $m_e$ is electron rest mass, and $a_0$ is the Bohr radius:\n\n"
        "$$E_{\\text{h}} = \\frac{e^2}{4\\pi \\varepsilon_0 a_0} = \\alpha^2 m_e c^2 \\approx 4.359744722 \\times 10^{-18}\\,\\text{J} \\approx 27.211386\\,\\text{eV}$$\n\n"
        "By the virial theorem, $1\\,E_{\\text{h}}$ equals twice the ground-state ionization energy of the hydrogen atom (neglecting nuclear mass and relativistic corrections): "
        "$1\\,E_{\\text{h}} = 2\\,\\text{Ry}$ ($2$ rydbergs)."
    ),

    # 26. hausdorff dimension (index 240)
    240: (
        "In fractal geometry and geometric measure theory, a non-negative real number $d_H$ assigned to a metric space $X$ that extends the "
        "notion of integer topological dimension. For a subset $S$ covered by balls of diameter $r_i \\le \\delta$, the $d$-dimensional Hausdorff measure "
        "is $\\mathcal{H}^d(S) = \\lim_{\\delta \\to 0} \\inf \\sum r_i^d$. The Hausdorff dimension is the critical threshold where measure transitions:\n\n"
        "$$d_H(S) = \\inf\\{d \\ge 0 : \\mathcal{H}^d(S) = 0\\} = \\sup\\{d \\ge 0 : \\mathcal{H}^d(S) = \\infty\\}$$\n\n"
        "For standard Euclidean objects, $d_H$ is an integer (point: $0$, line: $1$, disk: $2$, sphere: $3$), while for fractals it is typically non-integer "
        "(e.g., Cantor set: $d_H = \\frac{\\ln 2}{\\ln 3} \\approx 0.6309$; Koch snowflake curve: $d_H = \\frac{\\ln 4}{\\ln 3} \\approx 1.2619$)."
    ),

    # 27. haversine (index 246)
    246: (
        "A historical trigonometric function equal to half the versine, denoted $\\text{hav}(\\theta)$:\n\n"
        "$$\\text{hav}(\\theta) = \\frac{\\text{vers}(\\theta)}{2} = \\frac{1 - \\cos \\theta}{2} = \\sin^2\\left(\\frac{\\theta}{2}\\right)$$\n\n"
        "The haversine formula calculates the great-circle distance $d$ between two points on a sphere of radius $R$ given geographic latitudes "
        "$(\\phi_1, \\phi_2)$ and longitudes $(\\lambda_1, \\lambda_2)$:\n\n"
        "$$\\text{hav}\\left(\\frac{d}{R}\\right) = \\text{hav}(\\Delta \\phi) + \\cos \\phi_1 \\cos \\phi_2 \\, \\text{hav}(\\Delta \\lambda)$$\n\n"
        "Widely employed in celestial navigation and geodesy because it avoids catastrophic numerical cancellation when calculating distances between closely spaced points."
    ),

    # 28. hazard rate function (index 256)
    256: (
        "In survival analysis and reliability engineering, the instantaneous failure rate $h(t)$ of an entity at time $t$, conditional on survival up to time $t$. "
        "Expressed mathematically in terms of the probability density function $f(t)$, cumulative distribution function $F(t)$, and survival function $S(t) = 1 - F(t)$:\n\n"
        "$$h(t) = \\lim_{\\Delta t \\to 0} \\frac{P(t \\le T < t + \\Delta t \\mid T \\ge t)}{\\Delta t} = \\frac{f(t)}{S(t)} = -\\frac{d}{dt}\\ln S(t)$$\n\n"
        "The cumulative hazard function is $H(t) = \\int_0^t h(u)\\,du = -\\ln S(t)$, from which survival probability is $S(t) = e^{-H(t)}$."
    ),

    # 29. heat capacity (index 285)
    285: (
        "In thermodynamics, the extensive physical quantity $C$ representing the ratio of heat energy $\\delta Q$ transferred to a closed system "
        "to the resulting change in temperature $dT$:\n\n"
        "$$C = \\frac{\\delta Q}{dT}, \\quad \\text{SI unit: } \\text{J}\\cdot\\text{K}^{-1}$$\n\n"
        "At constant volume, the heat capacity is $C_V = \\left(\\frac{\\partial U}{\\partial T}\\right)_V$; at constant pressure, $C_p = \\left(\\frac{\\partial H}{\\partial T}\\right)_p$. "
        "For an ideal gas, Mayer's relation states $C_p - C_V = nR$. The specific heat capacity $c = \\frac{C}{m}$ relates total heat transfer to mass and temperature change: $Q = mc\\Delta T$."
    ),

    # 30. heat equation (index 287)
    287: (
        "A parabolic second-order partial differential equation describing the diffusion of thermal energy in a medium over time. For a medium with "
        "thermal conductivity $k$, density $\\rho$, and specific heat capacity $c_p$, temperature distribution $u(\\mathbf{x}, t)$ satisfies:\n\n"
        "$$\\frac{\\partial u}{\\partial t} = \\alpha \\nabla^2 u$$\n\n"
        "where $\\alpha = \\frac{k}{\\rho c_p}$ is the thermal diffusivity (in $\\text{m}^2/\\text{s}$) and $\\nabla^2 = \\sum_{i=1}^n \\frac{\\partial^2}{\\partial x_i^2}$ "
        "is the spatial Laplacian operator. In one dimension: $\\frac{\\partial u}{\\partial t} = \\alpha \\frac{\\partial^2 u}{\\partial x^2}$. "
        "Fundamental solutions (heat kernel) take Gaussian form: $\\Phi(x, t) = \\frac{1}{\\sqrt{4\\pi \\alpha t}} e^{-\\frac{x^2}{4\\alpha t}}$ for $t > 0$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(h_entries):
        w = h_entries[idx]['word']
        h_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (H has {len(h_entries)} entries)")

data['H'] = h_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section H Batch 2.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
