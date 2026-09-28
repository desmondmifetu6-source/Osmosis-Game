import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

M = data['M']

enrichments = {
    "mach number": {
        "formula": r"$$\text{Ma} = \frac{v}{c_s}, \qquad c_s = \sqrt{\frac{\gamma R T}{M_m}}$$",
        "formula_description": (
            r"$v$ = object speed, $c_s$ = local speed of sound, $\gamma$ = adiabatic index, "
            r"$R$ = gas constant, $T$ = temperature, $M_m$ = molar mass. "
            r"Ma $< 1$: subsonic; Ma $= 1$: sonic; Ma $> 1$: supersonic; Ma $> 5$: hypersonic. "
            r"Mach angle: $\sin\mu = 1/\text{Ma}$."
        )
    },
    "mach angle": {
        "formula": r"$$\sin\mu = \frac{1}{\text{Ma}} = \frac{c_s}{v}$$",
        "formula_description": (
            r"Half-angle of the Mach cone formed by a supersonic object. "
            r"$\mu$ = Mach angle, Ma = Mach number $> 1$. "
            "The cone's pressure wave (shock wave) propagates at exactly this angle to the direction of motion."
        )
    },
    "maclaurin's series": {
        "formula": r"$$f(x) = \sum_{n=0}^{\infty} \frac{f^{(n)}(0)}{n!}\,x^n = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \cdots$$",
        "formula_description": (
            r"Taylor series centred at $x = 0$. Key expansions: "
            r"$e^x = \sum x^n/n!$, $\sin x = \sum (-1)^n x^{2n+1}/(2n+1)!$, "
            r"$\cos x = \sum (-1)^n x^{2n}/(2n)!$, $(1+x)^k = \sum \binom{k}{n}x^n$. "
            r"Named after Colin Maclaurin (1698–1746)."
        )
    },
    "maclaurin's formula": {
        "formula": r"$$f(x) = f(0) + xf'(0) + \frac{x^2}{2!}f''(0) + \cdots + \frac{x^n}{n!}f^{(n)}(0) + R_n$$",
        "formula_description": (
            r"Finite form with remainder $R_n = \dfrac{x^{n+1}}{(n+1)!}f^{(n+1)}(\theta x)$, $0 < \theta < 1$ (Lagrange form). "
            "Special case of Taylor's formula about $a = 0$."
        )
    },
    "madelung constant": {
        "formula": r"$$M = \sum_{j} \frac{(\pm 1)}{r_j/r_0}$$",
        "formula_description": (
            r"Geometric factor in lattice energy; depends only on crystal structure. "
            r"NaCl: $M \approx 1.7476$; CsCl: $M \approx 1.7627$; ZnS (wurtzite): $M \approx 1.6413$. "
            r"Appears in Born–Landé: $U = -\dfrac{N_A M z^+z^-e^2}{4\pi\varepsilon_0 r_0}\!\left(1-\dfrac{1}{n}\right)$."
        )
    },
    "maxwell's equations": {
        "formula": (
            r"$$\nabla\cdot\mathbf{E} = \frac{\rho}{\varepsilon_0}, \quad "
            r"\nabla\cdot\mathbf{B} = 0, \quad "
            r"\nabla\times\mathbf{E} = -\frac{\partial\mathbf{B}}{\partial t}, \quad "
            r"\nabla\times\mathbf{B} = \mu_0\mathbf{J} + \mu_0\varepsilon_0\frac{\partial\mathbf{E}}{\partial t}$$"
        ),
        "formula_description": (
            r"The four fundamental laws of electromagnetism in differential form. "
            r"1: Gauss's law (electric). 2: Gauss's law (magnetic — no monopoles). "
            r"3: Faraday's law. 4: Ampère-Maxwell law (displacement current $\varepsilon_0\partial\mathbf{E}/\partial t$ added by Maxwell). "
            r"Predict EM waves propagating at $c = 1/\sqrt{\mu_0\varepsilon_0} \approx 3\times10^8\ \mathrm{m\,s^{-1}}$."
        )
    },
    "maxwell-boltzmann distribution": {
        "formula": r"$$f(v) = 4\pi n\!\left(\frac{m}{2\pi k_B T}\right)^{3/2} v^2\, e^{-mv^2/2k_BT}$$",
        "formula_description": (
            r"Speed distribution of molecules in an ideal gas. "
            r"Most probable speed: $v_p = \sqrt{2k_BT/m}$. "
            r"Mean speed: $\bar{v} = \sqrt{8k_BT/\pi m}$. "
            r"RMS speed: $v_{\text{rms}} = \sqrt{3k_BT/m}$. "
            r"Order: $v_p < \bar{v} < v_{\text{rms}}$."
        )
    },
    "mendel's laws": {
        "formula": r"$$P(\text{Aa}) = 2pq,\quad P(\text{AA}) = p^2,\quad P(\text{aa}) = q^2 \quad (p+q=1)$$",
        "formula_description": (
            r"Hardy-Weinberg form of Mendel's segregation ratios. "
            r"Monohybrid cross $\text{Aa}\times\text{Aa}$: offspring ratio $1\,\text{AA}:2\,\text{Aa}:1\,\text{aa}$ (genotype), $3:1$ (phenotype). "
            r"Dihybrid cross: $9:3:3:1$ phenotype ratio. "
            r"Law of independent assortment: $P(A\cap B) = P(A)\cdot P(B)$ for unlinked genes."
        )
    },
    "michaelis-menten equation": {
        "formula": r"$$v = \frac{V_{\max}[\text{S}]}{K_m + [\text{S}]}, \qquad K_m = \frac{k_{-1}+k_2}{k_1}$$",
        "formula_description": (
            r"Enzyme kinetics: $v$ = reaction rate, $V_{\max} = k_2[\text{E}]_{\text{total}}$, "
            r"$K_m$ = Michaelis constant (substrate concentration at half-maximal rate). "
            r"Lineweaver-Burk linearisation: $\dfrac{1}{v} = \dfrac{K_m}{V_{\max}[\text{S}]} + \dfrac{1}{V_{\max}}$."
        )
    },
    "moment of inertia": {
        "formula": r"$$I = \sum_i m_i r_i^2 = \int r^2\,dm, \qquad \tau = I\alpha$$",
        "formula_description": (
            r"Rotational analogue of mass. Parallel axis theorem: $I = I_{\text{cm}} + Md^2$. "
            r"Perpendicular axis theorem (2D): $I_z = I_x + I_y$. "
            r"Common values: solid cylinder $I = \tfrac{1}{2}MR^2$; sphere $I = \tfrac{2}{5}MR^2$; rod about centre $I = \tfrac{1}{12}ML^2$."
        )
    },
    "momentum": {
        "formula": r"$$\mathbf{p} = m\mathbf{v}, \qquad \mathbf{F}_{\text{net}} = \frac{d\mathbf{p}}{dt}$$",
        "formula_description": (
            r"SI unit: $\mathrm{kg\,m\,s^{-1}} = \mathrm{N\,s}$. "
            r"Relativistic: $\mathbf{p} = \gamma m_0\mathbf{v}$. "
            r"Angular momentum: $\mathbf{L} = \mathbf{r}\times\mathbf{p} = I\boldsymbol{\omega}$. "
            r"Energy-momentum relation: $E^2 = (pc)^2 + (m_0c^2)^2$."
        )
    },
    "magnetic flux": {
        "formula": r"$$\Phi_B = \int_S \mathbf{B}\cdot d\mathbf{A} = BA\cos\theta \quad (\text{uniform } \mathbf{B})$$",
        "formula_description": (
            r"SI unit: Weber (Wb = V$\cdot$s = kg$\cdot$m$^2\cdot$s$^{-2}\cdot$A$^{-1}$). "
            r"Faraday's law: $\mathcal{E} = -d\Phi_B/dt$. "
            r"Gauss's law for magnetism: $\oint \mathbf{B}\cdot d\mathbf{A} = 0$ (no magnetic monopoles)."
        )
    },
    "magnetic field": {
        "formula": r"$$\mathbf{F} = q\mathbf{v}\times\mathbf{B}, \qquad \oint \mathbf{B}\cdot d\mathbf{l} = \mu_0 I_{\text{enc}}$$",
        "formula_description": (
            r"SI unit: Tesla (T = kg$\cdot$s$^{-2}\cdot$A$^{-1}$). "
            r"Biot-Savart law: $d\mathbf{B} = \dfrac{\mu_0 I}{4\pi}\dfrac{d\mathbf{l}\times\hat{r}}{r^2}$. "
            r"Long straight wire: $B = \mu_0 I / 2\pi r$. Solenoid: $B = \mu_0 n I$."
        )
    },
    "mass-energy equivalence": {
        "formula": r"$$E = mc^2, \qquad E^2 = (pc)^2 + (m_0 c^2)^2$$",
        "formula_description": (
            r"Einstein's relation: rest energy $E_0 = m_0c^2$ where $m_0$ = rest mass, "
            r"$c = 2.998\times10^8\ \mathrm{m\,s^{-1}}$. "
            r"Total energy: $E = \gamma m_0 c^2$. "
            r"$1\ \mathrm{u} = 931.5\ \mathrm{MeV}/c^2$. Binding energy $= \Delta m \cdot c^2$."
        )
    },
    "mean free path": {
        "formula": r"$$\lambda = \frac{1}{\sqrt{2}\,\pi d^2 n} = \frac{k_B T}{\sqrt{2}\,\pi d^2 p}$$",
        "formula_description": (
            r"Average distance a molecule travels between collisions. "
            r"$d$ = molecular diameter, $n$ = number density, $p$ = pressure. "
            r"At STP for air: $\lambda \approx 68\ \mathrm{nm}$. "
            r"Viscosity relation: $\eta = \tfrac{1}{3}\rho\bar{v}\lambda$."
        )
    },
    "mirror formula": {
        "formula": r"$$\frac{1}{f} = \frac{1}{v} + \frac{1}{u}, \qquad m = -\frac{v}{u}, \qquad f = \frac{R}{2}$$",
        "formula_description": (
            r"For spherical mirrors: $f$ = focal length, $v$ = image distance, $u$ = object distance "
            r"(sign convention: distances measured from pole; real positive for concave). "
            r"Magnification $m > 0$: virtual/upright; $m < 0$: real/inverted."
        )
    },
    "modulus of elasticity": {
        "formula": r"$$E = \frac{\sigma}{\varepsilon} = \frac{F/A}{\Delta L/L_0}$$",
        "formula_description": (
            r"Young's modulus $E$: ratio of tensile stress $\sigma$ to tensile strain $\varepsilon$. "
            r"Shear modulus: $G = \tau/\gamma$. Bulk modulus: $K = -V\,dP/dV$. "
            r"Poisson's ratio: $\nu = -\varepsilon_{\text{lateral}}/\varepsilon_{\text{axial}}$. "
            r"Relation: $E = 2G(1+\nu) = 3K(1-2\nu)$."
        )
    },
    "molar mass": {
        "formula": r"$$M = \frac{m}{n}, \qquad n = \frac{m}{M} = \frac{N}{N_A}$$",
        "formula_description": (
            r"$M$ = molar mass (g$\cdot$mol$^{-1}$), $m$ = mass (g), $n$ = amount of substance (mol). "
            r"$N_A = 6.022\times10^{23}\ \mathrm{mol^{-1}}$ (Avogadro constant). "
            r"Ideal gas: $pV = nRT$, so $M = \rho RT/p$ (vapour density method)."
        )
    },
    "molarity": {
        "formula": r"$$c = \frac{n}{V} = \frac{m}{MV}, \qquad c_1V_1 = c_2V_2 \text{ (dilution)}$$",
        "formula_description": (
            r"SI unit: mol$\cdot$m$^{-3}$; common unit: mol$\cdot$L$^{-1}$ (M). "
            r"$n$ = moles of solute, $V$ = volume of solution. "
            r"Dilution law: $c_1V_1 = c_2V_2$ (moles of solute conserved). "
            r"Molality $b = n_{\text{solute}}/m_{\text{solvent}}$ (mol$\cdot$kg$^{-1}$)."
        )
    },
    "muon": {
        "formula": r"$$m_\mu = 105.66\ \mathrm{MeV}/c^2 \approx 207\,m_e, \qquad \tau_\mu = 2.197\ \mu\mathrm{s}$$",
        "formula_description": (
            r"Second-generation lepton; charge $-e$, spin $\tfrac{1}{2}$. "
            r"Decays: $\mu^- \to e^- + \bar{\nu}_e + \nu_\mu$. "
            r"Relativistic time dilation allows cosmic muons to reach Earth's surface: "
            r"$t' = \gamma\tau_\mu$ with $\gamma \sim 20$ at $3\ \mathrm{km}$ altitude."
        )
    },
}

count = 0
for entry in M:
    word = entry.get('word', '').strip().lower()
    if word in enrichments and 'formula' not in entry:
        entry['formula'] = enrichments[word]['formula']
        entry['formula_description'] = enrichments[word]['formula_description']
        count += 1
        print(f"  [OK] {entry['word']}")

data['M'] = M
with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone. {count} entries enriched.")
