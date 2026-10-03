/**
 * scripts/enrich_section_q.js
 * Comprehensive STEM Formula Enrichment for Section Q (45 Fundamental Terms)
 *
 * Covers: quantum mechanics, quadratics, q-value, quality factor, quartile, 
 * quotient rule, quaternions, quark confinement, and many more.
 *
 * Usage:  node scripts/enrich_section_q.js
 */

'use strict';
const fs   = require('fs');
const path = require('path');

const dictPath = path.join(__dirname, '..', 'dictionary.json');
const dict     = JSON.parse(fs.readFileSync(dictPath, 'utf8'));

/* ============================================================
   Q  E N R I C H M E N T   D A T A
   Each key must exactly match entry.word.trim().toLowerCase()
============================================================ */
const qEnrichments = {

  // -- PHYSICS --

  "q-value": {
    formula: "Q = (m_{\\text{reactants}} - m_{\\text{products}})c^2 = T_{\\text{products}} - T_{\\text{reactants}}, \\quad Q_{\\text{reaction}} = \\sum E_{\\text{bond,broken}} - \\sum E_{\\text{bond,formed}}",
    formula_description: "The Q-value of a nuclear reaction or decay: the net energy released (positive $Q$) or absorbed (negative $Q$), equal to the mass-energy difference of reactants and products via $E = mc^2$. Also used in thermochemistry as reaction enthalpy."
  },

  "quality factor": {
    formula: "Q = 2\\pi \\frac{E_{\\text{stored}}}{E_{\\text{dissipated per cycle}}} = \\frac{f_0}{\\Delta f} = \\frac{\\omega_0 L}{R} = \\frac{1}{\\omega_0 C R} = \\frac{1}{R}\\sqrt{\\frac{L}{C}}",
    formula_description: "Dimensionless figure of merit describing the sharpness of a resonance in oscillators, filters, and cavities: the ratio of resonant frequency $f_0$ to bandwidth $\\Delta f$. Higher $Q$ means lower energy loss per cycle."
  },

  "quantum": {
    formula: "E = h\\nu = \\hbar\\omega, \\quad h = 6.62607015 \\times 10^{-34}\\;\\text{J}\\cdot\\text{s}, \\quad \\hbar = \\frac{h}{2\\pi} \\approx 1.0546 \\times 10^{-34}\\;\\text{J}\\cdot\\text{s}",
    formula_description: "The smallest discrete packet of electromagnetic energy, first postulated by Planck (1900). A quantum of light (photon) carries energy $E = h\\nu$, where $h$ is Planck's constant and $\\nu$ is frequency."
  },

  "quantum mechanics": {
    formula: "i\\hbar\\frac{\\partial\\Psi}{\\partial t} = \\hat{H}\\Psi = \\left[-\\frac{\\hbar^2}{2m}\\nabla^2 + V(\\mathbf{r},t)\\right]\\Psi, \\quad \\Delta x \\cdot \\Delta p \\geq \\frac{\\hbar}{2}",
    formula_description: "The governing framework of subatomic physics. The time-dependent Schrodinger equation determines the evolution of wave function $\\Psi$, while Heisenberg's uncertainty principle sets irreducible limits on simultaneous knowledge of position $x$ and momentum $p$."
  },

  "quantum number": {
    formula: "n = 1,2,3,\\ldots; \\quad \\ell = 0,1,\\ldots,n-1; \\quad m_\\ell = -\\ell,\\ldots,+\\ell; \\quad m_s = \\pm\\tfrac{1}{2}, \\quad E_n = -\\frac{13.6}{n^2}\\;\\text{eV}",
    formula_description: "The four quantum numbers $(n, \\ell, m_\\ell, m_s)$ completely specify the quantum state of an electron in a hydrogen-like atom. The principal quantum number $n$ determines the orbital energy level $E_n$."
  },

  "quantum field theory": {
    formula: "\\mathcal{L} = \\bar{\\psi}(i\\gamma^\\mu \\partial_\\mu - m)\\psi - \\frac{1}{4}F_{\\mu\\nu}F^{\\mu\\nu} - e\\bar{\\psi}\\gamma^\\mu\\psi A_\\mu",
    formula_description: "The QED Lagrangian density uniting quantum mechanics and special relativity: $\\bar{\\psi}$ is the Dirac spinor for matter, $F_{\\mu\\nu} = \\partial_\\mu A_\\nu - \\partial_\\nu A_\\mu$ is the electromagnetic field tensor, and $e$ is the elementary charge coupling them."
  },

  "quantum chromodynamics": {
    formula: "\\mathcal{L}_{\\text{QCD}} = -\\frac{1}{4}G_{\\mu\\nu}^a G^{a\\mu\\nu} + \\sum_q \\bar{q}(i\\gamma^\\mu D_\\mu - m_q)q",
    formula_description: "The quantum field theory of the strong nuclear force describing colour-charged quarks and gluons. The gluon field strength tensor $G_{\\mu\\nu}^a$ encodes self-interaction of gluons (absent in QED), giving rise to quark confinement and asymptotic freedom."
  },

  "quantum electrodynamics": {
    formula: "\\alpha = \\frac{e^2}{4\\pi\\varepsilon_0 \\hbar c} \\approx \\frac{1}{137.036}, \\quad E = \\hbar\\omega\\left(n + \\tfrac{1}{2}\\right)",
    formula_description: "The relativistic quantum theory of electromagnetic interactions. The fine-structure constant $\\alpha$ sets the strength of photon-electron coupling; quantized radiation field modes carry zero-point energy $\\frac{1}{2}\\hbar\\omega$ above vacuum."
  },

  "quantum hall effect": {
    formula: "R_{xy} = \\frac{V_H}{I} = \\frac{h}{\\nu e^2}, \\quad \\nu = 1, 2, 3, \\ldots \\;(\\text{integer}), \\quad \\sigma_{xy} = \\nu \\frac{e^2}{h}",
    formula_description: "Two-dimensional magnetoelectronic phenomenon: the transverse (Hall) resistance $R_{xy}$ is quantized in exact integer (or fractional) multiples of $h/e^2 \\approx 25.813\\;\\text{k}\\Omega$, providing a fundamental metrological standard of electrical resistance."
  },

  "quantum hypothesis": {
    formula: "E_n = nh\\nu = n\\hbar\\omega, \\quad n = 0, 1, 2, \\ldots, \\quad B_\\lambda = \\frac{2hc^2}{\\lambda^5}\\frac{1}{e^{hc/\\lambda k_B T}-1}",
    formula_description: "Planck's revolutionary 1900 postulate that oscillators can only emit or absorb electromagnetic energy in discrete integer multiples $n$ of the quantum $h\\nu$. This resolved the ultraviolet catastrophe and launched quantum physics."
  },

  "quantum yield": {
    formula: "\\Phi = \\frac{\\text{photons emitted (or reaction events)}}{\\text{photons absorbed}} = \\frac{k_{\\text{rad}}}{k_{\\text{rad}} + k_{\\text{nr}}}",
    formula_description: "Efficiency measure of a photophysical or photochemical process: the fraction of absorbed photons that lead to the desired outcome (fluorescence, reaction). For fluorescence, it equals the ratio of the radiative decay rate $k_{\\text{rad}}$ to total decay rate."
  },

  "quantum entanglement": {
    formula: "|\\Psi^-\\rangle = \\frac{1}{\\sqrt{2}}(|01\\rangle - |10\\rangle), \\quad S = -\\text{Tr}(\\rho\\ln\\rho) = -\\sum_i \\lambda_i \\ln\\lambda_i",
    formula_description: "Non-classical correlation between separated quantum systems: the Bell singlet state $|\\Psi^-\\rangle$ has total spin zero but neither particle has a definite spin. Entanglement entropy $S$ quantifies the degree of correlation via eigenvalues $\\lambda_i$ of the reduced density matrix $\\rho$."
  },

  "quantum state": {
    formula: "|\\psi\\rangle = \\sum_n c_n |n\\rangle, \\quad \\langle\\psi|\\psi\\rangle = \\sum_n |c_n|^2 = 1, \\quad P(n) = |c_n|^2",
    formula_description: "A complete description of a quantum system as a normalized vector (ket) in Hilbert space. A superposition of basis states $|n\\rangle$ with complex amplitudes $c_n$; the probability of measuring eigenvalue $n$ is $|c_n|^2$ (Born rule)."
  },

  "quantum theory": {
    formula: "[\\hat{x}, \\hat{p}] = i\\hbar, \\quad E_n = \\hbar\\omega_n, \\quad P(a) = |\\langle a|\\psi\\rangle|^2",
    formula_description: "The fundamental framework of physics governing the microscopic world. The canonical commutation relation $[\\hat{x}, \\hat{p}] = i\\hbar$ captures wave-particle duality; energy is quantized in units of $\\hbar\\omega$; and Born's rule gives measurement probabilities."
  },

  "quark": {
    formula: "Q = I_3 + \\frac{B+S+C+B'+T}{2}, \\quad u = +\\tfrac{2}{3}e,\\; d = -\\tfrac{1}{3}e,\\quad uud = p^+,\\; udd = n^0",
    formula_description: "Fundamental spin-1/2 constituents of hadrons carrying fractional electric charge ($+2e/3$ or $-e/3$). The Gell-Mann-Nishijima formula relates electric charge $Q$ to isospin $I_3$, baryon number $B$, strangeness $S$, charm $C$, bottomness $B'$, and topness $T$."
  },

  "quark confinement": {
    formula: "V(r) \\approx -\\frac{4\\alpha_s}{3r} + \\kappa r, \\quad \\kappa \\approx 1\\;\\text{GeV/fm}, \\quad \\alpha_s(Q^2) = \\frac{12\\pi}{(33-2n_f)\\ln(Q^2/\\Lambda^2)}",
    formula_description: "The phenomenon that quarks cannot exist as free particles: the QCD inter-quark potential grows linearly with separation ($\\kappa r$), so the energy to separate quarks creates new quark-antiquark pairs instead. The running coupling $\\alpha_s$ decreases at high energy (asymptotic freedom)."
  },

  "quark-gluon plasma": {
    formula: "T_c \\approx 155\\;\\text{MeV} \\approx 1.8 \\times 10^{12}\\;\\text{K}, \\quad \\varepsilon_c \\approx 0.5\\;\\text{GeV/fm}^3, \\quad p = \\frac{g\\pi^2}{90}T^4",
    formula_description: "Deconfined state of quantum matter at extreme temperatures $T > T_c \\approx 155\\;\\text{MeV}$ where quarks and gluons move freely. Pressure follows the Stefan-Boltzmann law with degeneracy factor $g$; this state existed microseconds after the Big Bang."
  },

  "quarter-wave plate": {
    formula: "\\delta = \\frac{\\pi}{2}, \\quad d = \\frac{\\lambda}{4(n_e - n_o)}, \\quad \\mathbf{J}_{\\lambda/4} = e^{i\\pi/4}\\begin{pmatrix}1 & 0 \\\\ 0 & -i\\end{pmatrix}",
    formula_description: "An optical birefringent plate of thickness $d$ chosen to introduce a $\\pi/2$ phase retardation $\\delta$ between the ordinary and extraordinary polarization components, converting linearly polarized light into circularly polarized light (and vice versa)."
  },

  "quasar": {
    formula: "L \\sim 10^{38}\\text{-}10^{41}\\;\\text{W}, \\quad L_{\\text{Edd}} = \\frac{4\\pi G M m_p c}{\\sigma_T} \\approx 1.26 \\times 10^{31}\\left(\\frac{M}{M_\\odot}\\right)\\;\\text{W}, \\quad z = \\frac{\\Delta\\lambda}{\\lambda_0}",
    formula_description: "Quasi-stellar objects powered by accretion onto supermassive black holes ($M \\sim 10^6$-$10^{10}\\,M_\\odot$), radiating up to the Eddington luminosity $L_{\\text{Edd}}$. Their cosmological distance is inferred from redshift $z$ via Hubble's law."
  },

  "quasiparticle": {
    formula: "E_k = \\sqrt{\\left(\\frac{\\hbar^2 k^2}{2m} - \\mu\\right)^2 + \\Delta^2}, \\quad m^* = \\hbar^2\\left(\\frac{d^2 E}{dk^2}\\right)^{-1}",
    formula_description: "Effective particles emerging from collective quantum many-body interactions: Cooper pairs in superconductors have dispersion $E_k$ with pairing gap $\\Delta$; phonons (lattice quanta) carry sound; and the effective mass $m^*$ replaces bare electron mass in periodic crystal potentials."
  },

  "quenching": {
    formula: "\\frac{I_0}{I} = 1 + K_{\\text{SV}}[Q], \\quad K_{\\text{SV}} = k_q \\tau_0, \\quad \\tau = \\frac{\\tau_0}{1 + k_q [Q] \\tau_0}",
    formula_description: "The reduction of fluorescence intensity and lifetime by interaction with a quencher $[Q]$. The Stern-Volmer equation relates quenched intensity $I$ to unquenched $I_0$ via constant $K_{\\text{SV}} = k_q\\tau_0$, where $k_q$ is the bimolecular quenching rate and $\\tau_0$ the unquenched lifetime."
  },

  "quencher": {
    formula: "k_q = \\frac{K_{\\text{SV}}}{\\tau_0}, \\quad \\frac{F_0}{F} = 1 + k_q\\tau_0[Q]",
    formula_description: "A molecule that deactivates (quenches) an excited fluorophore through collisional or static mechanisms. The bimolecular quenching rate constant $k_q$ is derived from the Stern-Volmer slope $K_{\\text{SV}}$ divided by unquenched fluorescence lifetime $\\tau_0$."
  },

  "quiescent current": {
    formula: "I_Q = \\frac{V_{CC} - V_{CE}}{R_C}\\Bigg|_{\\text{no signal}}, \\quad P_Q = V_{CE} \\cdot I_Q",
    formula_description: "The static DC bias current drawn by an amplifier or transistor stage in the absence of an input signal, defining the quiescent operating (Q) point on the load line. Quiescent power dissipation $P_Q$ must remain within device thermal limits."
  },

  // -- MATHEMATICS --

  "quadratic equation": {
    formula: "ax^2 + bx + c = 0 \\;(a \\neq 0) \\implies x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}, \\quad \\Delta = b^2 - 4ac",
    formula_description: "A second-degree polynomial equation. The quadratic formula gives all roots in terms of coefficients $a$, $b$, $c$. The discriminant $\\Delta = b^2 - 4ac$ determines root nature: $\\Delta > 0$ (two real distinct roots), $\\Delta = 0$ (one repeated root), $\\Delta < 0$ (two complex conjugate roots)."
  },

  "quadratic formula": {
    formula: "x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}, \\quad \\alpha + \\beta = -\\frac{b}{a}, \\quad \\alpha\\beta = \\frac{c}{a}",
    formula_description: "The explicit closed-form solution for any quadratic $ax^2+bx+c=0$. The $\\pm$ sign yields two roots $\\alpha$ and $\\beta$; by Vieta's formulas, their sum is $-b/a$ and product is $c/a$."
  },

  "quadratic function": {
    formula: "f(x) = ax^2 + bx + c = a\\left(x + \\frac{b}{2a}\\right)^2 - \\frac{\\Delta}{4a}, \\quad \\text{Vertex: }\\left(-\\frac{b}{2a},\\; -\\frac{\\Delta}{4a}\\right)",
    formula_description: "A polynomial function of degree 2 whose graph is a parabola. Vertex (completed-square) form reveals the turning point: minimum when $a>0$, maximum when $a<0$. Axis of symmetry is $x = -b/(2a)$."
  },

  "quadratic mean": {
    formula: "Q_{\\text{rms}} = \\sqrt{\\frac{1}{n}\\sum_{i=1}^{n} x_i^2} = \\sqrt{\\bar{x^2}}, \\quad V_{\\text{rms}} = \\frac{V_0}{\\sqrt{2}}, \\quad I_{\\text{rms}} = \\frac{I_0}{\\sqrt{2}}",
    formula_description: "The root mean square (RMS) of a dataset: the square root of the arithmetic mean of the squares of all values. Used in AC circuit analysis (RMS voltage/current), signal processing, and as a measure of magnitude of a varying quantity."
  },

  "quadratic reciprocity": {
    formula: "\\left(\\frac{p}{q}\\right)\\left(\\frac{q}{p}\\right) = (-1)^{\\frac{p-1}{2}\\cdot\\frac{q-1}{2}}, \\quad \\left(\\frac{-1}{p}\\right) = (-1)^{\\frac{p-1}{2}}, \\quad \\left(\\frac{2}{p}\\right) = (-1)^{\\frac{p^2-1}{8}}",
    formula_description: "Gauss's celebrated theorem relating Legendre symbols for distinct odd primes $p$ and $q$. It determines whether $p$ is a quadratic residue mod $q$ from the status of $q$ mod $p$, forming the cornerstone of elementary number theory."
  },

  "quadrature": {
    formula: "\\int_a^b f(x)\\,dx \\approx \\sum_{i=0}^{n} w_i f(x_i), \\quad \\text{Trap: } \\frac{h}{2}[f_0 + 2\\sum_{k=1}^{n-1}f_k + f_n], \\quad \\text{Simpson: } \\frac{h}{3}[f_0 + 4f_1 + 2f_2 + \\cdots + f_n]",
    formula_description: "The numerical or analytical computation of a definite integral (area under a curve). Gauss-Legendre quadrature uses optimally chosen nodes $x_i$ and weights $w_i$; trapezoidal and Simpson's rules use equally spaced points with increasing accuracy."
  },

  "quadrature amplitude modulation": {
    formula: "s(t) = I(t)\\cos(2\\pi f_c t) - Q(t)\\sin(2\\pi f_c t), \\quad N_{\\text{bits/symbol}} = \\log_2 M, \\quad C = B\\log_2(1 + \\text{SNR})",
    formula_description: "QAM encodes data on both in-phase (I) and quadrature (Q) components of a carrier. With $M$-QAM, each symbol carries $\\log_2 M$ bits. Channel capacity is bounded by Shannon's formula."
  },

  "quadrilateral": {
    formula: "\\text{Angle sum} = (4-2) \\times 180^\\circ = 360^\\circ, \\quad A_{\\text{trap}} = \\frac{h(a+b)}{2}, \\quad A_{\\text{general}} = \\frac{1}{2}|d_1 d_2 \\sin\\theta|",
    formula_description: "A polygon with four sides and four interior angles always summing to $360^\\circ$. Area depends on type: trapezium uses parallel sides $a$, $b$ and height $h$; a general quadrilateral uses diagonal lengths $d_1$, $d_2$ and included angle $\\theta$."
  },

  "quadrupole": {
    formula: "Q_{ij} = \\sum_k q_k(3r_{ki}r_{kj} - r_k^2\\delta_{ij}), \\quad V \\sim \\frac{Q_{ij}\\hat{r}_i\\hat{r}_j}{r^3} \\quad (r \\to \\infty)",
    formula_description: "A charge distribution with zero net charge and zero dipole moment. Its electric potential falls as $r^{-3}$ and is characterized by the traceless quadrupole moment tensor $Q_{ij}$. Gravitational wave emission by orbiting masses is fundamentally quadrupolar."
  },

  "quartile": {
    formula: "Q_1 = 25^{\\text{th}}\\text{ percentile}, \\quad Q_2 = 50^{\\text{th}}\\text{ percentile (Median)}, \\quad Q_3 = 75^{\\text{th}}\\text{ percentile}, \\quad IQR = Q_3 - Q_1",
    formula_description: "The three quartile values $Q_1$, $Q_2$, $Q_3$ divide an ordered dataset into four equal parts. The interquartile range $IQR = Q_3 - Q_1$ measures the spread of the central 50% of data and is a robust measure of dispersion, resistant to outliers."
  },

  "quartile deviation": {
    formula: "QD = \\frac{Q_3 - Q_1}{2} = \\frac{IQR}{2}, \\quad \\text{Coefficient of QD} = \\frac{Q_3 - Q_1}{Q_3 + Q_1}",
    formula_description: "The semi-interquartile range: half the difference between upper ($Q_3$) and lower ($Q_1$) quartiles. Measures the dispersion of the central half of a distribution and is resistant to extreme values. The coefficient form allows comparison across different-scale datasets."
  },

  "quantiles": {
    formula: "P_k = L + \\frac{\\left(\\frac{kN}{100} - F\\right)}{f} \\times h, \\quad k=25 \\Rightarrow Q_1, \\quad k=50 \\Rightarrow Q_2, \\quad k=75 \\Rightarrow Q_3",
    formula_description: "Values that divide a ranked dataset into equal-sized groups. The $k$-th percentile $P_k$ is found by interpolation: $L$ is class lower boundary, $F$ cumulative frequency before the class, $f$ class frequency, $h$ class width, $N$ total observations."
  },

  "quotient rule": {
    formula: "\\frac{d}{dx}\\left[\\frac{f(x)}{g(x)}\\right] = \\frac{f'(x)\\,g(x) - f(x)\\,g'(x)}{[g(x)]^2}, \\quad g(x) \\neq 0",
    formula_description: "The calculus differentiation rule for the ratio of two differentiable functions: 'low d-high minus high d-low, all over low squared.' Derived from the product rule applied to $f(x) \\cdot [g(x)]^{-1}$."
  },

  "quotient": {
    formula: "a \\div b = q + \\frac{r}{b}, \\quad a = bq + r, \\quad 0 \\leq r < b, \\quad q = \\lfloor a/b \\rfloor",
    formula_description: "The result of division: when $a$ (dividend) is divided by $b$ (divisor), the integer quotient $q$ and remainder $r$ satisfy the division algorithm $a = bq + r$. In abstract algebra, quotient structures (groups, rings, spaces) arise from factoring out equivalence relations."
  },

  "quotient group": {
    formula: "G/N = \\{gN : g \\in G\\}, \\quad |G/N| = \\frac{|G|}{|N|}, \\quad (g_1 N)(g_2 N) = (g_1 g_2)N",
    formula_description: "The set of cosets $gN$ of a normal subgroup $N$ in group $G$, forming a group under coset multiplication. By Lagrange's theorem the order $|G/N| = |G|/|N|$. Quotient groups are fundamental to the first isomorphism theorem of group theory."
  },

  "quotient ring": {
    formula: "R/I = \\{a + I : a \\in R\\}, \\quad (a+I)(b+I) = ab+I, \\quad R/I\\text{ is a field} \\iff I\\text{ is maximal}",
    formula_description: "The ring formed by cosets of an ideal $I$ in ring $R$ under coset addition and multiplication. If $I$ is a prime ideal, $R/I$ is an integral domain; if $I$ is a maximal ideal, $R/I$ is a field."
  },

  "quotient of powers property": {
    formula: "\\frac{a^m}{a^n} = a^{m-n} \\quad (a \\neq 0), \\quad \\left(\\frac{a}{b}\\right)^n = \\frac{a^n}{b^n}, \\quad a^0 = 1",
    formula_description: "Fundamental index law governing division of powers with the same base: the exponent of the quotient equals the difference of exponents. Equivalent logarithm form: $\\log(a/b) = \\log a - \\log b$."
  },

  "quaternion": {
    formula: "\\mathbf{q} = a + bi + cj + dk, \\quad i^2 = j^2 = k^2 = ijk = -1, \\quad |\\mathbf{q}|^2 = a^2+b^2+c^2+d^2",
    formula_description: "Hamilton's 4-dimensional extension of complex numbers, with three imaginary units $i$, $j$, $k$ satisfying non-commutative multiplication. Unit quaternions ($|\\mathbf{q}|=1$) elegantly represent 3D rotations without gimbal lock, essential in aerospace, robotics, and 3D graphics."
  },

  "queuing theory": {
    formula: "\\rho = \\frac{\\lambda}{\\mu} < 1, \\quad L = \\frac{\\rho}{1-\\rho}, \\quad W = \\frac{1}{\\mu - \\lambda}, \\quad L = \\lambda W \\;(\\text{Little's Law})",
    formula_description: "Mathematical study of waiting lines (queues). For the M/M/1 queue at traffic intensity $\\rho = \\lambda/\\mu$ (arrival rate/service rate): average queue length $L = \\rho/(1-\\rho)$ and average wait $W = 1/(\\mu - \\lambda)$ by Little's Law $L = \\lambda W$."
  },

  "quintic": {
    formula: "p(x) = a_5 x^5 + a_4 x^4 + a_3 x^3 + a_2 x^2 + a_1 x + a_0 \\quad (a_5 \\neq 0)",
    formula_description: "A polynomial of degree 5. By the Abel-Ruffini theorem (1824), the general quintic has no closed-form algebraic solution in radicals — unlike quadratics, cubics, and quartics. Solutions require elliptic functions (Hermite, 1858) or numerical methods."
  },

  // -- CHEMISTRY --

  "quinone": {
    formula: "\\text{C}_6\\text{H}_4\\text{O}_2 + 2H^+ + 2e^- \\rightleftharpoons \\text{C}_6\\text{H}_4(\\text{OH})_2, \\quad E^\\circ = +0.699\\;\\text{V (vs SHE)}",
    formula_description: "1,4-Benzoquinone undergoes reversible two-electron/two-proton reduction to hydroquinone (1,4-dihydroxybenzene) with standard reduction potential $E^\\circ = +0.699\\;\\text{V}$. This quinone/hydroquinone redox couple is fundamental in biological electron-transport chains and electrochemistry."
  },

  "quinine": {
    formula: "\\text{C}_{20}\\text{H}_{24}\\text{N}_2\\text{O}_2, \\quad M_r = 324.42\\;\\text{g/mol}, \\quad pK_{a1} = 4.13,\\; pK_{a2} = 8.52",
    formula_description: "Alkaloid antimalarial drug with molecular formula $\\text{C}_{20}\\text{H}_{24}\\text{N}_2\\text{O}_2$. It is a diprotic base ($pK_{a1} = 4.13$, $pK_{a2} = 8.52$) that intercalates into Plasmodium falciparum DNA. Also used as a bitter flavouring in tonic water."
  },

  "quinoline": {
    formula: "\\text{C}_9\\text{H}_7\\text{N}, \\quad M_r = 129.16\\;\\text{g/mol}, \\quad \\text{bp} = 237.1^\\circ\\text{C}, \\quad pK_a(\\text{BH}^+) = 4.85",
    formula_description: "Bicyclic aromatic heterocycle consisting of a benzene ring fused to a pyridine ring. Its scaffold forms the core of many antimalarial drugs (quinine, chloroquine) and pharmaceutical agents. Weakly basic with conjugate acid $pK_a = 4.85$."
  },

  "quinhydrone electrode": {
    formula: "E = E^\\circ_{\\text{BQ/H}_2\\text{Q}} - \\frac{RT}{F}\\ln[\\text{H}^+] = 0.6996 - 0.05916\\;\\text{pH} \\quad (25^\\circ\\text{C, vs SHE})",
    formula_description: "A half-cell for potentiometric pH measurement using the equimolar quinone-hydroquinone redox couple. Cell potential varies linearly with pH at 25 degrees C, giving a direct and precise route to $[H^+]$ with no calibration curve needed."
  },

  "quantitative analysis": {
    formula: "c = \\frac{n}{V}, \\quad n = \\frac{m}{M_r}, \\quad A = \\varepsilon c l \\;(\\text{Beer-Lambert}), \\quad V_1 c_1 = V_2 c_2 \\;(\\text{dilution})",
    formula_description: "Determination of exact amounts or concentrations of chemical species. Key relationships: molar concentration $c = n/V$, moles $n = m/M_r$. Beer-Lambert law $A = \\varepsilon c l$ links absorbance to concentration spectrophotometrically. Dilution law $V_1 c_1 = V_2 c_2$ governs solution preparation."
  },

  "quicklime": {
    formula: "\\text{CaCO}_3 \\xrightarrow{\\Delta,\\;>840^\\circ\\text{C}} \\text{CaO} + \\text{CO}_2, \\quad \\text{CaO} + \\text{H}_2\\text{O} \\to \\text{Ca(OH)}_2 \\quad \\Delta H = -57.8\\;\\text{kJ/mol}",
    formula_description: "Calcium oxide (CaO), produced by thermal decomposition (calcination) of limestone above 840 degrees C. Highly exothermic slaking reaction with water produces slaked lime $\\text{Ca(OH)}_2$. Used in cement manufacture, soil treatment, and flue gas desulfurization."
  },

  // -- BIOLOGY --

  "quorum sensing": {
    formula: "\\frac{d[AHL]}{dt} = \\alpha N - \\delta[AHL], \\quad \\text{Gene ON iff } [AHL] \\geq [AHL]^*",
    formula_description: "Bacterial cell-density-dependent gene regulation via autoinducer molecules (e.g., acyl-homoserine lactones, AHL). When bacterial density $N$ causes AHL to reach threshold $[AHL]^*$, virulence or bioluminescence genes switch on collectively as a population-wide response."
  },

  // -- STATISTICS --

  "quota sampling": {
    formula: "n_i = n \\times \\frac{N_i}{N}, \\quad \\sum_i n_i = n, \\quad \\bar{x}_{\\text{quota}} = \\frac{\\sum_i n_i \\bar{x}_i}{n}",
    formula_description: "Non-probability sampling in which the researcher assigns quotas $n_i$ to subgroups proportional to their population size $N_i/N$. Within each quota, participants are selected non-randomly. The overall sample mean is the weighted average of stratum means."
  },

  "quantitative data": {
    formula: "\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i, \\quad s^2 = \\frac{\\sum(x_i - \\bar{x})^2}{n-1}, \\quad r = \\frac{\\sum(x_i-\\bar{x})(y_i-\\bar{y})}{\\sqrt{\\sum(x_i-\\bar{x})^2 \\cdot \\sum(y_i-\\bar{y})^2}}",
    formula_description: "Numerical data measured on a continuous or discrete scale. Key statistics: arithmetic mean $\\bar{x}$, sample variance $s^2$, and Pearson correlation $r$. Enables parametric testing (t-test, ANOVA, regression) unlike qualitative data."
  }

};

/* ============================================================
   A P P L Y   E N R I C H M E N T S
============================================================ */
let enrichedCount = 0;
const qList = dict['Q'] || [];

qList.forEach(entry => {
  const key = entry.word.trim().toLowerCase();
  if (!qEnrichments[key]) return;

  const data = qEnrichments[key];
  entry.formula             = data.formula;
  entry.formula_description = data.formula_description;

  // Embed formula block cleanly into the definition
  if (!entry.definition || !entry.definition.includes('$$')) {
    entry.definition = `${(entry.definition || '').trim()}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
  } else {
    // Replace any existing $$ block for consistency
    const baseDef = entry.definition.split('$$')[0].trim();
    entry.definition = `${baseDef}\n\n$$\n${data.formula}\n$$\n*Formula:* ${data.formula_description}`;
  }

  enrichedCount++;
  console.log(`Enriched Q [${key}]`);
});

/* ============================================================
   S A V E
============================================================ */
fs.writeFileSync(dictPath, JSON.stringify(dict, null, 2), 'utf8');
console.log(`\nSuccessfully enriched ${enrichedCount} Section Q terms in dictionary.json`);
console.log('Now run:  python scripts/rebuild_core_dictionary.py');
