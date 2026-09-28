import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

L = data['L']

enrichments = {
    "l'hopital's rule": {
        "formula": r"$$\lim_{x \to c} \frac{f(x)}{g(x)} = \lim_{x \to c} \frac{f'(x)}{g'(x)}$$",
        "formula_description": (
            "Where $f(c) = g(c) = 0$ (or both $\pm\infty$). "
            "Differentiate numerator and denominator separately — not the quotient rule. "
            "Named after Guillaume de L'Hôpital (1661–1704)."
        )
    },
    "lactic acid": {
        "formula": r"$$\text{CH}_3\text{CH(OH)COOH}$$",
        "formula_description": (
            "Molecular formula $\mathrm{C_3H_6O_3}$, molar mass $= 90.08\ \mathrm{g\,mol^{-1}}$. "
            "An alpha hydroxy carboxylic acid; produced in muscles during anaerobic respiration via: "
            r"$\text{C}_6\text{H}_{12}\text{O}_6 \rightarrow 2\,\text{CH}_3\text{CH(OH)COOH}$."
        )
    },
    "lactic acid fermentation": {
        "formula": r"$$\text{C}_6\text{H}_{12}\text{O}_6 \xrightarrow{\text{LDH}} 2\,\text{CH}_3\text{CH(OH)COOH}$$",
        "formula_description": (
            "Glucose is converted to lactic acid with a net gain of $2$ ATP. "
            "No oxygen required; pyruvate acts as the terminal electron acceptor. "
            r"Overall: $\Delta G = -196\ \mathrm{kJ\,mol^{-1}}$."
        )
    },
    "lagrange form of the remainder": {
        "formula": r"$$R_n(x) = \frac{f^{(n+1)}(c)}{(n+1)!}(x - a)^{n+1}$$",
        "formula_description": (
            "For some $c$ between $a$ and $x$. "
            "Gives the error when a Taylor polynomial of degree $n$ approximates $f(x)$ at $a$. "
            r"If $|f^{(n+1)}(x)| \le M$ on $[a,x]$, then $|R_n(x)| \le \dfrac{M\,|x-a|^{n+1}}{(n+1)!}$."
        )
    },
    "lagrange interpolation formula": {
        "formula": r"$$P(x) = \sum_{j=0}^{n} y_j \prod_{\substack{i=0\\i\neq j}}^{n} \frac{x - x_i}{x_j - x_i}$$",
        "formula_description": (
            "Constructs a unique polynomial of degree $\le n$ passing through "
            "$(x_0,y_0),(x_1,y_1),\ldots,(x_n,y_n)$. "
            r"Each basis polynomial $\ell_j(x) = \prod_{i\neq j}\frac{x-x_i}{x_j-x_i}$ satisfies $\ell_j(x_k)=\delta_{jk}$."
        )
    },
    "lagrange method of multipliers": {
        "formula": r"$$\nabla f = \lambda\,\nabla g \quad \Longleftrightarrow \quad \nabla\bigl(f - \lambda g\bigr) = \mathbf{0}$$",
        "formula_description": (
            "Finds extrema of $f(x,y,\ldots)$ subject to constraint $g(x,y,\ldots)=0$. "
            "$\lambda$ is the Lagrange multiplier. "
            "For multiple constraints $g_i$: $\nabla f = \sum_i \lambda_i \nabla g_i$."
        )
    },
    "lagrange multipliers": {
        "formula": r"$$\nabla f(\mathbf{x}^*) = \sum_{i=1}^{m} \lambda_i \,\nabla g_i(\mathbf{x}^*)$$",
        "formula_description": (
            "At a constrained extremum $\mathbf{x}^*$, the gradient of the objective $f$ "
            "is a linear combination of the constraint gradients $\nabla g_i$. "
            "The scalars $\lambda_i$ are Lagrange multipliers."
        )
    },
    "lagrange's equations": {
        "formula": r"$$\frac{d}{dt}\!\left(\frac{\partial \mathcal{L}}{\partial \dot{q}_i}\right) - \frac{\partial \mathcal{L}}{\partial q_i} = Q_i$$",
        "formula_description": (
            "Where $\mathcal{L} = T - V$ is the Lagrangian (kinetic minus potential energy), "
            "$q_i$ are generalised coordinates, $\dot{q}_i$ are generalised velocities, "
            "and $Q_i$ are non-conservative generalised forces. "
            "For conservative systems $Q_i = 0$."
        )
    },
    "lagrange's four-square theorem": {
        "formula": r"$$\forall\, n \in \mathbb{Z}^+,\quad n = a^2 + b^2 + c^2 + d^2 \quad (a,b,c,d \in \mathbb{Z}_{\ge 0})$$",
        "formula_description": (
            "Every positive integer can be expressed as the sum of four perfect squares. "
            "Proved by Lagrange in 1770. "
            "Example: $7 = 4+1+1+1 = 2^2+1^2+1^2+1^2$."
        )
    },
    "lagrange's linear equation": {
        "formula": r"$$\sum_{i=1}^{n} P_i(x_1,\ldots,x_n)\,\frac{\partial z}{\partial x_i} = R(x_1,\ldots,x_n,\,z)$$",
        "formula_description": (
            "A first-order quasi-linear PDE of the form $Pp + Qq = R$ in two variables. "
            "Solved via the method of characteristics: "
            r"$\dfrac{dx}{P} = \dfrac{dy}{Q} = \dfrac{dz}{R}$."
        )
    },
    "lagrange's theorem": {
        "formula": r"$$|H| \;\Big|\; |G| \quad \Longrightarrow \quad [G:H] = \frac{|G|}{|H|}$$",
        "formula_description": (
            "If $H$ is a subgroup of a finite group $G$, then the order of $H$ divides the order of $G$. "
            "$[G:H]$ is the index (number of distinct cosets of $H$ in $G$). "
            "Corollary: the order of any element divides $|G|$."
        )
    },
    "lambert's laws": {
        "formula": r"$$I = I_0\cos\theta \qquad \text{and} \qquad I = I_0\,e^{-\mu x}$$",
        "formula_description": (
            "Lambert's cosine law: intensity of emitted/reflected radiation $I$ falls as $\cos\theta$ "
            "where $\theta$ is the angle from the normal. "
            "Lambert-Beer law: $A = \varepsilon c l$ where $A$ is absorbance, "
            "$\varepsilon$ is molar absorptivity, $c$ is concentration and $l$ is path length."
        )
    },
    "landau levels": {
        "formula": r"$$E_n = \hbar\omega_c\!\left(n + \frac{1}{2}\right), \quad \omega_c = \frac{eB}{m_e}$$",
        "formula_description": (
            "Quantised energy levels of a free electron in a uniform magnetic field $B$. "
            "$n = 0, 1, 2, \ldots$ is the Landau level index, $\omega_c$ is the cyclotron frequency. "
            "Degeneracy of each level per unit area: $eB/h$."
        )
    },
    "landé interval rule": {
        "formula": r"$$\Delta E_{J,\,J-1} \propto J_{\max}(J_{\max}+1) - J_{\min}(J_{\min}+1)$$",
        "formula_description": (
            "Energy splitting between adjacent $J$ levels in a multiplet is proportional to the "
            "larger $J$ value. Specifically: "
            r"$E_J - E_{J-1} = A\,J$ where $A = \lambda\langle\mathbf{L}\cdot\mathbf{S}\rangle/(2JL)$ "
            "and $J$ runs from $|L-S|$ to $L+S$."
        )
    },
    "langmuir adsorption isotherm": {
        "formula": r"$$\theta = \frac{K_{\mathrm{ads}}\,p}{1 + K_{\mathrm{ads}}\,p}$$",
        "formula_description": (
            r"$\theta$ = fractional surface coverage, $p$ = gas pressure, "
            r"$K_{\mathrm{ads}}$ = adsorption equilibrium constant. "
            "Assumes monolayer adsorption, equivalent sites, no lateral interactions. "
            r"Linearised form: $\dfrac{p}{\theta} = \dfrac{1}{K_{\mathrm{ads}}} + p$."
        )
    },
    "langmuir frequency": {
        "formula": r"$$\omega_p = \sqrt{\frac{n_e\,e^2}{\varepsilon_0\,m_e}}$$",
        "formula_description": (
            r"Plasma (Langmuir) frequency: $n_e$ = electron number density, "
            r"$e$ = elementary charge, $\varepsilon_0$ = permittivity of free space, "
            r"$m_e$ = electron mass. "
            r"EM waves with $\omega < \omega_p$ cannot propagate through the plasma."
        )
    },
    "laplace distribution": {
        "formula": r"$$f(x;\,\mu,b) = \frac{1}{2b}\exp\!\left(-\frac{|x-\mu|}{b}\right), \quad b > 0$$",
        "formula_description": (
            r"Mean $= \mu$, variance $= 2b^2$. "
            r"CDF: $F(x) = \tfrac{1}{2} + \tfrac{1}{2}\operatorname{sgn}(x-\mu)\!\left[1 - e^{-|x-\mu|/b}\right]$. "
            "Also called the double-exponential distribution; heavier tails than the Gaussian."
        )
    },
    "laplace equation": {
        "formula": r"$$\nabla^2 \phi = \frac{\partial^2\phi}{\partial x^2} + \frac{\partial^2\phi}{\partial y^2} + \frac{\partial^2\phi}{\partial z^2} = 0$$",
        "formula_description": (
            "Solutions are called harmonic functions. Governs electrostatic potential in free space, "
            "steady-state heat conduction, irrotational fluid flow, and gravitational potential. "
            r"In spherical coords: $\nabla^2\phi = \frac{1}{r^2}\frac{\partial}{\partial r}\!\left(r^2\frac{\partial\phi}{\partial r}\right) + \frac{1}{r^2\sin\theta}\frac{\partial}{\partial\theta}\!\left(\sin\theta\frac{\partial\phi}{\partial\theta}\right) + \frac{1}{r^2\sin^2\theta}\frac{\partial^2\phi}{\partial\varphi^2} = 0$."
        )
    },
    "laplace operator": {
        "formula": r"$$\nabla^2 f = \Delta f = \operatorname{div}(\nabla f) = \sum_{i=1}^{n}\frac{\partial^2 f}{\partial x_i^2}$$",
        "formula_description": (
            "Also written $\Delta$ or del-squared. In 3D Cartesian: "
            r"$\nabla^2 f = \dfrac{\partial^2 f}{\partial x^2}+\dfrac{\partial^2 f}{\partial y^2}+\dfrac{\partial^2 f}{\partial z^2}$. "
            r"In 2D polar: $\nabla^2 f = \dfrac{\partial^2 f}{\partial r^2}+\dfrac{1}{r}\dfrac{\partial f}{\partial r}+\dfrac{1}{r^2}\dfrac{\partial^2 f}{\partial\theta^2}$."
        )
    },
    "laplace transform": {
        "formula": r"$$\mathcal{L}\{f(t)\}(s) = \int_0^{\infty} f(t)\,e^{-st}\,dt = F(s)$$",
        "formula_description": (
            r"Converts ODEs into algebraic equations. Key pairs: "
            r"$\mathcal{L}\{1\}=\frac{1}{s}$, $\mathcal{L}\{e^{at}\}=\frac{1}{s-a}$, "
            r"$\mathcal{L}\{t^n\}=\frac{n!}{s^{n+1}}$, $\mathcal{L}\{\sin\omega t\}=\frac{\omega}{s^2+\omega^2}$. "
            r"Inverse via Bromwich integral: $f(t)=\frac{1}{2\pi i}\int_{\gamma-i\infty}^{\gamma+i\infty}F(s)\,e^{st}\,ds$."
        )
    },
    "laplace's correction": {
        "formula": r"$$v = \sqrt{\frac{\gamma P}{\rho}} = \sqrt{\frac{\gamma RT}{M}}$$",
        "formula_description": (
            r"Speed of sound in a gas; $\gamma = C_p/C_v$ is the adiabatic index, "
            r"$P$ = pressure, $\rho$ = density. "
            r"Newton's original (isothermal) result $v = \sqrt{P/\rho}$ is too low by factor $\sqrt{\gamma}$. "
            r"For air at 0°C: $\gamma \approx 1.402$, giving $v \approx 331\ \mathrm{m\,s^{-1}}$."
        )
    },
    "larmor precession": {
        "formula": r"$$\omega_L = \frac{eB}{2m_e}, \qquad f_L = \frac{eB}{4\pi m_e}$$",
        "formula_description": (
            r"Larmor frequency of precession of electron orbital magnetic moment in field $B$. "
            r"Numerically: $\omega_L \approx 8.794\times10^{10}\,B\ \mathrm{rad\,s^{-1}}$ (with $B$ in Tesla). "
            r"General form for charge $q$, mass $m$: $\boldsymbol{\omega}_L = -\dfrac{q}{2m}\mathbf{B}$."
        )
    },
    "latent heat": {
        "formula": r"$$Q = mL, \qquad L_f \approx 334\ \mathrm{kJ\,kg^{-1}}\ (\text{water}),\quad L_v \approx 2260\ \mathrm{kJ\,kg^{-1}}\ (\text{water})$$",
        "formula_description": (
            r"$Q$ = heat energy transferred, $m$ = mass, $L$ = specific latent heat. "
            r"Latent heat of fusion $L_f$: solid $\leftrightarrow$ liquid. "
            r"Latent heat of vaporisation $L_v$: liquid $\leftrightarrow$ gas. "
            r"Thermodynamically: $L = T\,\Delta S = \Delta H$ at constant $T$ and $P$."
        )
    },
    "lattice energy": {
        "formula": r"$$U = -\frac{N_A M z^+ z^- e^2}{4\pi\varepsilon_0\,r_0}\!\left(1 - \frac{1}{n}\right)$$",
        "formula_description": (
            r"Born–Landé equation; $M$ = Madelung constant, $z^+,z^-$ = ion charges, "
            r"$r_0$ = nearest-neighbour distance, $n$ = Born exponent (~9 for NaCl). "
            r"For NaCl: $M \approx 1.748$, $U \approx -787\ \mathrm{kJ\,mol^{-1}}$. "
            "Calculated via the Born–Haber cycle experimentally."
        )
    },
    "laurent expansion": {
        "formula": r"$$f(z) = \sum_{n=-\infty}^{\infty} a_n (z-z_0)^n, \quad a_n = \frac{1}{2\pi i}\oint_C \frac{f(z)}{(z-z_0)^{n+1}}\,dz$$",
        "formula_description": (
            r"Valid in an annulus $r < |z - z_0| < R$. "
            r"Terms with $n < 0$ form the principal part; if finitely many, $z_0$ is a pole. "
            r"Coefficient $a_{-1}$ is the residue at $z_0$, critical for contour integration."
        )
    },
}

# Apply enrichments
count = 0
for entry in L:
    word = entry.get('word', '').strip().lower()
    if word in enrichments:
        entry['formula'] = enrichments[word]['formula']
        entry['formula_description'] = enrichments[word]['formula_description']
        count += 1
        print(f"  [OK] {entry['word']}")

data['L'] = L

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone. {count}/{len(enrichments)} entries enriched.")
