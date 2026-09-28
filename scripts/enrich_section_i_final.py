"""
enrich_section_i_final.py
=========================
Section I Formula Enrichment - Final Batch (Candidates 31 to 48)
Completing Section I formulas into KaTeX ($ ... $ and $$ ... $$).
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

i_entries = data.get('I', [])

UPDATES = {
    # 31. integrated rate law (index 533)
    533: (
        "In chemical kinetics, mathematical expressions relating reactant or product concentrations directly to elapsed time $t$ by integrating differential rate laws:\n\n"
        "* **Zero-order** ($-\\frac{d[A]}{dt} = k$):\n"
        "$$[A]_t = [A]_0 - kt, \\qquad t_{1/2} = \\frac{[A]_0}{2k}$$\n\n"
        "* **First-order** ($-\\frac{d[A]}{dt} = k[A]$):\n"
        "$$\\ln[A]_t = \\ln[A]_0 - kt \\implies [A]_t = [A]_0 e^{-kt}, \\qquad t_{1/2} = \\frac{\\ln 2}{k} \\approx \\frac{0.693}{k}$$\n\n"
        "* **Second-order** ($-\\frac{d[A]}{dt} = k[A]^2$):\n"
        "$$\\frac{1}{[A]_t} = \\frac{1}{[A]_0} + kt, \\qquad t_{1/2} = \\frac{1}{k[A]_0}$$\n\n"
        "Linear plots of $[A]$ vs $t$, $\\ln[A]$ vs $t$, and $1/[A]$ vs $t$ uniquely diagnose reaction order."
    ),

    # 32. integrating factor (index 535)
    535: (
        "In ordinary differential equations, a non-zero function $\\mu(x)$ by which a first-order linear differential equation "
        "$y' + P(x)y = Q(x)$ is multiplied to transform its left-hand side into the exact derivative of a product $\\frac{d}{dx}[\\mu(x)y]$:\n\n"
        "$$\\mu(x) = e^{\\int P(x)\\,dx}$$\n\n"
        "Multiplying through gives $\\frac{d}{dx}[\\mu(x)y] = \\mu(x)Q(x)$, yielding the explicit general solution:\n\n"
        "$$y(x) = \\frac{1}{\\mu(x)} \\left( \\int \\mu(x) Q(x)\\,dx + C \\right)$$"
    ),

    # 33. integration by parts (index 538)
    538: (
        "A foundational integration technique derived from the product rule of differential calculus $\\frac{d}{dx}(uv) = u\\frac{dv}{dx} + v\\frac{du}{dx}$:\n\n"
        "$$\\int u\\,dv = uv - \\int v\\,du$$\n\n"
        "For definite integrals: $\\int_a^b u\\,dv = [uv]_a^b - \\int_a^b v\\,du$. For example, integrating $\\ln x$ with $u = \\ln x$ and $dv = dx$ ($du = \\frac{1}{x}dx, v = x$):\n\n"
        "$$\\int \\ln x\\,dx = x\\ln x - \\int x\\left(\\frac{1}{x}\\right)dx = x\\ln x - x + C$$\n\n"
        "The LIATE mnemonic (Logarithmic, Inverse trigonometric, Algebraic, Trigonometric, Exponential) assists in selecting $u$."
    ),

    # 34. integration by substitution (index 539)
    539: (
        "Also known as $u$-substitution, an integration technique that reverses the chain rule of differentiation. If $u = g(x)$ is a differentiable "
        "function whose range is an interval where $f$ is continuous:\n\n"
        "$$\\int f(g(x)) g'(x)\\,dx = \\int f(u)\\,du$$\n\n"
        "For example, evaluating $\\int \\cos(ax + b)\\,dx$: setting $u = ax + b \\implies du = a\\,dx$ yields $\\frac{1}{a}\\int \\cos u\\,du = \\frac{1}{a}\\sin(ax + b) + C$."
    ),

    # 35. integration by trigonometric substitution (index 540)
    540: (
        "An integration method used to eliminate algebraic radicals by substituting trigonometric functions using Pythagorean identities:\n\n"
        "* For $\\sqrt{a^2 - x^2}$: substitute $x = a\\sin\\theta \\implies dx = a\\cos\\theta\\,d\\theta$, using $1 - \\sin^2\\theta = \\cos^2\\theta$\n"
        "* For $\\sqrt{a^2 + x^2}$: substitute $x = a\\tan\\theta \\implies dx = a\\sec^2\\theta\\,d\\theta$, using $1 + \\tan^2\\theta = \\sec^2\\theta$\n"
        "* For $\\sqrt{x^2 - a^2}$: substitute $x = a\\sec\\theta \\implies dx = a\\sec\\theta\\tan\\theta\\,d\\theta$, using $\\sec^2\\theta - 1 = \\tan^2\\theta$\n\n"
        "For example, $\\int \\frac{dx}{\\sqrt{a^2 - x^2}} = \\int \\frac{a\\cos\\theta\\,d\\theta}{a\\cos\\theta} = \\theta + C = \\arcsin\\left(\\frac{x}{a}\\right) + C$."
    ),

    # 36. interior angle (index 595)
    595: (
        "An angle formed inside a closed polygon between two adjacent sides. For any simple polygon with $n$ sides ($n \\ge 3$), the sum of all $n$ interior angles is:\n\n"
        "$$S = (n - 2) \\times 180^\\circ = (n - 2)\\pi\\,\\text{rad}$$\n\n"
        "In a regular polygon with $n$ equal sides, each interior angle measures:\n\n"
        "$$\\theta = \\frac{(n - 2) \\times 180^\\circ}{n} = \\frac{(n - 2)\\pi}{n}\\,\\text{rad}$$\n\n"
        "Each interior angle is supplementary to the corresponding exterior angle: $\\theta_{\\text{int}} + \\theta_{\\text{ext}} = 180^\\circ$."
    ),

    # 37. intermediate value theorem (index 608)
    608: (
        "A fundamental theorem of real analysis proved by Bernhard Bolzano in 1817. It states that if a real-valued function $f: [a, b] \\to \\mathbb{R}$ "
        "is continuous on the closed interval $[a, b]$, and $u$ is any real number strictly between $f(a)$ and $f(b)$:\n\n"
        "$$\\exists c \\in (a, b) \\quad \\text{such that} \\quad f(c) = u$$\n\n"
        "A critical corollary is Bolzano's theorem on roots: if $f(a)$ and $f(b)$ have opposite signs ($f(a)f(b) < 0$), there exists at least one root $c \\in (a, b)$ "
        "where $f(c) = 0$, forming the mathematical foundation for numerical bisection root-finding algorithms."
    ),

    # 38. internal resistance (index 630)
    630: (
        "In electrical engineering and circuit theory, the inherent resistance $r_{\\text{int}}$ present within a practical source of electrical energy (such as a battery, chemical cell, or generator). "
        "When supplying a current $I$ to an external load resistance $R_L$, internal voltage drop $Ir_{\\text{int}}$ reduces the terminal potential difference $V_L$ below the open-circuit electromotive force (emf) $\\mathcal{E}$:\n\n"
        "$$V_L = \\mathcal{E} - I r_{\\text{int}}, \\qquad I = \\frac{\\mathcal{E}}{R_L + r_{\\text{int}}}$$\n\n"
        "The internal resistance is determined from terminal voltage and load current by $r_{\\text{int}} = \\frac{\\mathcal{E} - V_L}{I} = R_L\\left(\\frac{\\mathcal{E}}{V_L} - 1\\)$. "
        "By the maximum power transfer theorem, maximum power is delivered to the load when $R_L = r_{\\text{int}}$."
    ),

    # 39. interval of convergence (index 701)
    701: (
        "In real analysis, the set of all real values of $x$ for which a given formal power series $\\sum_{n=0}^\\infty c_n (x - a)^n$ converges to a finite sum. "
        "By Cauchy-Hadamard theorem, there exists a radius of convergence $R \\in [0, \\infty]$ given by:\n\n"
        "$$\\frac{1}{R} = \\limsup_{n \\to \\infty} \\sqrt[n]{|c_n|} = \\lim_{n \\to \\infty} \\left| \\frac{c_{n+1}}{c_n} \\right|$$\n\n"
        "The series converges absolutely for $|x - a| < R$ and diverges for $|x - a| > R$. The interval of convergence is an interval centered at $a$ "
        "with endpoints $a - R$ and $a + R$, which may be open $(a-R, a+R)$, closed $[a-R, a+R]$, or half-open, depending on endpoint convergence."
    ),

    # 40. inverse function theorem (index 761)
    761: (
        "In multivariable differential calculus, a foundational theorem stating that if $\\mathbf{f}: U \\subseteq \\mathbb{R}^n \\to \\mathbb{R}^n$ is a continuously "
        "differentiable ($C^1$) mapping and its Jacobian matrix $\\mathbf{J}_{\\mathbf{f}}(\\mathbf{a})$ is invertible (non-zero Jacobian determinant) at $\\mathbf{a} \\in U$:\n\n"
        "$$\\det(\\mathbf{J}_{\\mathbf{f}}(\\mathbf{a})) \\neq 0$$\n\n"
        "then $\\mathbf{f}$ is a local diffeomorphism: there exists an open neighborhood $V$ of $\\mathbf{a}$ such that $\\mathbf{f}|_V$ is invertible, its inverse "
        "$\\mathbf{f}^{-1}$ is $C^1$, and the derivative of the inverse satisfies:\n\n"
        "$$\\mathbf{J}_{\\mathbf{f}^{-1}}(\\mathbf{f}(\\mathbf{a})) = [\\mathbf{J}_{\\mathbf{f}}(\\mathbf{a})]^{-1}$$"
    ),

    # 41. inverse matrix (index 764)
    764: (
        "For an $n \\times n$ square matrix $\\mathbf{A}$, the unique matrix $\\mathbf{A}^{-1}$ that yields the identity matrix $\\mathbf{I}_n$ under matrix multiplication:\n\n"
        "$$\\mathbf{A}\\mathbf{A}^{-1} = \\mathbf{A}^{-1}\\mathbf{A} = \\mathbf{I}_n$$\n\n"
        "$\\mathbf{A}^{-1}$ exists if and only if $\\mathbf{A}$ is non-singular ($\\det(\\mathbf{A}) \\neq 0$). For a $2 \\times 2$ matrix:\n\n"
        "$$\\mathbf{A} = \\begin{bmatrix} a & b \\\\[4pt] c & d \\end{bmatrix} \\implies \\mathbf{A}^{-1} = \\frac{1}{ad - bc} \\begin{bmatrix} d & -b \\\\[4pt] -c & a \\end{bmatrix}$$\n\n"
        "In general, $\\mathbf{A}^{-1} = \\frac{1}{\\det(\\mathbf{A})} \\text{adj}(\\mathbf{A})$, where $\\text{adj}(\\mathbf{A})$ is the adjugate matrix (transpose of the cofactor matrix)."
    ),

    # 42. inverse square law (index 770)
    770: (
        "A physical law stating that a specified physical intensity or field quantity $I$ is inversely proportional to the square of the distance $r$ from the point source:\n\n"
        "$$I \\propto \\frac{1}{r^2} \\implies I = \\frac{P}{4\\pi r^2}$$\n\n"
        "Fundamental manifestations include:\n"
        "* **Newton's law of universal gravitation**: $F_g = G\\frac{m_1 m_2}{r^2}$\n"
        "* **Coulomb's law of electrostatics**: $F_e = \\frac{1}{4\\pi \\varepsilon_0}\\frac{|q_1 q_2|}{r^2}$\n"
        "* **Radiant flux / Sound intensity**: $I = \\frac{P_{\\text{source}}}{4\\pi r^2}$\n\n"
        "Arises geometrically because the surface area of a sphere scales as $A = 4\\pi r^2$ in 3-dimensional Euclidean space."
    ),

    # 43. ionic equation (index 832)
    832: (
        "A chemical equation in which electrolytes in aqueous solution are represented as dissociated ions. For example, the neutralization of sodium hydroxide by hydrochloric acid:\n\n"
        "$$\\text{Molecular: } \\text{NaOH}_{(aq)} + \\text{HCl}_{(aq)} \\longrightarrow \\text{NaCl}_{(aq)} + \\text{H}_2\\text{O}_{(l)}$$\n\n"
        "$$\\text{Complete ionic: } \\text{Na}^+_{(aq)} + \\text{OH}^-_{(aq)} + \\text{H}^+_{(aq)} + \\text{Cl}^-_{(aq)} \\longrightarrow \\text{Na}^+_{(aq)} + \\text{Cl}^-_{(aq)} + \\text{H}_2\\text{O}_{(l)}$$\n\n"
        "Canceling spectator ions ($\\text{Na}^+, \\text{Cl}^-$) yields the net ionic equation:\n\n"
        "$$\\text{H}^+_{(aq)} + \\text{OH}^-_{(aq)} \\longrightarrow \\text{H}_2\\text{O}_{(l)}$$"
    ),

    # 44. ionic product of water (index 837)
    837: (
        "The thermodynamic autoionization equilibrium constant of pure liquid water, denoted $K_w$, representing the self-ionization reaction $2\\text{H}_2\\text{O}_{(l)} \\rightleftharpoons \\text{H}_3\\text{O}^+_{(aq)} + \\text{OH}^-_{(aq)}$:\n\n"
        "$$K_w = [\\text{H}^+][\\text{OH}^-] = [\\text{H}_3\\text{O}^+][\\text{OH}^-]$$\n\n"
        "At $25\\,^\\circ\\text{C}$ ($298.15\\,\\text{K}$), $K_w = 1.008 \\times 10^{-14}\\,\\text{mol}^2\\cdot\\text{dm}^{-6}$, giving:\n\n"
        "$$\\text{p}K_w = -\\log_{10} K_w = \\text{pH} + \\text{pOH} = 14.00$$\n\n"
        "Because autoionization is endothermic ($\\Delta H^\\circ > 0$), $K_w$ increases with temperature, reaching $5.47 \\times 10^{-14}$ at $50\\,^\\circ\\text{C}$ (neutral $\\text{pH} \\approx 6.63$)."
    ),

    # 45. ionic strength (index 839)
    839: (
        "A measure of the total electrical concentration of ions in an electrolyte solution, introduced by Gilbert N. Lewis and Merle Randall in 1921. Denoted $I$, it is defined as:\n\n"
        "$$I = \\frac{1}{2} \\sum_{i=1}^n c_i z_i^2 = \\frac{1}{2} \\sum_{i=1}^n m_i z_i^2$$\n\n"
        "where $c_i$ (or $m_i$) is the molar (or molal) concentration of ion species $i$, and $z_i$ is its integer ionic valence charge number. "
        "Governs mean activity coefficients via the Debye-Hückel limiting law: $\\log_{10} \\gamma_\\pm = -A |z_+ z_-| \\sqrt{I}$."
    ),

    # 46. isobaric process (index 921)
    921: (
        "In thermodynamics, a reversible or irreversible thermodynamic process in which the pressure of a system remains strictly constant ($\\Delta P = 0$ or $P = \\text{const}$):\n\n"
        "$$W = \\int_{V_1}^{V_2} P\\,dV = P(V_2 - V_1) = P\\Delta V$$\n\n"
        "By the First Law of Thermodynamics, heat transferred $Q_p$ equals the change in enthalpy $H$:\n\n"
        "$$Q_p = \\Delta U + W = \\Delta H = n C_{p,m} \\Delta T$$\n\n"
        "For an ideal gas undergoing isobaric expansion, Charles's law applies: $\\frac{V_1}{T_1} = \\frac{V_2}{T_2}$."
    ),

    # 47. isochoric process (index 924)
    924: (
        "In thermodynamics, a process carried out at constant volume ($\\Delta V = 0$ or $V = \\text{const}$), also termed an isovolumetric process. "
        "Because boundary displacement is zero, the mechanical boundary work done by the system is identically zero:\n\n"
        "$$W = \\int P\\,dV = 0$$\n\n"
        "By the First Law of Thermodynamics, all heat added to the system converts directly into internal energy $U$:\n\n"
        "$$Q_V = \\Delta U = n C_{V,m} \\Delta T$$\n\n"
        "For an ideal gas, pressure varies directly with temperature according to Gay-Lussac's law: $\\frac{P_1}{T_1} = \\frac{P_2}{T_2}$."
    ),

    # 48. isothermal process (index 1003)
    1003: (
        "In thermodynamics, a process occurring at constant thermodynamic temperature ($\\Delta T = 0$ or $T = \\text{const}$). "
        "For an ideal gas whose internal energy depends exclusively on temperature, $\\Delta U = 0$, meaning all heat absorbed is converted into work ($Q = W$). "
        "The reversible work done during isothermal expansion from volume $V_1$ to $V_2$ is:\n\n"
        "$$W = \\int_{V_1}^{V_2} P\\,dV = nRT \\int_{V_1}^{V_2} \\frac{dV}{V} = nRT \\ln\\left(\\frac{V_2}{V_1}\\right) = nRT \\ln\\left(\\frac{P_1}{P_2}\\right)$$\n\n"
        "Satisfies Boyle's law: $P_1 V_1 = P_2 V_2$."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(i_entries):
        w = i_entries[idx]['word']
        i_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")
    else:
        print(f"[ERROR] Index {idx} out of range (I has {len(i_entries)} entries)")

data['I'] = i_entries

with open(DICT_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section I Final.")

# Rebuild core_dictionary.js
rebuild_script = os.path.join(BASE_DIR, 'scripts', 'rebuild_core_dictionary.py')
print(f"Rebuilding core_dictionary.js via {rebuild_script}...")
res = subprocess.run([sys.executable, rebuild_script], capture_output=True, text=True)
if res.returncode == 0:
    print("Rebuild completed successfully!")
else:
    print("Error during rebuild:")
    print(res.stderr)
