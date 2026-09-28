import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

M = data['M']

enrichments = {
    "mendeleev's periodic law": {
        "formula": r"$$Z \uparrow \;\Rightarrow\; \text{properties periodic}, \qquad E_n = -\frac{Z^2 \cdot 13.6\ \mathrm{eV}}{n^2}$$",
        "formula_description": (
            r"Properties of elements recur periodically with increasing atomic number $Z$. "
            r"Hydrogen-like ionisation energy for period trends: $E_n = -Z^2 \cdot 13.6/n^2\ \mathrm{eV}$. "
            "Modern form: properties are periodic functions of $Z$ (not atomic mass as Mendeleev originally stated)."
        )
    },
    "melting point": {
        "formula": r"$$\Delta T_f = K_f \cdot b \cdot i, \qquad K_f = \frac{R T_f^{*2} M_{\text{solvent}}}{1000\,\Delta H_f}$$",
        "formula_description": (
            r"Freezing point depression: $\Delta T_f$ = depression, $K_f$ = cryoscopic constant, "
            r"$b$ = molality (mol$\cdot$kg$^{-1}$), $i$ = van't Hoff factor. "
            r"For water: $K_f = 1.86\ \mathrm{K\cdot kg\cdot mol^{-1}}$. "
            r"At melting point: $\Delta G_{\text{fus}} = 0$, so $T_m = \Delta H_f / \Delta S_f$."
        )
    },
    "markov chain": {
        "formula": r"$$P(X_{n+1}=j \mid X_n=i,\,X_{n-1},\ldots) = P(X_{n+1}=j \mid X_n=i) = p_{ij}$$",
        "formula_description": (
            r"Memoryless (Markov) property: next state depends only on current state. "
            r"Transition matrix $\mathbf{P}$: rows sum to 1, $p_{ij} \ge 0$. "
            r"Stationary distribution $\boldsymbol{\pi}$: $\boldsymbol{\pi}\mathbf{P} = \boldsymbol{\pi}$, $\sum_i \pi_i = 1$. "
            r"Chapman-Kolmogorov: $p_{ij}^{(m+n)} = \sum_k p_{ik}^{(m)}p_{kj}^{(n)}$."
        )
    },
    "moseley's law": {
        "formula": r"$$\sqrt{f} = a(Z - b), \qquad f = \frac{3cR_\infty}{4}(Z-1)^2 \quad (K_\alpha)$$",
        "formula_description": (
            r"Frequency $f$ of characteristic X-ray emission vs atomic number $Z$. "
            r"$a, b$ = constants depending on spectral series; $R_\infty$ = Rydberg constant. "
            r"$K_\alpha$ line: transition $n=2\to1$; $K_\beta$: $n=3\to1$. "
            "Established atomic number as the true organising principle of the periodic table (Moseley, 1913)."
        )
    },
    "mole fraction": {
        "formula": r"$$x_i = \frac{n_i}{\sum_j n_j}, \qquad \sum_i x_i = 1$$",
        "formula_description": (
            r"Dimensionless; $n_i$ = moles of component $i$. "
            r"Partial pressure: $P_i = x_i P_{\text{total}}$ (Dalton's law). "
            r"Raoult's law: $P_i = x_i P_i^*$ where $P_i^*$ = vapour pressure of pure $i$. "
            r"Related to molarity $c_i$ and molality $b_i$ via solution density."
        )
    },
    "molality": {
        "formula": r"$$b = \frac{n_{\text{solute}}}{m_{\text{solvent}}\ (\mathrm{kg})}, \qquad \Delta T_b = K_b b i$$",
        "formula_description": (
            r"SI unit: mol$\cdot$kg$^{-1}$ (m). Independent of temperature (unlike molarity). "
            r"Boiling point elevation: $K_b(\text{water}) = 0.512\ \mathrm{K\cdot kg\cdot mol^{-1}}$. "
            r"Freezing point depression: $K_f(\text{water}) = 1.86\ \mathrm{K\cdot kg\cdot mol^{-1}}$. "
            r"Van't Hoff factor $i$: number of particles per formula unit in solution."
        )
    },
    "magnetic resonance": {
        "formula": r"$$f_0 = \frac{\gamma B_0}{2\pi}, \qquad \gamma_H = 2.675\times10^8\ \mathrm{rad\,s^{-1}\,T^{-1}}$$",
        "formula_description": (
            r"Larmor frequency for NMR: $f_0$ = resonance frequency, $\gamma$ = gyromagnetic ratio, "
            r"$B_0$ = static field strength. "
            r"At $B_0 = 1\ \mathrm{T}$: $f_0 \approx 42.6\ \mathrm{MHz}$ for $^1\text{H}$. "
            r"Chemical shift: $\delta = \dfrac{f_{\text{sample}} - f_{\text{ref}}}{f_{\text{ref}}}\times10^6\ (\text{ppm})$."
        )
    },
    "manning equation": {
        "formula": r"$$V = \frac{1}{n}\,R_h^{2/3}\,S^{1/2}$$",
        "formula_description": (
            r"Average flow velocity in an open channel; "
            r"$n$ = Manning roughness coefficient, $R_h = A/P$ = hydraulic radius (flow area / wetted perimeter), "
            r"$S$ = channel slope (dimensionless). "
            r"Flow rate: $Q = VA$. Roughness $n \approx 0.012$ (smooth concrete) to $0.04$ (natural streams)."
        )
    },
    "matthiessen's rule": {
        "formula": r"$$\rho = \rho_{\text{phonon}}(T) + \rho_{\text{impurity}}$$",
        "formula_description": (
            r"Total electrical resistivity is the sum of independent scattering contributions: "
            r"lattice vibrations (temperature-dependent) and impurity/defect scattering (temperature-independent). "
            r"$\rho_{\text{phonon}} \propto T$ at high $T$ (Bloch-Grüneisen); $\propto T^5$ at low $T$. "
            r"Fails when scattering mechanisms are coupled."
        )
    },
    "maxwell's demon": {
        "formula": r"$$\Delta S_{\text{universe}} \ge 0, \qquad k_B \ln 2 \text{ per bit erased (Landauer)}$$",
        "formula_description": (
            r"Thought experiment: a demon sorting fast/slow molecules seems to violate 2nd law. "
            r"Resolution (Landauer 1961): memory erasure costs $k_B T \ln 2$ of free energy per bit, "
            r"restoring $\Delta S \ge 0$. "
            r"Links information theory to thermodynamics: $S = -k_B \sum p_i \ln p_i$."
        )
    },
    "maxwell's thermodynamic relations": {
        "formula": (
            r"$$\left(\frac{\partial T}{\partial V}\right)_S = -\left(\frac{\partial P}{\partial S}\right)_V, \quad"
            r"\left(\frac{\partial T}{\partial P}\right)_S = \left(\frac{\partial V}{\partial S}\right)_P$$"
            "\n"
            r"$$\left(\frac{\partial S}{\partial V}\right)_T = \left(\frac{\partial P}{\partial T}\right)_V, \quad"
            r"\left(\frac{\partial S}{\partial P}\right)_T = -\left(\frac{\partial V}{\partial T}\right)_P$$"
        ),
        "formula_description": (
            r"Four relations derived from exactness of $dU$, $dH$, $dA$, $dG$. "
            r"Potentials: $U$ (internal energy), $H = U+PV$ (enthalpy), "
            r"$A = U-TS$ (Helmholtz), $G = H-TS$ (Gibbs). "
            r"Allow unmeasurable quantities ($\partial S/\partial V$) to be expressed in measurable ones."
        )
    },
    "mean value theorem": {
        "formula": r"$$f'(c) = \frac{f(b)-f(a)}{b-a}, \quad c \in (a,b)$$",
        "formula_description": (
            r"There exists at least one $c$ in $(a,b)$ where the instantaneous rate equals the average rate. "
            r"Requires $f$ continuous on $[a,b]$, differentiable on $(a,b)$. "
            r"Cauchy MVT: $\dfrac{f'(c)}{g'(c)} = \dfrac{f(b)-f(a)}{g(b)-g(a)}$. "
            "Foundation of L'Hôpital's rule and Taylor's theorem."
        )
    },
    "michelson-morley experiment": {
        "formula": r"$$\Delta t = \frac{2L}{c}\!\left(\frac{v^2}{c^2}\right), \qquad \Delta\phi = \frac{4\pi L v^2}{\lambda c^2}$$",
        "formula_description": (
            r"Expected fringe shift due to Earth's motion through the ether (never observed). "
            r"Path length difference between arms: $\delta = v^2 L/c^2$. "
            "Null result (1887) disproved the luminiferous ether and led directly to special relativity."
        )
    },
    "mirror formula": {
        "formula": r"$$\frac{1}{f} = \frac{1}{v} + \frac{1}{u}, \qquad m = -\frac{v}{u}, \qquad f = \frac{R}{2}$$",
        "formula_description": (
            r"For spherical mirrors: $f$ = focal length, $v$ = image distance, $u$ = object distance. "
            r"Concave mirror: $f > 0$; convex: $f < 0$. "
            r"$m > 0$: virtual/upright image; $m < 0$: real/inverted image. "
            r"Centre of curvature $C$ is at distance $R = 2f$ from pole."
        )
    },
    "molecular orbital theory": {
        "formula": r"$$\psi_{\pm} = \frac{1}{\sqrt{2(1\pm S)}}\bigl(\phi_A \pm \phi_B\bigr), \qquad S = \int \phi_A^*\phi_B\,dV$$",
        "formula_description": (
            r"Bonding MO ($\psi_+$): constructive interference, lower energy than AOs. "
            r"Antibonding MO ($\psi_-$): node between nuclei, higher energy. "
            r"Bond order $= \dfrac{N_{\text{bonding}} - N_{\text{antibonding}}}{2}$. "
            r"$S$ = overlap integral."
        )
    },
    "möbius function": {
        "formula": r"$$\mu(n) = \begin{cases} 1 & n=1 \\ (-1)^k & n = p_1p_2\cdots p_k \text{ (distinct primes)}\\ 0 & p^2 \mid n \end{cases}$$",
        "formula_description": (
            r"Number-theoretic function. Möbius inversion: if $g(n) = \sum_{d|n}f(d)$ then $f(n)=\sum_{d|n}\mu(d)g(n/d)$. "
            r"Fundamental identity: $\sum_{d|n}\mu(d) = [n=1]$. "
            r"Appears in Riemann hypothesis: $\sum_{n=1}^x \mu(n) = O(\sqrt{x}\log x)$ iff RH true."
        )
    },
    "molar volume": {
        "formula": r"$$V_m = \frac{V}{n} = \frac{RT}{P} \quad (\text{ideal gas}), \qquad V_m^{\text{STP}} = 22.414\ \mathrm{L\,mol^{-1}}$$",
        "formula_description": (
            r"Volume occupied by one mole of substance. At STP ($0°\text{C}$, $101.325\ \mathrm{kPa}$): "
            r"$22.414\ \mathrm{L\,mol^{-1}}$ for ideal gas. "
            r"Van der Waals: $\left(P + \dfrac{a}{V_m^2}\right)(V_m - b) = RT$. "
            r"Critical molar volume: $V_{m,c} = 3b$."
        )
    },
    "malus's law": {
        "formula": r"$$I = I_0 \cos^2\theta$$",
        "formula_description": (
            r"Intensity of plane-polarised light after passing through a polariser at angle $\theta$ to the polarisation axis. "
            r"$I_0$ = initial intensity. At $\theta = 0°$: full transmission. At $\theta = 90°$: complete extinction. "
            "Named after Étienne-Louis Malus (1808)."
        )
    },
    "manning's roughness coefficient": {
        "formula": r"$$Q = \frac{1}{n}\,A\,R_h^{2/3}\,S^{1/2}$$",
        "formula_description": (
            r"Volumetric flow rate $Q$ in open channel; $A$ = cross-sectional area, "
            r"$R_h$ = hydraulic radius, $S$ = slope, $n$ = roughness (Manning's $n$). "
            r"Typical $n$: clean earth $0.022$, gravel $0.029$, natural stream $0.035$–$0.05$."
        )
    },
    "mendel's law of segregation": {
        "formula": r"$$P(\text{Aa}) = \frac{1}{2},\quad P(\text{AA}) = P(\text{aa}) = \frac{1}{4} \quad \text{from Aa}\times\text{Aa}$$",
        "formula_description": (
            r"Each diploid organism carries two alleles for each gene; "
            r"they segregate equally into gametes (probability $\tfrac{1}{2}$ each). "
            r"Punnett square for monohybrid: genotype ratio $1:2:1$, phenotype ratio $3:1$ (dominant:recessive). "
            r"Probability of $k$ dominant offspring from $n$: $P = \binom{n}{k}\left(\tfrac{3}{4}\right)^k\!\left(\tfrac{1}{4}\right)^{n-k}$."
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
