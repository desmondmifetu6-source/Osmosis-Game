import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

L = data['L']

enrichments = {
    "law of conservation of energy": {
        "formula": r"$$E_{\text{total}} = K + U = \text{constant}, \qquad \Delta E_{\text{system}} + \Delta E_{\text{surroundings}} = 0$$",
        "formula_description": (
            r"Kinetic energy $K = \tfrac{1}{2}mv^2$, potential energy $U$. "
            r"First law of thermodynamics form: $\Delta U = Q - W$ where $Q$ is heat added and $W$ is work done by system. "
            "Energy cannot be created or destroyed, only transformed between forms."
        )
    },
    "law of conservation of mass": {
        "formula": r"$$\sum m_{\text{reactants}} = \sum m_{\text{products}}, \qquad \frac{\partial \rho}{\partial t} + \nabla \cdot (\rho \mathbf{v}) = 0$$",
        "formula_description": (
            r"In a closed system, total mass is constant. "
            r"Continuity equation (fluid form): $\frac{\partial\rho}{\partial t} + \nabla\cdot(\rho\mathbf{v})=0$. "
            "Lavoisier's law; modified relativistically by mass-energy equivalence $E = mc^2$."
        )
    },
    "law of conservation of momentum": {
        "formula": r"$$\mathbf{p}_{\text{total}} = \sum_i m_i \mathbf{v}_i = \text{constant} \quad \text{(no external force)}$$",
        "formula_description": (
            r"For a collision: $m_1\mathbf{u}_1 + m_2\mathbf{u}_2 = m_1\mathbf{v}_1 + m_2\mathbf{v}_2$. "
            r"Elastic collision additionally conserves KE: $\tfrac{1}{2}m_1u_1^2+\tfrac{1}{2}m_2u_2^2 = \tfrac{1}{2}m_1v_1^2+\tfrac{1}{2}m_2v_2^2$. "
            "Follows from Newton's third law and translational symmetry (Noether's theorem)."
        )
    },
    "le chatelier's principle": {
        "formula": r"$$K_c = \frac{[\text{products}]^{\text{stoich}}}{[\text{reactants}]^{\text{stoich}}}, \qquad \Delta G^\circ = -RT\ln K$$",
        "formula_description": (
            r"If a system at equilibrium is disturbed, it shifts to oppose the change. "
            r"Reaction quotient $Q_c$ vs $K_c$: if $Q_c < K_c$ reaction shifts right; if $Q_c > K_c$ shifts left. "
            r"Van't Hoff: $\frac{d\ln K}{dT} = \frac{\Delta H^\circ}{RT^2}$."
        )
    },
    "legendre polynomials": {
        "formula": r"$$P_n(x) = \frac{1}{2^n n!}\frac{d^n}{dx^n}\bigl[(x^2-1)^n\bigr]$$",
        "formula_description": (
            r"Rodrigues' formula. Solutions to Legendre's ODE: $(1-x^2)y''-2xy'+n(n+1)y=0$. "
            r"Orthogonality: $\int_{-1}^{1}P_m(x)P_n(x)\,dx = \dfrac{2}{2n+1}\delta_{mn}$. "
            r"First few: $P_0=1$, $P_1=x$, $P_2=\tfrac{1}{2}(3x^2-1)$, $P_3=\tfrac{1}{2}(5x^3-3x)$."
        )
    },
    "leibniz rule": {
        "formula": r"$$\frac{d^n}{dx^n}\bigl[f(x)g(x)\bigr] = \sum_{k=0}^{n}\binom{n}{k}f^{(k)}(x)\,g^{(n-k)}(x)$$",
        "formula_description": (
            r"Generalised product rule for the $n$-th derivative. "
            r"Integral form (differentiation under the integral sign): "
            r"$\dfrac{d}{dx}\!\int_{a(x)}^{b(x)}\!f(x,t)\,dt = f(x,b)\,b'(x) - f(x,a)\,a'(x) + \int_{a}^{b}\frac{\partial f}{\partial x}\,dt$."
        )
    },
    "lens formula": {
        "formula": r"$$\frac{1}{f} = \frac{1}{v} - \frac{1}{u} = \frac{1}{v} + \frac{1}{|u|}, \qquad m = \frac{v}{u}$$",
        "formula_description": (
            r"$f$ = focal length, $v$ = image distance, $u$ = object distance (sign convention: real-is-positive). "
            r"Lensmaker's equation: $\dfrac{1}{f} = (n-1)\!\left(\dfrac{1}{R_1} - \dfrac{1}{R_2}\right)$. "
            r"Magnification $m = h_i/h_o = v/u$."
        )
    },
    "lenz's law": {
        "formula": r"$$\mathcal{E} = -\frac{d\Phi_B}{dt}, \qquad \Phi_B = \int \mathbf{B}\cdot d\mathbf{A}$$",
        "formula_description": (
            r"The induced EMF $\mathcal{E}$ opposes the change in magnetic flux $\Phi_B$ that caused it (negative sign). "
            r"Faraday's law magnitude: $|\mathcal{E}| = N\dfrac{d\Phi_B}{dt}$ for $N$ turns. "
            "A consequence of conservation of energy — it resists the change driving induction."
        )
    },
    "lewis acid": {
        "formula": r"$$\text{A} + :\text{B} \longrightarrow \text{A:B}$$",
        "formula_description": (
            r"Lewis acid $\text{A}$ = electron-pair acceptor; Lewis base $\text{B}$ = electron-pair donor. "
            r"Broader than Brønsted-Lowry definition (no $\text{H}^+$ required). "
            r"Examples: $\text{BF}_3 + \text{NH}_3 \rightarrow \text{F}_3\text{B:NH}_3$; "
            r"$\text{AlCl}_3$, $\text{Fe}^{3+}$, $\text{Cu}^{2+}$ are Lewis acids."
        )
    },
    "linear momentum": {
        "formula": r"$$\mathbf{p} = m\mathbf{v}, \qquad \mathbf{F} = \frac{d\mathbf{p}}{dt}$$",
        "formula_description": (
            r"SI unit: $\mathrm{kg\,m\,s^{-1}}$ (= $\mathrm{N\,s}$). "
            r"Impulse-momentum theorem: $\mathbf{J} = \Delta\mathbf{p} = \int \mathbf{F}\,dt$. "
            r"Relativistic momentum: $\mathbf{p} = \gamma m_0 \mathbf{v}$ where $\gamma = 1/\sqrt{1-v^2/c^2}$."
        )
    },
    "lorentz force": {
        "formula": r"$$\mathbf{F} = q(\mathbf{E} + \mathbf{v}\times\mathbf{B})$$",
        "formula_description": (
            r"Force on a charge $q$ moving with velocity $\mathbf{v}$ in electric field $\mathbf{E}$ and magnetic field $\mathbf{B}$. "
            r"Magnetic component $q\mathbf{v}\times\mathbf{B}$ does no work (perpendicular to $\mathbf{v}$). "
            r"Cyclotron radius: $r = \dfrac{mv}{|q|B}$; cyclotron frequency: $\omega_c = \dfrac{|q|B}{m}$."
        )
    },
    "lorentz transformation": {
        "formula": r"$$t' = \gamma\!\left(t - \frac{vx}{c^2}\right),\quad x' = \gamma(x - vt),\quad \gamma = \frac{1}{\sqrt{1 - v^2/c^2}}$$",
        "formula_description": (
            r"Special relativity coordinate transform between inertial frames $S$ and $S'$ with relative velocity $v$. "
            r"Time dilation: $\Delta t' = \gamma\,\Delta t_0$. "
            r"Length contraction: $L = L_0/\gamma$. "
            r"Velocity addition: $u' = \dfrac{u - v}{1 - uv/c^2}$."
        )
    },
    "loschmidt constant": {
        "formula": r"$$n_0 = \frac{N_A}{V_m} = \frac{p}{k_B T}\bigg|_{T=273.15\,\text{K}} \approx 2.6868\times10^{25}\ \mathrm{m^{-3}}$$",
        "formula_description": (
            r"Number of molecules per unit volume of an ideal gas at STP. "
            r"$N_A = 6.022\times10^{23}\ \mathrm{mol^{-1}}$, $V_m = 22.414\ \mathrm{L\,mol^{-1}}$ at STP. "
            "Named after Josef Loschmidt (1821–1895), who first estimated atomic sizes."
        )
    },
    "law of mass action": {
        "formula": r"$$K_c = \frac{\prod[\text{products}]^{\nu_i}}{\prod[\text{reactants}]^{\nu_j}}, \qquad K_p = K_c(RT)^{\Delta n}$$",
        "formula_description": (
            r"For reaction $aA + bB \rightleftharpoons cC + dD$: "
            r"$K_c = \dfrac{[\text{C}]^c[\text{D}]^d}{[\text{A}]^a[\text{B}]^b}$. "
            r"$\Delta n = (c+d)-(a+b)$ = change in moles of gas. "
            r"Related to Gibbs energy: $\Delta G^\circ = -RT\ln K$."
        )
    },
    "law of radioactive decay": {
        "formula": r"$$N(t) = N_0\,e^{-\lambda t}, \qquad t_{1/2} = \frac{\ln 2}{\lambda} \approx \frac{0.693}{\lambda}$$",
        "formula_description": (
            r"$N(t)$ = number of undecayed nuclei at time $t$, $N_0$ = initial count, $\lambda$ = decay constant. "
            r"Activity $A = \lambda N = A_0 e^{-\lambda t}$ (SI unit: Becquerel = $\mathrm{s^{-1}}$). "
            r"Mean lifetime: $\tau = 1/\lambda$; $t_{1/2} = \tau\ln 2$."
        )
    },
    "laminar flow": {
        "formula": r"$$\text{Re} = \frac{\rho v D}{\mu} < 2300 \quad (\text{laminar}), \qquad Q = \frac{\pi r^4 \Delta P}{8 \mu L}$$",
        "formula_description": (
            r"Reynolds number $\text{Re}$ determines flow regime. "
            r"Hagen-Poiseuille equation: volumetric flow rate $Q$ through a pipe of radius $r$, length $L$, "
            r"pressure drop $\Delta P$, dynamic viscosity $\mu$. "
            r"Velocity profile: parabolic, $v(r) = \dfrac{\Delta P}{4\mu L}(R^2 - r^2)$."
        )
    },
    "law of partial pressures": {
        "formula": r"$$P_{\text{total}} = \sum_{i} P_i, \qquad P_i = x_i P_{\text{total}}$$",
        "formula_description": (
            r"Dalton's law: total pressure of a gas mixture equals the sum of partial pressures $P_i$. "
            r"Mole fraction $x_i = n_i / n_{\text{total}}$. "
            r"For ideal gases: $P_i V = n_i RT$."
        )
    },
    "law of definite proportions": {
        "formula": r"$$\frac{m_A}{m_B} = \text{constant for compound } AB$$",
        "formula_description": (
            r"Proust's law: a pure chemical compound always contains its elements in a fixed mass ratio. "
            r"Example: water is always $\text{H}_2\text{O}$: "
            r"$m_\text{H} : m_\text{O} = 2\times1.008 : 15.999 \approx 1:8$. "
            "Foundation of stoichiometry and atomic theory."
        )
    },
    "law of multiple proportions": {
        "formula": r"$$\frac{m_{B_1}}{m_{B_2}} = \frac{p}{q} \quad (p,q \in \mathbb{Z}^+, \text{ small})$$",
        "formula_description": (
            r"Dalton's law: when two elements form more than one compound, "
            r"the masses of one element combining with a fixed mass of the other are in a simple integer ratio. "
            r"Example: CO vs CO$_2$ — oxygen ratio is $1:2$."
        )
    },
    "lenz's law": {
        "formula": r"$$\mathcal{E} = -\frac{d\Phi_B}{dt}, \qquad \Phi_B = \int \mathbf{B}\cdot d\mathbf{A}$$",
        "formula_description": (
            r"The induced EMF opposes the change in flux. Negative sign = Lenz's law. "
            r"For a coil of $N$ turns: $\mathcal{E} = -N\dfrac{d\Phi_B}{dt}$. "
            "Energy is conserved — the opposing current dissipates exactly the energy supplied by the agent causing flux change."
        )
    },
}

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

print(f"\nDone. {count} entries enriched.")
