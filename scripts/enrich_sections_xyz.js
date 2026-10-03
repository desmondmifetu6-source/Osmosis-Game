/**
 * scripts/enrich_sections_xyz.js
 * STEM Formula Enrichment for Sections X, Y, Z
 *
 * X: x-axis, x-intercept, x-ray diffraction
 * Y: yield, Young's modulus, y-intercept
 * Z: z-score, zero, zenith angle, Zeeman effect
 *
 * Usage: node scripts/enrich_sections_xyz.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

const enrichments = {

  // ═══════ X ═══════

  "x-intercept": {
    formula: "y = 0 \\implies x = -\\frac{b}{a} \\text{ (line)}, \\quad x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a} \\text{ (quadratic)}",
    formula_description: "The point(s) where a curve crosses the x-axis (i.e., where $y = 0$). For linear equation $y = ax + b$, the x-intercept is $-b/a$; for a quadratic, use the quadratic formula."
  },

  "x-ray diffraction": {
    formula: "n\\lambda = 2d\\sin\\theta \\quad (\\text{Bragg's Law}), \\quad n = 1,2,3,\\ldots",
    formula_description: "Bragg's Law governs constructive interference of X-rays scattered by crystal planes separated by spacing $d$: $n\\lambda = 2d\\sin\\theta$. Used to determine crystal structure and atomic spacing."
  },

  // ═══════ Y ═══════

  "y-intercept": {
    formula: "x = 0 \\implies y = c \\text{ in } y = mx + c, \\quad y_0 = f(0), \\quad b_0 \\text{ in regression: } \\hat{y} = b_0 + b_1 x",
    formula_description: "The value of $y$ when $x = 0$: the point where a line or curve crosses the y-axis. In linear equation $y = mx + c$, the y-intercept is $c$; in regression analysis it is the constant term $b_0$."
  },

  "young's double slit experiment": {
    formula: "\\Delta y = \\frac{\\lambda D}{d}, \\quad \\text{path difference} = d\\sin\\theta \\approx d\\theta, \\quad n\\lambda = d\\sin\\theta \\text{ (bright fringe)}",
    formula_description: "Demonstrates wave nature of light: fringe spacing $\\Delta y = \\lambda D/d$ depends on wavelength $\\lambda$, slit-to-screen distance $D$, and slit separation $d$. Constructive interference at $d\\sin\\theta = n\\lambda$."
  },

  "young's modulus": {
    formula: "E = \\frac{\\text{Stress}}{\\text{Strain}} = \\frac{F/A}{\\Delta L/L_0} = \\frac{FL_0}{A \\Delta L}, \\quad \\Delta L = \\frac{FL_0}{AE}",
    formula_description: "Elastic modulus measuring stiffness of a solid material: ratio of tensile stress to tensile strain in the linear elastic region (below the yield point). SI unit: Pascal (Pa) or GPa."
  },

  "yield point": {
    formula: "\\sigma_Y \\approx \\frac{F_Y}{A_0}, \\quad \\varepsilon = \\frac{\\Delta L}{L_0}, \\quad \\text{UTS} = \\frac{F_{\\max}}{A_0}",
    formula_description: "Stress at which a material begins to deform plastically (permanently). Beyond the yield point $\\sigma_Y$, the material will not return to its original shape on removal of the load."
  },

  "yield": {
    formula: "\\%\\text{ yield} = \\frac{\\text{actual yield}}{\\text{theoretical yield}} \\times 100\\%, \\quad n_{\\text{theoretical}} = \\min\\left(\\frac{n_A}{a}, \\frac{n_B}{b}\\right)",
    formula_description: "Percentage yield compares the actual amount of product obtained to the maximum theoretical amount predicted by stoichiometry. Losses occur due to side reactions, incomplete reactions, and transfer losses."
  },

  // ═══════ Z ═══════

  "z-score": {
    formula: "Z = \\frac{X - \\mu}{\\sigma} = \\frac{\\bar{X} - \\mu}{\\sigma/\\sqrt{n}}, \\quad P(-1.96 < Z < 1.96) = 0.95",
    formula_description: "Standardised score measuring how many standard deviations a value $X$ lies from the mean $\\mu$. Used to find probabilities from the standard normal table. For samples: $Z = (\\bar{X}-\\mu)/(\\sigma/\\sqrt{n})$."
  },

  "zeeman effect": {
    formula: "\\Delta E = m_l \\mu_B B, \\quad \\mu_B = \\frac{e\\hbar}{2m_e} = 9.274 \\times 10^{-24}\\text{ J/T}, \\quad \\Delta\\nu = \\frac{eB}{4\\pi m_e}",
    formula_description: "Splitting of atomic spectral lines in an external magnetic field $B$: each energy level splits by $\\Delta E = m_l \\mu_B B$ where $\\mu_B$ is the Bohr magneton and $m_l$ is the magnetic quantum number."
  },

  "zero": {
    formula: "0 + a = a, \\quad 0 \\cdot a = 0, \\quad a^0 = 1 \\;(a \\neq 0), \\quad \\lim_{x \\to 0} \\frac{\\sin x}{x} = 1",
    formula_description: "The additive identity element: $0 + a = a$ for all $a$. Multiplying any number by zero yields zero. The indeterminate form $0/0$ requires L'Hôpital's rule or limit analysis."
  },

  "zeroth law of thermodynamics": {
    formula: "A \\sim B \\text{ and } B \\sim C \\implies A \\sim C, \\quad T_A = T_B = T_C \\text{ (thermal equilibrium)}",
    formula_description: "If system A is in thermal equilibrium with B, and B with C, then A and C are in equilibrium with each other. Defines the concept of temperature as a transitive property."
  },

  "zero order reaction": {
    formula: "[A]_t = [A]_0 - kt, \\quad t_{1/2} = \\frac{[A]_0}{2k}, \\quad \\text{Rate} = k \\quad (\\text{independent of } [A])",
    formula_description: "Chemical reaction where rate is independent of reactant concentration: $\\text{Rate} = k$. Concentration decreases linearly with time; half-life $t_{1/2} = [A]_0/2k$ decreases as reaction proceeds."
  },

  "zenith angle": {
    formula: "z = 90^\\circ - \\alpha, \\quad \\cos z = \\sin\\phi\\sin\\delta + \\cos\\phi\\cos\\delta\\cos H",
    formula_description: "The angle between a celestial body and the zenith (point directly overhead). Complement of altitude $\\alpha$. In solar energy and astronomy, the solar zenith angle determines solar irradiance on a surface."
  }

};

/* ============================================================
   EXECUTION  –  runs across X, Y, Z sections
============================================================ */
const SECTIONS = ['X', 'Y', 'Z'];
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

console.log(`Matching X/Y/Z terms found: ${totalMatches} / ${Object.keys(enrichments).length}`);
console.log(`Updated entries: ${totalUpdated}`);

fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log("Successfully updated dictionary.json with Sections X, Y, Z STEM formulas!");
