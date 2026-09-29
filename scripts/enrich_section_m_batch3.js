const fs = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const rawData = fs.readFileSync(dictPath, 'utf8');
const data = JSON.parse(rawData);

const M = data['M'];

const enrichments = {
  "malus' law": {
    formula: "$$I = I_0 \\cos^2\\theta$$",
    formula_description: "Transmitted intensity $I$ of plane-polarized light through an analyzer oriented at angle $\\theta$ relative to the transmission axis of the polarizer. $I = I_0$ at $\\theta = 0^\\circ$; $I = 0$ at $\\theta = 90^\\circ$ (complete extinction)."
  },
  "magnetic constant": {
    formula: "$$\\mu_0 = 4\\pi \\times 10^{-7}\\ \\mathrm{H\\cdot m^{-1}} \\approx 1.2566 \\times 10^{-6}\\ \\mathrm{N\\cdot A^{-2}}, \\qquad c = \\frac{1}{\\sqrt{\\varepsilon_0 \\mu_0}}$$",
    formula_description: "Permeability of free space ($\\mu_0$). Relates magnetic flux density $\\mathbf{B}$ to magnetic field strength $\\mathbf{H}$ in vacuum ($\\mathbf{B} = \\mu_0 \\mathbf{H}$) and ties directly to the speed of light $c$ via Maxwell's electrodynamics."
  },
  "madelung's rule": {
    formula: "$$E \\propto (n + l), \\quad \\text{if } (n_1+l_1) = (n_2+l_2) \\implies \\text{lower } n \\text{ fills first}$$",
    formula_description: "Determines electron subshell filling sequence (Aufbau $(n+l)$ rule). Subshells fill in increasing order of $n+l$. For ties (e.g. $3d$ vs $4p$, both $n+l=5$), the orbital with smaller principal quantum number $n$ fills first."
  },
  "magnus effect": {
    formula: "$$\\mathbf{F}_L = \\rho_\\infty \\mathbf{v}_\\infty \\times \\boldsymbol{\\Gamma}, \\qquad F_L = 2\\pi r^2 \\rho v \\omega L$$",
    formula_description: "Lift force generated on a spinning cylinder or sphere moving through a fluid of density $\\rho$. $v$ = flow velocity, $\\omega$ = angular spin speed, $\\Gamma = 2\\pi r^2 \\omega$ = circulation (Kutta–Joukowski theorem)."
  },
  "markovnikoff's rule": {
    formula: "$$\\mathrm{R{-}CH{=}CH_2} + \\mathrm{HX} \\;\\longrightarrow\\; \\mathrm{R{-}CH(X){-}CH_3} \\quad (3^\\circ > 2^\\circ > 1^\\circ \\text{ carbocation stability})$$",
    formula_description: "Electrophilic addition of hydrogen halides (HX) to unsymmetrical alkenes: hydrogen bonds to the carbon already possessing more hydrogen atoms, proceeding via the more stable carbocation intermediate."
  },
  "mass action law": {
    formula: "$$a\\mathrm{A} + b\\mathrm{B} \\rightleftharpoons c\\mathrm{C} + d\\mathrm{D}, \\qquad K_c = \\frac{[\\mathrm{C}]^c [\\mathrm{D}]^d}{[\\mathrm{A}]^a [\\mathrm{B}]^b}, \\quad \\Delta G^\\circ = -RT \\ln K$$",
    formula_description: "The rate and thermodynamic equilibrium of a chemical reaction are directly proportional to the product of active masses (concentrations) of reactants raised to their stoichiometric powers."
  },
  "maxwell's distribution": {
    formula: "$$f(v) = 4\\pi \\left(\\frac{m}{2\\pi k_B T}\\right)^{\\!3/2} v^2 \\exp\\!\\left(-\\frac{mv^2}{2k_B T}\\right)$$",
    formula_description: "Probability distribution of molecular speeds $v$ in an ideal gas at thermal equilibrium. Characteristic speeds: most probable $v_p = \\sqrt{2k_B T/m}$, average $\\bar{v} = \\sqrt{8k_B T/\\pi m}$, RMS $v_{\\text{rms}} = \\sqrt{3k_B T/m}$."
  },
  "meissner effect": {
    formula: "$$\\mathbf{B} = 0 \\quad (T < T_c), \\qquad \\nabla^2\\mathbf{B} = \\frac{1}{\\lambda_L^2}\\mathbf{B}, \\quad \\lambda_L = \\sqrt{\\frac{m}{\\mu_0 n_s e^2}}$$",
    formula_description: "Complete expulsion of magnetic flux lines from the interior of a superconductor cooled below critical temperature $T_c$. Governed by London's second equation with penetration depth $\\lambda_L$."
  },
  "mellin transform": {
    formula: "$$\\{\\mathcal{M}f\\}(s) = \\varphi(s) = \\int_{0}^{\\infty} x^{s-1} f(x)\\,dx, \\qquad f(x) = \\frac{1}{2\\pi i} \\int_{c-i\\infty}^{c+i\\infty} x^{-s} \\varphi(s)\\,ds$$",
    formula_description: "Multiplicative integral transform closely related to Dirichlet series and the Riemann zeta function $\\zeta(s)\\Gamma(s) = \\mathcal{M}[1/(e^x-1)]$. Foundational in analytic number theory and asymptotic analysis."
  },
  "mid-ordinate rule": {
    formula: "$$\\int_{a}^{b} f(x)\\,dx \\approx h \\sum_{i=1}^{n} f\\!\\left(\\frac{x_{i-1} + x_i}{2}\\right), \\qquad h = \\frac{b - a}{n}, \\quad |E| \\le \\frac{(b-a)^3}{24n^2} M_2$$",
    formula_description: "Midpoint numerical integration evaluating $f(x)$ at the midpoint of each subinterval $m_i$. Offers global error $\\mathcal{O}(h^2)$ with half the truncation error of the trapezoidal rule."
  },
  "mariotte law": {
    formula: "$$P_1 V_1 = P_2 V_2 \\quad (T = \\text{constant}), \\qquad P V = \\text{constant}$$",
    formula_description: "Boyle–Mariotte law: for a given mass of an ideal gas at constant temperature, pressure is inversely proportional to volume ($P \\propto 1/V$)."
  },
  "mass-energy equation": {
    formula: "$$E_0 = m_0 c^2, \\qquad E^2 = (pc)^2 + (m_0 c^2)^2, \\qquad E = \\gamma m_0 c^2 = \\frac{m_0 c^2}{\\sqrt{1 - v^2/c^2}}$$",
    formula_description: "Einstein's relativistic mass-energy equivalence principle relating total energy $E$, momentum $p$, rest mass $m_0$, and speed of light $c$."
  },
  "mathieu's differential equation": {
    formula: "$$\\frac{d^2 y}{dx^2} + (a - 2q \\cos 2x)y = 0$$",
    formula_description: "Second-order linear ODE with periodic coefficients; models parametric resonance, elliptical drumhead oscillations, and ion motion inside quadrupole mass filters."
  },
  "max-flow min-cut theorem": {
    formula: "$$\\max |f| = \\min_{S,T} c(S, T) = \\min_{S,T} \\sum_{u \\in S, v \\in T} c(u, v)$$",
    formula_description: "Ford–Fulkerson theorem in combinatorial optimization: the maximum flow passing from source to sink in a flow network equals the minimum capacity of an $s\\text{-}t$ cut separating them."
  },
  "maximum modulus theorem": {
    formula: "$$|f(z_0)| \\le \\max_{z \\in \\partial D} |f(z)| \\quad \\forall\\, z_0 \\in D$$",
    formula_description: "Complex analysis: if $f(z)$ is holomorphic on a bounded domain $D$ and continuous on $\\overline{D}$, its modulus $|f(z)|$ cannot achieve a strict local maximum inside $D$ unless $f$ is constant."
  },
  "maximum value theorem": {
    formula: "$$f \\in C[a,b] \\;\\implies\\; \\exists\\, c, d \\in [a,b] \\text{ such that } f(c) \\le f(x) \\le f(d) \\quad \\forall\\, x \\in [a,b]$$",
    formula_description: "Extreme Value Theorem (EVT): any continuous real-valued function on a closed and bounded interval $[a, b]$ attains both its absolute minimum and absolute maximum at least once."
  },
  "moore's law": {
    formula: "$$N(t) = N_0 \\cdot 2^{t / T}, \\qquad T \\approx 18\\text{--}24\\ \\text{months}$$",
    formula_description: "Empirical observation by Gordon Moore (1965): the density of transistors on integrated circuit chips doubles approximately every 18 to 24 months."
  },
  "morera's theorem": {
    formula: "$$\\oint_{\\gamma} f(z)\\,dz = 0 \\quad (\\forall \\text{ closed loops } \\gamma \\subset D) \\implies f(z) \\text{ is holomorphic on } D$$",
    formula_description: "Converse of Cauchy's integral theorem: if $f$ is continuous on an open domain $D$ and its contour integral along every closed curve vanishes, then $f$ is analytic throughout $D$."
  },
  "multinomial distribution": {
    formula: "$$P(X_1=k_1, \\ldots, X_m=k_m) = \\frac{n!}{\\prod_{i=1}^m k_i!} \\prod_{i=1}^m p_i^{k_i}, \\quad \\sum_{i=1}^m k_i = n, \\ \\sum_{i=1}^m p_i = 1$$",
    formula_description: "Generalization of the binomial distribution to $m$ discrete categories with probabilities $p_1, \\dots, p_m$ in $n$ independent mutually exclusive trials."
  },
  "multinomial theorem": {
    formula: "$$\\left(\\sum_{i=1}^m x_i\\right)^{\\!n} = \\sum_{k_1+\\cdots+k_m=n} \\binom{n}{k_1, k_2, \\ldots, k_m} \\prod_{t=1}^m x_t^{k_t}, \\quad \\binom{n}{k_1, \\dots, k_m} = \\frac{n!}{k_1!\\cdots k_m!}$$",
    formula_description: "Algebraic expansion of the $n$-th power of a multivariable sum, with coefficients equal to the number of permutations of a multiset."
  },
  "multiplication law of probability": {
    formula: "$$P(A \\cap B) = P(A) \\cdot P(B \\mid A) = P(B) \\cdot P(A \\mid B), \\qquad P(A \\cap B) = P(A)P(B) \\iff \\text{independent}$$",
    formula_description: "Calculates the joint probability of two events; for statistically independent events, reduces to the direct product $P(A \\cap B) = P(A) \\cdot P(B)$."
  },
  "möbius inversion formula": {
    formula: "$$g(n) = \\sum_{d \\mid n} f(d) \\iff f(n) = \\sum_{d \\mid n} \\mu(d)\\,g\\!\\left(\\frac{n}{d}\\right)$$",
    formula_description: "Fundamental identity in arithmetic number theory. $\\mu(d)$ is the Möbius function: $+1$ if square-free with even prime count, $-1$ with odd prime count, $0$ if non-square-free."
  },
  "mössbauer effect": {
    formula: "$$E_R = \\frac{E_\\gamma^2}{2 M c^2}, \\qquad f_{\\text{LM}} = \\exp\\!\\left(-\\frac{k^2 \\langle x^2 \\rangle}{3}\\right) = \\exp\\!\\left(-\\frac{E_\\gamma^2 \\langle x^2 \\rangle}{3(\\hbar c)^2}\\right)$$",
    formula_description: "Recoilless emission and resonant absorption of gamma photons by atomic nuclei bound in solid crystal lattices. Enables extremely high-resolution hyperfine spectroscopy."
  },
  "mitscherlich's law": {
    formula: "$$\\text{Substances of similar crystal structure} \\iff \\text{similar chemical formulas / stoichiometry}$$",
    formula_description: "Law of Isomorphism (1819): chemical compounds with analogous stoichiometry and atomic ratios crystallize into identical isomorphic forms and interfacial angles."
  }
};

let count = 0;
for (const entry of M) {
  const word = (entry.word || '').trim().toLowerCase();
  if (enrichments[word] && !entry.formula) {
    entry.formula = enrichments[word].formula;
    entry.formula_description = enrichments[word].formula_description;
    count++;
    console.log(`  [OK] ${entry.word}`);
  }
}

data['M'] = M;
fs.writeFileSync(dictPath, JSON.stringify(data, null, 2), 'utf8');
console.log(`\nSuccessfully enriched ${count} entries in Section M.`);
