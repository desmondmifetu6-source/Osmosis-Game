"""
enrich_section_f_batch_1.py
===========================
Section F Formula Enrichment - Batch 1 (Terms 1 to 50)
Typesetting mathematical, chemical, and physical formulas into KaTeX ($ ... $ and $$ ... $$).
"""

import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

f_entries = data.get('F', [])

UPDATES = {
    # 1. f-sigma set
    5: (
        "A subset of a topological space expressible as the countable union of closed sets, conventionally denoted $F_\\sigma$ (from French 'fermé' for closed and 'somme' for union):\n\n"
        "$$A = \\bigcup_{n=1}^\\infty F_n$$\n\n"
        "where each $F_n$ is a closed set. In any metric space, every open set is an $F_\\sigma$ set, as is the set of rational numbers $\\mathbb{Q}$ as a subset of the real line $\\mathbb{R}$. The topological dual is a $G_\\delta$ set (a countable intersection of open sets)."
    ),

    # 2. fact extensions
    26: (
        "In arithmetic education, the systematic extension of fundamental number facts to higher orders of magnitude using base-10 place-value properties. For example, knowing the basic multiplication fact $5 \\times 10 = 50$ directly extends to $50 \\times 10 = 500$, $500 \\div 10 = 50$, and $50 \\times 100 = 5000$ across all four basic arithmetic operations."
    ),

    # 3. fact family
    27: (
        "A collection of related arithmetic operations linking three numbers through inverse operations. In addition and subtraction, a fact family linking $a, b, c$ where $a + b = c$ consists of four equations:\n\n"
        "$$a + b = c, \\quad b + a = c, \\quad c - a = b, \\quad c - b = a$$\n\n"
        "(e.g., $10 + 6 = 16$, $6 + 10 = 16$, $16 - 6 = 10$, and $16 - 10 = 6$). In multiplication and division with $a \\times b = c$ ($b \\neq 0$):\n\n"
        "$$a \\times b = c, \\quad b \\times a = c, \\quad c \\div a = b, \\quad c \\div b = a$$\n\n"
        "(e.g., $4 \\times 6 = 24$, $6 \\times 4 = 24$, $24 \\div 6 = 4$, and $24 \\div 4 = 6$)."
    ),

    # 4. factor
    29: (
        "1. In arithmetic and algebra, an integer or polynomial that divides another evenly with zero remainder (a divisor). For example, the integer factors of $24$ are $\\{\\pm 1, \\pm 2, \\pm 3, \\pm 4, \\pm 6, \\pm 8, \\pm 12, \\pm 24\\}$; the polynomial $f(x) = 2x^3 + 3x^2 - 5x - 6$ factors over $\\mathbb{R}$ as $(x + 1)(x + 2)(2x - 3)$. 2. In permutation groups, any of a set of disjoint cycles whose composition equals a given permutation. 3. In biological and medical sciences, an environmental condition (abiotic/biotic factor) or physiological agent such as clotting factors or growth factors."
    ),

    # 5. factor formulae
    31: (
        "The standard sum-to-product trigonometric identities (Simpson's formulas):\n\n"
        "$$\\sin A + \\sin B = 2\\sin\\left(\\frac{A + B}{2}\\right)\\cos\\left(\\frac{A - B}{2}\\right)$$\n\n"
        "$$\\sin A - \\sin B = 2\\sin\\left(\\frac{A - B}{2}\\right)\\cos\\left(\\frac{A + B}{2}\\right)$$\n\n"
        "$$\\cos A + \\cos B = 2\\cos\\left(\\frac{A + B}{2}\\right)\\cos\\left(\\frac{A - B}{2}\\right)$$\n\n"
        "$$\\cos A - \\cos B = -2\\sin\\left(\\frac{A + B}{2}\\right)\\sin\\left(\\frac{A - B}{2}\\right)$$"
    ),

    # 6. factor theorem
    39: (
        "A foundational algebraic theorem (a direct consequence of the polynomial remainder theorem) stating that a linear polynomial $(x - k)$ is a factor of a polynomial $f(x)$ if and only if $k$ is a root of $f(x)$:\n\n"
        "$$f(k) = 0 \\iff (x - k) \\mid f(x)$$\n\n"
        "For example, for $f(x) = x^3 + 2x^2 + 3x - 6$, evaluating at $x = 1$ gives $f(1) = 1 + 2 + 3 - 6 = 0$; therefore $(x - 1)$ is an exact algebraic factor of $f(x)$."
    ),

    # 7. factorial
    43: (
        "The mathematical function denoted by an exclamation mark ($!$), defining the product of all positive integers less than or equal to a non-negative integer $n$:\n\n"
        "$$n! = \\prod_{k=1}^n k = n \\times (n - 1) \\times \\dots \\times 2 \\times 1$$\n\n"
        "with the empty product definition $0! = 1$. Evaluated iteratively: $1! = 1$, $2! = 2$, $3! = 6$, $4! = 24$, $5! = 120$. Generalized to complex numbers via the Euler gamma function: $\\Gamma(n + 1) = n!$."
    ),

    # 8. factorial series
    45: (
        "An infinite mathematical series whose general terms involve reciprocal products of shifted linear factors (Pochhammer symbols or falling factorials):\n\n"
        "$$\\sum_{n=0}^\\infty \\frac{a_n}{z(z + 1)(z + 2)\\dots(z + n)}$$\n\n"
        "for $z \\notin \\{0, -1, -2, \\dots\\}$. Factorial series share key convergence and analytic properties with ordinary Dirichlet series in the complex half-plane $\\operatorname{Re}(z) > \\lambda$."
    ),

    # 9. fahrenheit, gabriel daneil
    54: (
        "Gabriel Daniel Fahrenheit (1686–1736), German physicist and precision instrument maker who invented the mercury-in-glass thermometer (1714) and established the Fahrenheit temperature scale. The conversion formulas connecting degrees Fahrenheit ($^\\circ\\text{F}$) and degrees Celsius ($^\\circ\\text{C}$) are:\n\n"
        "$$T_{^\\circ\\text{C}} = (T_{^\\circ\\text{F}} - 32) \\times \\frac{5}{9}$$\n\n"
        "$$T_{^\\circ\\text{F}} = \\left(T_{^\\circ\\text{C}} \\times \\frac{9}{5}\\right) + 32$$\n\n"
        "On this scale, the normal freezing point of pure water is $32\\,^\\circ\\text{F}$ ($0\\,^\\circ\\text{C}$) and the standard boiling point is $212\\,^\\circ\\text{F}$ ($100\\,^\\circ\\text{C}$) at $1\\,\\text{atm}$."
    ),

    # 10. failure rate
    55: (
        "In reliability engineering and survival analysis, the instantaneous hazard rate $h(t)$ defining the conditional probability of system failure during interval $[t, t + \\Delta t]$, given that it survived up to time $t$:\n\n"
        "$$h(t) = \\lim_{\\Delta t \\to 0} \\frac{P(t \\le T < t + \\Delta t \\mid T > t)}{\\Delta t} = \\frac{f(t)}{R(t)} = -\\frac{d}{dt}\\ln R(t)$$\n\n"
        "where $f(t)$ is the failure probability density function and $R(t) = 1 - F(t)$ is the reliability (survival) function."
    ),

    # 11. false position
    73: (
        "The method of false position (*regula falsi*), a root-finding algorithm combining the guaranteed convergence of the bisection method with the linear interpolation speed of the secant method. Given an interval $[a, b]$ with $f(a)f(b) < 0$, the root estimate is computed as the $x$-intercept of the secant line connecting $(a, f(a))$ and $(b, f(b))$:\n\n"
        "$$c = \\frac{a f(b) - b f(a)}{f(b) - f(a)} = b - f(b)\\frac{b - a}{f(b) - f(a)}$$"
    ),

    # 12. family of confocal central conics
    79: (
        "A one-parameter family of central quadric curves (ellipses and hyperbolas) sharing identical foci $F_1, F_2 = (\\pm c, 0)$, described analytically in Cartesian coordinates by:\n\n"
        "$$\\frac{x^2}{a^2 + \\lambda} + \\frac{y^2}{b^2 + \\lambda} = 1$$\n\n"
        "where $\\lambda$ is an arbitrary parameter. For $-b^2 < \\lambda < \\infty$ the curves are confocal ellipses; for $-a^2 < \\lambda < -b^2$ they form confocal orthogonal hyperbolas. The governing first-order differential equation for the orthogonal trajectories is $(xy' - y)(yy' + x) = (a^2 - b^2)y'$."
    ),

    # 13. family of curves
    80: (
        "A set of planar geometric curves defined by a single analytical equation involving one or more arbitrary parameters. For example, $y = 2x^2 + C$ represents a family of congruent parabolas translated vertically by parameter $C$, satisfying the ordinary differential equation $\\frac{dy}{dx} = 4x$."
    ),

    # 14. farad
    89: (
        "The SI derived unit of electrical capacitance, named in honour of Michael Faraday, with symbol $\\text{F}$. A capacitor has a capacitance of $1\\,\\text{farad}$ when storing an electric charge of $1\\,\\text{coulomb}$ creates an electric potential difference of $1\\,\\text{volt}$ across its plates:\n\n"
        "$$1\\,\\text{F} = 1\\,\\text{C}\\cdot\\text{V}^{-1} = 1\\,\\text{s}^4\\cdot\\text{A}^2\\cdot\\text{m}^{-2}\\cdot\\text{kg}^{-1}$$\n\n"
        "In practical electronics, microfarads ($1\\,\\mu\\text{F} = 10^{-6}\\,\\text{F}$), nanofarads ($1\\,\\text{nF} = 10^{-9}\\,\\text{F}$), and picofarads ($1\\,\\text{pF} = 10^{-12}\\,\\text{F}$) are standard."
    ),

    # 15. faraday constant
    96: (
        "The fundamental physical constant $F$ representing the magnitude of electric charge per mole of electrons. Defined as the product of the Avogadro constant $N_A$ and elementary charge $e$:\n\n"
        "$$F = N_A e = (6.02214076 \\times 10^{23}\\,\\text{mol}^{-1})(1.602176634 \\times 10^{-19}\\,\\text{C}) = 96485.33212\\dots\\,\\text{C}\\cdot\\text{mol}^{-1}$$\n\n"
        "It acts as the primary conversion factor in electrochemical cell equations and Faraday's laws of electrolysis."
    ),

    # 16. faraday's law of electromagnetic induction
    99: (
        "The fundamental law of electromagnetism stating that the electromotive force (EMF, $\\mathcal{E}$) induced in an electrical circuit is directly proportional to the negative time rate of change of magnetic flux $\\Phi_B$ enclosed by the circuit:\n\n"
        "$$\\mathcal{E} = -N\\frac{d\\Phi_B}{dt}$$\n\n"
        "where $\\Phi_B = \\iint_S \\mathbf{B} \\cdot d\\mathbf{A}$ and $N$ is the number of turns. Expressed locally in Maxwell's third equation (Maxwell-Faraday equation) as $\\nabla \\times \\mathbf{E} = -\\frac{\\partial \\mathbf{B}}{\\partial t}$."
    ),

    # 17. faraday's laws of electrolysis
    100: (
        "The quantitative laws of electrochemical decomposition established by Michael Faraday: 1. First Law: the mass $m$ of a substance altered or liberated at an electrode is directly proportional to the total electric charge $Q = It$ passed:\n\n"
        "$$m = Z Q = Z I t$$\n\n"
        "where $Z$ is the electrochemical equivalent. 2. Second Law: for a given quantity of electric charge, the deposited mass is proportional to the substance's equivalent weight (molar mass $M$ divided by valence number $z$):\n\n"
        "$$m = \\frac{Q M}{z F} = \\frac{I t M}{z F}$$\n\n"
        "where $F \\approx 96485\\,\\text{C}\\cdot\\text{mol}^{-1}$ is the Faraday constant."
    ),

    # 18. farkas' lemma
    105: (
        "A celebrated solvability theorem and alternative theorem in convex geometry and linear programming, established by Gyula Farkas. For a given matrix $\\mathbf{A} \\in \\mathbb{R}^{m \\times n}$ and vector $\\mathbf{b} \\in \\mathbb{R}^m$, exactly one of the following two statements holds:\n\n"
        "1. There exists a vector $\\mathbf{x} \\in \\mathbb{R}^n$ such that $\\mathbf{A}\\mathbf{x} = \\mathbf{b}$ and $\\mathbf{x} \\ge \\mathbf{0}$.\n"
        "2. There exists a vector $\\mathbf{y} \\in \\mathbb{R}^m$ such that $\\mathbf{A}^T\\mathbf{y} \\ge \\mathbf{0}$ and $\\mathbf{b}^T\\mathbf{y} < 0$.\n\n"
        "This lemma forms the mathematical bedrock of the Karush-Kuhn-Tucker (KKT) optimality conditions and strong duality in linear programming."
    ),

    # 19. fatou's lemma
    135: (
        "A foundational theorem in Lebesgue integration and measure theory relating the integral of the limit inferior of a sequence of non-negative measurable functions to the limit inferior of their integrals. If $\\{f_n\\}$ is a sequence of non-negative measurable functions on a measure space $(X, \\Sigma, \\mu)$, then:\n\n"
        "$$\\int_X \\liminf_{n \\to \\infty} f_n\\,d\\mu \\le \\liminf_{n \\to \\infty} \\int_X f_n\\,d\\mu$$\n\n"
        "Crucial in establishing the monotone convergence theorem and Lebesgue's dominated convergence theorem."
    ),

    # 20. feit-thompson theorem
    166: (
        "The monumental Odd Order Theorem in finite group theory proved by Walter Feit and John G. Thompson (1963), stating that every finite group of odd order is solvable:\n\n"
        "$$|G| \\equiv 1 \\pmod 2 \\implies G \\text{ is solvable}$$\n\n"
        "Equivalently, every non-abelian finite simple group has even order (and hence contains an element of order 2, an involution). The proof spanned an entire 255-page journal issue and was a pivotal breakthrough toward the full Classification of Finite Simple Groups."
    ),

    # 21. fejer's theorem
    167: (
        "A classical theorem in harmonic analysis proved by Lipót Fejér (1900), stating that if $f: \\mathbb{R} \\to \\mathbb{C}$ is a continuous $2\\pi$-periodic function, then the sequence of Cesàro means (arithmetic means of partial sums) $\\sigma_n(f)(x)$ of the Fourier series of $f$ converges uniformly to $f(x)$ on $[-\\pi, \\pi]$:\n\n"
        "$$\\lim_{n \\to \\infty} \\sigma_n(f)(x) = \\lim_{n \\to \\infty} \\frac{1}{n+1}\\sum_{k=0}^n S_k(f)(x) = f(x)$$\n\n"
        "This resolves the convergence issues of standard Fourier partial sums, which need not converge pointwise for continuous functions."
    ),

    # 22. fenchel's duality theorem
    181: (
        "A fundamental theorem in convex optimization and nonlinear analysis. Let $f: X \\to \\mathbb{R} \\cup \\{+\\infty\\}$ be a proper convex function and $g: X \\to \\mathbb{R} \\cup \\{-\\infty\\}$ be a proper concave function on a normed space $X$. Under standard qualification conditions ($0 \\in \\operatorname{core}(\\operatorname{dom} f - \\operatorname{dom} g)$):\n\n"
        "$$\\inf_{x \\in X} [f(x) - g(x)] = \\max_{x^* \\in X^*} [g_*(x^*) - f^*(x^*)]$$\n\n"
        "where $f^*$ is the convex Fenchel conjugate of $f$ and $g_*$ is the concave conjugate of $g$."
    ),

    # 23. fermat's last theorem
    188: (
        "The renowned number-theoretic theorem formulated by Pierre de Fermat in 1637 and proved by Andrew Wiles in 1995. It states that no three positive integers $a, b, c$ can satisfy the Diophantine equation:\n\n"
        "$$a^n + b^n = c^n$$\n\n"
        "for any integer value of $n > 2$. (For $n = 2$, infinitely many primitive integer solutions exist as Pythagorean triples, e.g., $3^2 + 4^2 = 5^2$)."
    ),

    # 24. fermat's little theorem
    189: (
        "A fundamental result in elementary number theory: if $p$ is a prime number and $a$ is any integer not divisible by $p$ ($\\gcd(a, p) = 1$), then:\n\n"
        "$$a^{p-1} \\equiv 1 \\pmod p$$\n\n"
        "Equivalently, for any integer $a$ and prime $p$:\n\n"
        "$$a^p \\equiv a \\pmod p$$\n\n"
        "Widely utilized in modular arithmetic, the Fermat primality test, and the RSA public-key cryptographic algorithm."
    ),

    # 25. fermat's spiral
    191: (
        "A parabolic spiral curve discovered by Pierre de Fermat, characterized in polar coordinates $(r, \\theta)$ by the relationship:\n\n"
        "$$r^2 = a^2 \\theta \\implies r = \\pm a\\sqrt{\\theta}$$\n\n"
        "where $a$ is a non-zero scaling constant. It possesses central symmetry with respect to the origin. In phyllotaxis, sunflower seed arrangements and plant florets naturally model Fermat's spiral using the golden divergence angle $\\theta \\approx 137.508^\\circ$."
    ),

    # 26. fermi constant
    197: (
        "The fundamental coupling constant $G_F$ governing the strength of the weak interaction in particle physics (Fermi's four-fermion interaction theory of beta decay):\n\n"
        "$$\\frac{G_F}{(\\hbar c)^3} = \\frac{\\sqrt{2}}{8}\\frac{g^2}{M_W^2} = 1.1663787(6) \\times 10^{-5}\\,\\text{GeV}^{-2}$$\n\n"
        "In SI units, $G_F \\approx 1.43585 \\times 10^{-62}\\,\\text{J}\\cdot\\text{m}^3$. It is experimentally determined with ultra-high precision from the measurement of the muon lifetime $\\tau_\\mu$."
    ),

    # 27. ferrel's law
    214: (
        "A meteorological principle formulated by William Ferrel (1856), derived from the Coriolis effect on a rotating Earth. It states that any fluid parcel (wind or ocean current) moving freely over the Earth's surface undergoes an apparent horizontal deflection to the right in the Northern Hemisphere and to the left in the Southern Hemisphere, governed by the horizontal Coriolis acceleration:\n\n"
        "$$a_C = 2 v \\Omega \\sin\\phi$$\n\n"
        "where $v$ is flow speed, $\\Omega = 7.292 \\times 10^{-5}\\,\\text{rad}\\cdot\\text{s}^{-1}$ is Earth's angular velocity, and $\\phi$ is latitude."
    ),

    # 28. fibonacci distribution
    253: (
        "In discrete probability theory, the probability distribution of the waiting time (number of Bernoulli trials $X$) until the first occurrence of two consecutive successes in independent trials with success probability $p = 1/2$. The probability mass function is expressed in terms of Fibonacci numbers $F_n$ as:\n\n"
        "$$P(X = x) = \\frac{F_{x-1}}{2^x}, \\quad x = 2, 3, 4, \\dots$$\n\n"
        "where $F_1 = 1, F_2 = 1, F_3 = 2, F_4 = 3, \\dots$, summing to $\\sum_{x=2}^\\infty P(X = x) = 1$."
    ),

    # 29. fick's laws
    281: (
        "The governing physical laws of molecular diffusion formulated by Adolf Fick (1855): 1. Fick's First Law relates the diffusive particle flux $\\mathbf{J}$ to the concentration gradient $\\nabla c$:\n\n"
        "$$\\mathbf{J} = -D \\nabla c \\quad \\left(\\text{in 1D: } J = -D\\frac{dc}{dx}\\right)$$\n\n"
        "where $D$ is the diffusion coefficient. 2. Fick's Second Law describes the time evolution of concentration under non-steady state conditions:\n\n"
        "$$\\frac{\\partial c}{\\partial t} = D \\nabla^2 c = D \\frac{\\partial^2 c}{\\partial x^2}$$"
    ),

    # 30. field of fractions
    292: (
        "The quotient field $\\operatorname{Quot}(R)$ of an integral domain $R$, defined as the set of equivalence classes of formal fractions $\\frac{a}{b}$ with $a, b \\in R$ and $b \\neq 0$, where $\\frac{a}{b} = \\frac{c}{d} \\iff ad = bc$. Addition and multiplication are defined by:\n\n"
        "$$\\frac{a}{b} + \\frac{c}{d} = \\frac{ad + bc}{bd}, \\quad \\frac{a}{b} \\cdot \\frac{c}{d} = \\frac{ac}{bd}$$\n\n"
        "It is the smallest field containing $R$ as a subring (e.g., the rational field $\\mathbb{Q} = \\operatorname{Quot}(\\mathbb{Z})$ and rational functions $k(x) = \\operatorname{Quot}(k[x])$)."
    ),

    # 31. field of sets
    294: (
        "In set theory and Boolean algebra, an algebraic structure consisting of a family $\\mathcal{F}$ of subsets of a universal set $U$ that is closed under finite unions, intersections, and complements. Fundamental laws include:\n\n"
        "1. Commutative laws: $A \\cup B = B \\cup A$, $A \\cap B = B \\cap A$\n"
        "2. Associative laws: $(A \\cup B) \\cup C = A \\cup (B \\cup C)$, $(A \\cap B) \\cap C = A \\cap (B \\cap C)$\n"
        "3. Distributive laws: $A \\cap (B \\cup C) = (A \\cap B) \\cup (A \\cap C)$, $A \\cup (B \\cap C) = (A \\cup B) \\cap (A \\cup C)$\n"
        "4. De Morgan's laws: $(A \\cup B)^c = A^c \\cap B^c$, $(A \\cap B)^c = A^c \\cup B^c$."
    ),

    # 33. fine structure constant
    359: (
        "The fundamental dimensionless coupling constant $\\alpha$ characterizing the strength of the electromagnetic interaction between charged elementary particles, introduced by Arnold Sommerfeld (1916):\n\n"
        "$$\\alpha = \\frac{e^2}{4\\pi \\varepsilon_0 \\hbar c} = \\frac{e^2 c \\mu_0}{2 h} \\approx \\frac{1}{137.035999206}$$\n\n"
        "It dictates the fine structure splitting of atomic spectral lines due to relativistic spin-orbit coupling and quantum electrodynamic radiative corrections."
    ),

    # 34. finite
    368: (
        "Having a bounded, definite count or extent. In set theory, a set $S$ is finite if there exists a natural number $n \\in \\mathbb{N}$ and a bijection $f: S \\to \\{1, 2, \\dots, n\\}$, in which case the cardinality is $|S| = n$. The empty set $\\emptyset$ has cardinality $0$."
    ),

    # 35. finite fourier transform
    373: (
        "The Discrete Fourier Transform (DFT), mapping a finite sequence of $N$ equally spaced discrete-time complex samples $x_0, x_1, \\dots, x_{N-1}$ into frequency domain coefficients $X_0, X_1, \\dots, X_{N-1}$ according to:\n\n"
        "$$X_k = \\sum_{n=0}^{N-1} x_n e^{-i 2\\pi k n / N}, \\quad k = 0, 1, \\dots, N-1$$\n\n"
        "with inverse transformation (IDFT) $x_n = \\frac{1}{N}\\sum_{k=0}^{N-1} X_k e^{i 2\\pi k n / N}$. Computed in $O(N \\log N)$ operations via the Fast Fourier Transform (FFT) algorithm."
    ),

    # 36. first isomorphism theorem
    415: (
        "The foundational theorem in modern algebra (proved by Emmy Noether) relating homomorphisms, kernels, and quotient structures. For any group homomorphism $\\phi: G \\to H$, the quotient group $G / \\ker(\\phi)$ is naturally isomorphic to the image $\\operatorname{im}(\\phi)$:\n\n"
        "$$G / \\ker(\\phi) \\cong \\operatorname{im}(\\phi)$$\n\n"
        "via the canonical isomorphism $\\bar{\\phi}(g\\ker\\phi) = \\phi(g)$. Analogous theorems hold identically for rings ($R / \\ker\\phi \\cong \\operatorname{im}\\phi$), modules, and vector spaces ($V / \\ker T \\cong \\operatorname{im} T$)."
    ),

    # 37. first law of thermodynamics
    416: (
        "The principle of conservation of energy applied to thermodynamic systems, stating that the change in internal energy $\\Delta U$ of a closed system is the difference between net heat $Q$ added to the system and net work $W$ performed by the system on its surroundings:\n\n"
        "$$\\Delta U = Q - W$$\n\n"
        "(or $\\Delta U = Q + W_{\\text{on}}$ where work is defined as work done on the system). In differential form: $dU = dq - dw$."
    ),

    # 38. first principles
    418: (
        "In calculus, evaluating the derivative of a function $f(x)$ directly from the foundational limit definition without relying on shortcut differentiation rules:\n\n"
        "$$f'(x) = \\frac{dy}{dx} = \\lim_{h \\to 0} \\frac{f(x + h) - f(x)}{h}$$\n\n"
        "For example, for $f(x) = x^3$:\n\n"
        "$$f'(x) = \\lim_{h \\to 0} \\frac{(x + h)^3 - x^3}{h} = \\lim_{h \\to 0} \\frac{3x^2 h + 3xh^2 + h^3}{h} = \\lim_{h \\to 0} (3x^2 + 3xh + h^2) = 3x^2$$"
    ),

    # 39. first-order differential equations
    421: (
        "A differential equation involving an independent variable $x$, an unknown function $y(x)$, and only its first derivative $\\frac{dy}{dx}$:\n\n"
        "$$F\\left(x, y, \\frac{dy}{dx}\\right) = 0$$\n\n"
        "Standard forms include: separable ($\frac{dy}{dx} = g(x)h(y)$), linear first-order ($\frac{dy}{dx} + P(x)y = Q(x)$ solved via integrating factor $I(x) = e^{\\int P(x)\\,dx}$), and exact equations ($M\\,dx + N\\,dy = 0$)."
    ),

    # 40. fission
    434: (
        "A nuclear reaction or radioactive decay process wherein an atomic nucleus of high mass number splits into two or more intermediate-mass nuclei (fission fragments), accompanied by the release of neutrons, gamma radiation, and substantial nuclear binding energy ($\x7e200\\,\\text{MeV}$ per event). A representative neutron-induced fission of uranium-235 is:\n\n"
        "$${}^{235}_{92}\\text{U} + {}^1_0 n \\to {}^{236}_{92}\\text{U}^* \\to {}^{141}_{56}\\text{Ba} + {}^{92}_{36}\\text{Kr} + 3\\,{}^1_0 n + 200\\,\\text{MeV}$$"
    ),

    # 41. fixed point
    449: (
        "1. In mathematics, an element $x^*$ in the domain of a function $f$ that is mapped to itself by the function:\n\n"
        "$$f(x^*) = x^*$$\n\n"
        "For instance, $f(x) = x^2$ has fixed points at $x = 0$ and $x = 1$. 2. In metrology and thermodynamics, an invariant, highly reproducible temperature standard used to calibrate temperature scales (e.g., the ice point at $0\\,^\\circ\\text{C} = 273.15\\,\\text{K}$ and the triple point of water at $273.16\\,\\text{K}$)."
    ),

    # 42. fixed point iteration
    450: (
        "A numerical iterative method for approximating roots of an equation. The equation $g(x) = 0$ is reformulated into the equivalent fixed-point form $x = f(x)$. Starting with an initial guess $x_0$, successive approximations are generated by the recurrence relation:\n\n"
        "$$x_{n+1} = f(x_n), \\quad n = 0, 1, 2, \\dots$$\n\n"
        "By the Banach fixed-point theorem, if $|f'(x)| < 1$ in an interval containing the root $x^*$, the sequence converges linearly to $x^* = f(x^*)$."
    ),

    # 43. fixed point theorem
    451: (
        "Any of several major theorems in mathematics asserting that under specific topological or analytical conditions, a mapping admits at least one fixed point $f(x^*) = x^*$. 1. Banach fixed-point theorem: every contraction mapping $T: X \\to X$ on a complete metric space ($d(Tx, Ty) \\le k d(x, y)$ with $0 \\le k < 1$) has a unique fixed point. 2. Brouwer fixed-point theorem: every continuous map from a compact convex subset of $\\mathbb{R}^n$ to itself has at least one fixed point."
    ),

    # 44. floating point number
    538: (
        "A standardized representation of real numbers in digital computers (IEEE 754 standard) using a signed significand (mantissa) multiplied by a base raised to an integer exponent:\n\n"
        "$$x = (-1)^s \\times (1.m)_2 \\times 2^{e - \\text{bias}}$$\n\n"
        "where $s$ is the sign bit ($0$ for positive, $1$ for negative), $m$ is the fractional significand, $e$ is the stored biased exponent, and $\\text{bias} = 2^{k-1} - 1$ ($127$ for 32-bit single precision, $1023$ for 64-bit double precision)."
    ),

    # 45. floor function
    550: (
        "The greatest integer function, denoted $\\lfloor x \\rfloor$, which maps any real number $x$ to the unique integer $k \\in \\mathbb{Z}$ satisfying:\n\n"
        "$$\\lfloor x \\rfloor = \\max \\{m \\in \\mathbb{Z} : m \\le x\\}$$\n\n"
        "satisfying the double inequality $\\lfloor x \\rfloor \\le x < \\lfloor x \\rfloor + 1$. For example, $\\lfloor 3.7 \\rfloor = 3$, $\\lfloor 5 \\rfloor = 5$, and $\\lfloor -2.3 \\rfloor = -3$."
    ),

    # 46. floquet theorem
    553: (
        "A foundational theorem in ordinary differential equations regarding linear systems with periodic coefficients $\\frac{d\\mathbf{y}}{dt} = \\mathbf{A}(t)\\mathbf{y}$ where $\\mathbf{A}(t + T) = \\mathbf{A}(t)$. Floquet's theorem states that the fundamental matrix solution $\\boldsymbol{\\Phi}(t)$ can be factorized as:\n\n"
        "$$\\boldsymbol{\\Phi}(t) = \\mathbf{P}(t) e^{t \\mathbf{R}}$$\n\n"
        "where $\\mathbf{P}(t + T) = \\mathbf{P}(t)$ is a periodic matrix and $\\mathbf{R}$ is a constant matrix whose eigenvalues are the Floquet characteristic exponents $\\mu_i$."
    ),

    # 47. floral formula
    557: (
        "A standardized biological notation using letters, numbers, and symbols to represent floral symmetry, organ counts, and structural relationships: $K$ (calyx/sepals), $C$ (corolla/petals), $P$ (perianth/tepals), $A$ (androecium/stamens), and $G$ (gynoecium/carpels). For example, $\\text{K}_5\\,\\text{C}_5\\,\\text{A}_\\infty\\,\\text{G}_{(5)}$ denotes a flower with $5$ free sepals, $5$ free petals, indefinite stamens, and a superior ovary of $5$ fused carpels."
    ),

    # 48. fluctuation-dissipation theorem
    583: (
        "A cornerstone theorem of statistical physics formulated by Herbert Callen and Theodore Welton, establishing a universal relationship between spontaneous thermal fluctuations in a system at thermal equilibrium and its response (dissipation) to external perturbations. For an observable $A$ with spectral noise power density $S_A(\\omega)$ and dynamic generalized susceptibility $\\chi(\\omega)$:\n\n"
        "$$S_A(\\omega) = \\frac{2 k_B T}{\\omega} \\operatorname{Im}[\\chi(\\omega)]$$\n\n"
        "It unifies Brownian motion (Einstein relation $D = \\mu k_B T$) and electrical thermal noise (Johnson-Nyquist formula $V_{\\text{noise}}^2 = 4 k_B T R \\Delta f$)."
    ),

    # 49. fluorine
    617: (
        "A highly toxic, corrosive, pale yellow diatomic halogen gas ($\x5ctext{F}_2$), atomic number $9$, relative atomic mass $18.9984$, melting point $-219.67\\,^\\circ\\text{C}$ ($53.48\\,\\text{K}$), and boiling point $-188.11\\,^\\circ\\text{C}$ ($85.04\\,\\text{K}$). Possessing ground-state electron configuration $1s^2 2s^2 2p^5$, it is the most electronegative ($3.98$ on Pauling scale) and reactive of all chemical elements, reacting vigorously with virtually all elements including water:\n\n"
        "$$2\\text{F}_2 + 2\\text{H}_2\\text{O} \\to 4\\text{HF} + \\text{O}_2$$"
    ),

    # 50. fokker-planck equation
    666: (
        "A partial differential equation in non-equilibrium statistical mechanics describing the time evolution of the probability density function $P(x, t)$ of the position or velocity of a particle under the combined influence of drag forces and random Gaussian fluctuations:\n\n"
        "$$\\frac{\\partial P(x, t)}{\\partial t} = -\\frac{\\partial}{\\partial x}\\left[D^{(1)}(x, t) P(x, t)\\right] + \\frac{\\partial^2}{\\partial x^2}\\left[D^{(2)}(x, t) P(x, t)\\right]$$\n\n"
        "where $D^{(1)}(x, t)$ is the drift coefficient and $D^{(2)}(x, t) > 0$ is the diffusion coefficient. Also known as the Kolmogorov forward equation."
    )
}

count = 0
for idx, new_def in UPDATES.items():
    if idx < len(f_entries):
        w = f_entries[idx]['word']
        f_entries[idx]['definition'] = new_def
        count += 1
        print(f"Updated [{idx}] {w}")

data['F'] = f_entries

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully enriched {count} terms in Section F Batch 1.")
