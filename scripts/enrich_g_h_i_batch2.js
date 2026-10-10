const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict = JSON.parse(fs.readFileSync(dictPath, 'utf8'));
console.log('Loaded dictionary.json successfully.');

const updatesG = {
  "gauge pressure": "Pressure measured relative to ambient atmospheric pressure $P_{atm}$:\n\n$$P_{gauge} = P_{abs} - P_{atm}$$\n\nPositive gauge pressure indicates pressure above atmospheric; negative (vacuum) gauge pressure is below. Tyres and blood pressure are measured in gauge pressure. Absolute pressure is always $\\geq 0$.",

  "generating function": "A formal power series that encodes a sequence $\\{a_n\\}$ as its coefficients:\n\n$$G(x) = \\sum_{n=0}^{\\infty} a_n x^n$$\n\nOrdinary generating functions (OGFs) encode sequences directly; exponential generating functions (EGFs) use $a_n/n!$. Used to solve recurrence relations, count combinatorial objects, and derive closed-form expressions.",

  "geometric distribution": "The probability distribution of the number of Bernoulli trials $X$ needed to get the first success (probability $p$):\n\n$$P(X = k) = (1-p)^{k-1}p, \\quad k = 1, 2, 3, \\ldots$$\n\nMean $\\mu = 1/p$, variance $\\sigma^2 = (1-p)/p^2$. The only discrete distribution with the memoryless property: $P(X > m+n \\mid X > m) = P(X > n)$.",

  "geometric sequence": "A sequence in which each term is obtained by multiplying the previous term by a fixed common ratio $r$:\n\n$$a_n = a_1 \\cdot r^{n-1}$$\n\nFor example, $2, 6, 18, 54, \\ldots$ has $r = 3$. The sequence converges to 0 when $|r| < 1$.",

  "geometric series": "The sum of a geometric sequence. For finite $n$ terms:\n\n$$S_n = a_1 \\frac{1 - r^n}{1 - r}, \\quad r \\neq 1$$\n\nFor an infinite geometric series with $|r| < 1$:\n\n$$S_\\infty = \\frac{a_1}{1 - r}$$\n\nDiverges for $|r| \\geq 1$ (unless $r = 1$ trivially). Widely used in finance (annuities, present value).",

  "geosynchronous orbit": "An orbit where the satellite's period exactly equals Earth's rotation period ($T = 86{,}400\\,\\text{s}$). Orbital radius from Earth's centre:\n\n$$r = \\left(\\frac{GM_E T^2}{4\\pi^2}\\right)^{1/3} \\approx 42{,}164\\,\\text{km}$$\n\nA geostationary orbit is a special geosynchronous orbit that is also circular and equatorial — satellite appears fixed in the sky.",

  "gibbs' phase rule": "Gives the degrees of thermodynamic freedom $F$ for a system at equilibrium:\n\n$$F = C - P + 2$$\n\nwhere $C$ is the number of chemical components and $P$ is the number of phases. For water at its triple point: $C=1$, $P=3$, so $F=0$ — a uniquely determined point with no freedom in temperature or pressure.",

  "gibbs-duhem equation": "A fundamental thermodynamic relation constraining changes in chemical potentials $\\mu_i$ of components in a mixture at constant $T$ and $P$:\n\n$$\\sum_i n_i\\,d\\mu_i = 0 \\quad (\\text{const. } T, P)$$\n\nGenerally: $SdT - VdP + \\sum_i n_i d\\mu_i = 0$. Implies that chemical potentials of mixture components are not all independent — a key result for solution thermodynamics.",

  "golden ratio": "The unique positive ratio $\\phi$ satisfying $a/b = (a+b)/a$:\n\n$$\\phi = \\frac{1 + \\sqrt{5}}{2} \\approx 1.61803\\ldots$$\n\nAlgebraic identity: $\\phi^2 = \\phi + 1$. Appears in the Fibonacci sequence ($F_{n+1}/F_n \\to \\phi$), regular pentagons, logarithmic spirals, and art. The reciprocal $1/\\phi = \\phi - 1$.",

  "goldman equation": "Predicts the resting membrane potential $V_m$ of a cell based on ion permeabilities $P$ and concentrations:\n\n$$V_m = \\frac{RT}{F}\\ln\\frac{P_K[\\text{K}^+]_o + P_{Na}[\\text{Na}^+]_o + P_{Cl}[\\text{Cl}^-]_i}{P_K[\\text{K}^+]_i + P_{Na}[\\text{Na}^+]_i + P_{Cl}[\\text{Cl}^-]_o}$$\n\nwhere $R$ is the gas constant, $T$ is absolute temperature, $F$ is Faraday's constant. Generalises the Nernst equation to multiple ions.",

  "gram-schmidt process": "An algorithm for orthonormalising a set of linearly independent vectors $\\{\\mathbf{v}_1, \\ldots, \\mathbf{v}_k\\}$:\n\n$$\\mathbf{u}_j = \\mathbf{v}_j - \\sum_{i=1}^{j-1}\\frac{\\langle\\mathbf{v}_j, \\mathbf{u}_i\\rangle}{\\langle\\mathbf{u}_i, \\mathbf{u}_i\\rangle}\\mathbf{u}_i$$\n\nThen normalise: $\\mathbf{e}_j = \\mathbf{u}_j/\\|\\mathbf{u}_j\\|$. Produces an orthonormal basis. Used in QR decomposition.",

  "grashof number": "A dimensionless number characterising the ratio of buoyancy to viscous forces in natural convection:\n\n$$Gr = \\frac{g\\beta(T_s - T_\\infty)L^3}{\\nu^2}$$\n\nwhere $g$ is gravitational acceleration, $\\beta$ is thermal expansion coefficient, $T_s - T_\\infty$ is temperature difference, $L$ is characteristic length, $\\nu$ is kinematic viscosity. Analogous to Reynolds number for forced convection.",

  "gravitational acceleration": "The acceleration due to gravity on an object near a large mass $M$ at distance $r$:\n\n$$g = \\frac{GM}{r^2}$$\n\nAt Earth's surface: $g \\approx 9.81\\,\\text{m s}^{-2}$. Varies with latitude and altitude. The weight of a mass $m$ is $W = mg$. In free fall, all objects accelerate at $g$ regardless of mass (equivalence principle).",

  "gravitational constant": "The universal constant $G$ in Newton's law of gravitation:\n\n$$G = 6.674 \\times 10^{-11}\\,\\text{N m}^2\\text{kg}^{-2}$$\n\nAppears in $F = Gm_1m_2/r^2$ and $g = GM/r^2$. Difficult to measure precisely; first determined by Cavendish (1798) using a torsion balance. Weakest of the four fundamental forces.",

  "gravitational field": "The region of space around a mass $M$ in which another mass experiences a gravitational force. Field strength (intensity) at distance $r$:\n\n$$\\mathbf{g} = -\\frac{GM}{r^2}\\hat{r}$$\n\nUnits: N kg⁻¹ or m s⁻². The gravitational potential $V = -GM/r$. Gravitational field lines point toward the mass; field strength falls off as $1/r^2$.",

  "gravitational energy": "The energy associated with the gravitational interaction between masses. Gravitational potential energy of mass $m$ at distance $r$ from mass $M$:\n\n$$E_p = -\\frac{GMm}{r}$$\n\nNear Earth's surface: $E_p \\approx mgh$. The binding energy of a system is the energy required to separate all masses to infinity. Total mechanical energy in orbit: $E = -GMm/(2r)$.",

  "gregory's series": "An infinite series expansion for $\\pi/4$, attributed to James Gregory and Leibniz:\n\n$$\\frac{\\pi}{4} = 1 - \\frac{1}{3} + \\frac{1}{5} - \\frac{1}{7} + \\cdots = \\sum_{n=0}^{\\infty}\\frac{(-1)^n}{2n+1}$$\n\nConverges slowly. Derived from $\\arctan(1) = \\pi/4$ and the Taylor series $\\arctan x = \\sum (-1)^n x^{2n+1}/(2n+1)$.",

  "growth rate": "In biology, the rate of increase in size or number of a population. Exponential growth:\n\n$$\\frac{dN}{dt} = rN \\implies N(t) = N_0 e^{rt}$$\n\nwhere $r$ is the intrinsic rate of increase. Logistic growth (with carrying capacity $K$):\n\n$$\\frac{dN}{dt} = rN\\left(1 - \\frac{N}{K}\\right)$$\n\nIn chemistry, the rate of a reaction $r = k[A]^m[B]^n$ (rate law).",

  "gyromagnetic ratio": "The ratio of a particle's magnetic dipole moment $\\mu$ to its angular momentum $L$:\n\n$$\\gamma = \\frac{\\mu}{L} = \\frac{q}{2m} \\cdot g$$\n\nFor a proton: $\\gamma_p = 2.675 \\times 10^8\\,\\text{rad s}^{-1}\\text{T}^{-1}$. Determines the Larmor precession frequency $\\omega_L = \\gamma B$ of a magnetic moment in field $B$. Central to NMR and MRI."
};

const updatesH = {
  "hamilton's principle of least action": "A variational principle stating that the actual path taken by a physical system between two states extremises (usually minimises) the action $S$:\n\n$$S = \\int_{t_1}^{t_2} L(q, \\dot{q}, t)\\,dt$$\n\nwhere $L = T - V$ is the Lagrangian. Leads to the Euler-Lagrange equations: $\\frac{d}{dt}\\frac{\\partial L}{\\partial \\dot{q}} - \\frac{\\partial L}{\\partial q} = 0$.",

  "hawking radiation": "Thermal radiation theoretically emitted by black holes due to quantum effects near the event horizon. Black hole temperature:\n\n$$T_{BH} = \\frac{\\hbar c^3}{8\\pi G M k_B}$$\n\nwhere $M$ is the black hole mass, $k_B$ is Boltzmann's constant, $\\hbar$ is the reduced Planck constant, $G$ is Newton's constant, $c$ is the speed of light. Predicts that black holes slowly evaporate.",

  "heat flux": "The rate of heat energy transfer per unit area perpendicular to the direction of flow:\n\n$$q = -k\\frac{dT}{dx} \\quad \\text{(Fourier's Law, 1D)}$$\n\nUnits: W m⁻². In vector form: $\\mathbf{q} = -k\\nabla T$. The negative sign indicates heat flows from hot to cold regions. Thermal conductivity $k$ (W m⁻¹ K⁻¹) is a material property.",

  "heat of reaction": "The enthalpy change $\\Delta_r H$ associated with a chemical reaction at constant pressure:\n\n$$\\Delta_r H = \\sum \\Delta_f H^\\circ(\\text{products}) - \\sum \\Delta_f H^\\circ(\\text{reactants})$$\n\nExothermic reactions ($\\Delta H < 0$) release heat; endothermic ($\\Delta H > 0$) absorb heat. Measured by calorimetry. Standard enthalpy refers to 298 K, 1 bar conditions.",

  "helmholtz energy": "A thermodynamic potential for systems at constant temperature and volume:\n\n$$A = U - TS$$\n\n$$dA = -SdT - PdV + \\sum_i \\mu_i dn_i$$\n\nA process at constant $T$ and $V$ is spontaneous when $\\Delta A < 0$. Also called Helmholtz free energy. Minimised at equilibrium in canonical (NVT) statistical ensembles.",

  "hilbert transform": "An integral transform relating real and imaginary parts of analytic signals:\n\n$$\\mathcal{H}\\{f\\}(t) = \\frac{1}{\\pi}\\,\\text{P.V.}\\int_{-\\infty}^{\\infty}\\frac{f(\\tau)}{t - \\tau}\\,d\\tau$$\n\nProduces a 90° phase shift at every frequency. Used in signal processing to create analytic signals, compute instantaneous frequency, and build single-sideband modulators.",

  "homologous series": "A family of organic compounds with the same functional group differing by a $-\\text{CH}_2-$ unit. General formula for alkanes:\n\n$$\\text{C}_n\\text{H}_{2n+2}, \\quad n = 1, 2, 3, \\ldots$$\n\nEach member differs in molecular formula by $\\text{CH}_2$ (14 mass units). Physical properties (boiling point, density) change gradually. Alcohols: $\\text{C}_n\\text{H}_{2n+1}\\text{OH}$; carboxylic acids: $\\text{C}_n\\text{H}_{2n+1}\\text{COOH}$.",

  "hubble constant": "The proportionality constant $H_0$ in Hubble's law relating recession velocity $v$ of a galaxy to its distance $d$:\n\n$$v = H_0 d$$\n\nCurrent measurement: $H_0 \\approx 67$–$73\\,\\text{km s}^{-1}\\text{Mpc}^{-1}$ (1 Mpc ≈ 3.09 × 10²² m). Its reciprocal gives an estimate of the age of the universe: $t \\approx 1/H_0 \\approx 14\\,\\text{Gyr}$.",

  "hydrogen spectrum": "The discrete emission/absorption spectrum of hydrogen arising from transitions between quantised energy levels (Bohr model):\n\n$$\\frac{1}{\\lambda} = R_H\\left(\\frac{1}{n_1^2} - \\frac{1}{n_2^2}\\right), \\quad n_2 > n_1$$\n\nwhere $R_H = 1.097 \\times 10^7\\,\\text{m}^{-1}$ is the Rydberg constant. Series: Lyman ($n_1=1$, UV), Balmer ($n_1=2$, visible), Paschen ($n_1=3$, IR).",

  "hypergeometric distribution": "The probability distribution for sampling $k$ successes from a population of $N$ objects containing $K$ successes, without replacement, in $n$ draws:\n\n$$P(X = k) = \\frac{\\binom{K}{k}\\binom{N-K}{n-k}}{\\binom{N}{n}}$$\n\nMean: $\\mu = nK/N$. Variance: $\\sigma^2 = n\\frac{K}{N}\\frac{N-K}{N}\\frac{N-n}{N-1}$. Reduces to binomial when sampling with replacement.",

  "hypergeometric series": "A power series whose successive coefficient ratios are rational functions of the index. The Gauss hypergeometric series:\n\n$$_2F_1(a,b;c;z) = \\sum_{n=0}^{\\infty}\\frac{(a)_n(b)_n}{(c)_n n!}z^n$$\n\nwhere $(a)_n = a(a+1)\\cdots(a+n-1)$ is the Pochhammer symbol. Unifies many special functions: elementary functions, Legendre polynomials, Jacobi polynomials, elliptic integrals.",

  "hydration energy": "The energy released when an ion in the gas phase becomes surrounded by water molecules (hydrated):\n\n$$\\Delta H_{hyd} = \\Delta H_{latt} + \\Delta H_{sol}$$\n\nBorn–Landé approximation relates $\\Delta H_{hyd}$ to ionic charge $z$ and radius $r$:\n\n$$\\Delta H_{hyd} \\propto -\\frac{z^2}{r}$$\n\nHighly charged, small ions (e.g. $\\text{Al}^{3+}$) have very large (negative) hydration energies.",

  "hydroelectric power": "Electrical power generated from the potential energy of water at height $h$ flowing at mass flow rate $\\dot{m}$:\n\n$$P = \\eta \\dot{m} g h = \\eta \\rho Q g h$$\n\nwhere $\\eta$ is efficiency, $\\rho$ is water density, $Q$ is volumetric flow rate (m³/s), $g$ is gravitational acceleration, $h$ is head (height difference). Typical large hydroelectric plant efficiency: 85–95%.",

  "hyperbolic orbit": "A trajectory with eccentricity $e > 1$ — an object with total mechanical energy $E > 0$ (unbound). Hyperbolic excess velocity $v_\\infty$:\n\n$$v_\\infty = \\sqrt{\\frac{2E}{m}} = \\sqrt{v^2 - v_{esc}^2}$$\n\nwhere $v_{esc} = \\sqrt{2GM/r}$ is escape velocity. Semi-major axis: $a = -GM/v_\\infty^2$ (negative for hyperbola). Used in gravity-assist (slingshot) manoeuvres.",

  "highest common factor, hcf": "The largest positive integer that divides each of two or more integers without remainder. For integers $a$ and $b$:\n\n$$\\text{HCF}(a,b) = \\text{HCF}(b, a \\bmod b)$$\n\n(Euclidean algorithm). Relationship to LCM: $\\text{HCF}(a,b) \\times \\text{LCM}(a,b) = |ab|$. Also written $\\gcd(a,b)$ (greatest common divisor)."
};

const updatesI = {
  "instantaneous acceleration": "The rate of change of velocity at a specific instant:\n\n$$\\mathbf{a} = \\lim_{\\Delta t \\to 0}\\frac{\\Delta\\mathbf{v}}{\\Delta t} = \\frac{d\\mathbf{v}}{dt} = \\frac{d^2\\mathbf{x}}{dt^2}$$\n\nThe slope of the velocity-time graph at a given point. Contrasted with average acceleration $\\bar{a} = \\Delta v/\\Delta t$ over a finite interval. SI unit: m s⁻².",

  "induced electromotive force": "An EMF generated in a conductor by a changing magnetic flux (Faraday's law of electromagnetic induction):\n\n$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt}, \\quad \\Phi_B = \\int \\mathbf{B}\\cdot d\\mathbf{A}$$\n\nFor a coil of $N$ turns: $\\mathcal{E} = -N\\,d\\Phi/dt$. The negative sign (Lenz's law) means the induced EMF opposes the change causing it.",

  "induced current": "An electric current generated in a conductor when placed in a changing magnetic field. Magnitude from Faraday's law:\n\n$$I_{ind} = \\frac{\\mathcal{E}}{R} = -\\frac{1}{R}\\frac{d\\Phi_B}{dt}$$\n\nwhere $R$ is the circuit resistance. Direction given by Lenz's law: the induced current creates a magnetic field that opposes the change in flux. Basis of electric generators and transformers.",

  "inertial force": "A fictitious force that appears in non-inertial (accelerating) reference frames to satisfy Newton's second law:\n\n$$\\mathbf{F}_{inertial} = -m\\mathbf{a}_{frame}$$\n\nExamples: centrifugal force $F_c = m\\omega^2 r$ (rotating frame), Coriolis force $\\mathbf{F}_{Cor} = -2m\\boldsymbol{\\omega}\\times\\mathbf{v}$. Not real forces — arise from the acceleration of the reference frame itself.",

  "integral": "The fundamental operation of integration, computing the antiderivative or area under a curve. Definite integral:\n\n$$\\int_a^b f(x)\\,dx = F(b) - F(a)$$\n\nwhere $F'(x) = f(x)$ (Fundamental Theorem of Calculus). Indefinite integral: $\\int f(x)\\,dx = F(x) + C$. Standard results: $\\int x^n dx = x^{n+1}/(n+1)+C$, $\\int e^x dx = e^x + C$.",

  "integral equation": "An equation in which the unknown function $f$ appears inside an integral. Fredholm equation of the second kind:\n\n$$f(x) = g(x) + \\lambda\\int_a^b K(x,t)f(t)\\,dt$$\n\nwhere $K(x,t)$ is the kernel and $g(x)$ is given. Volterra equations have a variable upper limit. Arise in physics, engineering, and probability.",

  "integral transform": "A linear operator mapping a function $f(t)$ to another $F(s)$ by integration against a kernel $K(s,t)$:\n\n$$F(s) = \\int_{-\\infty}^{\\infty} K(s,t)\\,f(t)\\,dt$$\n\nKey examples: Laplace transform $K = e^{-st}$ (solving ODEs); Fourier transform $K = e^{-i\\omega t}$ (frequency analysis); Mellin transform $K = t^{s-1}$ (multiplicative structure).",

  "integrated rate equation": "The concentration-time relationship obtained by integrating the rate law for a reaction. For first-order:\n\n$$\\ln[A] = \\ln[A]_0 - kt \\iff [A] = [A]_0 e^{-kt}$$\n\nFor second-order (one reactant): $\\frac{1}{[A]} = \\frac{1}{[A]_0} + kt$. For zero-order: $[A] = [A]_0 - kt$. Used to determine rate constants and half-lives from experimental data.",

  "inverse normal distribution": "The quantile function of the standard normal distribution — gives the $z$-score corresponding to a given cumulative probability $p$:\n\n$$z = \\Phi^{-1}(p)$$\n\nwhere $\\Phi$ is the standard normal CDF. Used to find critical values for hypothesis tests and confidence intervals. Example: $\\Phi^{-1}(0.975) \\approx 1.96$ (95% two-tailed CI).",

  "irrational number": "A real number that cannot be expressed as a ratio $p/q$ of two integers ($p, q \\in \\mathbb{Z}$, $q \\neq 0$). Characterised by a non-terminating, non-repeating decimal expansion:\n\n$$\\sqrt{2} = 1.41421356\\ldots, \\quad \\pi = 3.14159265\\ldots, \\quad e = 2.71828\\ldots$$\n\nProof that $\\sqrt{2}$ is irrational: assume $\\sqrt{2} = p/q$ in lowest terms; then $p^2 = 2q^2$ forces $p$ and $q$ both even — contradiction.",

  "ionisation/ionization energy": "The minimum energy required to remove one mole of electrons from one mole of gaseous atoms or ions:\n\n$$\\text{X}(g) \\to \\text{X}^+(g) + e^-, \\quad \\Delta H = IE_1$$\n\nFor hydrogen-like atoms (Bohr model): $IE = 13.6\\,\\text{eV} \\cdot Z^2/n^2$. First IE increases across a period (increasing nuclear charge); decreases down a group (increasing distance/shielding).",

  "ionisation/ionization constant": "The equilibrium constant for the ionisation of a weak acid $\\text{HA}$:\n\n$$K_a = \\frac{[\\text{H}^+][\\text{A}^-]}{[\\text{HA}]}$$\n\nStrong acids: $K_a \\gg 1$ (effectively complete ionisation). Weak acids: $K_a \\ll 1$. $\\text{p}K_a = -\\log_{10}K_a$. Analogously, $K_b$ for weak bases: $K_a \\times K_b = K_w = 1.0 \\times 10^{-14}$ at 25°C.",

  "intrinsic rate of increase": "The maximum per-capita population growth rate $r$ under ideal conditions (unlimited resources):\n\n$$r = b - d \\quad (\\text{birth rate minus death rate})$$\n\n$$N(t) = N_0 e^{rt}$$\n\nAlso written $r_{max}$ or $r_m$. Positive $r$ implies exponential growth; negative $r$ implies decline. Related to the finite rate of increase $\\lambda = e^r$ (multiplication per unit time).",

  "isotopic enrichment factor": "A measure of the degree of isotopic fractionation between two substances or phases, expressed as:\n\n$$\\varepsilon = \\left(\\frac{^hR_{product}}{^hR_{reactant}} - 1\\right) \\times 1000\\,\\text{‰}$$\n\nwhere $^hR$ is the ratio of the heavy to light isotope. Related to the fractionation factor $\\alpha$: $\\varepsilon \\approx (\\alpha - 1) \\times 1000$ for small fractionations. Used in stable isotope geochemistry.",

  "iterated series": "A double series summed by iterating two single summations:\n\n$$\\sum_{m=1}^{\\infty}\\sum_{n=1}^{\\infty} a_{mn}$$\n\nConvergence is not guaranteed just because both iterated sums exist and are finite — they may give different values. Fubini's theorem guarantees the double sum equals both iterated sums when $\\sum|a_{mn}|$ converges (absolute convergence).",

  "inhibitory postsynaptic potential": "A hyperpolarisation of the postsynaptic membrane that decreases the probability of an action potential. The membrane potential moves away from threshold:\n\n$$V_m \\to V_m - \\Delta V$$\n\nTypically caused by $\\text{Cl}^-$ influx (GABA-A receptors, $E_{Cl} \\approx -70\\,\\text{mV}$) or $\\text{K}^+$ efflux. Threshold typically around $-55\\,\\text{mV}$; resting potential around $-70\\,\\text{mV}$ for most neurons.",

  "internal energy density": "Energy stored per unit volume of a system:\n\n$$u = \\frac{U}{V}$$\n\nFor an ideal monatomic gas: $u = \\frac{3}{2}nRT/V = \\frac{3}{2}P$. For electromagnetic fields: $u = \\frac{1}{2}(\\varepsilon_0 E^2 + B^2/\\mu_0)$. For elastic materials: $u = \\frac{1}{2}\\sigma\\varepsilon$ (stress × strain).",

  "ion-dipole force": "An electrostatic attractive force between an ion and the partial charge of a polar molecule. Potential energy:\n\n$$U = -\\frac{qp\\cos\\theta}{4\\pi\\varepsilon_0 r^2}$$\n\nwhere $q$ is the ionic charge, $p$ is the molecular dipole moment, $\\theta$ is the angle between dipole and ion-dipole vector, $r$ is the separation distance. Stronger than dipole-dipole; responsible for ion hydration.",

  "ionic half equation": "Half-equations representing either the oxidation or reduction half of a redox reaction. For copper deposition:\n\n$$\\text{Cu}^{2+}(aq) + 2e^- \\to \\text{Cu}(s) \\quad (\\text{reduction})$$\n\nFor zinc dissolution: $\\text{Zn}(s) \\to \\text{Zn}^{2+}(aq) + 2e^-$ (oxidation). Must balance atoms AND charge. Full equation obtained by combining half-equations so electrons cancel.",

  "inverse ratio": "If $a:b = m:n$, the inverse ratio is $b:a = n:m$. For continuously varying quantities, inverse proportion:\n\n$$y \\propto \\frac{1}{x} \\iff xy = k \\text{ (constant)}$$\n\nGraphically: a rectangular hyperbola. Example: Boyle's Law — pressure and volume at constant temperature are in inverse proportion: $PV = nRT = \\text{const}$.",

  "isobaric mass-change determination": "Thermogravimetric analysis at constant pressure, tracking mass change $\\Delta m$ as temperature varies:\n\n$$\\alpha(T) = \\frac{m_0 - m(T)}{m_0 - m_f}$$\n\nwhere $\\alpha$ is the conversion fraction, $m_0$ is initial mass, $m(T)$ is mass at temperature $T$, and $m_f$ is final mass. Used in reaction kinetics and decomposition studies."
};

function findEntry(section, word) {
  const entries = dict[section];
  if (!entries) return null;
  return entries.find(e => e.word.toLowerCase() === word.toLowerCase()) || null;
}

let countG = 0, countH = 0, countI = 0;

for (const [word, def] of Object.entries(updatesG)) {
  const entry = findEntry('G', word);
  if (entry && !entry.definition.includes('$')) { entry.definition = def; countG++; }
}
for (const [word, def] of Object.entries(updatesH)) {
  const entry = findEntry('H', word);
  if (entry && !entry.definition.includes('$')) { entry.definition = def; countH++; }
}
for (const [word, def] of Object.entries(updatesI)) {
  const entry = findEntry('I', word);
  if (entry && !entry.definition.includes('$')) { entry.definition = def; countI++; }
}

console.log(`Updated Section G: ${countG} formulas enriched.`);
console.log(`Updated Section H: ${countH} formulas enriched.`);
console.log(`Updated Section I: ${countI} formulas enriched.`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log('Saved dictionary.json successfully.');
