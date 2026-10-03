/**
 * scripts/enrich_section_r.js
 * Comprehensive STEM Formula Enrichment for Section R (65 Fundamental Terms)
 *
 * Covers: radiation, decay, radius, Raman effect, Raoult's law, rate laws,
 * reaction kinetics, refraction, resistance, resistivity, Reynolds number,
 * Rydberg formula, Riemann integrals, Rolle's theorem, RMS speeds, etc.
 *
 * Usage: node scripts/enrich_section_r.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

/* ============================================================
   R  E N R I C H M E N T   D A T A
   Each key must match entry.word.trim().toLowerCase()
============================================================ */
const rEnrichments = {

  // -- MATHEMATICS & CALCULUS --

  "radian": {
    formula: "\\theta = \\frac{s}{r}, \\quad 1\\text{ rad} = \\frac{180^\\circ}{\\pi} \\approx 57.2958^\\circ, \\quad 2\\pi\\text{ rad} = 360^\\circ",
    formula_description: "The standard unit of angular measure: the angle subtended at the center of a circle by an arc equal in length to the radius $r$. Converted to degrees by multiplying by $180/\\pi$."
  },

  "radian measure": {
    formula: "\\theta = \\frac{\\text{arc length}}{\\text{radius}} = \\frac{s}{r}, \\quad s = r\\theta, \\quad A_{\\text{sector}} = \\frac{1}{2}r^2\\theta",
    formula_description: "The measure of a central angle in radians: arc length $s = r\\theta$ and sector area $A = \\frac{1}{2}r^2\\theta$ for angle $\\theta$ measured in radians."
  },

  "radicand": {
    formula: "\\sqrt[n]{x} = a \\iff a^n = x, \\quad \\sqrt[n]{x^m} = x^{m/n}, \\quad \\sqrt[n]{ab} = \\sqrt[n]{a}\\cdot\\sqrt[n]{b}",
    formula_description: "The number or expression $x$ under a radical sign $\\sqrt[n]{x}$. If $n$ is even, $x \\geq 0$ for real outputs; exponent rules dictate $\\sqrt[n]{x^m} = x^{m/n}$."
  },

  "radix": {
    formula: "N = \\sum_{i=-m}^{n-1} d_i \\cdot b^i = d_{n-1}b^{n-1} + \\dots + d_0 b^0 + d_{-1}b^{-1} + \\dots + d_{-m}b^{-m}",
    formula_description: "The base $b$ of a positional numeral system (e.g., $b=10$ decimal, $b=2$ binary, $b=16$ hexadecimal). Determines the number of unique digits and the power-of-$b$ weight of each digit position."
  },

  "random variable": {
    formula: "E[X] = \\sum_{i} x_i p(x_i) \\text{ or } \\int_{-\\infty}^{\\infty} x f(x)dx, \\quad \\text{Var}(X) = E[X^2] - (E[X])^2 = \\sigma^2",
    formula_description: "A numerical variable $X$ whose values depend on outcomes of a random phenomenon. Characterized by its probability mass function $p(x)$ (discrete) or probability density function $f(x)$ (continuous), with mean $E[X]$ and variance $\\text{Var}(X)$."
  },

  "rank of a matrix": {
    formula: "\\text{rank}(A) = \\text{dim}(\\text{col}(A)) = \\text{dim}(\\text{row}(A)), \\quad \\text{rank}(A) + \\text{nullity}(A) = n",
    formula_description: "The maximum number of linearly independent column (or row) vectors in matrix $A$. The Rank-Nullity Theorem states that for an $m \\times n$ matrix $A$, $\\text{rank}(A) + \\text{nullity}(A) = n$."
  },

  "ratio": {
    formula: "a : b = \\frac{a}{b}, \\quad \\frac{a}{b} = \\frac{c}{d} \\iff ad = bc, \\quad \\text{Ratio of areas} = \\left(\\frac{a}{b}\\right)^2",
    formula_description: "A quantitative relation showing the number of times one value contains or is contained within another. A proportion $a/b = c/d$ asserts equality of two ratios."
  },

  "ratio test": {
    formula: "L = \\lim_{n \\to \\infty} \\left| \\frac{a_{n+1}}{a_n} \\right|: \\quad L < 1 \\implies \\text{converges absolutely}, \\quad L > 1 \\implies \\text{diverges}",
    formula_description: "D'Alembert's convergence test for infinite series $\\sum a_n$: if $L < 1$ the series converges absolutely, if $L > 1$ it diverges, and if $L = 1$ the test is inconclusive."
  },

  "rational function": {
    formula: "f(x) = \\frac{P(x)}{Q(x)}, \\quad Q(x) \\neq 0, \\quad \\text{Vertical asymptotes at } Q(x) = 0",
    formula_description: "Any function defined as the quotient of two polynomial functions $P(x)$ and $Q(x)$. Discontinuities and vertical asymptotes occur at roots of the denominator $Q(x)=0$ not shared by $P(x)$."
  },

  "reciprocal": {
    formula: "x \\cdot \\frac{1}{x} = 1 \\quad (x \\neq 0), \\quad \\left(\\frac{a}{b}\\right)^{-1} = \\frac{b}{a}, \\quad f(x) = x^{-1}",
    formula_description: "The multiplicative inverse of a number $x$: a quantity which when multiplied by $x$ yields 1. For a fraction $a/b$, the reciprocal is $b/a$."
  },

  "reciprocal rule": {
    formula: "\\frac{d}{dx}\\left[\\frac{1}{g(x)}\\right] = -\\frac{g'(x)}{[g(x)]^2}, \\quad g(x) \\neq 0",
    formula_description: "Calculus rule for differentiating the reciprocal of a function $g(x)$, derived from the chain rule or quotient rule."
  },

  "rectangle": {
    formula: "A = l \\cdot w, \\quad P = 2(l + w), \\quad d = \\sqrt{l^2 + w^2}",
    formula_description: "A 4-sided polygon (quadrilateral) with four right angles ($90^\\circ$). Area $A = l w$, perimeter $P = 2(l+w)$, and diagonal length $d = \\sqrt{l^2+w^2}$."
  },

  "rectangular hyperbola": {
    formula: "xy = c^2 \\quad \\text{or} \\quad x^2 - y^2 = a^2, \\quad e = \\sqrt{2}, \\quad \\theta_{\\text{asymptotes}} = 90^\\circ",
    formula_description: "A hyperbola whose asymptotes are perpendicular ($90^\\circ$), having eccentricity $e = \\sqrt{2}$. When aligned with coordinate axes, its equation simplifies to $xy = c^2$."
  },

  "relative atomic mass": {
    formula: "A_r = \\frac{\\text{average mass of 1 atom of element}}{\\frac{1}{12} \\text{ mass of 1 atom of } ^{12}\\text{C}} = \\sum_{i} (f_i \\cdot M_i)",
    formula_description: "Dimensionless ratio of the average atomic mass of an element's naturally occurring isotopes (weighted by abundance $f_i$) to $1/12\\text{th}$ the mass of a carbon-12 atom."
  },

  "remainder theorem": {
    formula: "P(x) = (x - a)Q(x) + R \\implies P(a) = R; \\quad P(a) = 0 \\iff (x - a) \\text{ is a factor of } P(x)",
    formula_description: "Polynomial remainder theorem: when polynomial $P(x)$ is divided by $(x - a)$, the remainder equals $P(a)$. The Factor Theorem follows: $(x - a)$ is a factor if and only if $P(a) = 0$."
  },

  "riemann integral": {
    formula: "\\int_a^b f(x)\\,dx = \\lim_{\\|\\Delta x\\| \\to 0} \\sum_{i=1}^n f(x_i^*)\\,\\Delta x_i",
    formula_description: "The foundational definition of a definite integral as the limit of Riemann sums as partition width approaches zero, representing signed net area under curve $f(x)$."
  },

  "riemann sum": {
    formula: "S_n = \\sum_{i=1}^n f(c_i)\\,\\Delta x, \\quad \\Delta x = \\frac{b - a}{n}, \\quad c_i \\in [x_{i-1}, x_i]",
    formula_description: "An approximation of the area under a curve by dividing the interval $[a,b]$ into $n$ subintervals of width $\\Delta x$ and summing sample rectangle areas $f(c_i)\\Delta x$."
  },

  "riemann zeta function": {
    formula: "\\zeta(s) = \\sum_{n=1}^\\infty \\frac{1}{n^s} = \\prod_{p\\text{ prime}} \\frac{1}{1 - p^{-s}} \\quad (\\text{Re}(s) > 1)",
    formula_description: "Special function fundamental to number theory and quantum chaos. The Euler product formula connects $\\zeta(s)$ to the distribution of prime numbers."
  },

  "right triangle": {
    formula: "a^2 + b^2 = c^2, \\quad \\sin\\theta = \\frac{a}{c}, \\quad \\cos\\theta = \\frac{b}{c}, \\quad \\tan\\theta = \\frac{a}{b}, \\quad A = \\frac{1}{2}ab",
    formula_description: "A triangle containing one $90^\\circ$ right angle. Governed by the Pythagorean theorem $a^2 + b^2 = c^2$ and standard trigonometric ratios."
  },

  "ring": {
    formula: "(R, +, \\cdot): \\quad a(b+c) = ab + ac, \\quad (a+b)c = ac + bc",
    formula_description: "An algebraic structure consisting of a set $R$ equipped with two binary operations (addition $+$ and multiplication $\\cdot$) satisfying ring axioms: abelian group under $+$, associative multiplication, and left/right distributivity."
  },

  "rolle's theorem": {
    formula: "f(a) = f(b) \\implies \\exists c \\in (a,b) : f'(c) = 0",
    formula_description: "Calculus mean value theorem variant: if $f(x)$ is continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a) = f(b)$, then there exists at least one $c \\in (a,b)$ where $f'(c) = 0$."
  },

  "root mean square": {
    formula: "x_{\\text{rms}} = \\sqrt{\\frac{1}{n}\\sum_{i=1}^n x_i^2} = \\sqrt{\\frac{1}{T}\\int_0^T [f(t)]^2 dt}",
    formula_description: "Statistical measure defined as the square root of the mean of the squares of a set of values or continuous waveform $f(t)$."
  },

  // -- PHYSICS & ELECTRICITY --

  "radioactive decay": {
    formula: "N(t) = N_0 e^{-\\lambda t}, \\quad A(t) = \\lambda N(t) = A_0 e^{-\\lambda t}, \\quad t_{1/2} = \\frac{\\ln 2}{\\lambda} \\approx \\frac{0.693}{\\lambda}",
    formula_description: "First-order kinetics governing radioactive decay: the number of undecayed nuclei $N(t)$ decreases exponentially over time at decay constant $\\lambda$, with half-life $t_{1/2} = \\ln 2 / \\lambda$."
  },

  "radioactivity": {
    formula: "A = -\\frac{dN}{dt} = \\lambda N, \\quad A(t) = A_0 e^{-\\lambda t}, \\quad 1\\text{ Bq} = 1\\text{ decay/s}, \\quad 1\\text{ Ci} = 3.7 \\times 10^{10}\\text{ Bq}",
    formula_description: "The spontaneous emission of radiation from unstable atomic nuclei. Activity $A$ measures decay rate in Becquerels ($1\\text{ Bq} = 1\\text{ decay/s}$) or Curies ($1\\text{ Ci} = 3.7 \\times 10^{10}\\text{ Bq}$)."
  },

  "radius of curvature": {
    formula: "R = \\frac{[1 + (y')^2]^{3/2}}{|y''|}, \\quad a_c = \\frac{v^2}{R}, \\quad f = \\frac{R}{2}",
    formula_description: "The radius of the osculating circle that best fits a curve at a given point. For spherical mirrors, focal length $f = R/2$; for circular motion, centripetal acceleration $a_c = v^2/R$."
  },

  "radius of gyration": {
    formula: "k = \\sqrt{\\frac{I}{M}}, \\quad I = M k^2, \\quad k_{\\text{disk}} = \\frac{R}{\\sqrt{2}}, \\quad k_{\\text{sphere}} = \\sqrt{\\frac{2}{5}}R",
    formula_description: "The radial distance $k$ from a rotational axis at which the entire mass $M$ of a body could be concentrated without altering its moment of inertia $I = Mk^2$."
  },

  "raman effect": {
    formula: "\\Delta \\nu = \\nu_0 \\pm \\nu_{\\text{vib}}, \\quad E_{\\text{Stokes}} = h(\\nu_0 - \\nu_m), \\quad E_{\\text{anti-Stokes}} = h(\\nu_0 + \nu_m)",
    formula_description: "Inelastic scattering of photons by molecules, resulting in frequency shifts $\\Delta \\nu$ corresponding to vibrational or rotational energy transitions of the scattering medium."
  },

  "rayleigh scattering": {
    formula: "I(\\theta) = I_0 \\frac{1 + \\cos^2\\theta}{2 R^2} \\left(\\frac{2\\pi}{\\lambda}\\right)^4 \\left(\\frac{n^2-1}{n^2+2}\\right)^2 \\left(\\frac{d}{2}\\right)^6 \\implies I \\propto \\frac{1}{\\lambda^4}",
    formula_description: "Elastic scattering of light by particles smaller than the wavelength $\\lambda$. Scattering intensity varies inversely with $\\lambda^4$, explaining the blue color of the daytime sky."
  },

  "rayleigh-jeans law": {
    formula: "B_\\lambda(T) = \\frac{8\\pi k_B T}{\\lambda^4}, \\quad u(\\nu)\\,d\\nu = \\frac{8\\pi \\nu^2}{c^3} k_B T\\,d\\nu",
    formula_description: "Classical approximation of blackbody radiation intensity at long wavelengths. Fails at short wavelengths (the 'ultraviolet catastrophe'), resolved by Planck's quantum theory."
  },

  "rc circuit": {
    formula: "\\tau = RC, \\quad q(t) = Q_{\\text{max}}\\left(1 - e^{-t/RC}\\right), \\quad I(t) = \\frac{V_0}{R} e^{-t/RC}",
    formula_description: "An electrical circuit composed of resistors and capacitors. The time constant $\\tau = RC$ governs the exponential charging/discharging rate of charge $q(t)$ and current $I(t)$."
  },

  "reactance": {
    formula: "X_L = \\omega L = 2\\pi f L, \\quad X_C = \\frac{1}{\\omega C} = \\frac{1}{2\\pi f C}, \\quad Z = \\sqrt{R^2 + (X_L - X_C)^2}",
    formula_description: "The opposition of a circuit element to alternating current (AC) caused by inductance ($X_L$) or capacitance ($X_C$), measured in Ohms ($\\Omega$)."
  },

  "rectifier": {
    formula: "V_{\\text{dc, half}} = \\frac{V_m}{\\pi} \\approx 0.318 V_m, \\quad V_{\\text{dc, full}} = \\frac{2V_m}{\\pi} \\approx 0.637 V_m, \\quad V_{\\text{rms}} = \\frac{V_m}{\\sqrt{2}}",
    formula_description: "An electrical device converting alternating current (AC) to direct current (DC). Full-wave rectification doubles average output DC voltage relative to half-wave rectification."
  },

  "redshift": {
    formula: "z = \\frac{\\lambda_{\\text{obs}} - \\lambda_{\\text{emit}}}{\\lambda_{\\text{emit}}} = \\frac{\\Delta\\lambda}{\\lambda_0}, \\quad 1 + z = \\sqrt{\\frac{1 + v/c}{1 - v/c}} \\approx 1 + \\frac{v}{c}",
    formula_description: "The displacement of spectral lines toward longer (redder) wavelengths due to Doppler motion ($v$) or cosmic expansion of spacetime, quantified by redshift parameter $z$."
  },

  "refraction": {
    formula: "n_1 \\sin\\theta_1 = n_2 \\sin\\theta_2, \\quad n = \\frac{c}{v} = \\frac{\\lambda_0}{\\lambda}",
    formula_description: "The bending of a light wave as it passes across the boundary between two media with different refractive indices $n_1, n_2$, governed by Snell's Law."
  },

  "refractive index": {
    formula: "n = \\frac{c}{v} = \\sqrt{\\epsilon_r \\mu_r}, \\quad n = \\frac{\\sin i}{\\sin r} = \\frac{\\lambda_1}{\\lambda_2}",
    formula_description: "Dimensionless ratio of the speed of light in vacuum $c$ to phase velocity $v$ in a medium. Connects optical bending to relative permittivity $\\epsilon_r$ and permeability $\\mu_r$."
  },

  "relative density": {
    formula: "\\text{RD} = \\frac{\\rho_{\\text{substance}}}{\\rho_{\\text{water}}} = \\frac{m_{\\text{substance}}}{m_{\\text{equal volume of water}}} = \\frac{W_{\\text{air}}}{W_{\\text{air}} - W_{\\text{water}}}",
    formula_description: "Specific gravity: ratio of the density of a substance to the density of reference fluid (water at $4^\\circ\\text{C}$, $\\rho = 1000\\;\\text{kg/m}^3$). Determined via Archimedes' Principle."
  },

  "relative humidity": {
    formula: "\\text{RH} = \\frac{p_{H_2O}}{P_{H_2O}^*} \\times 100\\% = \\frac{\\text{actual vapor pressure}}{\\text{saturation vapor pressure}} \\times 100\\%",
    formula_description: "Percentage ratio of the partial pressure of water vapor in air to the equilibrium saturation vapor pressure at a given temperature."
  },

  "relative velocity": {
    formula: "\\mathbf{v}_{B/A} = \\mathbf{v}_B - \\mathbf{v}_A, \\quad v'_{x} = \\frac{v_x - u}{1 - uv_x/c^2} \\text{ (relativistic)}",
    formula_description: "The velocity of object $B$ as observed in the rest frame of object $A$. Governed by vector subtraction in classical mechanics and Einstein's velocity addition formula in relativity."
  },

  "relativity": {
    formula: "E = \\gamma m_0 c^2 = \\sqrt{(pc)^2 + (m_0 c^2)^2}, \\quad \\gamma = \\frac{1}{\\sqrt{1 - v^2/c^2}}, \\quad \\Delta t = \\gamma \\Delta t_0",
    formula_description: "Einstein's theory of space and time: special relativity introduces Lorentz factor $\\gamma$, time dilation $\\Delta t = \\gamma \\Delta t_0$, length contraction, and mass-energy equivalence $E=mc^2$."
  },

  "resistance": {
    formula: "R = \\frac{V}{I} = \\rho \\frac{L}{A}, \\quad P = I^2 R = \\frac{V^2}{R} = VI",
    formula_description: "Electric resistance: opposition to electric current flow governed by Ohm's Law $V = IR$. Proportional to length $L$ and resistivity $\\rho$, inversely proportional to cross-sectional area $A$."
  },

  "resistivity": {
    formula: "\\rho = R \\frac{A}{L} = \\frac{1}{\\sigma}, \\quad \\rho(T) = \\rho_0 [1 + \\alpha(T - T_0)]",
    formula_description: "Intrinsic property of a material measuring electrical opposition: $\\rho = RA/L$, inverse of conductivity $\\sigma$. Varies linearly with temperature coefficient $\\alpha$."
  },

  "resistor": {
    formula: "R_{\\text{series}} = \\sum_{i=1}^n R_i, \\quad \\frac{1}{R_{\\text{parallel}}} = \\sum_{i=1}^n \\frac{1}{R_i}, \\quad P = I^2 R",
    formula_description: "Passive electrical component implementing electrical resistance. Series connection sums resistance values; parallel connection sums conductances ($1/R$)."
  },

  "resonance": {
    formula: "f_0 = \\frac{1}{2\\pi\\sqrt{LC}}, \\quad \\omega_0 = \\frac{1}{\\sqrt{LC}}, \\quad Z_{\\text{min}} = R, \\quad I_{\\text{max}} = \\frac{V_0}{R}",
    formula_description: "Phenomenon in driven oscillating systems where amplitude reaches a maximum at resonant frequency $f_0$. In series RLC circuits, inductive reactance cancels capacitive reactance ($X_L = X_C$)."
  },

  "restitution": {
    formula: "e = \\frac{v_2 - v_1}{u_1 - u_2} = \\sqrt{\\frac{h_{\\text{rebound}}}{h_{\\text{drop}}}}, \\quad 0 \\leq e \\leq 1",
    formula_description: "Coefficient of restitution $e$: ratio of relative velocity of separation to relative velocity of approach in collisions. $e=1$ for perfectly elastic collisions, $e=0$ for perfectly inelastic collisions."
  },

  "resultant": {
    formula: "R = \\sqrt{F_1^2 + F_2^2 + 2F_1 F_2 \\cos\\theta}, \\quad \\tan\\alpha = \\frac{F_2 \\sin\\theta}{F_1 + F_2 \\cos\\theta}",
    formula_description: "The single vector obtained by combining two or more vectors. For forces $F_1, F_2$ at angle $\\theta$, magnitude is given by the law of cosines and direction by trigonometry."
  },

  "reynolds number": {
    formula: "Re = \\frac{\\rho v D}{\\mu} = \\frac{v D}{\\nu}, \\quad Re < 2300 \\implies \\text{laminar}, \\quad Re > 4000 \\implies \\text{turbulent}",
    formula_description: "Dimensionless quantity in fluid dynamics measuring the ratio of inertial forces to viscous forces. Predicts flow regime transitions between smooth laminar flow and chaotic turbulent flow."
  },

  "root mean square speed": {
    formula: "v_{\\text{rms}} = \\sqrt{\\frac{3RT}{M}} = \\sqrt{\\frac{3k_B T}{m}} = \\sqrt{\\frac{3P}{\\rho}}",
    formula_description: "The square root of the mean squared speed of gas molecules derived from kinetic theory of gases: directly proportional to the square root of absolute temperature $T$."
  },

  "rotational inertia": {
    formula: "I = \\sum m_i r_i^2 = \\int r^2 dm, \\quad K_{\\text{rot}} = \\frac{1}{2}I\\omega^2, \\quad L = I\\omega",
    formula_description: "Moment of inertia $I$: quantitative measure of a body's resistance to angular acceleration. Relates angular momentum $L = I\\omega$ and rotational kinetic energy $K = \\frac{1}{2}I\\omega^2$."
  },

  "rotational kinetic energy": {
    formula: "K_{\\text{rot}} = \\frac{1}{2} I \\omega^2 = \\frac{L^2}{2I}, \\quad K_{\\text{total}} = \\frac{1}{2}m v_{\\text{cm}}^2 + \\frac{1}{2}I_{\\text{cm}}\\omega^2",
    formula_description: "Kinetic energy due to rotation of an object: $K_{\\text{rot}} = \\frac{1}{2}I\\omega^2$. For a rolling body, total kinetic energy is the sum of translational and rotational kinetic energies."
  },

  "rutherford model": {
    formula: "\\frac{d\\sigma}{d\\Omega} = \\left(\\frac{z Z e^2}{4\\pi\\epsilon_0 \\cdot 4 E_k}\\right)^2 \\frac{1}{\\sin^4(\\theta/2)}, \\quad r_{\\text{min}} = \\frac{z Z e^2}{2\\pi\\epsilon_0 E_k}",
    formula_description: "Rutherford nuclear model of the atom: alpha particles scatter off a dense central nucleus of charge $Ze$ according to Coulomb's inverse-square law, establishing atomic nucleus radius $r_{\\text{min}}$."
  },

  "rydberg formula": {
    formula: "\\frac{1}{\\lambda} = R_\\infty Z^2 \\left(\\frac{1}{n_1^2} - \\frac{1}{n_2^2}\\right), \\quad R_\\infty = \\frac{m_e e^4}{8 \\epsilon_0^2 h^3 c} \\approx 1.097373 \\times 10^7 \\; \\text{m}^{-1}",
    formula_description: "Formula predicting spectral emission wavelengths $\\lambda$ of hydrogen-like elements as electrons transition between quantum levels $n_2 \\to n_1$, where $R_\\infty$ is the Rydberg constant."
  },

  // -- CHEMISTRY & THERMODYNAMICS --

  "raoult's law": {
    formula: "P_A = X_A P_A^\\circ, \\quad \\Delta P = X_B P_A^\\circ, \\quad P_{\\text{total}} = X_A P_A^\\circ + X_B P_B^\\circ",
    formula_description: "Thermodynamic chemistry law stating that partial vapor pressure of solvent $A$ above an ideal solution $P_A$ equals solvent mole fraction $X_A$ multiplied by pure solvent vapor pressure $P_A^\\circ$."
  },

  "rate constant": {
    formula: "k = A e^{-E_a / RT}, \\quad \\ln k = \\ln A - \\frac{E_a}{R T}",
    formula_description: "Reaction rate coefficient $k$ in chemical kinetics, governed by the Arrhenius equation: depends exponentially on activation energy $E_a$ and absolute temperature $T$."
  },

  "rate law": {
    formula: "\\text{Rate} = k [A]^m [B]^n, \\quad \\text{Overall order} = m + n, \\quad [A]_t = [A]_0 - kt \\text{ (0th order)}",
    formula_description: "Equation relating chemical reaction rate to reactant concentrations $[A], [B]$ raised to reaction order powers $m, n$, determined experimentally."
  },

  "rate of reaction": {
    formula: "r = -\\frac{1}{a}\\frac{d[A]}{dt} = -\\frac{1}{b}\\frac{d[B]}{dt} = \\frac{1}{c}\\frac{d[C]}{dt} = \\frac{1}{d}\\frac{d[D]}{dt}",
    formula_description: "Speed at which reactants turn into products in chemical reaction $aA + bB \\to cC + dD$: defined as change in concentration per unit time divided by stoichiometric coefficients."
  },

  "reactant": {
    formula: "aA + bB \\longrightarrow cC + dD, \\quad n_{\\text{limiting}} = \\min\\left(\\frac{n_A}{a}, \\frac{n_B}{b}\\right)",
    formula_description: "Starting substance consumed during a chemical reaction to form products. The limiting reactant determines maximum theoretical product yield based on stoichiometry."
  },

  "reaction quotient": {
    formula: "Q_c = \\frac{[C]^c [D]^d}{[A]^a [B]^b}, \\quad Q < K_c \\implies \\text{shift right}, \\quad Q > K_c \\implies \\text{shift left}",
    formula_description: "Ratio of product concentrations to reactant concentrations at any instant during a reaction. Comparing $Q_c$ to equilibrium constant $K_c$ determines reaction direction."
  },

  "redox": {
    formula: "\\text{Oxidation: } \\text{Zn} \\to \\text{Zn}^{2+} + 2e^-, \\quad \\text{Reduction: } \\text{Cu}^{2+} + 2e^- \\to \\text{Cu}, \\quad E^\\circ_{\\text{cell}} = E^\\circ_{\\text{cathode}} - E^\\circ_{\\text{anode}}",
    formula_description: "Reduction-oxidation chemical reaction involving electron transfer: oxidation is loss of electrons; reduction is gain of electrons. Standard cell potential $E^\\circ_{\\text{cell}}$ measures driving electromotive force."
  },

  "reversible reaction": {
    formula: "aA + bB \\rightleftharpoons cC + dD, \\quad K_c = \\frac{[C]^c [D]^d}{[A]^a [B]^b}, \\quad \\Delta G^\\circ = -RT \\ln K",
    formula_description: "Chemical reaction where products re-react to form reactants. Reaches dynamic equilibrium when forward and reverse reaction rates become equal ($\\,\\Delta G = 0\\,$)."
  }
};

/* ============================================================
   E N R I C H M E N T   E X E C U T I O N
============================================================ */
let matchCount = 0;
let updatedCount = 0;

if (!dict['R']) {
  console.error("Error: Section R not found in dictionary.json!");
  process.exit(1);
}

dict['R'].forEach((entry) => {
  const wordKey = entry.word.trim().toLowerCase();
  if (rEnrichments[wordKey]) {
    matchCount++;
    const enrich = rEnrichments[wordKey];
    
    // Add formula and formula_description properties
    entry.formula = enrich.formula;
    entry.formula_description = enrich.formula_description;
    
    // Append LaTeX block to definition if not already present
    const latexBlock = `\n\n$$\n${enrich.formula}\n$$\n*Formula:* ${enrich.formula_description}`;
    if (!entry.definition.includes('$$')) {
      entry.definition += latexBlock;
      updatedCount++;
    }
  }
});

console.log(`Matching R terms found: ${matchCount} / ${Object.keys(rEnrichments).length}`);
console.log(`Updated entries: ${updatedCount}`);

// Save back to dictionary.json
fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log("Successfully updated dictionary.json with Section R STEM formulas!");
