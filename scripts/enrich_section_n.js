/**
 * scripts/enrich_section_n.js
 * Comprehensive STEM Formula Enrichment for Section N
 */
const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

const nEnrichments = {
  "nernst equation": {
    formula: "E = E^\\circ - \\frac{RT}{zF} \\ln Q = E^\\circ - \\frac{0.0592}{z} \\log_{10} Q \\quad (\\text{at } 298\\text{ K})",
    formula_description: "Calculates the reduction potential of an electrochemical half-cell or full cell under non-standard conditions, where $E^\\circ$ is standard potential, $R$ is gas constant ($8.314\\text{ J/mol}\\cdot\\text{K}$), $T$ is temperature, $z$ is moles of electrons transferred, $F$ is Faraday's constant ($96,485\\text{ C/mol}$), and $Q$ is the reaction quotient."
  },
  "nernst-einstein equation": {
    formula: "D = \\mu k_B T = \\frac{u R T}{z F}",
    formula_description: "Relates the diffusion coefficient $D$ of particles to their electrical mobility $\\mu$ (or ionic mobility $u$), where $k_B$ is the Boltzmann constant, $T$ is absolute temperature, $z$ is ionic charge number, and $F$ is Faraday's constant."
  },
  "nernst heat theorem": {
    formula: "\\lim_{T \\to 0} \\Delta S = 0, \\quad \\lim_{T \\to 0} \\Delta G = \\lim_{T \\to 0} \\Delta H",
    formula_description: "The historical foundation of the Third Law of Thermodynamics: as absolute temperature $T$ approaches zero, the entropy change $\\Delta S$ for any reversible isothermal process between condensed phases approaches zero."
  },
  "navier-stokes equation": {
    formula: "\\rho \\left( \\frac{\\partial \\mathbf{u}}{\\partial t} + \\mathbf{u} \\cdot \\nabla \\mathbf{u} \\right) = -\\nabla p + \\mu \\nabla^2 \\mathbf{u} + \\mathbf{f}",
    formula_description: "The fundamental continuum equations governing fluid motion (Newton's second law for viscous fluids), where $\\rho$ is fluid density, $\\mathbf{u}$ is velocity field, $p$ is pressure, $\\mu$ is dynamic viscosity, and $\\mathbf{f}$ represents external body forces (e.g. gravity)."
  },
  "natural logarithm": {
    formula: "\\ln(x) = \\log_e(x) = \\int_{1}^{x} \\frac{1}{t} \\, dt, \\quad e^{\\ln(x)} = x",
    formula_description: "Logarithm to the mathematical base $e \\approx 2.71828$. Satisfies $\\frac{d}{dx}[\\ln(x)] = \\frac{1}{x}$ and fundamental identities $\\ln(ab) = \\ln a + \\ln b$ and $\\ln(a^b) = b \\ln a$."
  },
  "napierian logarithm": {
    formula: "\\text{NapLog}(x) = 10^7 \\ln\\left(\\frac{10^7}{x}\\right)",
    formula_description: "The historical logarithm introduced by John Napier (1614), defined originally with base $(1 - 10^{-7})^{10^7} \\approx 1/e$ scaled by $10^7$ to avoid decimals in astronomical navigation."
  },
  "negative binomial distribution": {
    formula: "P(X = k) = \\binom{k + r - 1}{k} p^r (1 - p)^k, \\quad \\mathbb{E}[X] = \\frac{r(1-p)}{p}, \\; \\mathrm{Var}(X) = \\frac{r(1-p)}{p^2}",
    formula_description: "Discrete probability distribution modeling the number of failures $k$ observed before achieving $r$ successes in independent Bernoulli trials with success probability $p$."
  },
  "negative exponential distribution": {
    formula: "f(x) = \\lambda e^{-\\lambda x} \\quad (x \\ge 0), \\quad F(x) = 1 - e^{-\\lambda x}, \\; \\mathbb{E}[X] = \\frac{1}{\\lambda}",
    formula_description: "Continuous memoryless probability distribution representing the time elapsed between independent Poisson point events occurring at a constant average rate $\\lambda$."
  },
  "net force": {
    formula: "\\mathbf{F}_{\\text{net}} = \\sum_{i=1}^{n} \\mathbf{F}_i = m \\mathbf{a} = \\frac{d\\mathbf{p}}{dt}",
    formula_description: "The vector sum of all external forces acting upon a body of mass $m$, dictating its acceleration $\\mathbf{a}$ and the time rate of change of its linear momentum $\\mathbf{p}$."
  },
  "newton": {
    formula: "1\\text{ N} = 1\\text{ kg}\\cdot\\text{m}/\\text{s}^2 = 10^5\\text{ dynes}",
    formula_description: "The SI derived unit of force, defined as the force required to accelerate a mass of one kilogram at the rate of one metre per second squared."
  },
  "newton's constant": {
    formula: "G = 6.67430(15) \\times 10^{-11} \\; \\text{m}^3\\text{ kg}^{-1}\\text{ s}^{-2} = \\text{N}\\cdot\\text{m}^2/\\text{kg}^2",
    formula_description: "The universal gravitational constant $G$ appearing in Newton's law of universal gravitation and Einstein's field equations of General Relativity."
  },
  "newton's formula": {
    formula: "x x' = f^2",
    formula_description: "Newton's conjugate mirror and thin-lens formula relating object distance $x$ and image distance $x'$ measured from their respective principal focal points to focal length $f$."
  },
  "newton's law of cooling": {
    formula: "\\frac{dT}{dt} = -k (T - T_{\\text{env}}) \\implies T(t) = T_{\\text{env}} + (T_0 - T_{\\text{env}})e^{-kt}",
    formula_description: "States that the rate of heat loss of a body is proportional to the difference in temperatures between the body ($T$) and its surrounding environment ($T_{\\text{env}}$), where $k > 0$ is heat transfer coefficient."
  },
  "newton's law of gravity": {
    formula: "\\mathbf{F} = -G \\frac{m_1 m_2}{r^2} \\hat{\\mathbf{r}}, \\quad U(r) = -G \\frac{m_1 m_2}{r}",
    formula_description: "Every point mass attracts every other point mass with a central force proportional to the product of their masses $m_1, m_2$ and inversely proportional to the square of the distance $r$ separating them."
  },
  "newton's laws of motion": {
    formula: "\\begin{cases} \\sum \\mathbf{F} = 0 \\implies \\mathbf{v} = \\text{const} & (\\text{1st: Inertia}) \\\\[4pt] \\mathbf{F}_{\\text{net}} = m\\mathbf{a} = \\frac{d\\mathbf{p}}{dt} & (\\text{2nd: Momentum}) \\\\[4pt] \\mathbf{F}_{AB} = -\\mathbf{F}_{BA} & (\\text{3rd: Action-Reaction}) \\end{cases}",
    formula_description: "The three classical laws formulated by Sir Isaac Newton in 1687 underpinning classical mechanics: the law of inertia, force and momentum rate of change, and mutual reciprocal action."
  },
  "newton's method": {
    formula: "x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}, \\quad |e_{n+1}| \\approx \\frac{|f''(r)|}{2|f'(r)|} |e_n|^2",
    formula_description: "The Newton–Raphson algorithm: an iterative numerical root-finding method that starts with an initial approximation $x_0$ and exhibits quadratic convergence near a simple root $r$."
  },
  "newton's rings": {
    formula: "r_m = \\sqrt{m \\lambda R} \\quad (\\text{dark rings, transmitted light: } r_m = \\sqrt{(m + \\tfrac{1}{2})\\lambda R})",
    formula_description: "Interference pattern produced by thin air-film reflection between a spherical lens of radius of curvature $R$ and an adjacent flat optical surface, yielding concentric circular fringes of radius $r_m$ for wavelength $\\lambda$."
  },
  "newton-cotes formulae": {
    formula: "\\int_a^b f(x) dx \\approx \\sum_{i=0}^n w_i f(x_i) \\quad (\\text{Trapezoid: } n=1; \\; \\text{Simpson's 1/3: } n=2)",
    formula_description: "Class of numerical quadrature formulas integrating equally spaced points, including the Trapezoidal rule (linear interpolation) and Simpson's rules (quadratic and cubic interpolations)."
  },
  "newtonian fluid": {
    formula: "\\tau = \\mu \\frac{du}{dy}",
    formula_description: "A fluid in which the viscous shear stress $\\tau$ is linearly proportional to the local strain rate (velocity gradient) $\\frac{du}{dy}$, where the proportionality constant $\\mu$ is independent of shear rate."
  },
  "nuclear binding energy": {
    formula: "B = \\Delta m \\cdot c^2 = \\left[ Z m_p + (A - Z)m_n - M_{\\text{nucleus}} \\right] c^2",
    formula_description: "The energy required to disassemble an atomic nucleus into its component protons ($Z$) and neutrons ($A-Z$), derived from mass defect $\\Delta m$ via mass-energy equivalence ($E = mc^2$)."
  },
  "nuclear energy": {
    formula: "E = \\Delta m \\cdot c^2 \\quad (\\approx 200\\text{ MeV per } ^{235}\\text{U fission})",
    formula_description: "Energy released by the rearrangement of nuclear bonds in fission or fusion processes, determined by the mass difference between reactants and reaction products multiplied by $c^2$."
  },
  "normal distribution": {
    formula: "f(x) = \\frac{1}{\\sigma \\sqrt{2\\pi}} \\exp\\left( -\\frac{(x - \\mu)^2}{2\\sigma^2} \\right), \\quad \\Phi(z) = \\frac{1}{\\sqrt{2\\pi}} \\int_{-\\infty}^z e^{-t^2/2} dt",
    formula_description: "The Gaussian continuous probability distribution characterized by mean $\\mu$ and standard deviation $\\sigma$, ubiquitously governing natural variations by virtue of the Central Limit Theorem."
  }
};

let enrichedCount = 0;
const nList = dict['N'] || [];

nList.forEach(entry => {
  const key = entry.word.trim().toLowerCase();
  if (nEnrichments[key]) {
    const data = nEnrichments[key];
    entry.formula = data.formula;
    entry.formula_description = data.formula_description;
    
    // Embed cleanly into definition if not already embedded
    if (!entry.definition.includes('$$')) {
      entry.definition = `${entry.definition.trim()}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
    }
    enrichedCount++;
    console.log(`Enriched N [${key}]`);
  }
});

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log(`\nSuccessfully enriched ${enrichedCount} Section N terms in dictionary.json!`);
