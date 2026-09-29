# 🚀 Osmosis Engineering Log & Next Session Roadmap

> **Session Date:** September 29, 2026  
> **Milestone Achieved:** Letter M Formula Enrichment Complete (51 Terms) + Universal Definition Embedder & Fast Node Builder  
> **Current Git Head:** `5c032f0` (`feat(formulas): embed formula blocks into definitions and rebuild runtime`)

---

## 📌 Executive Summary of Today's Work

1. **Letter M Formula Enrichment (Batch 3 Integrated):**
   - Added **24 new core STEM mathematical and physical formulas** with full KaTeX LaTeX typography and engineering descriptions.
   - Combined with Batch 1 (16 terms) and Batch 2 (11 terms), **Letter M now has 51 fully enriched formula terms**.

2. **UI Search & Formula Rendering Fix:**
   - **Root Cause Identified:** Previously, formulas were stored only under the separate `entry.formula` JSON property, but `module_library.js` and other screens render `entry.definition`.
   - **Engine Solution:** Created and ran [`scripts/embed_formulas_in_definitions.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/scripts/embed_formulas_in_definitions.js), which automatically embedded formula blocks (`$$...$$`) and descriptions directly into the `definition` field for **108 entries** across the dictionary.
   - Now, searching any formula term in `module_library.html` immediately renders the math equation card with the interactive copy button.

3. **High-Speed Node.js Runtime Builder:**
   - Created [`scripts/rebuild_core_dict.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/scripts/rebuild_core_dict.js) which generates [`core_dictionary.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_dictionary.js) (12.26 MB) in under 2 seconds without external dependencies.

---

## 🔬 Letter M — Enriched Formulas Overview (51 Terms Total)

### Batch 3 Terms (Added Today — 24 Terms)
| Term | Domain | Formula Summary |
|---|---|---|
| `malus' law` | Optics | $I = I_0 \cos^2\theta$ |
| `magnetic constant` | Electromagnetism | $\mu_0 = 4\pi \times 10^{-7}\ \text{H/m},\ c = 1/\sqrt{\varepsilon_0\mu_0}$ |
| `madelung's rule` | Quantum / Chemistry | $E \propto (n+l)$, lower $n$ fills first |
| `magnus effect` | Fluid Dynamics | $\mathbf{F}_L = \rho_\infty \mathbf{v}_\infty \times \boldsymbol{\Gamma}$ |
| `markovnikoff's rule` | Organic Chemistry | Carbocation stability in HX alkene addition |
| `mass action law` | Physical Chemistry | $K_c = \frac{[\text{C}]^c [\text{D}]^d}{[\text{A}]^a [\text{B}]^b},\ \Delta G^\circ = -RT\ln K$ |
| `maxwell's distribution` | Thermodynamics | $f(v) = 4\pi (m / 2\pi k_B T)^{3/2} v^2 e^{-mv^2 / 2k_B T}$ |
| `meissner effect` | Superconductivity | $\mathbf{B} = 0,\ \nabla^2\mathbf{B} = \frac{1}{\lambda_L^2}\mathbf{B}$ |
| `mellin transform` | Complex Analysis | $\{\mathcal{M}f\}(s) = \int_0^\infty x^{s-1} f(x)\,dx$ |
| `mid-ordinate rule` | Numerical Methods | $\int_a^b f(x) dx \approx h \sum f(m_i),\ \mathcal{O}(h^2)$ |
| `mariotte law` | Gas Laws | $P_1 V_1 = P_2 V_2\ (T = \text{const})$ |
| `mass-energy equation` | Special Relativity | $E_0 = m_0 c^2,\ E^2 = (pc)^2 + (m_0 c^2)^2$ |
| `mathieu's differential equation` | Mathematics | $y'' + (a - 2q\cos 2x)y = 0$ |
| `max-flow min-cut theorem` | Optimization | $\max \text{flow} = \min \text{cut}$ |
| `maximum modulus theorem` | Complex Analysis | $|f(z_0)| \le \max_{\partial D} |f(z)|$ |
| `maximum value theorem` | Real Analysis | Extreme Value Theorem on compact $[a,b]$ |
| `moore's law` | Computing | $N(t) = N_0 \cdot 2^{t/T}\ (T \approx 18\text{--}24\text{ mo})$ |
| `morera's theorem` | Complex Analysis | $\oint_\gamma f(z)dz = 0 \implies \text{holomorphic}$ |
| `multinomial distribution` | Probability | $P = \frac{n!}{\prod k_i!} \prod p_i^{k_i}$ |
| `multinomial theorem` | Algebra | $(\sum x_i)^n = \sum \binom{n}{k_1,\dots,k_m} \prod x_i^{k_i}$ |
| `multiplication law of probability`| Probability | $P(A \cap B) = P(A) \cdot P(B \mid A)$ |
| `möbius inversion formula` | Number Theory | $g(n) = \sum_{d \mid n} f(d) \iff f(n) = \sum_{d \mid n} \mu(d)g(n/d)$ |
| `mössbauer effect` | Nuclear Physics | $E_R = E_\gamma^2 / 2Mc^2,\ f_{\text{LM}} = \exp(-k^2\langle x^2\rangle / 3)$ |
| `mitscherlich's law` | Crystallography | Isomorphism law of crystals and stoichiometry |

### Batches 1 & 2 Terms (Committed in `ab417f8` & `06be327` — 27 Terms)
* `mach number`, `mach angle`, `maclaurin's series`, `maclaurin's formula`, `madelung constant`, `maxwell's equations`, `maxwell-boltzmann distribution`, `michaelis-menten kinetics`, `moment of inertia`, `momentum`, `magnetic field & flux`, `mass-energy equivalence`, `mean free path`, `modulus of elasticity`, `molar mass`, `muon`, `markov chain`, `maxwell relations`, `mean value theorem`, `melting point`, `michelson-morley experiment`, `molality`, `molar volume`, `mole fraction`, `molecular orbital theory`, `moseley's law`, `möbius function`.

---

## 📂 Key Files Modified / Created Today

| File | Purpose |
|---|---|
| [`dictionary.json`](file:///c:/Users/Desmond/Desktop/final_osmosis/dictionary.json) | Master STEM database with all 51 Section M formulas embedded |
| [`core_dictionary.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/core_dictionary.js) | Compiled browser runtime dictionary & search index |
| [`scripts/enrich_section_m_batch3.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/scripts/enrich_section_m_batch3.js) | Section M Batch 3 enrichment script |
| [`scripts/embed_formulas_in_definitions.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/scripts/embed_formulas_in_definitions.js) | Universal script that embeds `entry.formula` into `entry.definition` |
| [`scripts/rebuild_core_dict.js`](file:///c:/Users/Desmond/Desktop/final_osmosis/scripts/rebuild_core_dict.js) | Fast Node builder for `core_dictionary.js` |
| [`check this .md`](file:///c:/Users/Desmond/Desktop/final_osmosis/check%20this%20.md) | Permanent handoff & log file |

---

## 🎯 Next Session Launchpad (Where to Start Next Time)

1. **Section N Formula Enrichment (Next in Line):**
   - Section N contains **801 terms**.
   - Prime STEM candidates include:
     - *Nernst equation* ($E = E^\circ - \frac{RT}{zF} \ln Q$)
     - *Newton's laws of motion* ($F = ma$, $F = dp/dt$, action-reaction)
     - *Newton's law of cooling* ($\frac{dT}{dt} = -k(T - T_{\text{env}})$)
     - *Newton's law of universal gravitation* ($F = G \frac{m_1 m_2}{r^2}$)
     - *Newton–Raphson method* ($x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$)
     - *Navier–Stokes equations* ($\rho (\frac{\partial \mathbf{u}}{\partial t} + \mathbf{u}\cdot\nabla\mathbf{u}) = -\nabla p + \mu \nabla^2\mathbf{u} + \mathbf{f}$)
     - *Napierian / Natural logarithm* ($\ln x = \int_1^x \frac{1}{t}dt$)
     - *Norton's theorem* ($I_N, R_N$ equivalent circuit)
     - *Nuclear binding energy* ($\Delta E = \Delta m \cdot c^2$)
     - *Normal distribution* ($f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$)

2. **Publishing Local Commits to GitHub:**
   - In your authenticated terminal, simply run:
     ```bash
     git push
     ```
   - This will publish commits `5400db3` and `5c032f0` directly to origin.