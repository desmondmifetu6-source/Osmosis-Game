/**
 * scripts/enrich_sections_uvw.js
 * Comprehensive STEM Formula Enrichment for Sections U, V, W
 *
 * U: uniform motion, uncertainty principle, unit vectors, universal gravitation
 * V: velocity, voltage, volume, vector operations, Venn diagrams
 * W: wave, work, wavelength, Wien's law, weight, Wheatstone bridge
 *
 * Usage: node scripts/enrich_sections_uvw.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

/* ============================================================
   ENRICHMENT DATA  (keyed by word.trim().toLowerCase())
============================================================ */
const enrichments = {

  // ═══════════════════════════════════════════════
  //  U  –  SECTION U
  // ═══════════════════════════════════════════════

  "uncertainty principle": {
    formula: "\\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}, \\quad \\Delta E \\cdot \\Delta t \\geq \\frac{\\hbar}{2}, \\quad \\hbar = \\frac{h}{2\\pi} \\approx 1.055 \\times 10^{-34}\\text{ J·s}",
    formula_description: "Heisenberg's uncertainty principle: the product of positional uncertainty $\\Delta x$ and momentum uncertainty $\\Delta p$ is bounded below by $\\hbar/2$. Represents a fundamental quantum limit, not a measurement limitation."
  },

  "uniform motion": {
    formula: "v = \\text{const}, \\quad s = vt, \\quad a = 0, \\quad \\sum F = 0",
    formula_description: "Motion at constant speed in a straight line. By Newton's First Law, zero net force $\\sum F = 0$ is required. Distance $s = vt$; velocity-time graph is horizontal."
  },

  "uniform acceleration": {
    formula: "v = u + at, \\quad s = ut + \\frac{1}{2}at^2, \\quad v^2 = u^2 + 2as, \\quad s = \\frac{(u+v)}{2}t",
    formula_description: "Constant-acceleration motion governed by the four kinematic (SUVAT) equations. $u$ = initial velocity, $v$ = final velocity, $a$ = acceleration, $s$ = displacement, $t$ = time."
  },

  "unit vector": {
    formula: "\\hat{\\mathbf{u}} = \\frac{\\mathbf{v}}{|\\mathbf{v}|}, \\quad |\\hat{\\mathbf{u}}| = 1, \\quad \\hat{i}=(1,0,0),\\; \\hat{j}=(0,1,0),\\; \\hat{k}=(0,0,1)",
    formula_description: "A vector of magnitude 1 pointing in the direction of $\\mathbf{v}$. Any vector can be expressed as $\\mathbf{v} = v_x\\hat{i} + v_y\\hat{j} + v_z\\hat{k}$. Cartesian unit vectors $\\hat{i}, \\hat{j}, \\hat{k}$ form an orthonormal basis."
  },

  "universal gas constant": {
    formula: "R = 8.314 \\;\\text{J mol}^{-1}\\text{K}^{-1} = N_A k_B, \\quad PV = nRT, \\quad k_B = \\frac{R}{N_A} = 1.381 \\times 10^{-23}\\text{ J/K}",
    formula_description: "Proportionality constant $R$ in the ideal gas law $PV = nRT$, relating pressure, volume, amount (moles $n$) and temperature (Kelvin). Equal to Avogadro's number $N_A$ times Boltzmann's constant $k_B$."
  },

  "universal law of gravitation": {
    formula: "F = G\\frac{m_1 m_2}{r^2}, \\quad G = 6.674 \\times 10^{-11}\\;\\text{N m}^2\\text{kg}^{-2}, \\quad g = \\frac{GM}{r^2}",
    formula_description: "Newton's universal gravitation: every pair of masses attracts with force $F = Gm_1m_2/r^2$. Surface gravitational field strength $g = GM/R^2$ where $M$ is planetary mass and $R$ is radius."
  },

  "uniform distribution": {
    formula: "f(x) = \\frac{1}{b-a} \\quad (a \\leq x \\leq b), \\quad E[X] = \\frac{a+b}{2}, \\quad \\text{Var}(X) = \\frac{(b-a)^2}{12}",
    formula_description: "Probability distribution where all outcomes in interval $[a, b]$ are equally likely. Mean is the midpoint $(a+b)/2$; variance $(b-a)^2/12$."
  },

  // ═══════════════════════════════════════════════
  //  V  –  SECTION V
  // ═══════════════════════════════════════════════

  "vector": {
    formula: "\\mathbf{v} = v_x\\hat{i} + v_y\\hat{j} + v_z\\hat{k}, \\quad |\\mathbf{v}| = \\sqrt{v_x^2+v_y^2+v_z^2}, \\quad \\theta = \\arctan\\!\\left(\\frac{v_y}{v_x}\\right)",
    formula_description: "A mathematical object with both magnitude and direction. In 2D/3D, represented by components along orthogonal unit vectors. Magnitude and direction angle completely characterise a vector."
  },

  "vector product": {
    formula: "\\mathbf{a} \\times \\mathbf{b} = |\\mathbf{a}||\\mathbf{b}|\\sin\\theta\\,\\hat{n} = \\begin{vmatrix}\\hat{i}&\\hat{j}&\\hat{k}\\\\a_x&a_y&a_z\\\\b_x&b_y&b_z\\end{vmatrix}",
    formula_description: "Cross product of two vectors: produces a vector perpendicular to both with magnitude $|\\mathbf{a}||\\mathbf{b}|\\sin\\theta$. Used to compute torque $\\boldsymbol{\\tau} = \\mathbf{r} \\times \\mathbf{F}$ and angular momentum."
  },

  "velocity": {
    formula: "\\mathbf{v} = \\frac{d\\mathbf{s}}{dt}, \\quad v_{\\text{avg}} = \\frac{\\Delta s}{\\Delta t}, \\quad |\\mathbf{v}| = \\sqrt{v_x^2+v_y^2+v_z^2}",
    formula_description: "Rate of change of displacement with respect to time: a vector quantity with both speed (magnitude) and direction. Average velocity $\\bar{v} = \\Delta s / \\Delta t$; instantaneous velocity $v = ds/dt$."
  },

  "voltage": {
    formula: "V = \\frac{W}{Q} = IR, \\quad V = \\mathcal{E} - Ir, \\quad V_{\\text{rms}} = \\frac{V_m}{\\sqrt{2}}",
    formula_description: "Electric potential difference: work done per unit charge moving between two points $V = W/Q$. Terminal voltage $V = \\mathcal{E} - Ir$ accounts for internal resistance $r$ of an EMF source."
  },

  "volume": {
    formula: "V_{\\text{sphere}} = \\frac{4}{3}\\pi r^3, \\quad V_{\\text{cylinder}} = \\pi r^2 h, \\quad V_{\\text{cone}} = \\frac{1}{3}\\pi r^2 h, \\quad V_{\\text{cuboid}} = lwh",
    formula_description: "Three-dimensional extent of a solid measured in cubic units. Volume scales as the cube of any linear dimension. Key formulae for common solids: sphere, cylinder, cone, cuboid."
  },

  "venn diagram": {
    formula: "|A \\cup B| = |A| + |B| - |A \\cap B|, \\quad P(A \\cup B) = P(A) + P(B) - P(A \\cap B)",
    formula_description: "Diagram showing logical relationships between sets using overlapping circles. The inclusion-exclusion principle gives the cardinality of the union and underpins probability addition rule."
  },

  "viscosity": {
    formula: "F = \\eta A \\frac{dv}{dy}, \\quad \\eta = \\frac{\\tau}{\\dot{\\gamma}}, \\quad Re = \\frac{\\rho v D}{\\eta}",
    formula_description: "Dynamic viscosity $\\eta$: resistance of a fluid to shear deformation. Newton's law of viscosity: shear stress $\\tau = \\eta\\,dv/dy$. SI unit: Pascal-second (Pa·s)."
  },

  "volta cell": {
    formula: "\\mathcal{E} = E^\\circ_{\\text{cathode}} - E^\\circ_{\\text{anode}}, \\quad \\mathcal{E}_{\\text{Zn/Cu}} = +0.34 - (-0.76) = 1.10\\text{ V}",
    formula_description: "Electrochemical cell generating EMF from spontaneous redox reactions. Cell EMF equals the difference of standard reduction potentials of cathode and anode. Positive EMF indicates spontaneous reaction."
  },

  "variance": {
    formula: "\\text{Var}(X) = \\sigma^2 = E[(X-\\mu)^2] = E[X^2] - (E[X])^2 = \\frac{\\sum(x_i-\\bar{x})^2}{n}",
    formula_description: "Statistical measure of spread: average squared deviation from the mean. Population variance $\\sigma^2 = E[X^2] - (E[X])^2$; standard deviation $\\sigma = \\sqrt{\\text{Var}(X)}$."
  },

  // ═══════════════════════════════════════════════
  //  W  –  SECTION W
  // ═══════════════════════════════════════════════

  "wave": {
    formula: "y(x,t) = A\\sin(kx - \\omega t), \\quad v = f\\lambda, \\quad k = \\frac{2\\pi}{\\lambda}, \\quad \\omega = 2\\pi f",
    formula_description: "Periodic disturbance propagating energy through a medium or vacuum. Wave speed $v = f\\lambda$; wavenumber $k = 2\\pi/\\lambda$; angular frequency $\\omega = 2\\pi f$."
  },

  "wavelength": {
    formula: "\\lambda = \\frac{v}{f} = \\frac{c}{f} = \\frac{2\\pi}{k}, \\quad \\lambda_{\\text{visible}} \\approx 400\\text{–}700\\text{ nm}",
    formula_description: "Distance between two consecutive points in phase (e.g., two crests) in a wave. Inversely proportional to frequency: $\\lambda = v/f$. For electromagnetic radiation in vacuum, $v = c$."
  },

  "weight": {
    formula: "W = mg, \\quad g = \\frac{GM}{r^2}, \\quad g_{\\text{Earth}} \\approx 9.81\\text{ m/s}^2, \\quad W_{\\text{Moon}} = \\frac{W_{\\text{Earth}}}{6}",
    formula_description: "Gravitational force on an object: $W = mg$ where $m$ is mass and $g$ gravitational field strength. Not the same as mass; varies with location. Weight on Moon $\\approx W_{\\text{Earth}}/6$."
  },

  "work": {
    formula: "W = \\mathbf{F} \\cdot \\mathbf{d} = Fd\\cos\\theta, \\quad W = \\int_a^b F(x)\\,dx, \\quad W_{\\text{net}} = \\Delta KE = \\frac{1}{2}mv^2 - \\frac{1}{2}mu^2",
    formula_description: "Energy transferred by a force: $W = Fd\\cos\\theta$ for constant force $F$ at angle $\\theta$ to displacement $d$. Work-energy theorem: net work equals change in kinetic energy."
  },

  "work-energy theorem": {
    formula: "W_{\\text{net}} = \\Delta KE = \\frac{1}{2}mv^2 - \\frac{1}{2}mu^2 = \\int \\mathbf{F} \\cdot d\\mathbf{s}",
    formula_description: "The net work done on an object equals its change in kinetic energy. Unifies the concepts of force, displacement, and energy — fundamental to Newtonian mechanics."
  },

  "wien's law": {
    formula: "\\lambda_{\\max} T = b, \\quad b = 2.898 \\times 10^{-3}\\text{ m·K}, \\quad \\lambda_{\\max} = \\frac{b}{T}",
    formula_description: "Wien's displacement law: the peak wavelength $\\lambda_{\\max}$ of blackbody radiation is inversely proportional to temperature $T$. Explains why hot objects glow red then white then blue."
  },

  "wheatstone bridge": {
    formula: "\\frac{P}{Q} = \\frac{R}{S} \\implies I_G = 0 \\text{ (balanced)}, \\quad R_{\\text{unknown}} = \\frac{Q \\cdot S}{P}",
    formula_description: "Electrical circuit for precise resistance measurement. At balance, no current flows through galvanometer: ratio $P/Q = R/S$. Unknown resistance $R_x = QS/P$."
  },

  "wave equation": {
    formula: "\\frac{\\partial^2 y}{\\partial t^2} = v^2 \\frac{\\partial^2 y}{\\partial x^2}, \\quad v = \\sqrt{\\frac{T}{\\mu}} \\text{ (string)}, \\quad v = \\sqrt{\\frac{B}{\\rho}} \\text{ (sound)}",
    formula_description: "Partial differential equation describing wave propagation. Solution is $y(x,t) = A\\sin(kx \\pm \\omega t)$. Wave speed $v = \\sqrt{T/\\mu}$ for a stretched string of tension $T$ and linear mass density $\\mu$."
  },

  "wave-particle duality": {
    formula: "\\lambda = \\frac{h}{p} = \\frac{h}{mv}, \\quad E = pc = hf \\text{ (photon)}, \\quad E = h\\nu",
    formula_description: "de Broglie hypothesis: all matter exhibits wave-like properties with wavelength $\\lambda = h/p$ where $p$ is momentum. Confirmed by electron diffraction. Photons exhibit both wave ($f, \\lambda$) and particle ($E, p$) nature."
  },

  "work function": {
    formula: "\\phi = hf_0, \\quad KE_{\\max} = hf - \\phi = eV_s, \\quad \\lambda_{\\max} = \\frac{hc}{\\phi}",
    formula_description: "Minimum energy required to eject an electron from a metal surface in the photoelectric effect. Threshold frequency $f_0 = \\phi/h$. Maximum kinetic energy of emitted electron is $KE_{\\max} = hf - \\phi$."
  }

};

/* ============================================================
   EXECUTION  –  runs across all three sections
============================================================ */
const SECTIONS = ['U', 'V', 'W'];
let totalMatches = 0;
let totalUpdated = 0;

SECTIONS.forEach(sec => {
  if (!dict[sec]) {
    console.warn(`Warning: Section ${sec} not found – skipping.`);
    return;
  }
  dict[sec].forEach(entry => {
    const wordKey = entry.word.trim().toLowerCase();
    if (enrichments[wordKey]) {
      totalMatches++;
      const enrich = enrichments[wordKey];

      entry.formula = enrich.formula;
      entry.formula_description = enrich.formula_description;

      const latexBlock = `\n\n$$\n${enrich.formula}\n$$\n*Formula:* ${enrich.formula_description}`;
      if (!entry.definition.includes('$$')) {
        entry.definition += latexBlock;
        totalUpdated++;
      }
    }
  });
});

console.log(`Matching U/V/W terms found: ${totalMatches} / ${Object.keys(enrichments).length}`);
console.log(`Updated entries: ${totalUpdated}`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log("Successfully updated dictionary.json with Sections U, V, W STEM formulas!");
