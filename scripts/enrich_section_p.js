/**
 * scripts/enrich_section_p.js
 * Comprehensive STEM Formula Enrichment for Section P (33 Fundamental Terms)
 */
const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

const pEnrichments = {
  "planck constant": {
    formula: "h = 6.62607015 \\times 10^{-34}\\;\\text{J}\\cdot\\text{s} = 4.135667696 \\times 10^{-15}\\;\\text{eV}\\cdot\\text{s}, \\quad \\hbar = \\frac{h}{2\\pi} = 1.054571817 \\times 10^{-34}\\;\\text{J}\\cdot\\text{s}",
    formula_description: "The fundamental physical quantum constant relating photon energy to electromagnetic frequency ($E = h\\nu = \\hbar\\omega$). Serves as the universal quantum of action defining microscopic physics."
  },
  "planck's radiation law": {
    formula: "B_\\lambda(\\lambda, T) = \\frac{2hc^2}{\\lambda^5} \\frac{1}{e^{\\frac{hc}{\\lambda k_B T}} - 1}, \\quad B_\\nu(\\nu, T) = \\frac{2h\\nu^3}{c^2} \\frac{1}{e^{\\frac{h\\nu}{k_B T}} - 1}",
    formula_description: "Planck's spectral distribution describing the energy density and spectral radiance of black-body thermal radiation at temperature $T$, resolving the ultraviolet catastrophe of classical Rayleigh–Jeans physics."
  },
  "planck length": {
    formula: "\\ell_P = \\sqrt{\\frac{\\hbar G}{c^3}} \\approx 1.616255(18) \\times 10^{-35}\\;\\text{m}",
    formula_description: "The fundamental base unit of length in natural Planck units, defining the quantum scale beneath which classical spacetime geometry breaks down under quantum gravity."
  },
  "planck mass": {
    formula: "m_P = \\sqrt{\\frac{\\hbar c}{G}} \\approx 2.176434(24) \\times 10^{-8}\\;\\text{kg} \\approx 1.2209 \\times 10^{19}\\;\\text{GeV}/c^2",
    formula_description: "The natural unit of mass in Planck units, representing the mass at which an elementary particle's Compton wavelength equals its Schwarzschild radius."
  },
  "planck time": {
    formula: "t_P = \\sqrt{\\frac{\\hbar G}{c^5}} = \\frac{\\ell_P}{c} \\approx 5.391247(60) \\times 10^{-44}\\;\\text{s}",
    formula_description: "The time required for light in vacuum to travel one Planck length; the shortest theoretically meaningful physical interval of time in quantum cosmology."
  },
  "photoelectric effect": {
    formula: "K_{\\max} = h\\nu - \\Phi = h(\\nu - \\nu_0) = e V_0",
    formula_description: "Einstein's photoelectric equation: the maximum kinetic energy $K_{\\max}$ of emitted photoelectrons equals incident photon energy $h\\nu$ minus the metal's work function $\\Phi = h\\nu_0$, where $V_0$ is stopping voltage and $e$ is electron charge."
  },
  "pascal": {
    formula: "1\\;\\text{Pa} = 1\\;\\text{N/m}^2 = 1\\;\\text{kg}\\cdot\\text{m}^{-1}\\cdot\\text{s}^{-2} = 10^{-5}\\;\\text{bar} \\approx 9.8692 \\times 10^{-6}\\;\\text{atm}",
    formula_description: "The SI derived unit of pressure, mechanical stress, Young's modulus, and tensile strength, defined as one newton of perpendicular force applied uniformly across an area of one square metre."
  },
  "pascal's principle": {
    formula: "\\Delta P = \\rho g \\Delta h, \\quad \\frac{F_1}{A_1} = \\frac{F_2}{A_2} \\implies F_2 = F_1 \\left(\\frac{A_2}{A_1}\\right)",
    formula_description: "Pascal's law of fluid statics: an external pressure change applied to an enclosed, incompressible static fluid is transmitted undiminished throughout the fluid and to container walls, establishing hydraulic multiplication."
  },
  "poisson distribution": {
    formula: "P(X = k) = \\frac{\\lambda^k e^{-\\lambda}}{k!}, \\quad \\mathbb{E}[X] = \\lambda, \\quad \\mathrm{Var}(X) = \\lambda",
    formula_description: "Discrete probability distribution expressing the likelihood of $k$ independent events occurring in a fixed interval given a known average occurrence rate $\\lambda$."
  },
  "poisson's ratio": {
    formula: "\\nu = -\\frac{\\varepsilon_{\\text{transverse}}}{\\varepsilon_{\\text{axial}}} = -\\frac{\\Delta d / d_0}{\\Delta L / L_0}",
    formula_description: "The negative ratio of transverse (lateral) strain to axial (longitudinal) strain when a material undergoes tensile or compressive stress, typically ranging between $0.25$ and $0.35$ for elastic metals."
  },
  "poisson equation": {
    formula: "\\nabla^2 \\varphi = f, \\quad \\nabla^2 V = -\\frac{\\rho}{\\varepsilon_0} \\quad (\\text{Electrostatics}), \\quad \\nabla^2 \\Phi = 4\\pi G \\rho \\quad (\\text{Gravitation})",
    formula_description: "Fundamental second-order elliptic partial differential equation relating the Laplacian of an electrostatic potential $V$ (or gravitational potential $\\Phi$) to the source charge or mass density $\\rho$."
  },
  "poynting vector": {
    formula: "\\mathbf{S} = \\frac{1}{\\mu_0} (\\mathbf{E} \\times \\mathbf{B}) = \\mathbf{E} \\times \\mathbf{H}, \\quad \\langle S \\rangle = I = \\frac{1}{2 c \\mu_0} E_0^2",
    formula_description: "Vector quantity representing the directional energy flux density (rate of electromagnetic energy transfer per unit area in $\\text{W/m}^2$) of an electromagnetic field, where $\\mathbf{E}$ is electric field and $\\mathbf{B}$ is magnetic flux density."
  },
  "poiseuille's equation": {
    formula: "Q = \\frac{dV}{dt} = \\frac{\\pi r^4 \\Delta P}{8 \\mu L}, \\quad R_{\\text{flow}} = \\frac{8 \\mu L}{\\pi r^4}",
    formula_description: "The Hagen–Poiseuille law for laminar, incompressible, viscous fluid flow rate $Q$ through a cylindrical pipe of radius $r$ and length $L$ driven by pressure gradient $\\Delta P$ with dynamic viscosity $\\mu$."
  },
  "parallelogram law": {
    formula: "\\|\\mathbf{u} + \\mathbf{v}\\|^2 + \\|\\mathbf{u} - \\mathbf{v}\\|^2 = 2\\|\\mathbf{u}\\|^2 + 2\\|\\mathbf{v}\\|^2",
    formula_description: "Fundamental geometric theorem in inner product spaces: the sum of the squares of the lengths of all four sides of a parallelogram equals the sum of the squares of the lengths of its two diagonals."
  },
  "parallelogram of vectors": {
    formula: "R = \\sqrt{P^2 + Q^2 + 2PQ\\cos\\theta}, \\quad \\tan\\alpha = \\frac{Q\\sin\\theta}{P + Q\\cos\\theta}",
    formula_description: "The geometric and analytical rule of vector addition: when two coplanar vectors $\\mathbf{P}$ and $\\mathbf{Q}$ act at an angle $\theta$, their resultant $\\mathbf{R}$ forms the diagonal of the completed parallelogram at angle $\\alpha$."
  },
  "parallelogram of forces": {
    formula: "\\mathbf{F}_{\\text{net}} = \\mathbf{F}_1 + \\mathbf{F}_2, \\quad F_{\\text{net}} = \\sqrt{F_1^2 + F_2^2 + 2F_1 F_2 \\cos\\theta}",
    formula_description: "Classical statics principle for combining two concurrent force vectors $\\mathbf{F}_1$ and $\\mathbf{F}_2$ acting on a single point into a single statically equivalent resultant force."
  },
  "pythagoras' theorem": {
    formula: "a^2 + b^2 = c^2 \\iff c = \\sqrt{a^2 + b^2}, \\quad \\sin^2\\theta + \\cos^2\\theta = 1",
    formula_description: "Euclidean geometric theorem stating that in any right-angled triangle with legs $a$ and $b$, the square of the hypotenuse $c$ equals the sum of the squares of the other two sides."
  },
  "pendulum": {
    formula: "T = 2\\pi \\sqrt{\\frac{L}{g}} \\left(1 + \\frac{1}{4}\\sin^2\\frac{\\theta_0}{2} + \\dots\\right) \\approx 2\\pi \\sqrt{\\frac{L}{g}} \\quad (\\theta_0 \\ll 1\\text{ rad})",
    formula_description: "Period of oscillation $T$ for a simple gravitational pendulum of length $L$ in acceleration field $g$, under the small-angle simple harmonic motion approximation."
  },
  "potential energy": {
    formula: "U_g = mgh, \\quad U_s = \\frac{1}{2}kx^2, \\quad U_e = \\frac{1}{4\\pi\\varepsilon_0}\\frac{q_1 q_2}{r}, \\quad U_G = -\\frac{G M m}{r}",
    formula_description: "Stored mechanical, elastic, or field energy possessed by a body due to its position or spatial configuration within a conservative force field (satisfying $\\mathbf{F} = -\\nabla U$)."
  },
  "potential difference": {
    formula: "V = V_B - V_A = -\\int_A^B \\mathbf{E} \\cdot d\\mathbf{r} = \\frac{W}{q} = I R",
    formula_description: "The work done $W$ per unit electric charge $q$ in moving between two points in an electric field, measured in volts ($1\\;\\text{V} = 1\\;\\text{J/C}$)."
  },
  "power": {
    formula: "P = \\frac{dW}{dt} = \\mathbf{F} \\cdot \\mathbf{v}, \\quad P_{\\text{elec}} = V I = I^2 R = \\frac{V^2}{R}",
    formula_description: "The time rate of performing mechanical work or expending/transferring electrical energy, measured in watts ($1\\;\\text{W} = 1\\;\\text{J/s} = 1\\;\\text{N}\\cdot\\text{m/s}$)."
  },
  "pressure": {
    formula: "P = \\frac{dF_{\\perp}}{dA} \\approx \\frac{F}{A}, \\quad P_{\\text{hydro}} = P_0 + \\rho g h",
    formula_description: "The perpendicular compressive force exerted per unit area of a boundary surface, measured in pascals ($\\text{N/m}^2$). At depth $h$ in a static fluid, hydrostatic pressure increases by $\\rho g h$."
  },
  "partial pressure": {
    formula: "P_i = x_i P_{\\text{total}} = \\frac{n_i R T}{V}, \\quad P_{\\text{total}} = \\sum_{i=1}^k P_i \\quad (\\text{Dalton's Law})",
    formula_description: "Dalton's law of partial pressures: the pressure exerted by gas component $i$ in an ideal gas mixture equals its mole fraction $x_i$ times total pressure $P_{\\text{total}}$."
  },
  "photon": {
    formula: "E = h\\nu = \\hbar\\omega = \\frac{hc}{\\lambda}, \\quad p = \\frac{h}{\\lambda} = \\frac{E}{c}, \\quad m_0 = 0",
    formula_description: "The discrete quantum of electromagnetic radiation, carrying energy $E$ and momentum $p$ inversely proportional to wavelength $\\lambda$, with zero rest mass and speed $c$ in vacuum."
  },
  "ph": {
    formula: "\\text{pH} = -\\log_{10}[\\text{H}^+] = -\\log_{10}[\\text{H}_3\\text{O}^+], \\quad \\text{pH} + \\text{pOH} = 14.00 \\quad (\\text{at } 25^\\circ\\text{C})",
    formula_description: "The logarithmic scale introduced by Sørensen measuring aqueous acidity or alkalinity, defined as the negative base-10 logarithm of hydrogen/hydronium ion activity in moles per litre."
  },
  "phase rule": {
    formula: "F = C - P + 2",
    formula_description: "Gibbs' phase rule relating degrees of freedom $F$ (independent intensive state variables) to the number of non-reacting chemical components $C$ and coexisting phases $P$ in thermodynamic equilibrium."
  },
  "pauli exclusion principle": {
    formula: "\\Psi(\\mathbf{r}_1, s_1; \\mathbf{r}_2, s_2) = -\\Psi(\\mathbf{r}_2, s_2; \\mathbf{r}_1, s_1), \\quad \\{a_i, a_j^\\dagger\\} = \\delta_{ij}",
    formula_description: "Fundamental quantum mechanical principle establishing that two identical half-integer spin fermions (e.g. electrons) cannot occupy the same quantum state simultaneously, mandating antisymmetric wavefunctions."
  },
  "permutation": {
    formula: "^n P_r = P(n, r) = \\frac{n!}{(n - r)!}, \\quad P_{\\text{repeated}} = \\frac{n!}{n_1! \\, n_2! \\dots n_k!}",
    formula_description: "The total number of ordered arrangements of $r$ elements selected from $n$ distinct elements without replacement, where selection sequence and ordering are significant."
  },
  "prism": {
    formula: "n = \\frac{\\sin\\left(\\frac{A + D_m}{2}\\right)}{\\sin\\left(\\frac{A}{2}\\right)}, \\quad V_{\\text{prism}} = B \\cdot h",
    formula_description: "The optical prism formula relating refractive index $n$ to refracting apex angle $A$ and minimum deviation angle $D_m$. In stereometry, prism volume equals cross-sectional base area $B$ times height $h$."
  },
  "peltier effect": {
    formula: "\\dot{Q} = \\Pi_{AB} I = (\\Pi_A - \\Pi_B) I, \\quad \\Pi_{AB} = S_{AB} \\cdot T \\quad (\\text{Kelvin relation})",
    formula_description: "Thermoelectric effect wherein electric current $I$ passing across the junction of two distinct conductors generates or absorbs heat flux $\\dot{Q}$, proportional to relative Peltier coefficient $\\Pi_{AB}$ and absolute temperature $T$."
  },
  "projectile": {
    formula: "R = \\frac{v_0^2 \\sin(2\\theta)}{g}, \\quad H_{\\max} = \\frac{v_0^2 \\sin^2\\theta}{2g}, \\quad T_{\\text{flight}} = \\frac{2v_0 \\sin\\theta}{g}, \\quad y = x\\tan\\theta - \\frac{gx^2}{2v_0^2 \\cos^2\\theta}",
    formula_description: "Classical kinematic equations for projectile trajectory under gravitational acceleration $g$, giving range $R$, peak height $H_{\\max}$, flight time $T_{\\text{flight}}$, and parabolic trajectory."
  },
  "parabola": {
    formula: "y = a x^2 + b x + c, \\quad (x - h)^2 = 4p(y - k), \\quad r = \\frac{2p}{1 - \\cos\\theta}, \\quad e = 1",
    formula_description: "Conic section with eccentricity $e = 1$, defined as the locus of all points in a plane equidistant from a fixed focal point and a straight line directrix."
  },
  "piezoelectric effect": {
    formula: "P_i = d_{ijk} \\sigma_{jk} \\quad (\\text{Direct Effect}), \\quad \\varepsilon_{jk} = d_{ijk} E_i \\quad (\\text{Converse Effect})",
    formula_description: "Linear electromechanical interaction in non-centrosymmetric crystals (such as quartz or PZT) where mechanical stress $\\sigma$ generates dielectric polarization $P$ and applied electric field $E$ produces mechanical strain $\\varepsilon$."
  }
};

let enrichedCount = 0;
const pList = dict['P'] || [];

pList.forEach(entry => {
  const key = entry.word.trim().toLowerCase();
  if (pEnrichments[key]) {
    const data = pEnrichments[key];
    entry.formula = data.formula;
    entry.formula_description = data.formula_description;
    
    // Correct corrupted definition of pH if present
    if (key === 'ph' && entry.definition.includes('biological process by which green plants')) {
      entry.definition = "A logarithmic measure of the acidity or basicity of an aqueous solution, defined as the negative common logarithm of the hydrogen ion (or hydronium ion) concentration [H+]. Solutions with pH less than 7 are acidic, pH equal to 7 are neutral, and pH greater than 7 are basic (alkaline).";
    }

    // Embed cleanly into definition if not already embedded
    if (!entry.definition.includes('$$')) {
      entry.definition = `${entry.definition.trim()}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
    } else {
      // If $$ exists but formula isn't the standardized one, replace the KaTeX block cleanly
      const baseDef = entry.definition.split('$$')[0].trim();
      entry.definition = `${baseDef}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
    }
    enrichedCount++;
    console.log(`Enriched P [${key}]`);
  }
});

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log(`\nSuccessfully enriched ${enrichedCount} Section P terms in dictionary.json!`);
