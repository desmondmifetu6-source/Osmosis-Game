/**
 * scripts/enrich_section_o.js
 * Comprehensive STEM Formula Enrichment for Section O
 */
const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

const oEnrichments = {
  "ohm": {
    formula: "1\\;\\Omega = 1\\;\\text{V}/\\text{A} = 1\\;\\text{kg}\\cdot\\text{m}^2\\cdot\\text{s}^{-3}\\cdot\\text{A}^{-2}",
    formula_description: "The SI derived unit of electrical resistance, impedance, and reactance, defined as the resistance between two points of a conductor when a constant potential difference of 1 volt produces a current of 1 ampere."
  },
  "ohm's law": {
    formula: "V = IR \\iff I = \\frac{V}{R}, \\quad \\mathbf{J} = \\sigma \\mathbf{E} = \\frac{1}{\\rho} \\mathbf{E}",
    formula_description: "States that electric current $I$ through a conductor between two points is directly proportional to voltage $V$ across the two points and inversely proportional to resistance $R$. In microscopic form, current density $\\mathbf{J}$ equals conductivity $\\sigma$ times electric field $\\mathbf{E}$."
  },
  "ohmic heating": {
    formula: "P = I^2 R = \\frac{V^2}{R} = V I, \\quad Q = I^2 R t",
    formula_description: "Joule heating: the rate of electrical energy dissipated as thermal heat $P$ when current $I$ passes through a resistance $R$ over duration $t$."
  },
  "optical activity": {
    formula: "[\\alpha]_\\lambda^T = \\frac{\\alpha}{l \\cdot c}",
    formula_description: "Biot's law of optical rotation for chiral substances, where $\\alpha$ is measured rotation angle in degrees, $l$ is optical path length in decimetres, $c$ is concentration in $\\text{g/cm}^3$, and $[\\alpha]$ is specific rotation at temperature $T$ and wavelength $\\lambda$ (commonly sodium D-line $589\\text{ nm}$)."
  },
  "optical density": {
    formula: "OD = A = -\\log_{10}\\left(\\frac{I}{I_0}\\right) = \\varepsilon \\cdot c \\cdot l",
    formula_description: "Absorbance ($A$) in spectrophotometry defined by the Beer–Lambert law, relating transmitted light intensity $I$ to incident intensity $I_0$, molar absorptivity $\\varepsilon$, molar concentration $c$, and path length $l$."
  },
  "orbital period": {
    formula: "T = 2\\pi \\sqrt{\\frac{a^3}{G(M + m)}} \\implies T^2 = \\frac{4\\pi^2}{GM} a^3 \\quad (\\text{Kepler's Third Law})",
    formula_description: "The time required for an astronomical body of mass $m$ to complete one orbit around mass $M$ with semi-major axis $a$, dictated by Newton's formulation of Kepler's Third Law."
  },
  "orbital velocity": {
    formula: "v_{\\text{orb}} = \\sqrt{\\frac{GM}{r}}, \\quad v_{\\text{esc}} = \\sqrt{2}\\, v_{\\text{orb}} = \\sqrt{\\frac{2GM}{r}}",
    formula_description: "The speed required for a body to maintain a stable circular orbit of radius $r$ around a central mass $M$, where $v_{\\text{esc}}$ is the escape velocity."
  },
  "orbital quantum number": {
    formula: "L = \\sqrt{l(l+1)}\\,\\hbar, \\quad l \\in \\{0, 1, 2, \\dots, n-1\\}, \\quad L_z = m_l \\hbar",
    formula_description: "The azimuthal/orbital angular momentum quantum number $l$ quantifying the magnitude of atomic electron orbital angular momentum $L$ and its projection $L_z$ with magnetic quantum number $m_l \\in \\{-l, \\dots, +l\\}$."
  },
  "osmotic pressure": {
    formula: "\\Pi = i M R T = i \\left(\\frac{n}{V}\\right) R T",
    formula_description: "The van 't Hoff equation for osmotic pressure $\\Pi$, where $i$ is the van 't Hoff dissociation factor, $M = n/V$ is molarity, $R$ is ideal gas constant ($0.08206\\text{ L}\\cdot\\text{atm}/\\text{mol}\\cdot\\text{K}$ or $8.314\\text{ J/mol}\\cdot\\text{K}$), and $T$ is absolute temperature."
  },
  "osmotic potential": {
    formula: "\\Psi_s = -\\Pi = -i C R T",
    formula_description: "Solute potential (osmotic potential $\\Psi_s$) in plant physiology: represents the contribution of dissolved solutes to total water potential $\\Psi_w = \\Psi_s + \\Psi_p$, always taking a negative or zero value."
  },
  "order of reaction": {
    formula: "r = k [A]^m [B]^n, \\quad \\text{Overall Order } = m + n",
    formula_description: "Rate law in chemical kinetics, where reaction rate $r$ depends on rate constant $k$, reactant concentrations, and partial reaction orders $m$ and $n$ determined experimentally."
  },
  "order of convergence": {
    formula: "\\lim_{k \\to \\infty} \\frac{|e_{k+1}|}{|e_k|^p} = C \\quad (p=1: \\text{linear}, \\; p=2: \\text{quadratic})",
    formula_description: "Measure of the speed at which an iterative numerical sequence $x_k$ approaches its root/limit $r$, where $e_k = x_k - r$ and $p$ is the order of convergence."
  },
  "oxidation number": {
    formula: "\\sum_{\\text{atoms}} \\text{Oxidation Number} = \\text{Net Charge of Species}",
    formula_description: "Bookkeeping formal charge assigned to an atom in a molecule assuming all bonds are 100% ionic. Pure elements equal 0; alkali metals are +1; fluorine is -1; oxygen is generally -2."
  },
  "oscillator": {
    formula: "m \\ddot{x} + c \\dot{x} + k x = F(t) \\implies \\omega_0 = \\sqrt{\\frac{k}{m}}, \\quad f_0 = \\frac{1}{2\\pi}\\sqrt{\\frac{k}{m}}",
    formula_description: "Classical harmonic oscillator differential equation, where $m$ is mass, $c$ is damping coefficient, $k$ is spring stiffness, $\\omega_0$ is natural angular frequency, and $f_0$ is cyclic frequency."
  },
  "overtone": {
    formula: "f_n = n f_1 \\quad (\\text{strings / open pipes}), \\quad f_m = (2m - 1) f_1 \\quad (\\text{closed pipes})",
    formula_description: "Any frequency higher than the fundamental frequency ($f_1$) of a sound or vibrating system. The $n$-th harmonic corresponds to the $(n-1)$-th overtone."
  },
  "octet rule": {
    formula: "n s^2 n p^6 \\quad (\\text{8 valence electrons})",
    formula_description: "Chemical rule of thumb reflecting the stability of atoms possessing eight valence electrons, matching the closed-shell noble gas configuration."
  },
  "operational amplifier": {
    formula: "V_{\\text{out}} = A_{\\text{OL}}(V^+ - V^-), \\quad V_{\\text{out}} = -\\frac{R_f}{R_{\\text{in}}} V_{\\text{in}} \\quad (\\text{Inverting}), \\quad V_{\\text{out}} = \\left(1 + \\frac{R_f}{R_1}\\right) V_{\\text{in}} \\quad (\\text{Non-inverting})",
    formula_description: "High-gain DC-coupled differential voltage amplifier equations in open-loop and standard negative-feedback configurations."
  },
  "orthogonal matrix": {
    formula: "Q^T Q = Q Q^T = I \\iff Q^{-1} = Q^T, \\quad \\det(Q) = \\pm 1",
    formula_description: "A real square matrix whose columns and rows are orthonormal vectors, preserving Euclidean distances and angles under linear transformations (rotations and reflections)."
  },
  "orthogonal vectors": {
    formula: "\\mathbf{u} \\cdot \\mathbf{v} = \\sum_{i=1}^n u_i v_i = 0 \\iff \\mathbf{u} \\perp \\mathbf{v}",
    formula_description: "Two vectors in an inner product space whose dot product equals zero, signifying geometric perpendicularity ($90^\\circ$ angle)."
  },
  "orthogonal functions": {
    formula: "\\langle f, g \\rangle = \\int_a^b f(x) g(x) w(x) \\, dx = 0 \\quad (f \\ne g)",
    formula_description: "Functions whose inner product over an interval $[a,b]$ with weighting function $w(x)$ vanishes, forming the foundation of Fourier series, Legendre polynomials, and quantum state bases."
  },
  "odd function": {
    formula: "f(-x) = -f(x), \\quad \\int_{-a}^{a} f(x) \\, dx = 0",
    formula_description: "A mathematical function possessing rotational symmetry about the origin; the definite integral over any symmetric interval $[-a, a]$ is identically zero (e.g., $\\sin x, x^3$)."
  },
  "odds ratio": {
    formula: "OR = \\frac{p_1 / (1 - p_1)}{p_2 / (1 - p_2)} = \\frac{a \\cdot d}{b \\cdot c}",
    formula_description: "Statistic quantifying the association strength between an exposure and an outcome in biostatistics and epidemiology contingency tables."
  }
};

let enrichedCount = 0;
const oList = dict['O'] || [];

oList.forEach(entry => {
  const key = entry.word.trim().toLowerCase();
  if (oEnrichments[key]) {
    const data = oEnrichments[key];
    entry.formula = data.formula;
    entry.formula_description = data.formula_description;
    
    // Embed cleanly into definition if not already embedded
    if (!entry.definition.includes('$$')) {
      entry.definition = `${entry.definition.trim()}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
    }
    enrichedCount++;
    console.log(`Enriched O [${key}]`);
  }
});

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log(`\nSuccessfully enriched ${enrichedCount} Section O terms in dictionary.json!`);
