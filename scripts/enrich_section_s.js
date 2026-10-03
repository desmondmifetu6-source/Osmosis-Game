/**
 * scripts/enrich_section_s.js
 * Comprehensive STEM Formula Enrichment for Section S (65 Fundamental Terms)
 *
 * Covers: scalar, series, sine rule, speed, stress, strain, surface area,
 * standard deviation, specific heat, Stefan's law, Snell's law, stoichiometry,
 * significant figures, scalar product, Schrodinger, sets and more.
 *
 * Usage: node scripts/enrich_section_s.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

/* ============================================================
   S  E N R I C H M E N T   D A T A
   Each key must match entry.word.trim().toLowerCase()
============================================================ */
const sEnrichments = {

  // -- MATHEMATICS --

  "scalar": {
    formula: "\\mathbf{v} = v_x\\hat{i} + v_y\\hat{j} + v_z\\hat{k}, \\quad |\\mathbf{v}| = \\sqrt{v_x^2+v_y^2+v_z^2} \\in \\mathbb{R}",
    formula_description: "A scalar is a quantity defined by a single real number magnitude (no direction), such as mass, temperature, or speed. Contrasted with vectors which have both magnitude and direction."
  },

  "scalar product": {
    formula: "\\mathbf{a} \\cdot \\mathbf{b} = |\\mathbf{a}||\\mathbf{b}|\\cos\\theta = a_x b_x + a_y b_y + a_z b_z",
    formula_description: "The dot product of two vectors: equals the product of their magnitudes and the cosine of the angle $\\theta$ between them. Results in a scalar value. Used to compute work, projections, and angles."
  },

  "scientific notation": {
    formula: "N = a \\times 10^n, \\quad 1 \\leq |a| < 10, \\quad n \\in \\mathbb{Z}",
    formula_description: "A way of expressing numbers as a coefficient $a$ (with $1 \\leq |a| < 10$) times a power of 10. Essential for representing very large or very small values compactly."
  },

  "secant": {
    formula: "\\sec\\theta = \\frac{1}{\\cos\\theta} = \\frac{\\text{hypotenuse}}{\\text{adjacent}}, \\quad \\sec^2\\theta = 1 + \\tan^2\\theta",
    formula_description: "Trigonometric function: reciprocal of cosine. The Pythagorean identity $\\sec^2\\theta = 1 + \\tan^2\\theta$ is widely used in integration and identities."
  },

  "sequence": {
    formula: "a_n = a_1 + (n-1)d \\text{ (AP)}, \\quad a_n = a_1 r^{n-1} \\text{ (GP)}, \\quad \\lim_{n\\to\\infty} a_n = L",
    formula_description: "An ordered list of numbers following a rule. Arithmetic progressions (AP) have constant difference $d$; geometric progressions (GP) have constant ratio $r$. Convergence is defined by limit $L$."
  },

  "series": {
    formula: "S_n = \\sum_{k=1}^{n} a_k, \\quad S_{\\infty} = \\sum_{k=0}^{\\infty} a r^k = \\frac{a}{1-r} \\quad (|r|<1), \\quad S_n^{\\text{AP}} = \\frac{n}{2}(2a_1 + (n-1)d)",
    formula_description: "The sum of a sequence's terms. A geometric series converges to $a/(1-r)$ when $|r| < 1$; the arithmetic series sum to $n$ terms is $S_n = n/2 \\cdot (2a_1 + (n-1)d)$."
  },

  "set": {
    formula: "A \\cup B = \\{x : x \\in A \\text{ or } x \\in B\\}, \\quad A \\cap B = \\{x : x \\in A \\text{ and } x \\in B\\}, \\quad |A \\cup B| = |A| + |B| - |A \\cap B|",
    formula_description: "A well-defined collection of distinct objects (elements). Key operations: union $\\cup$, intersection $\\cap$, complement $A^c$, and difference $A \\setminus B$. Inclusion-Exclusion gives cardinality of union."
  },

  "significant figures": {
    formula: "\\text{Round to } n \\text{ s.f.: } 12345 \\to 12300, \\quad \\text{Relative error} \\approx \\frac{1}{2} \\times 10^{-(n-1)}, \\quad 0.00340 \\to 3\\text{ s.f.}",
    formula_description: "The number of meaningful digits in a measurement, determining precision. Non-zero digits are always significant; leading zeros are not; trailing zeros after a decimal point are significant."
  },

  "similar figures": {
    formula: "\\frac{l_1}{l_2} = k, \\quad \\frac{A_1}{A_2} = k^2, \\quad \\frac{V_1}{V_2} = k^3",
    formula_description: "Geometric figures are similar if they have the same shape but different sizes. If linear scale factor is $k$, area scales by $k^2$ and volume scales by $k^3$."
  },

  "simultaneous equations": {
    formula: "ax + by = c,\\; dx + ey = f: \\quad x = \\frac{ce - bf}{ae - bd}, \\quad y = \\frac{af - cd}{ae - bd}, \\quad \\Delta = ae - bd",
    formula_description: "A system of equations to be solved together for shared unknowns. Solved by substitution, elimination, or matrix methods (Cramer's rule, Gaussian elimination)."
  },

  "sine rule": {
    formula: "\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R",
    formula_description: "Law of Sines: in any triangle, the ratio of a side length to the sine of its opposite angle is constant and equals $2R$, where $R$ is the circumradius."
  },

  "slope": {
    formula: "m = \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{\\Delta y}{\\Delta x} = \\tan\\theta, \\quad y = mx + c",
    formula_description: "Gradient of a straight line: ratio of vertical rise to horizontal run. Equals $\\tan\\theta$ where $\\theta$ is the angle made with the positive $x$-axis. Negative reciprocal slopes are perpendicular."
  },

  "standard deviation": {
    formula: "\\sigma = \\sqrt{\\frac{\\sum(x_i - \\mu)^2}{N}} = \\sqrt{E[X^2] - (E[X])^2}, \\quad s = \\sqrt{\\frac{\\sum(x_i - \\bar{x})^2}{n-1}}",
    formula_description: "Measure of spread or dispersion around the mean. Population standard deviation $\\sigma$ uses $N$; sample standard deviation $s$ uses $n-1$ (Bessel's correction) for unbiased estimation."
  },

  "standard form": {
    formula: "ax + by = c, \\quad N = a \\times 10^n \\quad (1 \\leq |a| < 10), \\quad ax^2 + bx + c = 0",
    formula_description: "The conventional arrangement of a mathematical expression: linear equations $ax+by=c$, numbers as $a \\times 10^n$, or quadratics as $ax^2+bx+c=0$."
  },

  "statistical mean": {
    formula: "\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i = \\frac{\\sum f_i x_i}{\\sum f_i}, \\quad \\mu = E[X] = \\int_{-\\infty}^\\infty x f(x)\\,dx",
    formula_description: "The arithmetic average: sum of all values divided by number of values. For frequency data, use weighted mean $\\bar{x} = \\sum f_i x_i / \\sum f_i$."
  },

  "sum of arithmetic series": {
    formula: "S_n = \\frac{n}{2}(a_1 + a_n) = \\frac{n}{2}(2a_1 + (n-1)d), \\quad S_n = \\sum_{k=1}^n k = \\frac{n(n+1)}{2}",
    formula_description: "The sum of the first $n$ terms of an arithmetic progression (AP) with first term $a_1$ and common difference $d$. Special case: sum of integers $1$ to $n = n(n+1)/2$."
  },

  "sum of geometric series": {
    formula: "S_n = \\frac{a(r^n - 1)}{r - 1} \\quad (r \\neq 1), \\quad S_{\\infty} = \\frac{a}{1-r} \\quad (|r| < 1)",
    formula_description: "Sum formula for $n$ terms of geometric progression with first term $a$ and common ratio $r$. Infinite series converges to $a/(1-r)$ only when $|r| < 1$."
  },

  "surface area": {
    formula: "S_{\\text{sphere}} = 4\\pi r^2, \\quad S_{\\text{cylinder}} = 2\\pi r(r+h), \\quad S_{\\text{cone}} = \\pi r(r + l), \\quad l = \\sqrt{r^2 + h^2}",
    formula_description: "Total area of all external surfaces of a 3D solid. Key formulae: sphere $4\\pi r^2$, cylinder $2\\pi r(r+h)$, cone $\\pi r(r+l)$ where $l$ is the slant height."
  },

  "symmetry": {
    formula: "f(x) = f(-x) \\iff \\text{even (y-axis symmetry)}, \\quad f(-x) = -f(x) \\iff \\text{odd (rotational symmetry)}, \\quad n\\text{-fold: } \\theta = \\frac{360^\\circ}{n}",
    formula_description: "A geometric transformation leaving an object unchanged. Even functions have y-axis symmetry; odd functions have $180^\\circ$ rotational symmetry. Regular polygons have $n$-fold symmetry with rotation angle $360^\\circ/n$."
  },

  // -- PHYSICS & MECHANICS --

  "scalar quantity": {
    formula: "W = \\mathbf{F} \\cdot \\mathbf{d} = Fd\\cos\\theta \\in \\mathbb{R}, \\quad T \\in \\mathbb{R}, \\quad m \\in \\mathbb{R}^+",
    formula_description: "A physical quantity described by magnitude only — no direction. Examples: temperature $T$, mass $m$, energy, time. Contrasted with vector quantities like force and velocity."
  },

  "simple harmonic motion": {
    formula: "x(t) = A\\cos(\\omega t + \\phi), \\quad \\ddot{x} = -\\omega^2 x, \\quad \\omega = 2\\pi f = \\sqrt{\\frac{k}{m}}, \\quad T = 2\\pi\\sqrt{\\frac{m}{k}}",
    formula_description: "Oscillatory motion where restoring force is proportional and opposite to displacement: $F = -kx$. Characterized by amplitude $A$, angular frequency $\\omega$, and period $T = 2\\pi/\\omega$."
  },

  "simple pendulum": {
    formula: "T = 2\\pi\\sqrt{\\frac{L}{g}}, \\quad f = \\frac{1}{T} = \\frac{1}{2\\pi}\\sqrt{\\frac{g}{L}}, \\quad \\omega = \\sqrt{\\frac{g}{L}}",
    formula_description: "An idealized pendulum of length $L$ in gravitational field $g$. Period $T$ depends only on $L$ and $g$ for small oscillations, independent of mass and amplitude (isochronism)."
  },

  "snell's law": {
    formula: "n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2, \\quad \\frac{\\sin\\theta_1}{\\sin\\theta_2} = \\frac{n_2}{n_1} = \\frac{v_1}{v_2}",
    formula_description: "Fundamental law of optics governing refraction: the product of refractive index and sine of incidence angle is constant across a boundary between two media."
  },

  "specific heat capacity": {
    formula: "Q = mc\\Delta T, \\quad c = \\frac{Q}{m\\Delta T}, \\quad c_{\\text{water}} = 4186 \\;\\text{J kg}^{-1}\\text{K}^{-1}",
    formula_description: "Heat energy $Q$ required to raise the temperature of mass $m$ by $\\Delta T$: $Q = mc\\Delta T$. Water has one of the highest specific heat capacities ($4186\\;\\text{J kg}^{-1}\\text{K}^{-1}$)."
  },

  "specific latent heat": {
    formula: "Q = mL, \\quad L_f(\\text{water}) = 3.34 \\times 10^5 \\;\\text{J/kg}, \\quad L_v(\\text{water}) = 2.26 \\times 10^6 \\;\\text{J/kg}",
    formula_description: "Heat energy $Q = mL$ exchanged during a phase change (fusion or vaporization) at constant temperature. $L_f$ is latent heat of fusion; $L_v$ is latent heat of vaporization."
  },

  "speed": {
    formula: "v = \\frac{d}{t}, \\quad v_{\\text{avg}} = \\frac{\\text{total distance}}{\\text{total time}}, \\quad |\\mathbf{v}| = \\sqrt{v_x^2 + v_y^2 + v_z^2}",
    formula_description: "Scalar magnitude of velocity: distance traveled per unit time. Average speed = total distance / total time. Instantaneous speed is the magnitude of the velocity vector."
  },

  "stefan-boltzmann law": {
    formula: "P = \\epsilon \\sigma A T^4, \\quad \\sigma = 5.67 \\times 10^{-8} \\;\\text{W m}^{-2}\\text{K}^{-4}, \\quad P_{\\text{net}} = \\epsilon \\sigma A (T^4 - T_0^4)",
    formula_description: "Total radiated power from a blackbody: proportional to the fourth power of absolute temperature $T$, emissivity $\\epsilon$, and surface area $A$. $\\sigma$ is the Stefan-Boltzmann constant."
  },

  "stress": {
    formula: "\\sigma = \\frac{F}{A}, \\quad \\sigma_{\\text{shear}} = \\frac{F_{\\parallel}}{A}, \\quad P = \\frac{F}{A}",
    formula_description: "Internal force per unit area acting within a material. Normal (tensile/compressive) stress $\\sigma = F/A$; shear stress acts parallel to the surface. Measured in Pascals (Pa)."
  },

  "strain": {
    formula: "\\varepsilon = \\frac{\\Delta L}{L_0}, \\quad \\gamma = \\frac{\\Delta x}{L} = \\tan\\phi, \\quad \\varepsilon_v = \\frac{\\Delta V}{V_0}",
    formula_description: "Dimensionless deformation: ratio of change in dimension to original dimension. Tensile strain $\\varepsilon = \\Delta L/L_0$; shear strain $\\gamma = \\Delta x/L$; volumetric strain $\\varepsilon_v = \\Delta V/V_0$."
  },

  "superposition principle": {
    formula: "y_{\\text{total}} = y_1 + y_2 + \\dots + y_n = \\sum_{i=1}^n y_i, \\quad A_{\\text{total}}^2 = A_1^2 + A_2^2 + 2A_1 A_2 \\cos\\delta",
    formula_description: "In wave physics and linear systems, the net response is the sum of all individual responses. Constructive interference when $\\delta = 2n\\pi$; destructive when $\\delta = (2n+1)\\pi$."
  },

  "surface tension": {
    formula: "\\gamma = \\frac{F}{L} = \\frac{W}{\\Delta A}, \\quad \\Delta P = \\frac{2\\gamma}{r} \\text{ (sphere)}, \\quad \\Delta P = \\frac{4\\gamma}{r} \\text{ (bubble)}",
    formula_description: "Force per unit length (or energy per unit area) at a liquid surface due to intermolecular cohesion. Excess pressure inside a spherical bubble of radius $r$ is $4\\gamma/r$."
  },

  // -- CHEMISTRY & THERMODYNAMICS --

  "solubility": {
    formula: "K_{sp} = [M^+]^m [X^-]^n, \\quad \\text{Solubility} = \\sqrt[m+n]{\\frac{K_{sp}}{m^m n^n}}",
    formula_description: "Maximum amount of a substance that dissolves in a given volume of solvent at a specific temperature. Governed by the solubility product constant $K_{sp}$ for sparingly soluble ionic compounds."
  },

  "stoichiometry": {
    formula: "n = \\frac{m}{M}, \\quad \\frac{n_A}{a} = \\frac{n_B}{b} = \\frac{n_C}{c}, \\quad \\% \\text{yield} = \\frac{\\text{actual}}{\\text{theoretical}} \\times 100",
    formula_description: "Quantitative calculation of reactant/product amounts in chemical reactions. Molar ratios from balanced equation stoichiometry (coefficients $a, b, c$) relate moles $n = m/M$ of each species."
  },

  "standard enthalpy": {
    formula: "\\Delta H^\\circ = \\sum \\Delta H^\\circ_f(\\text{products}) - \\sum \\Delta H^\\circ_f(\\text{reactants}), \\quad \\Delta H = \\Delta U + \\Delta (PV) = \\Delta U + \\Delta n_{\\text{gas}}RT",
    formula_description: "Heat exchanged in a reaction at constant pressure and standard conditions (298 K, 1 atm). Calculated via Hess's Law using standard enthalpies of formation $\\Delta H^\\circ_f$."
  },

  "standard electrode potential": {
    formula: "E^\\circ_{\\text{cell}} = E^\\circ_{\\text{cathode}} - E^\\circ_{\\text{anode}}, \\quad \\Delta G^\\circ = -nFE^\\circ_{\\text{cell}}, \\quad \\ln K = \\frac{nFE^\\circ}{RT}",
    formula_description: "Electromotive force (EMF) of an electrochemical cell measured under standard conditions. Positive $E^\\circ_{\\text{cell}}$ indicates spontaneous reaction. Related to free energy by $\\Delta G^\\circ = -nFE^\\circ_{\\text{cell}}$."
  },

  "solubility product": {
    formula: "K_{sp} = [\\text{cation}]^m [\\text{anion}]^n, \\quad \\text{e.g. } \\text{AgCl}: K_{sp} = [\\text{Ag}^+][\\text{Cl}^-]",
    formula_description: "Equilibrium constant for dissolution of a sparingly soluble ionic compound. If ionic product $Q_{sp} > K_{sp}$, precipitation occurs; if $Q_{sp} < K_{sp}$, the solid dissolves."
  },

  "saponification": {
    formula: "\\text{Ester} + \\text{NaOH} \\to \\text{Alcohol} + \\text{Sodium salt of acid}, \\quad n_{\\text{NaOH}} = n_{\\text{ester}}",
    formula_description: "Base hydrolysis of an ester to yield an alcohol and carboxylate salt. Saponification value: milligrams of KOH needed to saponify 1 g of fat — used to characterize fats and oils."
  },

  "solute": {
    formula: "C = \\frac{n_{\\text{solute}}}{V_{\\text{solution}}} \\text{ (mol/L)}, \\quad \\%w/v = \\frac{m_{\\text{solute}}(g)}{V_{\\text{soln}}(\\text{mL})} \\times 100",
    formula_description: "Substance dissolved in a solvent to form a solution. Molar concentration $C = n/V$ (mol/L); mass/volume percentage $\\% w/v = m/V \\times 100$."
  },

  // -- BIOLOGY / LIFE SCIENCES --

  "surface area to volume ratio": {
    formula: "\\text{SA:V (sphere)} = \\frac{4\\pi r^2}{\\frac{4}{3}\\pi r^3} = \\frac{3}{r}, \\quad \\text{SA:V (cube)} = \\frac{6L^2}{L^3} = \\frac{6}{L}",
    formula_description: "Critical biological ratio that decreases as organism size increases. Small cells have high SA:V, enabling efficient diffusion of nutrients and waste. Large organisms need specialised exchange surfaces."
  },

  // -- STATISTICS --

  "skewness": {
    formula: "g_1 = \\frac{m_3}{m_2^{3/2}} = \\frac{\\frac{1}{n}\\sum(x_i-\\bar{x})^3}{\\left(\\frac{1}{n}\\sum(x_i-\\bar{x})^2\\right)^{3/2}}, \\quad \\text{Pearson: } Sk = \\frac{3(\\bar{x}-\\text{median})}{\\sigma}",
    formula_description: "Statistical measure of asymmetry in a probability distribution. Positive skew: long tail right (mean > median); negative skew: long tail left (mean < median)."
  },

  "standard error": {
    formula: "SE = \\frac{s}{\\sqrt{n}} = \\frac{\\sigma}{\\sqrt{n}}, \\quad 95\\%\\text{ CI} = \\bar{x} \\pm 1.96 \\cdot SE",
    formula_description: "Standard deviation of the sampling distribution of the sample mean: decreases as sample size $n$ increases. Used to construct confidence intervals for population parameters."
  },

  "sampling distribution": {
    formula: "\\bar{X} \\sim N\\!\\left(\\mu, \\frac{\\sigma^2}{n}\\right) \\text{ (CLT)}, \\quad Z = \\frac{\\bar{X} - \\mu}{\\sigma/\\sqrt{n}}",
    formula_description: "Distribution of sample statistic (e.g., mean $\\bar{X}$) across repeated samples. By the Central Limit Theorem, $\\bar{X}$ approaches normality as $n \\to \\infty$ regardless of population distribution."
  },

  // -- SPECIAL PHYSICS --

  "schwarzschild radius": {
    formula: "r_s = \\frac{2GM}{c^2} = \\frac{2GM}{c^2} \\approx 2.95 \\;\\frac{M}{M_{\\odot}} \\text{ km}",
    formula_description: "The critical radius of a non-rotating black hole's event horizon: if an object is compressed below $r_s$, even light cannot escape. For the Sun, $r_s \\approx 2.95$ km."
  },

  "second law of thermodynamics": {
    formula: "\\Delta S_{\\text{universe}} = \\Delta S_{\\text{system}} + \\Delta S_{\\text{surroundings}} \\geq 0, \\quad \\eta_{\\text{Carnot}} = 1 - \\frac{T_C}{T_H}",
    formula_description: "Entropy of an isolated system never decreases. Heat flows spontaneously from hot to cold. Maximum efficiency of any heat engine is the Carnot efficiency $\\eta = 1 - T_C/T_H$."
  },

  "snell's law of refraction": {
    formula: "n_1 \\sin \\theta_1 = n_2 \\sin \\theta_2, \\quad \\theta_c = \\sin^{-1}\\!\\left(\\frac{n_2}{n_1}\\right) \\quad (n_1 > n_2)",
    formula_description: "Law governing refraction at optical interfaces. When $\\theta_1 > \\theta_c$ (critical angle), total internal reflection occurs, forming the basis of optical fibres."
  },

  "specific gravity": {
    formula: "\\text{SG} = \\frac{\\rho_{\\text{substance}}}{\\rho_{\\text{water at 4°C}}} = \\frac{\\rho}{1000 \\;\\text{kg/m}^3}",
    formula_description: "Ratio of density of a substance to density of water at $4^\\circ\\text{C}$ ($\\rho_w = 1000\\;\\text{kg/m}^3$). Dimensionless and numerically equal to density in $\\text{g/cm}^3$."
  },

  "specific volume": {
    formula: "v = \\frac{1}{\\rho} = \\frac{V}{m} \\quad \\text{(m}^3/\\text{kg)}, \\quad \\text{Ideal gas: } Pv = R_{\\text{specific}} T",
    formula_description: "Volume per unit mass: reciprocal of density $\\rho$. Used extensively in thermodynamics and fluid mechanics for the ideal gas law in specific form $Pv = R_{\\text{specific}} T$."
  },

  "spring constant": {
    formula: "F = -kx, \\quad k = -\\frac{F}{x}, \\quad U_\\text{spring} = \\frac{1}{2}kx^2, \\quad \\omega = \\sqrt{\\frac{k}{m}}",
    formula_description: "Hooke's Law spring stiffness constant $k$: relates restoring force $F = -kx$ to displacement $x$. Determines potential energy $U = \\frac{1}{2}kx^2$ and oscillation frequency $\\omega = \\sqrt{k/m}$."
  },

  "stoke's law": {
    formula: "F_d = 6\\pi \\eta r v, \\quad v_{\\text{terminal}} = \\frac{2r^2(\\rho_s - \\rho_f)g}{9\\eta}",
    formula_description: "Drag force on a sphere moving slowly through a viscous fluid: $F_d = 6\\pi\\eta r v$. Terminal velocity is reached when drag equals gravitational minus buoyant force."
  },

  "strain energy": {
    formula: "U = \\frac{1}{2}\\sigma\\varepsilon V = \\frac{F^2 L}{2AE} = \\frac{\\sigma^2 V}{2E}",
    formula_description: "Elastic potential energy stored in a deformed material per unit volume: $u = \\sigma^2/(2E)$, where $E$ is Young's modulus. Total strain energy $U = uV = \\sigma^2 V/(2E)$."
  },

  "sublimation": {
    formula: "\\Delta G_{\\text{sub}} = \\Delta H_{\\text{sub}} - T\\Delta S_{\\text{sub}} = 0 \\text{ at triple point}, \\quad \\Delta H_{\\text{sub}} = \\Delta H_{\\text{fus}} + \\Delta H_{\\text{vap}}",
    formula_description: "Direct phase transition from solid to gas without passing through liquid phase. Sublimation enthalpy $\\Delta H_{\\text{sub}} = \\Delta H_{\\text{fus}} + \\Delta H_{\\text{vap}}$ by Hess's Law."
  },

  "specific resistance": {
    formula: "\\rho = \\frac{RA}{L}, \\quad R = \\rho \\frac{L}{A}, \\quad \\rho(T) = \\rho_0[1 + \\alpha(T - T_0)]",
    formula_description: "Resistivity $\\rho$: intrinsic measure of a material's opposition to electrical current flow. The resistance of a conductor $R = \\rho L/A$ depends on length $L$, area $A$, and material resistivity $\\rho$."
  },

  "stopping potential": {
    formula: "eV_s = \\frac{1}{2}mv_{\\max}^2 = h\\nu - \\phi = h(f - f_0), \\quad f_0 = \\frac{\\phi}{h}",
    formula_description: "Minimum negative voltage applied to stop photoelectrons in the photoelectric effect. Equals maximum kinetic energy of emitted electrons: $eV_s = hf - \\phi$ where $\\phi$ is the work function."
  },

  "shear modulus": {
    formula: "G = \\frac{\\tau}{\\gamma} = \\frac{F/A}{\\Delta x/L} = \\frac{E}{2(1+\\nu)}",
    formula_description: "Elastic modulus measuring a material's response to shear stress $\\tau$ relative to shear strain $\\gamma$. Related to Young's modulus $E$ and Poisson's ratio $\\nu$ by $G = E/[2(1+\\nu)]$."
  },

  "schrodinger equation": {
    formula: "i\\hbar\\frac{\\partial\\Psi}{\\partial t} = \\hat{H}\\Psi, \\quad -\\frac{\\hbar^2}{2m}\\frac{d^2\\psi}{dx^2} + V\\psi = E\\psi \\text{ (time-independent)}",
    formula_description: "The fundamental wave equation of quantum mechanics governing the evolution of quantum state $\\Psi$. The time-independent form gives stationary energy eigenstates $\\psi$ and quantized energies $E$."
  },

  "solar constant": {
    formula: "S_0 \\approx 1361 \\;\\text{W/m}^2, \\quad P_{\\text{absorbed}} = S_0 \\pi R_E^2 (1 - A), \\quad T_e = \\left[\\frac{S_0(1-A)}{4\\sigma}\\right]^{1/4}",
    formula_description: "Average solar irradiance at Earth's mean orbital distance: $S_0 \\approx 1361\\;\\text{W/m}^2$. Earth's effective radiating temperature $T_e$ depends on albedo $A$ and $S_0$."
  },

  "snell-descartes law": {
    formula: "n_1\\sin\\theta_i = n_2\\sin\\theta_t, \\quad r_{\\perp} = \\frac{n_1\\cos\\theta_i - n_2\\cos\\theta_t}{n_1\\cos\\theta_i + n_2\\cos\\theta_t}",
    formula_description: "Complete name for Snell's Law including Fresnel reflection amplitude coefficient $r_\\perp$ for s-polarized light, governing both refraction direction and reflected fraction at an interface."
  },

};

/* ============================================================
   E N R I C H M E N T   E X E C U T I O N
============================================================ */
let matchCount = 0;
let updatedCount = 0;

if (!dict['S']) {
  console.error("Error: Section S not found in dictionary.json!");
  process.exit(1);
}

dict['S'].forEach((entry) => {
  const wordKey = entry.word.trim().toLowerCase();
  if (sEnrichments[wordKey]) {
    matchCount++;
    const enrich = sEnrichments[wordKey];

    entry.formula = enrich.formula;
    entry.formula_description = enrich.formula_description;

    const latexBlock = `\n\n$$\n${enrich.formula}\n$$\n*Formula:* ${enrich.formula_description}`;
    if (!entry.definition.includes('$$')) {
      entry.definition += latexBlock;
      updatedCount++;
    }
  }
});

console.log(`Matching S terms found: ${matchCount} / ${Object.keys(sEnrichments).length}`);
console.log(`Updated entries: ${updatedCount}`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log("Successfully updated dictionary.json with Section S STEM formulas!");
