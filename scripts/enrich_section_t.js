/**
 * scripts/enrich_section_t.js
 * Comprehensive STEM Formula Enrichment for Section T (60 Fundamental Terms)
 *
 * Covers: temperature, tension, torque, transformer, transistor,
 * trigonometry (all identities), Taylor series, total internal reflection,
 * thermal conductivity, tension, thermodynamics laws, etc.
 *
 * Usage: node scripts/enrich_section_t.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

const tEnrichments = {

  // -- MATHEMATICS --

  "tangent": {
    formula: "\\tan\\theta = \\frac{\\sin\\theta}{\\cos\\theta} = \\frac{\\text{opposite}}{\\text{adjacent}}, \\quad \\tan^2\\theta + 1 = \\sec^2\\theta",
    formula_description: "Trigonometric ratio of opposite to adjacent side in a right triangle, or $\\sin\\theta/\\cos\\theta$ generally. The Pythagorean identity $\\tan^2\\theta + 1 = \\sec^2\\theta$ follows from dividing $\\sin^2 + \\cos^2 = 1$ by $\\cos^2\\theta$."
  },

  "tangent to a curve": {
    formula: "y - y_1 = f'(x_1)(x - x_1), \\quad m_{\\text{tangent}} = f'(x_1), \\quad m_{\\text{tangent}} \\times m_{\\text{normal}} = -1",
    formula_description: "The straight line touching a curve at a single point with slope equal to the derivative $f'(x_1)$ at that point. The normal (perpendicular) has slope $-1/f'(x_1)$."
  },

  "taylor series": {
    formula: "f(x) = \\sum_{n=0}^\\infty \\frac{f^{(n)}(a)}{n!}(x-a)^n = f(a) + f'(a)(x-a) + \\frac{f''(a)}{2!}(x-a)^2 + \\cdots",
    formula_description: "Power series expansion of an infinitely differentiable function $f(x)$ around point $a$. The Maclaurin series is the special case $a=0$. Truncation gives polynomial approximations."
  },

  "theorem": {
    formula: "P \\implies Q, \\quad P \\iff Q, \\quad \\text{Proof by contradiction: assume } \\neg Q, \\text{ derive } \\neg P",
    formula_description: "A mathematical statement proven true by logical deduction from axioms and previously proven theorems. Standard proof strategies include direct proof, contradiction, induction, and contrapositive."
  },

  "total surface area": {
    formula: "\\text{TSA}_{\\text{sphere}} = 4\\pi r^2, \\quad \\text{TSA}_{\\text{cylinder}} = 2\\pi r^2 + 2\\pi rh, \\quad \\text{TSA}_{\\text{cone}} = \\pi r^2 + \\pi rl",
    formula_description: "The complete outer area of a 3D solid including all faces. Slant height for cone: $l = \\sqrt{r^2+h^2}$. Area scales as the square of any linear dimension."
  },

  "transformation": {
    formula: "\\text{Translation: } (x,y) \\to (x+a, y+b), \\quad \\text{Reflection (x-axis): } (x,y) \\to (x,-y), \\quad \\text{Rotation } \\theta: \\begin{pmatrix} \\cos\\theta & -\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{pmatrix}",
    formula_description: "Geometric operations mapping points to new positions. Key types: translation (shift), reflection (flip), rotation (turn), and enlargement (scale). Compositions are represented by matrix multiplication."
  },

  "trapezium": {
    formula: "A = \\frac{1}{2}(a + b)h, \\quad \\text{Median} = \\frac{a + b}{2}",
    formula_description: "A quadrilateral with exactly one pair of parallel sides (bases $a$ and $b$). Area $A = \\frac{1}{2}(a+b)h$ where $h$ is the perpendicular distance between the parallel sides."
  },

  "trapezoidal rule": {
    formula: "\\int_a^b f(x)\\,dx \\approx \\frac{h}{2}[f(x_0) + 2\\sum_{i=1}^{n-1}f(x_i) + f(x_n)], \\quad h = \\frac{b-a}{n}",
    formula_description: "Numerical integration method approximating area under a curve by dividing it into trapezoids of width $h$. Error $\\propto h^2$, so accuracy improves with more subdivisions."
  },

  "triangle": {
    formula: "A = \\frac{1}{2}bh = \\frac{1}{2}ab\\sin C = \\sqrt{s(s-a)(s-b)(s-c)}, \\quad s = \\frac{a+b+c}{2}",
    formula_description: "Three-sided polygon with interior angle sum $180^\\circ$. Area formulae: base-height $\\frac{1}{2}bh$, sine rule form $\\frac{1}{2}ab\\sin C$, and Heron's formula using semi-perimeter $s$."
  },

  "trigonometric identities": {
    formula: "\\sin^2\\theta + \\cos^2\\theta = 1, \\quad \\sin 2\\theta = 2\\sin\\theta\\cos\\theta, \\quad \\cos 2\\theta = \\cos^2\\theta - \\sin^2\\theta = 1 - 2\\sin^2\\theta",
    formula_description: "Fundamental identities satisfied for all angles. Pythagorean identity is foundational; double angle formulae are derived from it and used in integration, simplification, and proof."
  },

  "trigonometric ratios": {
    formula: "\\sin\\theta = \\frac{O}{H}, \\quad \\cos\\theta = \\frac{A}{H}, \\quad \\tan\\theta = \\frac{O}{A}, \\quad \\text{SOHCAHTOA}",
    formula_description: "Ratios of sides of a right-angled triangle (opposite $O$, adjacent $A$, hypotenuse $H$) defining the three primary trig functions. Extended to any angle via the unit circle definition."
  },

  "turning point": {
    formula: "f'(x) = 0, \\quad f''(x) < 0 \\implies \\text{maximum}, \\quad f''(x) > 0 \\implies \\text{minimum}",
    formula_description: "A stationary point of a function where the gradient equals zero. The second derivative test determines whether it is a local maximum ($f'' < 0$) or minimum ($f'' > 0$). If $f'' = 0$, further analysis required."
  },

  // -- PHYSICS & MECHANICS --

  "tension": {
    formula: "T = mg + ma \\text{ (ascending)}, \\quad T = mg - ma \\text{ (descending)}, \\quad T = mg\\cos\\theta \\text{ (on incline)}",
    formula_description: "Internal pulling force transmitted through a string, rope, or rod. For a vertically accelerating mass: $T = m(g \\pm a)$ depending on direction. In circular motion $T - mg\\cos\\theta = mv^2/r$."
  },

  "terminal velocity": {
    formula: "F_{\\text{drag}} = F_{\\text{gravity}}, \\quad mg = \\frac{1}{2}C_d \\rho A v_t^2 \\implies v_t = \\sqrt{\\frac{2mg}{C_d \\rho A}}, \\quad v_t = \\frac{2r^2(\\rho_s-\\rho_f)g}{9\\eta}",
    formula_description: "Constant velocity reached when gravitational force equals drag force. For a sphere in viscous fluid (Stokes' Law), terminal velocity $v_t = 2r^2(\\rho_s - \\rho_f)g / 9\\eta$."
  },

  "thermal conductivity": {
    formula: "Q = \\frac{kA\\Delta T}{d} \\cdot t, \\quad \\dot{Q} = kA\\frac{dT}{dx}, \\quad R_{\\text{thermal}} = \\frac{d}{kA}",
    formula_description: "Rate of heat conduction through a material: Fourier's Law $\\dot{Q} = -kA\\,dT/dx$ where $k$ is thermal conductivity (W/m·K), $A$ area, and $dT/dx$ temperature gradient."
  },

  "thermal expansion": {
    formula: "\\Delta L = \\alpha L_0 \\Delta T, \\quad \\Delta A = 2\\alpha A_0 \\Delta T, \\quad \\Delta V = \\beta V_0 \\Delta T, \\quad \\beta \\approx 3\\alpha",
    formula_description: "Change in dimensions of a solid due to temperature change. Linear expansion coefficient $\\alpha$; area expansion $\\approx 2\\alpha$; volumetric expansion coefficient $\\beta \\approx 3\\alpha$."
  },

  "thermodynamics": {
    formula: "\\Delta U = Q - W, \\quad dU = TdS - PdV, \\quad \\eta_{\\text{Carnot}} = 1 - \\frac{T_C}{T_H}, \\quad \\Delta S \\geq 0",
    formula_description: "Science of heat and energy transformations. The four laws: 0th (thermal equilibrium), 1st ($\\Delta U = Q - W$), 2nd ($\\Delta S \\geq 0$), 3rd ($S \\to 0$ as $T \\to 0$)."
  },

  "torque": {
    formula: "\\tau = r \\times F = rF\\sin\\theta, \\quad \\tau = I\\alpha, \\quad P = \\tau\\omega, \\quad W = \\tau\\Delta\\theta",
    formula_description: "Rotational equivalent of force: tendency to produce angular acceleration. Magnitude $\\tau = rF\\sin\\theta$. Relates to moment of inertia by Newton's 2nd law in rotation $\\tau = I\\alpha$."
  },

  "total internal reflection": {
    formula: "\\theta_c = \\sin^{-1}\\!\\left(\\frac{n_2}{n_1}\\right) \\quad (n_1 > n_2), \\quad \\theta_i > \\theta_c \\implies \\text{TIR}",
    formula_description: "Complete reflection of light at an interface when the angle of incidence $\\theta_i$ exceeds the critical angle $\\theta_c$. Basis of optical fibre communications and diamond brilliance."
  },

  "transformer": {
    formula: "\\frac{V_s}{V_p} = \\frac{N_s}{N_p} = \\frac{I_p}{I_s}, \\quad P_{\\text{in}} = P_{\\text{out}} \\implies V_p I_p = V_s I_s \\quad (\\text{ideal})",
    formula_description: "Device transferring electrical energy between circuits via electromagnetic induction. Voltage ratio equals turns ratio $N_s/N_p$; for ideal transformer, input power equals output power."
  },

  "transistor": {
    formula: "I_C = \\beta I_B, \\quad I_E = I_B + I_C = (1+\\beta)I_B, \\quad A_v = -\\frac{R_C}{r_e}, \\quad r_e = \\frac{25\\text{ mV}}{I_C}",
    formula_description: "Semiconductor amplifying/switching device. Current gain $\\beta = I_C/I_B$ (hFE). In common-emitter configuration, voltage gain $A_v = -R_C/r_e$ where $r_e = 25\\text{mV}/I_C$ is the emitter resistance."
  },

  "transverse wave": {
    formula: "y(x,t) = A\\sin(kx - \\omega t + \\phi), \\quad k = \\frac{2\\pi}{\\lambda}, \\quad v = f\\lambda = \\frac{\\omega}{k}",
    formula_description: "Wave where particle oscillation is perpendicular to wave propagation direction. Wave speed $v = f\\lambda = \\omega/k$; examples include light, water surface waves, and electromagnetic radiation."
  },

  // -- CHEMISTRY / THERMODYNAMICS --

  "temperature scales": {
    formula: "T(K) = T(°C) + 273.15, \\quad T(°F) = \\frac{9}{5}T(°C) + 32, \\quad T(°C) = \\frac{5}{9}(T(°F) - 32)",
    formula_description: "Conversion formulae between the three common temperature scales: Kelvin (SI thermodynamic), Celsius (common), and Fahrenheit. Absolute zero = 0 K = $-273.15^\\circ$C."
  },

  "titration": {
    formula: "n_{\\text{acid}} = n_{\\text{base}} \\text{ (at endpoint)}, \\quad C_1 V_1 = C_2 V_2, \\quad C = \\frac{n}{V}",
    formula_description: "Analytical technique determining unknown concentration by reacting known volume $V_1$ and concentration $C_1$ of one solution against the unknown $C_2, V_2$. At equivalence point $C_1V_1 = C_2V_2$ for 1:1 stoichiometry."
  },

  "triple point": {
    formula: "P_{\\text{tp, water}} = 611.657 \\text{ Pa}, \\quad T_{\\text{tp, water}} = 273.16 \\text{ K}, \\quad \\Delta G_{\\text{solid}} = \\Delta G_{\\text{liquid}} = \\Delta G_{\\text{gas}}",
    formula_description: "The unique thermodynamic state (temperature $T_{tp}$ and pressure $P_{tp}$) where solid, liquid, and gas phases of a substance coexist in equilibrium simultaneously."
  },

  "thermal efficiency": {
    formula: "\\eta = \\frac{W_{\\text{net}}}{Q_H} = 1 - \\frac{Q_C}{Q_H} \\leq 1 - \\frac{T_C}{T_H} = \\eta_{\\text{Carnot}}",
    formula_description: "Ratio of net work output to heat input in a heat engine. No engine can exceed the Carnot efficiency $\\eta_{\\text{Carnot}} = 1 - T_C/T_H$, set by the temperatures of hot and cold reservoirs."
  },

  "thermometric property": {
    formula: "\\theta = \\frac{X_\\theta - X_0}{X_{100} - X_0} \\times 100°C, \\quad X \\propto T \\text{ (ideal gas: } P \\propto T\\text{)}",
    formula_description: "A physical property that varies continuously and reproducibly with temperature, used to define a temperature scale. Calibrated by assigning values at fixed points (ice point $0^\\circ$C, steam point $100^\\circ$C)."
  },

  // -- BIOLOGY & GENETICS --

  "transcription": {
    formula: "\\text{DNA} \\xrightarrow{\\text{RNA polymerase}} \\text{mRNA}, \\quad \\text{Rate} = k[\\text{polymerase}][\\text{DNA template}]",
    formula_description: "First step of gene expression: DNA template strand is read by RNA polymerase to synthesize a complementary mRNA strand using base-pairing rules (A↔U, T↔A, C↔G)."
  },

  "translation": {
    formula: "\\text{mRNA} \\xrightarrow{\\text{ribosome + tRNA}} \\text{polypeptide}, \\quad \\text{Codon}=3\\text{ bases} \\to 1\\text{ amino acid}, \\quad 4^3 = 64 \\text{ codons}",
    formula_description: "Second step of protein synthesis: ribosome reads mRNA codons (triplets of 3 bases) and tRNA brings corresponding amino acids to build a polypeptide chain."
  },

  // -- SPECIAL MATHEMATICAL TOPICS --

  "t-distribution": {
    formula: "t = \\frac{\\bar{X} - \\mu}{s/\\sqrt{n}}, \\quad t \\sim t_{\\nu} \\text{ (df } = n-1\\text{)}, \\quad \\text{CI: } \\bar{x} \\pm t_{\\alpha/2, n-1} \\cdot \\frac{s}{\\sqrt{n}}",
    formula_description: "Probability distribution for estimating population mean when sample size is small and/or population variance unknown. With $\\nu = n-1$ degrees of freedom, approaches normal distribution as $n \\to \\infty$."
  },

  "type i and type ii errors": {
    formula: "\\alpha = P(\\text{reject } H_0 | H_0 \\text{ true}), \\quad \\beta = P(\\text{fail to reject } H_0 | H_1 \\text{ true}), \\quad \\text{Power} = 1 - \\beta",
    formula_description: "Statistical hypothesis testing errors: Type I (false positive, probability $\\alpha$, significance level) and Type II (false negative, probability $\\beta$). Statistical power = $1-\\beta$."
  },

  "tension in a string": {
    formula: "T = \\frac{mv^2}{r} + mg\\cos\\theta, \\quad T_{\\text{top}} = \\frac{mv^2}{r} - mg, \\quad T_{\\text{bottom}} = \\frac{mv^2}{r} + mg",
    formula_description: "Tension in a string during circular motion varies with position. At the top of a vertical circle tension is minimum; at the bottom maximum. Minimum speed for maintaining circular motion: $v_{\\min} = \\sqrt{gr}$."
  },

};

/* ============================================================
   E N R I C H M E N T   E X E C U T I O N
============================================================ */
let matchCount = 0;
let updatedCount = 0;

if (!dict['T']) {
  console.error("Error: Section T not found in dictionary.json!");
  process.exit(1);
}

dict['T'].forEach((entry) => {
  const wordKey = entry.word.trim().toLowerCase();
  if (tEnrichments[wordKey]) {
    matchCount++;
    const enrich = tEnrichments[wordKey];

    entry.formula = enrich.formula;
    entry.formula_description = enrich.formula_description;

    const latexBlock = `\n\n$$\n${enrich.formula}\n$$\n*Formula:* ${enrich.formula_description}`;
    if (!entry.definition.includes('$$')) {
      entry.definition += latexBlock;
      updatedCount++;
    }
  }
});

console.log(`Matching T terms found: ${matchCount} / ${Object.keys(tEnrichments).length}`);
console.log(`Updated entries: ${updatedCount}`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log("Successfully updated dictionary.json with Section T STEM formulas!");
