const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

console.log('Loaded dictionary.json successfully.');

const updatesG = {
  "g factor": "The dimensionless quantity relating the magnetic moment of a particle to its angular momentum (spin). For the electron:\n\n$$\\mu = g \\frac{e}{2m_e} S$$\n\nwhere $g \\approx 2.00232$ for an electron (with QED corrections), $e$ is the elementary charge, $m_e$ is the electron mass, and $S$ is the spin angular momentum. Also called the Landé g-factor in atomic physics.",

  "g-force": "Apparent weight experienced per unit mass relative to standard gravitational acceleration $g_0 = 9.80665\\,\\text{m s}^{-2}$:\n\n$$\\text{g-force} = \\frac{a}{g_0}$$\n\nwhere $a$ is the net proper acceleration. A g-force of 1 g corresponds to normal Earth surface weight; sustained exposure above 5 g causes loss of consciousness.",

  "galactic coordinates": "A spherical coordinate system centred on the Sun with the galactic plane as the reference. Galactic longitude $l$ is measured from the galactic centre and galactic latitude $b$ from the galactic plane:\n\n$$b = \\arcsin(\\sin\\delta_0 \\sin\\delta + \\cos\\delta_0 \\cos\\delta \\cos(\\alpha - \\alpha_0))$$\n\nwhere $\\alpha, \\delta$ are right ascension and declination and $\\alpha_0, \\delta_0$ are the coordinates of the galactic north pole.",

  "galvanic cell": "An electrochemical cell that converts chemical energy into electrical energy via spontaneous redox reactions. The electromotive force (EMF) is given by the Nernst equation:\n\n$$E = E^\\circ - \\frac{RT}{nF}\\ln Q$$\n\nwhere $E^\\circ$ is the standard EMF, $R$ is the gas constant, $T$ is temperature, $n$ is the number of electrons transferred, $F$ is Faraday's constant, and $Q$ is the reaction quotient.",

  "gamma decay": "Radioactive decay in which an excited nucleus emits a high-energy photon (gamma ray) without changing $Z$ or $A$:\n\n$$^A_Z\\text{X}^* \\rightarrow {^A_Z\\text{X}} + \\gamma$$\n\nThe energy of the emitted photon equals the energy difference between nuclear states: $E_\\gamma = hf = E_i - E_f$. No change in atomic number or mass number occurs.",

  "gamma distribution": "A continuous probability distribution with shape parameter $k > 0$ and rate parameter $\\lambda > 0$:\n\n$$f(x;k,\\lambda) = \\frac{\\lambda^k x^{k-1} e^{-\\lambda x}}{\\Gamma(k)}, \\quad x > 0$$\n\nMean $\\mu = k/\\lambda$, variance $\\sigma^2 = k/\\lambda^2$. Generalises the exponential distribution (k = 1) and chi-squared distribution.",

  "gamma function": "An extension of the factorial function to complex numbers, defined for $\\text{Re}(z) > 0$ by:\n\n$$\\Gamma(z) = \\int_0^\\infty t^{z-1}e^{-t}\\,dt$$\n\nKey identity: $\\Gamma(n+1) = n!$ for non-negative integers. Also satisfies $\\Gamma(z+1) = z\\,\\Gamma(z)$ and the reflection formula $\\Gamma(z)\\Gamma(1-z) = \\pi/\\sin(\\pi z)$.",

  "gamma radiation": "Electromagnetic radiation emitted from excited atomic nuclei with wavelengths $\\lambda < 10^{-11}\\,\\text{m}$ and photon energies $E > 100\\,\\text{keV}$:\n\n$$E = hf = \\frac{hc}{\\lambda}$$\n\nPenetrates materials far more effectively than alpha or beta radiation. Attenuated exponentially: $I = I_0 e^{-\\mu x}$ where $\\mu$ is the linear attenuation coefficient.",

  "gas constant": "The universal constant $R$ appearing in the ideal gas law:\n\n$$R = 8.314\\,\\text{J mol}^{-1}\\text{K}^{-1}$$\n\nRelates pressure, volume, temperature, and amount of substance: $PV = nRT$. Equals the product of the Boltzmann constant and Avogadro's number: $R = k_B N_A$.",

  "gas laws": "Combined relationships between pressure $P$, volume $V$, and temperature $T$ for an ideal gas:\n\n$$\\frac{P_1 V_1}{T_1} = \\frac{P_2 V_2}{T_2} \\quad \\text{(Combined Gas Law)}$$\n\nBoyle's Law: $P \\propto 1/V$ at constant $T$. Charles's Law: $V \\propto T$ at constant $P$. Gay-Lussac's Law: $P \\propto T$ at constant $V$. Ideal Gas Law: $PV = nRT$.",

  "gauss's law": "One of Maxwell's equations relating electric flux through a closed surface to the enclosed charge:\n\n$$\\oint_S \\mathbf{E} \\cdot d\\mathbf{A} = \\frac{Q_{\\text{enc}}}{\\varepsilon_0}$$\n\nIn differential form: $\\nabla \\cdot \\mathbf{E} = \\rho/\\varepsilon_0$, where $\\rho$ is charge density and $\\varepsilon_0$ is the permittivity of free space.",

  "gauss's law for magnetism": "One of Maxwell's equations, stating that magnetic monopoles do not exist — all field lines form closed loops:\n\n$$\\oint_S \\mathbf{B} \\cdot d\\mathbf{A} = 0$$\n\nIn differential form: $\\nabla \\cdot \\mathbf{B} = 0$. Implies that magnetic flux through any closed surface is always zero.",

  "gaussian distribution": "The normal probability distribution with mean $\\mu$ and standard deviation $\\sigma$:\n\n$$f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}}\\exp\\!\\left(-\\frac{(x-\\mu)^2}{2\\sigma^2}\\right)$$\n\nThe bell curve. ~68% of data falls within $\\pm 1\\sigma$, ~95% within $\\pm 2\\sigma$, ~99.7% within $\\pm 3\\sigma$ of the mean.",

  "gaussian elimination": "A systematic method for solving systems of linear equations by row-reducing an augmented matrix $[A|b]$ to upper-triangular form, then back-substituting:\n\n$$\\begin{pmatrix} a_{11} & a_{12} & \\cdots \\\\ 0 & a_{22} & \\cdots \\\\ 0 & 0 & \\cdots \\end{pmatrix} \\mathbf{x} = \\mathbf{b}$$\n\nComplexity: $O(n^3)$ for an $n \\times n$ system. Forms the basis of LU decomposition.",

  "geostationary orbit": "A circular orbit at altitude $h$ above the equator where the orbital period equals Earth's rotation period ($T = 24\\,\\text{h}$). Radius from Earth's centre:\n\n$$r = \\left(\\frac{GM_E T^2}{4\\pi^2}\\right)^{1/3} \\approx 42{,}164\\,\\text{km}$$\n\nSatellites here appear stationary relative to Earth's surface. Used for weather and communications satellites.",

  "gibbs free energy": "A thermodynamic potential determining spontaneity of reactions at constant temperature and pressure:\n\n$$G = H - TS$$\n\n$$\\Delta G = \\Delta H - T\\Delta S$$\n\nA reaction is spontaneous when $\\Delta G < 0$. At equilibrium $\\Delta G = 0$. Related to the equilibrium constant: $\\Delta G^\\circ = -RT\\ln K$.",

  "gibbs phase rule": "Governs the number of degrees of freedom $F$ in a thermodynamic system:\n\n$$F = C - P + 2$$\n\nwhere $C$ = number of components and $P$ = number of phases. For a single-component system ($C=1$) at a triple point ($P=3$): $F = 0$ (invariant point).",

  "gradient": "The vector operator giving the direction and rate of greatest increase of a scalar field $f$:\n\n$$\\nabla f = \\frac{\\partial f}{\\partial x}\\hat{i} + \\frac{\\partial f}{\\partial y}\\hat{j} + \\frac{\\partial f}{\\partial z}\\hat{k}$$\n\nThe magnitude $|\\nabla f|$ gives the maximum rate of change; the direction is perpendicular to level surfaces of $f$.",

  "graham's law": "States that the rate of effusion (or diffusion) of a gas is inversely proportional to the square root of its molar mass $M$:\n\n$$\\frac{r_1}{r_2} = \\sqrt{\\frac{M_2}{M_1}}$$\n\nLighter gases effuse faster. At the same temperature and pressure, the ratio of rates equals the inverse ratio of the square roots of their molar masses.",

  "gravitational field strength": "The force per unit mass exerted on a test mass in a gravitational field. Near a mass $M$ at distance $r$:\n\n$$g = \\frac{GM}{r^2}$$\n\nUnits: $\\text{N kg}^{-1}$ or $\\text{m s}^{-2}$. At Earth's surface, $g \\approx 9.81\\,\\text{m s}^{-2}$. Equivalent to gravitational acceleration.",

  "gravitational potential": "The work done per unit mass bringing a test mass from infinity to a point in a gravitational field:\n\n$$V_g = -\\frac{GM}{r}$$\n\nNegative because gravity is attractive. The gravitational potential energy of mass $m$ at point $r$ is $E_p = mV_g = -GMm/r$.",

  "gravitational potential energy": "The energy stored by a mass $m$ in a gravitational field at height $h$ (near Earth's surface):\n\n$$E_p = mgh$$\n\nFor large separations from a central mass $M$ at distance $r$:\n\n$$E_p = -\\frac{GMm}{r}$$\n\nThe zero reference point is at infinity. Near Earth's surface, $g = 9.81\\,\\text{m s}^{-2}$ is taken as constant.",

  "green's theorem": "Relates a line integral around a closed curve $C$ to a double integral over the region $D$ it encloses:\n\n$$\\oint_C (P\\,dx + Q\\,dy) = \\iint_D \\left(\\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y}\\right)dA$$\n\nA special case of Stokes' theorem in two dimensions. Used in calculating area and flux in 2D fields.",

  "group velocity": "The velocity at which the envelope of a wave packet (the group of waves) propagates through a medium:\n\n$$v_g = \\frac{d\\omega}{dk}$$\n\nwhere $\\omega$ is angular frequency and $k$ is wavenumber. Equals the phase velocity $v_p = \\omega/k$ only in non-dispersive media. Carries energy and information.",

  "half life": "The time required for half of a radioactive sample to decay:\n\n$$t_{1/2} = \\frac{\\ln 2}{\\lambda} = \\frac{0.693}{\\lambda}$$\n\nwhere $\\lambda$ is the decay constant. The number of remaining nuclei after time $t$: $N(t) = N_0 \\cdot 2^{-t/t_{1/2}} = N_0 e^{-\\lambda t}$.",

  "gyroscopic precession": "The rotation of a spinning gyroscope's axis under an applied torque $\\boldsymbol{\\tau}$, perpendicular to both the spin angular momentum $\\mathbf{L}$ and the torque:\n\n$$\\boldsymbol{\\Omega}_p = \\frac{\\boldsymbol{\\tau}}{L} = \\frac{\\tau}{I\\omega}$$\n\nwhere $I$ is the moment of inertia and $\\omega$ is the spin angular velocity. Precessional rate increases as spin rate decreases."
};

const updatesH = {
  "haber process": "Industrial synthesis of ammonia from nitrogen and hydrogen:\n\n$$\\text{N}_2(g) + 3\\text{H}_2(g) \\rightleftharpoons 2\\text{NH}_3(g) \\quad \\Delta H = -92\\,\\text{kJ mol}^{-1}$$\n\nConditions: iron catalyst, 400–500°C, 150–300 atm pressure. Yield is a compromise between thermodynamic favourability (low $T$) and kinetic feasibility (high $T$). Basis of nitrogen-based fertiliser production.",

  "hadamard inequality": "An upper bound on the absolute value of a matrix determinant in terms of its column (or row) vectors $\\mathbf{v}_1, \\ldots, \\mathbf{v}_n$:\n\n$$|\\det A| \\leq \\prod_{j=1}^{n}\\|\\mathbf{v}_j\\|$$\n\nEquality holds if and only if the columns are mutually orthogonal. Provides geometric intuition: the determinant (volume of parallelepiped) is maximised when column vectors are orthogonal.",

  "half-life": "The time required for half of a radioactive sample to decay, or for a reactant concentration to fall to half its initial value:\n\n$$t_{1/2} = \\frac{\\ln 2}{\\lambda} \\approx \\frac{0.693}{\\lambda}$$\n\nFor a first-order reaction: $t_{1/2} = \\ln 2 / k$ (independent of initial concentration). For a second-order reaction: $t_{1/2} = 1/(k[A]_0)$.",

  "harmonic motion": "Oscillatory motion described by a sinusoidal function of time:\n\n$$x(t) = A\\cos(\\omega t + \\phi)$$\n\nwhere $A$ is amplitude, $\\omega = 2\\pi f$ is angular frequency, and $\\phi$ is the phase. The restoring force obeys Hooke's law: $F = -kx$. Period $T = 2\\pi/\\omega = 2\\pi\\sqrt{m/k}$.",

  "harmonic oscillator": "A system experiencing a restoring force proportional to displacement ($F = -kx$), producing simple harmonic motion. Quantum mechanical energy levels:\n\n$$E_n = \\left(n + \\frac{1}{2}\\right)\\hbar\\omega, \\quad n = 0, 1, 2, \\ldots$$\n\nClassical: $\\omega = \\sqrt{k/m}$. The zero-point energy $E_0 = \\hbar\\omega/2$ is a purely quantum effect.",

  "harmonic series": "The divergent infinite series:\n\n$$\\sum_{n=1}^{\\infty}\\frac{1}{n} = 1 + \\frac{1}{2} + \\frac{1}{3} + \\frac{1}{4} + \\cdots = \\infty$$\n\nPartial sums grow as $H_n \\approx \\ln n + \\gamma$ where $\\gamma \\approx 0.5772$ is the Euler–Mascheroni constant. Divergence was first proven by Nicole Oresme (~1350).",

  "heat capacity": "The amount of heat energy $Q$ required to raise the temperature of a substance by one kelvin:\n\n$$C = \\frac{dQ}{dT}$$\n\nSpecific heat capacity: $c = C/m$ (per unit mass). Molar heat capacity: $C_m = C/n$ (per mole). At constant pressure: $C_p$; at constant volume: $C_v$. For ideal gases: $C_p - C_v = R$.",

  "heat equation": "A partial differential equation describing how heat diffuses through a medium over time:\n\n$$\\frac{\\partial u}{\\partial t} = \\alpha \\nabla^2 u$$\n\nIn one dimension: $\\partial u/\\partial t = \\alpha\\,\\partial^2 u/\\partial x^2$, where $u(x,t)$ is temperature and $\\alpha = k/(\\rho c_p)$ is thermal diffusivity ($k$ = thermal conductivity, $\\rho$ = density, $c_p$ = specific heat).",

  "heat of combustion": "The enthalpy change when one mole of a substance undergoes complete combustion under standard conditions:\n\n$$\\Delta_c H^\\circ = \\sum \\Delta_f H^\\circ(\\text{products}) - \\sum \\Delta_f H^\\circ(\\text{reactants})$$\n\nMeasured by bomb calorimetry. Example for methane: $\\text{CH}_4 + 2\\text{O}_2 \\to \\text{CO}_2 + 2\\text{H}_2\\text{O}$, $\\Delta H = -890\\,\\text{kJ mol}^{-1}$.",

  "heat of formation": "Standard enthalpy of formation $\\Delta_f H^\\circ$: the enthalpy change when one mole of a compound is formed from its elements in their standard states at 298 K and 1 bar:\n\n$$\\Delta_r H^\\circ = \\sum \\Delta_f H^\\circ(\\text{products}) - \\sum \\Delta_f H^\\circ(\\text{reactants})$$\n\n(Hess's Law). By convention, $\\Delta_f H^\\circ$ of any element in its standard state = 0.",

  "heisenberg uncertainty principle": "A fundamental quantum limit on the precision with which conjugate variables can be simultaneously known:\n\n$$\\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}$$\n\nFor energy and time: $\\Delta E \\cdot \\Delta t \\geq \\hbar/2$. Where $\\hbar = h/(2\\pi)$ is the reduced Planck constant. Not a measurement limitation but a fundamental property of quantum systems.",

  "henderson-hasselbalch equation": "Relates the pH of a buffer solution to the $\\text{p}K_a$ of the weak acid and the concentration ratio of conjugate base to acid:\n\n$$\\text{pH} = \\text{p}K_a + \\log\\frac{[\\text{A}^-]}{[\\text{HA}]}$$\n\nUsed to prepare buffers at desired pH values. Maximum buffering capacity occurs when $[\\text{A}^-] = [\\text{HA}]$ (i.e. pH = p$K_a$).",

  "henry's law": "The amount of gas dissolved in a liquid is proportional to its partial pressure above the liquid:\n\n$$c = k_H \\cdot p$$\n\nwhere $c$ is the dissolved gas concentration, $p$ is the partial pressure, and $k_H$ is Henry's law constant (temperature-dependent). Explains carbonation of beverages and gas exchange in lungs.",

  "heron's formula": "Computes the area $A$ of a triangle with sides $a$, $b$, $c$ and semi-perimeter $s = (a+b+c)/2$:\n\n$$A = \\sqrt{s(s-a)(s-b)(s-c)}$$\n\nRequires no knowledge of angles. Equivalent to $A = \\frac{1}{2}ab\\sin C$. Generalises to cyclic polygons via Brahmagupta's formula.",

  "hertz": "The SI unit of frequency, equal to one cycle per second:\n\n$$f = \\frac{1}{T} \\quad (\\text{Hz} = \\text{s}^{-1})$$\n\nRelated to angular frequency by $\\omega = 2\\pi f$. Named after Heinrich Hertz, who experimentally confirmed Maxwell's prediction of electromagnetic waves. Used to measure vibrations, waves, and processor clock speeds.",

  "hooke's law": "The restoring force exerted by a spring is proportional to its extension $x$ from equilibrium:\n\n$$F = -kx$$\n\nwhere $k$ is the spring constant (stiffness, units N/m). Holds within the elastic limit. Leads directly to simple harmonic motion when applied to mass-spring systems: $\\omega = \\sqrt{k/m}$.",

  "huygens' principle": "Every point on a wavefront acts as a secondary source of spherical wavelets. The new wavefront is the envelope of these wavelets:\n\n$$\\text{New wavefront} = \\bigcup \\text{secondary wavelets at time }\\Delta t$$\n\nExplains diffraction, refraction (Snell's law follows), and interference. The mathematical form is expressed via the Kirchhoff diffraction integral.",

  "hydrostatic pressure": "The pressure exerted by a static fluid at depth $h$ below the surface:\n\n$$P = P_0 + \\rho g h$$\n\nwhere $P_0$ is atmospheric pressure, $\\rho$ is fluid density, $g$ is gravitational acceleration, and $h$ is depth. Acts equally in all directions (Pascal's principle). Basis of hydraulic systems.",

  "hyperbola": "A conic section defined as the locus of points where the difference of distances from two foci $F_1$ and $F_2$ is constant:\n\n$$|PF_1 - PF_2| = 2a$$\n\nStandard form: $\\dfrac{x^2}{a^2} - \\dfrac{y^2}{b^2} = 1$ where $c^2 = a^2 + b^2$. Asymptotes: $y = \\pm (b/a)x$. Eccentricity $e = c/a > 1$.",

  "hyperbolic functions": "Analogues of trigonometric functions defined via exponentials:\n\n$$\\sinh x = \\frac{e^x - e^{-x}}{2}, \\quad \\cosh x = \\frac{e^x + e^{-x}}{2}, \\quad \\tanh x = \\frac{\\sinh x}{\\cosh x}$$\n\nIdentity: $\\cosh^2 x - \\sinh^2 x = 1$. Arise in solutions to differential equations and describe the shape of a hanging cable (catenary).",

  "hypothesis testing": "Statistical procedure to decide between a null hypothesis $H_0$ and alternative $H_1$ based on sample data:\n\n$$z = \\frac{\\bar{X} - \\mu_0}{\\sigma/\\sqrt{n}}$$\n\nReject $H_0$ if the test statistic falls in the critical region (p-value $< \\alpha$). Type I error: rejecting a true $H_0$ (probability $\\alpha$). Type II error: failing to reject a false $H_0$ (probability $\\beta$).",

  "ideal gas law": "The fundamental equation of state combining Boyle's, Charles's, and Avogadro's laws:\n\n$$PV = nRT$$\n\nwhere $P$ is pressure (Pa), $V$ is volume (m³), $n$ is moles, $R = 8.314\\,\\text{J mol}^{-1}\\text{K}^{-1}$, and $T$ is absolute temperature (K). Assumes point particles with no intermolecular forces.",

  "impulse": "The change in momentum of an object produced by a force acting over a time interval:\n\n$$\\mathbf{J} = \\int_{t_1}^{t_2} \\mathbf{F}\\,dt = \\Delta \\mathbf{p} = m\\mathbf{v}_f - m\\mathbf{v}_i$$\n\nFor a constant force: $J = F \\Delta t$. Units: N·s = kg·m/s. The impulse-momentum theorem is a direct consequence of Newton's second law.",

  "index of refraction": "The ratio of the speed of light in a vacuum $c$ to its speed in a medium $v$:\n\n$$n = \\frac{c}{v}$$\n\nDetermines the degree of bending at an interface (Snell's law): $n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2$. For glass, $n \\approx 1.5$; for diamond, $n \\approx 2.42$.",

  "inductance": "The property of a conductor by which a change in current induces an EMF. Self-inductance $L$:\n\n$$\\mathcal{E} = -L\\frac{dI}{dt}$$\n\nFor a solenoid: $L = \\mu_0 N^2 A / \\ell$. Energy stored: $U = \\frac{1}{2}LI^2$. Mutual inductance $M$ between two coils: $\\mathcal{E}_2 = -M\\,dI_1/dt$.",

  "integral calculus": "Branch of calculus dealing with the accumulation of quantities. The definite integral of $f(x)$ from $a$ to $b$:\n\n$$\\int_a^b f(x)\\,dx = \\lim_{n\\to\\infty}\\sum_{i=1}^n f(x_i)\\Delta x$$\n\nBy the Fundamental Theorem of Calculus: $\\int_a^b f(x)\\,dx = F(b) - F(a)$ where $F' = f$. Computes areas, volumes, and accumulated quantities."
};

const updatesI = {
  "ideal gas": "A theoretical gas in which molecules occupy negligible volume and exert no intermolecular forces. Obeys:\n\n$$PV = nRT$$\n\nwhere $P$ = pressure, $V$ = volume, $n$ = moles of gas, $R = 8.314\\,\\text{J mol}^{-1}\\text{K}^{-1}$, $T$ = absolute temperature. Real gases deviate from ideal behaviour at high pressures and low temperatures (van der Waals equation).",

  "impedance": "The total opposition to alternating current flow in a circuit, combining resistance $R$ and reactance $X$:\n\n$$Z = \\sqrt{R^2 + X^2}, \\quad \\text{or in complex form: } Z = R + jX$$\n\nFor capacitive reactance: $X_C = 1/(\\omega C)$. For inductive reactance: $X_L = \\omega L$. Ohm's law in AC circuits: $V = IZ$. Units: ohms ($\\Omega$).",

  "impulse-momentum theorem": "The net impulse applied to an object equals its change in momentum:\n\n$$\\mathbf{J} = \\Delta\\mathbf{p} = m\\mathbf{v}_f - m\\mathbf{v}_i$$\n\nFor constant force $F$ over time $\\Delta t$: $J = F\\Delta t$. Derived from Newton's second law integrated over time. Explains why airbags (longer collision time) reduce force in crashes.",

  "induced emf": "An electromotive force generated by a changing magnetic flux through a circuit (Faraday's law):\n\n$$\\mathcal{E} = -\\frac{d\\Phi_B}{dt} = -N\\frac{d\\Phi}{dt}$$\n\nwhere $\\Phi_B = B A \\cos\\theta$ is magnetic flux, $N$ is number of turns. The negative sign (Lenz's law) indicates the induced EMF opposes the change in flux.",

  "infinite series": "The sum of infinitely many terms of a sequence $\\{a_n\\}$:\n\n$$S = \\sum_{n=1}^{\\infty} a_n = \\lim_{N\\to\\infty}\\sum_{n=1}^N a_n$$\n\nConverges if the limit exists and is finite. Geometric series: $\\sum_{n=0}^{\\infty} ar^n = a/(1-r)$ for $|r| < 1$. Convergence tested by ratio, root, integral, or comparison tests.",

  "information entropy": "A measure of uncertainty or information content in a probability distribution (Shannon entropy):\n\n$$H = -\\sum_{i} p_i \\log_2 p_i \\quad \\text{(bits)}$$\n\nFor a uniform distribution of $n$ equally likely outcomes: $H = \\log_2 n$. Maximum entropy means maximum uncertainty. Foundation of information theory, data compression, and cryptography.",

  "instantaneous velocity": "The rate of change of position at a specific instant in time — the derivative of displacement:\n\n$$v = \\lim_{\\Delta t \\to 0}\\frac{\\Delta x}{\\Delta t} = \\frac{dx}{dt}$$\n\nContrasted with average velocity $\\bar{v} = \\Delta x / \\Delta t$. Represents the slope of the position-time graph at a given point.",

  "integration by parts": "A technique for integrating products of functions, derived from the product rule:\n\n$$\\int u\\,dv = uv - \\int v\\,du$$\n\nChoose $u$ and $dv$ using the LIATE rule (Logarithmic, Inverse trig, Algebraic, Trig, Exponential). Example: $\\int x e^x\\,dx = xe^x - e^x + C$.",

  "interference": "The superposition of two or more waves leading to constructive or destructive combinations:\n\n$$\\text{Constructive: } \\Delta = m\\lambda \\quad (m = 0, \\pm1, \\pm2, \\ldots)$$\n$$\\text{Destructive: } \\Delta = (m + \\tfrac{1}{2})\\lambda$$\n\nwhere $\\Delta$ is path difference. Young's double-slit fringe spacing: $y = \\lambda D/d$, where $D$ is screen distance and $d$ is slit separation.",

  "internal energy": "The total microscopic energy of a system — kinetic energy of molecules plus potential energy of molecular interactions:\n\n$$\\Delta U = Q - W$$\n\n(First Law of Thermodynamics), where $Q$ is heat added to the system and $W$ is work done by the system. For an ideal monatomic gas: $U = \\frac{3}{2}nRT$.",

  "inverse square law": "Physical laws where a quantity decreases proportionally to the square of the distance from the source:\n\n$$I \\propto \\frac{1}{r^2}$$\n\nExamples: gravitational force $F = Gm_1m_2/r^2$; Coulomb's law $F = kq_1q_2/r^2$; light intensity $I = P/(4\\pi r^2)$. Arises from the spreading of energy/force over a spherical surface area.",

  "ion product of water": "The equilibrium constant for the autoionisation of water:\n\n$$\\text{H}_2\\text{O}(l) \\rightleftharpoons \\text{H}^+(aq) + \\text{OH}^-(aq)$$\n\n$$K_w = [\\text{H}^+][\\text{OH}^-] = 1.0 \\times 10^{-14} \\text{ at } 25^\\circ\\text{C}$$\n\n$\\text{pH} + \\text{pOH} = 14$ at 25°C. $K_w$ increases with temperature — water autoionises more at higher temperatures.",

  "ionisation energy": "The minimum energy required to remove an electron from an atom or ion in its ground state in the gas phase:\n\n$$\\text{X}(g) \\to \\text{X}^+(g) + e^-$$\n\n$$IE = -E_n = \\frac{Z^2 \\cdot 13.6\\,\\text{eV}}{n^2}$$\n\nfor hydrogen-like atoms (Bohr model), where $Z$ = nuclear charge, $n$ = principal quantum number. Increases across a period; decreases down a group.",

  "isentropic process": "A reversible adiabatic process in which entropy remains constant ($\\Delta S = 0$). For an ideal gas:\n\n$$PV^\\gamma = \\text{constant}, \\quad TV^{\\gamma-1} = \\text{constant}, \\quad TP^{(1-\\gamma)/\\gamma} = \\text{constant}$$\n\nwhere $\\gamma = C_p/C_v$ is the adiabatic index. Describes processes in compressors, turbines, and nozzles.",

  "isothermal process": "A thermodynamic process at constant temperature ($\\Delta T = 0$). For an ideal gas:\n\n$$PV = nRT = \\text{constant}$$\n\nWork done by the gas: $W = nRT\\ln(V_f/V_i) = nRT\\ln(P_i/P_f)$. On a $PV$ diagram, an isothermal process follows a hyperbola. Internal energy change $\\Delta U = 0$ for an ideal gas.",

  "iteration": "A method for solving equations by repeatedly applying a formula to successive approximations. Newton's method:\n\n$$x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}$$\n\nConverges quadratically to a root of $f(x) = 0$ near the initial guess. The fixed-point iteration $x_{n+1} = g(x_n)$ converges when $|g'(x)| < 1$ near the solution.",

  "iterated integral": "A double (or multiple) integral computed by successive single integrations:\n\n$$\\iint_R f(x,y)\\,dA = \\int_a^b\\left(\\int_c^d f(x,y)\\,dy\\right)dx$$\n\nFubini's theorem guarantees the order of integration can be exchanged when $f$ is continuous on $R$. Used to compute volumes, masses, and moments of 2D and 3D regions.",

  "interval estimate": "A range of values $[\\hat{\\theta}_L, \\hat{\\theta}_U]$ likely to contain the true population parameter, characterised by confidence level $1-\\alpha$:\n\n$$\\bar{x} \\pm z_{\\alpha/2}\\frac{\\sigma}{\\sqrt{n}} \\quad \\text{(confidence interval for mean)}$$\n\nA 95% CI means that in repeated sampling, 95% of such intervals will contain the true parameter. Wider intervals give higher confidence but less precision.",

  "intrinsic semi-conductor": "A pure semiconductor in which charge carriers are generated thermally. Carrier concentration $n_i$:\n\n$$n_i = \\sqrt{N_c N_v}\\exp\\!\\left(-\\frac{E_g}{2k_BT}\\right)$$\n\nwhere $N_c$, $N_v$ are effective densities of states in the conduction and valence bands, $E_g$ is the band gap, $k_B$ is Boltzmann's constant. Equal numbers of electrons and holes: $n = p = n_i$.",

  "inverse function": "A function $f^{-1}$ that reverses the action of $f$. If $f: A \\to B$ is bijective, then:\n\n$$f^{-1}(y) = x \\iff f(x) = y$$\n\n$(f^{-1} \\circ f)(x) = x$ and $(f \\circ f^{-1})(y) = y$. The graph of $f^{-1}$ is the reflection of the graph of $f$ about the line $y = x$. Example: $\\ln x$ is the inverse of $e^x$.",

  "irradiance": "The radiant flux (power) received per unit area of a surface, from all directions in a hemisphere:\n\n$$E = \\frac{d\\Phi}{dA}$$\n\nSI unit: W·m⁻². Also called intensity in optics. For a point source of power $P$ at distance $r$: $E = P/(4\\pi r^2)$ (follows the inverse square law).",

  "isomerism": "The phenomenon where two or more compounds have the same molecular formula but different structural arrangements or spatial orientations:\n\n$$\\text{Structural (constitutional): different connectivity}$$\n$$\\text{Stereoisomerism: same connectivity, different 3D arrangement}$$\n\nFor enantiomers: optical rotation $+\\alpha$ and $-\\alpha$ (equal magnitude, opposite sign). Chiral centre (asymmetric carbon): four different substituents give $2^n$ possible stereoisomers for $n$ chiral centres.",

  "isosceles triangle": "A triangle with two equal sides $a = b$. The base angles are equal:\n\n$$\\alpha = \\beta = \\frac{180^\\circ - \\gamma}{2}$$\n\nArea: $A = \\frac{a}{4}\\sqrt{4a^2 - b^2}$ where $b$ is the base. The perpendicular from the apex to the base bisects it (line of symmetry). A special case with $a = b = c$ is the equilateral triangle.",

  "isotope": "Atoms of the same element (same proton number $Z$) but different mass numbers (different neutron numbers $N$):\n\n$$A = Z + N$$\n\nwhere $A$ is mass number, $Z$ is atomic (proton) number, $N$ is neutron number. Example: $^{12}$C, $^{13}$C, $^{14}$C all have $Z = 6$. Radioactive isotopes decay; stable isotopes do not."
};

// Helper: find entry by word (case-insensitive)
function findEntry(section, word) {
  const entries = dict[section];
  if (!entries) return null;
  return entries.find(e => e.word.toLowerCase() === word.toLowerCase()) || null;
}

let countG = 0, countH = 0, countI = 0;

// Apply Section G
for (const [word, def] of Object.entries(updatesG)) {
  const entry = findEntry('G', word);
  if (entry && !entry.definition.includes('$')) {
    entry.definition = def;
    countG++;
  }
}

// Apply Section H
for (const [word, def] of Object.entries(updatesH)) {
  const entry = findEntry('H', word);
  if (entry && !entry.definition.includes('$')) {
    entry.definition = def;
    countH++;
  }
}

// Apply Section I
for (const [word, def] of Object.entries(updatesI)) {
  const entry = findEntry('I', word);
  if (entry && !entry.definition.includes('$')) {
    entry.definition = def;
    countI++;
  }
}

console.log(`Updated Section G: ${countG} formulas enriched.`);
console.log(`Updated Section H: ${countH} formulas enriched.`);
console.log(`Updated Section I: ${countI} formulas enriched.`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log('Saved dictionary.json successfully.');
