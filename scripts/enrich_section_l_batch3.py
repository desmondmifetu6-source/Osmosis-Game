import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

L = data['L']

enrichments = {
    "lami's theorem": {
        "formula": r"$$\frac{F_1}{\sin\alpha_1} = \frac{F_2}{\sin\alpha_2} = \frac{F_3}{\sin\alpha_3}$$",
        "formula_description": (
            r"For three concurrent coplanar forces $F_1, F_2, F_3$ in equilibrium, "
            r"each force divided by the sine of the angle between the other two is constant. "
            r"$\alpha_1$ is the angle between $F_2$ and $F_3$, etc. Analogue of the sine rule for statics."
        )
    },
    "langevin equation": {
        "formula": r"$$m\ddot{x} = -\gamma \dot{x} + \sqrt{2\gamma k_B T}\,\xi(t)$$",
        "formula_description": (
            r"Stochastic ODE for Brownian motion; $\gamma$ = damping coefficient, "
            r"$\xi(t)$ = Gaussian white noise with $\langle\xi(t)\xi(t')\rangle = \delta(t-t')$. "
            r"Diffusion coefficient: $D = k_B T / \gamma$ (Einstein relation). "
            r"Overdamped limit: $\gamma\dot{x} = F + \sqrt{2\gamma k_B T}\,\xi(t)$."
        )
    },
    "lapse rate": {
        "formula": r"$$\Gamma = -\frac{dT}{dz}, \qquad \Gamma_d = \frac{g}{C_p} \approx 9.8\ \mathrm{K\,km^{-1}}$$",
        "formula_description": (
            r"Rate of temperature decrease with altitude in the atmosphere. "
            r"Dry adiabatic lapse rate $\Gamma_d = g/C_p$; "
            r"environmental (standard) lapse rate $\approx 6.5\ \mathrm{K\,km^{-1}}$. "
            r"If $\Gamma > \Gamma_d$: absolutely unstable (convection); $\Gamma < \Gamma_m$: absolutely stable."
        )
    },
    "law of combining volumes": {
        "formula": r"$$V_A : V_B : V_C = a : b : c \quad \text{(Gay-Lussac's law)}$$",
        "formula_description": (
            r"At constant temperature and pressure, volumes of gaseous reactants and products "
            r"are in simple integer ratios. "
            r"Example: $2\,\text{H}_2(\text{g}) + \text{O}_2(\text{g}) \to 2\,\text{H}_2\text{O}(\text{g})$: "
            r"volumes $2:1:2$."
        )
    },
    "law of conservation of charge": {
        "formula": r"$$Q_{\text{total}} = \sum_i q_i = \text{constant}, \qquad \frac{\partial\rho}{\partial t} + \nabla\cdot\mathbf{J} = 0$$",
        "formula_description": (
            r"Net electric charge in an isolated system is conserved. "
            r"Continuity equation: $\partial\rho/\partial t + \nabla\cdot\mathbf{J} = 0$ "
            r"where $\rho$ = charge density, $\mathbf{J}$ = current density. "
            "One of the exact conservation laws of nature — no exception ever observed."
        )
    },
    "law of conservation of linear momentum": {
        "formula": r"$$\mathbf{p}_{\text{total}} = \sum_i m_i\mathbf{v}_i = \text{const} \quad (\mathbf{F}_{\text{ext}} = \mathbf{0})$$",
        "formula_description": (
            r"Total linear momentum is conserved when net external force is zero. "
            r"Impulse-momentum: $\mathbf{F}_{\text{ext}}\,\Delta t = \Delta\mathbf{p}$. "
            "Follows from Newton's third law; equivalent to translational symmetry via Noether's theorem."
        )
    },
    "law of cosines": {
        "formula": r"$$c^2 = a^2 + b^2 - 2ab\cos C$$",
        "formula_description": (
            r"Generalises Pythagoras: for a triangle with sides $a, b, c$ and angle $C$ opposite side $c$. "
            r"Similarly: $a^2 = b^2 + c^2 - 2bc\cos A$; $b^2 = a^2 + c^2 - 2ac\cos B$. "
            r"When $C = 90°$: reduces to $c^2 = a^2 + b^2$."
        )
    },
    "law of cosine": {
        "formula": r"$$c^2 = a^2 + b^2 - 2ab\cos C$$",
        "formula_description": (
            r"Generalises Pythagoras: for a triangle with sides $a, b, c$ and angle $C$ opposite side $c$. "
            r"Similarly: $a^2 = b^2 + c^2 - 2bc\cos A$; $b^2 = a^2 + c^2 - 2ac\cos B$. "
            r"When $C = 90°$: reduces to $c^2 = a^2 + b^2$."
        )
    },
    "law of flotation": {
        "formula": r"$$\rho_{\text{object}}\,V_{\text{total}}\,g = \rho_{\text{fluid}}\,V_{\text{submerged}}\,g$$",
        "formula_description": (
            r"A floating object displaces fluid equal in weight to its own weight. "
            r"Fraction submerged: $\dfrac{V_{\text{sub}}}{V_{\text{total}}} = \dfrac{\rho_{\text{obj}}}{\rho_{\text{fluid}}}$. "
            r"Archimedes' principle: buoyant force $F_b = \rho_f V_{\text{sub}} g$."
        )
    },
    "law of large numbers": {
        "formula": r"$$\bar{X}_n = \frac{1}{n}\sum_{i=1}^{n} X_i \xrightarrow{n\to\infty} \mu = E[X]$$",
        "formula_description": (
            r"Sample mean converges to population mean. "
            r"Weak LLN: $P(|\bar{X}_n - \mu| > \varepsilon) \to 0$ for all $\varepsilon > 0$. "
            r"Strong LLN: $\bar{X}_n \to \mu$ almost surely. Requires finite variance $\sigma^2 < \infty$."
        )
    },
    "law of sines": {
        "formula": r"$$\frac{a}{\sin A} = \frac{b}{\sin B} = \frac{c}{\sin C} = 2R$$",
        "formula_description": (
            r"For a triangle with sides $a, b, c$ opposite angles $A, B, C$ and circumradius $R$. "
            r"Area form: $\text{Area} = \dfrac{abc}{4R} = \dfrac{1}{2}ab\sin C$. "
            "Used to solve oblique triangles given AAS, ASA, or SSA."
        )
    },
    "law of tangents": {
        "formula": r"$$\frac{a - b}{a + b} = \frac{\tan\!\left(\tfrac{A-B}{2}\right)}{\tan\!\left(\tfrac{A+B}{2}\right)}$$",
        "formula_description": (
            r"Relates two sides $a, b$ and their opposite angles $A, B$ in any triangle. "
            "Alternative to the law of sines for solving oblique triangles. "
            r"Particularly useful when two sides and the included angle are known."
        )
    },
    "law of universal gravitation": {
        "formula": r"$$F = G\frac{m_1 m_2}{r^2}, \qquad G = 6.674\times10^{-11}\ \mathrm{N\,m^2\,kg^{-2}}$$",
        "formula_description": (
            r"Newton's law: every mass attracts every other mass with force proportional to "
            r"their product and inversely proportional to the square of their separation $r$. "
            r"Gravitational field: $\mathbf{g} = -\dfrac{Gm}{r^2}\hat{r}$; "
            r"escape velocity: $v_e = \sqrt{2GM/R}$."
        )
    },
    "laws of electromagnetic induction": {
        "formula": r"$$\mathcal{E} = -N\frac{d\Phi_B}{dt}, \qquad \Phi_B = \int_S \mathbf{B}\cdot d\mathbf{A}$$",
        "formula_description": (
            r"Faraday's first law: changing flux induces EMF. "
            r"Faraday's second law: EMF $\propto$ rate of flux change. "
            r"Lenz's law (sign): induced current opposes flux change. "
            r"Motional EMF: $\mathcal{E} = Bvl$ for conductor of length $l$ moving at $v$ in field $B$."
        )
    },
    "laws of reflection": {
        "formula": r"$$\theta_i = \theta_r \qquad (\text{angle of incidence} = \text{angle of reflection})$$",
        "formula_description": (
            r"Both angles measured from the normal to the surface. "
            r"Incident ray, reflected ray, and normal are coplanar. "
            r"For a spherical mirror: $\dfrac{1}{f} = \dfrac{1}{v} + \dfrac{1}{u}$, $f = R/2$."
        )
    },
    "laws of refraction": {
        "formula": r"$$n_1\sin\theta_1 = n_2\sin\theta_2 \qquad \text{(Snell's law)}$$",
        "formula_description": (
            r"$n_1, n_2$ = refractive indices of media 1 and 2; "
            r"$\theta_1, \theta_2$ = angles from normal. "
            r"Critical angle for TIR: $\theta_c = \arcsin\!\left(\dfrac{n_2}{n_1}\right)$ (when $n_1 > n_2$). "
            r"Refractive index: $n = c/v = \sqrt{\varepsilon_r \mu_r}$."
        )
    },
    "lawson criterion": {
        "formula": r"$$n\,\tau_E \ge \frac{12\,k_B T}{\langle\sigma v\rangle\,E_\alpha} \approx 10^{20}\ \mathrm{m^{-3}\,s} \quad (D\text{-}T \text{ at } 10\,\text{keV})$$",
        "formula_description": (
            r"Condition for nuclear fusion ignition: $n$ = plasma density, $\tau_E$ = energy confinement time. "
            r"Triple product form: $n T \tau_E \gtrsim 3\times10^{21}\ \mathrm{m^{-3}\,keV\,s}$. "
            "Named after John Lawson (1957); the fundamental target for fusion reactor design."
        )
    },
    "lambda series": {
        "formula": r"$$\Lambda = \sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n^s} = \left(1 - 2^{1-s}\right)\zeta(s)$$",
        "formula_description": (
            r"Dirichlet eta function (alternating zeta series). "
            r"Related to Riemann zeta function $\zeta(s) = \sum n^{-s}$ via $\eta(s) = (1-2^{1-s})\zeta(s)$. "
            r"Converges for $\text{Re}(s) > 0$, broader than $\zeta(s)$ which needs $\text{Re}(s)>1$."
        )
    },
    "lacunary series": {
        "formula": r"$$f(z) = \sum_{k=0}^{\infty} a_k z^{n_k}, \qquad \liminf_{k\to\infty}\frac{n_{k+1}}{n_k} > 1$$",
        "formula_description": (
            r"A power series with large gaps between non-zero terms (lacunae). "
            r"Hadamard's gap theorem: if $n_{k+1}/n_k \ge q > 1$ for all $k$, "
            "then the circle of convergence is a natural boundary — the series cannot be analytically continued beyond it."
        )
    },
}

count = 0
for entry in L:
    word = entry.get('word', '').strip().lower()
    if word in enrichments and 'formula' not in entry:
        entry['formula'] = enrichments[word]['formula']
        entry['formula_description'] = enrichments[word]['formula_description']
        count += 1
        print(f"  [OK] {entry['word']}")

data['L'] = L
with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nDone. {count} entries enriched.")
