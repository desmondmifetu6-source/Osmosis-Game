"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION C (BATCH 4 - FINAL)
=====================================================================
Enriches mathematical, physical, and chemical formulas for Section C
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

BATCH_C4_DEFINITIONS = {
    "consistent": (
        "1. In mathematics, a system of equations that possesses at least one solution (or infinitely many solutions). "
        "For example, the linear system $x + y + z = 3$ and $x + y + 2z = 4$ is consistent. "
        "2. In mathematical logic, a set of statements or formal system from which no contradiction can be deduced. "
        "3. In statistics, an estimator whose probability of differing from the true parameter by more than any given amount tends to zero as sample size $n \\to \\infty$."
    ),
    "constant": (
        "1. A fixed numerical value or invariant quantity that does not vary within a given context. "
        "For example, in the linear equation $y = mx + c$, $m$ and $c$ are constants while $x$ and $y$ are variables. "
        "2. Fundamental mathematical constants include $\\pi \\approx 3.14159$ and Euler's number $e \\approx 2.71828$. "
        "3. In physics, an invariant physical quantity such as Planck's constant $h$ or the speed of light in vacuum $c$."
    ),
    "constant of integration": (
        "An arbitrary constant $C$ added to the antiderivative of a function to represent the entire family of antiderivatives: "
        "$$\\int f(x) \\, dx = F(x) + C$$ "
        "where $F'(x) = f(x)$."
    ),
    "constitutive equation": (
        "A relation between physical quantities specific to a material describing its response to applied external forces. "
        "For example, for an incompressible Newtonian viscous fluid, the Cauchy stress tensor is given by: "
        "$$\\boldsymbol{\\sigma} = -p \\mathbf{I} + 2\\eta \\left( \\boldsymbol{\\Sigma} - \\frac{1}{3} \\operatorname{tr}(\\boldsymbol{\\Sigma})\\mathbf{I} \\right)$$ "
        "where $p$ is hydrostatic pressure, $\\eta$ is dynamic viscosity, and $\\boldsymbol{\\Sigma}$ is the strain-rate tensor."
    ),
    "constitutive equations": (
        "Material-dependent relations connecting electromagnetic or mechanical fields. "
        "In electromagnetism: "
        "$$\\mathbf{D} = \\varepsilon \\mathbf{E}, \\quad \\mathbf{B} = \\mu \\mathbf{H}$$ "
        "where $\\mathbf{D}$ is electric displacement, $\\varepsilon$ is permittivity, $\\mathbf{E}$ is electric field, "
        "$\\mathbf{B}$ is magnetic flux density, $\\mu$ is magnetic permeability, and $\\mathbf{H}$ is magnetic field intensity."
    ),
    "contact force": (
        "In continuum mechanics, the surface force experienced by material points of a body due to physical contact across internal surfaces or external boundaries. "
        "The total contact force on a sub-body with boundary $\\partial \\mathcal{B}_t$ is: "
        "$$\\mathbf{F}_c = \\int_{\\partial \\mathcal{B}_t} \\mathbf{t}(\\mathbf{x}, \\mathbf{n}) \\, da$$ "
        "where $\\mathbf{t}(\\mathbf{x}, \\mathbf{n})$ is the Cauchy traction vector."
    ),
    "contact torque": (
        "In continuum mechanics, the total moment of surface traction forces and surface couples acting across a boundary $\\partial \\mathcal{B}_t$: "
        "$$\\mathbf{M}_c = \\int_{\\partial \\mathcal{B}_t} \\mathbf{x} \\times \\mathbf{t}(\\mathbf{x}, \\mathbf{n}) \\, da + \\int_{\\partial \\mathcal{B}_t} \\mathbf{m}(\\mathbf{x}, \\mathbf{n}) \\, da$$ "
        "where $\\mathbf{x}$ is position, $\\mathbf{t}$ is traction, and $\\mathbf{m}$ is surface couple density."
    ),
    "continued fraction": (
        "A representation of a real number as an integer part plus the reciprocal of another number, which in turn is written similarly: "
        "$$x = a_0 + \\cfrac{b_1}{a_1 + \\cfrac{b_2}{a_2 + \\cfrac{b_3}{a_3 + \\dots}}}$$ "
        "Every rational number has a finite continued fraction, while every irrational number has a unique infinite continued fraction."
    ),
    "continuity equation": (
        "A differential equation expressing the local conservation of mass, charge, or probability in a continuum. "
        "For fluid flow with density $\\rho$ and velocity $\\mathbf{v}$: "
        "$$\\frac{\\partial \\rho}{\\partial t} + \\nabla \\cdot (\\rho \\mathbf{v}) = 0$$"
    ),
    "continuous": (
        "A function $f(x)$ where small changes in the input produce arbitrarily small changes in the output. "
        "Formally, $f$ is continuous at $a$ if $\\lim_{x \\to a} f(x) = f(a)$, meaning for every $\\varepsilon > 0$, "
        "there exists $\\delta > 0$ such that: "
        "$$|x - a| < \\delta \\implies |f(x) - f(a)| < \\varepsilon$$"
    ),
    "continuous distribution function": (
        "The cumulative distribution function (CDF) of a continuous random variable $X$, defined for all real $b$ by: "
        "$$F(b) = P(X \\le b) = \\int_{-\\infty}^b f(x) \\, dx$$ "
        "where $f(x)$ is the continuous probability density function (PDF)."
    ),
    "convergent in mean": (
        "A sequence of integrable functions $\\{f_n\\}$ converging to $f$ in the $L^1$ norm on $[a, b]$, satisfying: "
        "$$\\lim_{n \\to \\infty} \\int_a^b |f_n(x) - f(x)| \\, dx = 0$$"
    ),
    "conversion fact": (
        "A fixed conversion relationship between measurement units, such as $1\\text{ inch} = 2.54\\text{ cm}$ or $1\\text{ lb} \\approx 0.4536\\text{ kg}$."
    ),
    "convex": (
        "1. A geometric set in which the line segment joining any two points in the set lies entirely within the set: "
        "$$\\forall x, y \\in S, \\, t \\in [0, 1] \\implies tx + (1 - t)y \\in S$$ "
        "2. A real-valued function $f$ satisfying: "
        "$$f(tx + (1 - t)y) \\le t f(x) + (1 - t) f(y), \\quad \\forall t \\in [0, 1]$$ "
        "Examples include $f(x) = x^2$ and $f(x) = e^x$."
    ),
    "convex combination": (
        "A linear combination of points $\\mathbf{x}_1, \\dots, \\mathbf{x}_k$ with non-negative coefficients summing to $1$: "
        "$$\\mathbf{x} = \\sum_{i=1}^k \\alpha_i \\mathbf{x}_i, \\quad \\text{where } \\alpha_i \\ge 0 \\text{ and } \\sum_{i=1}^k \\alpha_i = 1$$"
    ),
    "convex polyhedron": (
        "A three-dimensional solid bounded by flat polygonal faces whose interior angles are all less than $180^\\circ$. "
        "Algebraically, it can be defined as the intersection of a finite number of half-spaces: $M\\mathbf{x} \\le \\mathbf{b}$."
    ),
    "convolution": (
        "A mathematical operation on two functions $f$ and $g$ that produces a third function expressing how the shape of one is modified by the other: "
        "$$(f * g)(t) = \\int_{-\\infty}^\\infty f(\\tau) g(t - \\tau) \\, d\\tau$$"
    ),
    "correlation": (
        "A statistical measure indicating the extent to which two or more variables fluctuate together. "
        "Quantified by the correlation coefficient $r \\in [-1, 1]$, where $+1$ denotes perfect direct relationship, "
        "$-1$ denotes perfect inverse relationship, and $0$ indicates no linear association."
    ),
    "correlation coefficient": (
        "Pearson's correlation coefficient $\\rho_{X,Y}$ between random variables $X$ and $Y$: "
        "$$\\rho_{X,Y} = \\frac{\\operatorname{Cov}(X, Y)}{\\sigma_X \\sigma_Y} = \\frac{E[XY] - E[X]E[Y]}{\\sqrt{(E[X^2] - (E[X])^2)(E[Y^2] - (E[Y])^2)}}$$"
    ),
    "correlation coefficient sample": (
        "The sample correlation coefficient $r$ computed from $n$ paired observations $(x_i, y_i)$: "
        "$$r = \\frac{S_{xy}}{\\sqrt{S_{xx} S_{yy}}} = \\frac{\\sum (x_i - \\bar{x})(y_i - \\bar{y})}{\\sqrt{\\sum (x_i - \\bar{x})^2 \\sum (y_i - \\bar{y})^2}}$$"
    ),
    "cosecant": (
        "The reciprocal of the sine function in trigonometry: "
        "$$\\csc\\theta = \\frac{1}{\\sin\\theta} = \\frac{\\text{hypotenuse}}{\\text{opposite}}$$ "
        "The hyperbolic cosecant is defined as $\\operatorname{csch} x = \\frac{1}{\\sinh x} = \\frac{2}{e^x - e^{-x}}$."
    ),
    "cosh": (
        "The hyperbolic cosine function, defined in terms of the exponential function: "
        "$$\\cosh z = \\frac{e^z + e^{-z}}{2} = \\cos(iz)$$ "
        "It satisfies the fundamental hyperbolic identity: "
        "$$\\cosh^2 z - \\sinh^2 z = 1$$"
    ),
    "cosine": (
        "A primary trigonometric function defined in a right-angled triangle as: "
        "$$\\cos\\theta = \\frac{\\text{adjacent}}{\\text{hypotenuse}}$$ "
        "In a triangle with sides $a, b, c$, the Law of Cosines states: "
        "$$c^2 = a^2 + b^2 - 2ab\\cos C$$"
    ),
    "cosine law": (
        "The Law of Cosines relates the lengths of the sides of any triangle to the cosine of one of its angles: "
        "$$a^2 = b^2 + c^2 - 2bc\\cos A$$ "
        "$$b^2 = a^2 + c^2 - 2ac\\cos B$$ "
        "$$c^2 = a^2 + b^2 - 2ab\\cos C$$"
    ),
    "cotangent": (
        "The reciprocal of the tangent function: "
        "$$\\cot\\theta = \\frac{1}{\\tan\\theta} = \\frac{\\cos\\theta}{\\sin\\theta} = \\frac{\\text{adjacent}}{\\text{opposite}}$$ "
        "The hyperbolic cotangent is $\\coth x = \\frac{\\cosh x}{\\sinh x} = \\frac{e^x + e^{-x}}{e^x - e^{-x}}$."
    ),
    "coulomb force": (
        "The electrostatic force between two stationary electric charges $q_1$ and $q_2$ separated by distance $r$: "
        "$$F = k_e \\frac{|q_1 q_2|}{r^2} = \\frac{1}{4\\pi\\varepsilon_0} \\frac{|q_1 q_2|}{r^2}$$ "
        "where $\\varepsilon_0 \\approx 8.854 \\times 10^{-12}\\text{ F/m}$ is the permittivity of free space."
    ),
    "coulomb's law": (
        "The physical law stating that the electrostatic force of attraction or repulsion between two point charges is directly proportional to the product of the charges and inversely proportional to the square of the distance between them: "
        "$$F = \\frac{1}{4\\pi\\varepsilon_0} \\frac{q_1 q_2}{r^2}$$"
    ),
    "coulombmeter": (
        "An electrical measuring instrument used to determine electric charge $Q$ in coulombs. "
        "When charge accumulates on a calibrated capacitor of known capacitance $C$ producing voltage $V$: "
        "$$Q = CV$$"
    ),
    "countably additive": (
        "A property of a set function or measure $\\mu$ on a $\\sigma$-algebra such that for any countable collection of mutually disjoint sets $\\{A_n\\}_{n=1}^\\infty$: "
        "$$\\mu\\left( \\bigcup_{n=1}^\\infty A_n \\right) = \\sum_{n=1}^\\infty \\mu(A_n)$$"
    ),
    "counter example": (
        "An exception to a proposed general rule or statement that demonstrates its falsehood. "
        "For example, $\\sqrt{2}$ serves as a counterexample disproving the statement that all square roots of positive integers are rational."
    ),
    "counting-up subtracting": (
        "A mental subtraction technique by counting forward from the subtrahend to the minuend. "
        "For example, for $87 - 49$: start at $49$, add $30$ to get $79$, then add $8$ to reach $87$; difference is $30 + 8 = 38$."
    ),
    "couple": (
        "A system of two parallel forces $\\mathbf{F}$ and $-\\mathbf{F}$ of equal magnitude acting in opposite directions along different lines of action. "
        "The torque or moment of the couple is independent of reference point and is given by: "
        "$$\\tau = F \\cdot d$$ "
        "where $d$ is the perpendicular distance between their lines of action. For example, $5\\text{ N} \\times 2\\text{ m} = 10\\text{ N}\\cdot\\text{m}$."
    ),
    "covariance": (
        "A measure of the joint variability of two random variables $X$ and $Y$: "
        "$$\\operatorname{Cov}(X, Y) = E[(X - E[X])(Y - E[Y])] = E[XY] - E[X]E[Y]$$"
    ),
    "covariance matrix": (
        "A symmetric square matrix whose $(i, j)$-th entry is the covariance between random variables $X_i$ and $X_j$: "
        "$$\\boldsymbol{\\Sigma}_{ij} = \\operatorname{Cov}(X_i, X_j) = E[(X_i - \\mu_i)(X_j - \\mu_j)]$$ "
        "where the diagonal entries $\\boldsymbol{\\Sigma}_{ii} = \\operatorname{Var}(X_i)$."
    ),
    "cramer's rule": (
        "An explicit formula for solving a system of linear equations using determinants. "
        "For a $2 \\times 2$ system $a_1 x + b_1 y = k_1$ and $a_2 x + b_2 y = k_2$: "
        "$$x = \\frac{\\begin{vmatrix} k_1 & b_1 \\\\ k_2 & b_2 \\end{vmatrix}}{\\begin{vmatrix} a_1 & b_1 \\\\ a_2 & b_2 \\end{vmatrix}}, \\quad y = \\frac{\\begin{vmatrix} a_1 & k_1 \\\\ a_2 & k_2 \\end{vmatrix}}{\\begin{vmatrix} a_1 & b_1 \\\\ a_2 & b_2 \\end{vmatrix}}$$"
    ),
    "cresol": (
        "Any of three isomeric methylphenols (ortho-, meta-, and para-cresol) with chemical formula $\\text{CH}_3\\text{C}_6\\text{H}_4\\text{OH}$, "
        "used in disinfectants, phenolic resins, and chemical synthesis."
    ),
    "critical angle": (
        "The angle of incidence in an optically denser medium for which the angle of refraction into a rarer medium is $90^\\circ$. "
        "By Snell's law, the critical angle $\\theta_c$ is given by: "
        "$$\\sin\\theta_c = \\frac{n_2}{n_1} = \\frac{1}{\\mu}$$ "
        "where $\\mu$ is the relative refractive index."
    ),
    "critical density": (
        "1. In cosmology, the average matter density required for the universe to be spatially flat: "
        "$$\\rho_c = \\frac{3H_0^2}{8\\pi G} \\approx 10^{-26}\\text{ kg/m}^3$$ "
        "where $H_0$ is Hubble's constant and $G$ is Newton's gravitational constant. "
        "2. In thermodynamics, the density of a substance at its critical point."
    ),
    "cross multiplication": (
        "A method of solving proportional fractions: "
        "$$\\frac{a}{b} = \\frac{c}{d} \\implies a \\cdot d = b \\cdot c$$"
    ),
    "cross product": (
        "The vector cross product of two 3D vectors $\\mathbf{A}$ and $\\mathbf{B}$: "
        "$$\\mathbf{A} \\times \\mathbf{B} = \\begin{vmatrix} \\mathbf{i} & \\mathbf{j} & \\mathbf{k} \\\\ a_1 & a_2 & a_3 \\\\ b_1 & b_2 & b_3 \\end{vmatrix} = (a_2 b_3 - a_3 b_2)\\mathbf{i} + (a_3 b_1 - a_1 b_3)\\mathbf{j} + (a_1 b_2 - a_2 b_1)\\mathbf{k}$$ "
        "Its magnitude is $|\\mathbf{A} \\times \\mathbf{B}| = |\\mathbf{A}||\\mathbf{B}|\\sin\\theta$."
    ),
    "cross ratio": (
        "A projective invariant assigned to four collinear points $P, Q, R, S$: "
        "$$(P, Q; R, S) = \\frac{\\overline{PR} \\cdot \\overline{QS}}{\\overline{QR} \\cdot \\overline{PS}}$$"
    ),
    "cruciform": (
        "A cross-shaped geometric plane curve with Cartesian equation: "
        "$$x^2 y^2 - a^2 x^2 - a^2 y^2 = 0$$ "
        "asymptotic to the lines $x = \\pm a$ and $y = \\pm a$."
    ),
    "cryogenics": (
        "The branch of physics and engineering studying the production and effects of extremely low temperatures, "
        "conventionally defined as temperatures below $-123.15^\\circ\\text{C}$ ($150\\text{ K}$)."
    ),
    "cryoscopic constant": (
        "The constant $K_f$ relating molality $b$ to freezing point depression $\\Delta T_f$: "
        "$$\\Delta T_f = K_f \\cdot b$$ "
        "For water, $K_f = 1.853\\text{ K}\\cdot\\text{kg/mol}$."
    ),
    "cube root": (
        "A number that when multiplied by itself three times gives the original quantity: "
        "$$y = \\sqrt[3]{x} = x^{1/3} \\iff y^3 = x$$"
    ),
    "cubic equation": (
        "A polynomial equation of degree 3 in one variable: "
        "$$ax^3 + bx^2 + cx + d = 0, \\quad a \\ne 0$$"
    ),
    "cubic expansion": (
        "The fractional change in volume of a material per degree temperature change, given by volumetric expansion coefficient $\\gamma$: "
        "$$\\gamma = \\frac{V_2 - V_1}{V_1(\\theta_2 - \\theta_1)} = \\frac{\\Delta V}{V_0 \\Delta\\theta}$$"
    ),
    "cubic function": (
        "A third-degree polynomial function of the form: "
        "$$f(x) = ax^3 + bx^2 + cx + d, \\quad a \\ne 0$$"
    ),
    "cubic polynomial": (
        "A polynomial expression of degree 3, such as $f(x) = ax^3 + bx^2 + cx + d$ where $a \\ne 0$."
    ),
    "cuboid": (
        "A convex hexahedron whose six faces are all rectangles. For edge lengths $a, b, c$: "
        "$$\\text{Volume } V = abc, \\quad \\text{Surface Area } S = 2(ab + bc + ca)$$"
    ),
    "cumulant": (
        "Coefficients $\\kappa_r$ in the Taylor series expansion of the cumulant-generating function $K(t) = \\ln E[e^{tX}]$: "
        "$$\\kappa_1 = \\mu, \\quad \\kappa_2 = \\sigma^2, \\quad \\kappa_3 = \\mu_3, \\quad \\kappa_4 = \\mu_4 - 3\\mu_2^2$$"
    ),
    "cumulative distribution function": (
        "The function giving the probability that a random variable $X$ will take a value less than or equal to $x$: "
        "$$F(x) = P(X \\le x) = \\int_{-\\infty}^x f(t) \\, dt$$ "
        "where $f(t) = F'(t)$ is the probability density function."
    ),
    "cumulative odds ratio": (
        "A measure in proportional odds models for ordinal variables: "
        "$$R_j = \\frac{P(Y \\le j \\mid E_1) / P(Y > j \\mid E_1)}{P(Y \\le j \\mid E_2) / P(Y > j \\mid E_2)}$$"
    ),
    "cumulative probability": (
        "The probability that a discrete random variable $X$ is less than or equal to a specific value $x_k$: "
        "$$P(X \\le x_k) = \\sum_{j=1}^k P(X = x_j)$$"
    ),
    "cumulenes": (
        "Hydrocarbons possessing three or more consecutive cumulative double bonds: "
        "$$R_2\\text{C}=\\text{C}=\\text{C}=\\text{C}R_2$$"
    ),
    "curie": (
        "In magnetism, the Curie-Weiss law relates magnetic susceptibility $\\chi$ to absolute temperature $T$: "
        "$$\\chi = \\frac{C}{T - \\theta_W}$$ "
        "where $C$ is the Curie constant and $\\theta_W$ is the Weiss temperature."
    ),
    "curie's law": (
        "The law stating that the magnetic susceptibility $\\chi$ of a paramagnetic material is inversely proportional to temperature: "
        "$$M = \\frac{C B}{T} \\quad \\text{or} \\quad \\chi = \\frac{C}{T}$$ "
        "where $M$ is magnetization, $B$ is applied magnetic field, $T$ is temperature in kelvins, and $C$ is Curie's constant."
    ),
    "curvature vector": (
        "For a space curve $\\mathbf{r}(s)$ parametrized by arc length $s$: "
        "$$\\mathbf{k} = \\frac{d\\mathbf{T}}{ds} = \\kappa \\mathbf{N}$$ "
        "where $\\mathbf{T}$ is the unit tangent vector, $\\kappa$ is curvature, and $\\mathbf{N}$ is the principal unit normal."
    ),
    "curvilinear": (
        "Formed, bounded, or characterized by curved lines. In vector calculus, line integrals along a smooth parameterized curve $\\mathbf{r}(t)$ for $t \\in [a, b]$: "
        "$$\\int_C \\phi \\, ds = \\int_a^b \\phi(\\mathbf{r}(t)) \\|\\mathbf{r}'(t)\\| \\, dt$$"
    ),
    "cut": (
        "1. In complex analysis, a branch cut removed from the complex plane (e.g. $(-\\infty, 0]$ for principal logarithm $\\operatorname{Ln} z$). "
        "2. In graph theory and topology, a set of edges or points whose removal disconnects the space."
    ),
    "cyanic acid": (
        "An unstable chemical compound with formula $\\text{HOCN}$ (structure $\\text{H}-\\text{O}-\\text{C}\\equiv\\text{N}$), "
        "melting point $-86^\\circ\\text{C}$ ($187\\text{ K}$) and boiling point $23.5^\\circ\\text{C}$ ($296.65\\text{ K}$)."
    ),
    "cyanogen": (
        "A toxic, colourless gas with chemical formula $\\text{C}_2\\text{N}_2$ (or $(\\text{CN})_2$), "
        "melting point $-28^\\circ\\text{C}$ ($245\\text{ K}$) and boiling point $-21^\\circ\\text{C}$ ($252\\text{ K}$)."
    ),
    "cycle": (
        "1. A complete series of states or events that repeats regularly. "
        "2. In permutation group theory, a cyclic permutation $\\gamma$ of length $l$ satisfying $\\gamma^l = e$."
    ),
    "cyclic permutation": (
        "The arrangement of $n$ distinct items in a circular ring, where rotational equivalences yield: "
        "$$(n - 1)!$$"
    ),
    "cyclo-octatetraene": (
        "A non-aromatic conjugated polyene cyclic hydrocarbon with chemical formula $\\text{C}_8\\text{H}_8$, "
        "melting point $-5^\\circ\\text{C}$ to $-3^\\circ\\text{C}$ ($268 - 270\\text{ K}$) and boiling point $142 - 143^\\circ\\text{C}$ ($415 - 416\\text{ K}$)."
    ),
    "cyclohexadiene": (
        "A cyclic conjugated or non-conjugated diene with formula $\\text{C}_6\\text{H}_8$, including 1,3-cyclohexadiene and 1,4-cyclohexadiene."
    ),
    "cyclohexadiene-1,4-dione": (
        "A yellow crystalline solid (commonly known as 1,4-benzoquinone) with chemical formula $\\text{C}_6\\text{H}_4\\text{O}_2$, "
        "melting point $116^\\circ\\text{C}$ ($389\\text{ K}$)."
    ),
    "cycloid": (
        "The curve traced by a point on the rim of a rolling circle of radius $a$ along a straight line: "
        "$$x = a(\\theta - \\sin\\theta), \\quad y = a(1 - \\cos\\theta)$$"
    ),
    "cyclometric functions": (
        "The fundamental trigonometric ratio functions defined in a right triangle: "
        "$$\\sin x = \\frac{\\text{opp}}{\\text{hyp}}, \\quad \\cos x = \\frac{\\text{adj}}{\\text{hyp}}, \\quad \\tan x = \\frac{\\text{opp}}{\\text{adj}}$$ "
        "$$\\cot x = \\frac{\\text{adj}}{\\text{opp}}, \\quad \\sec x = \\frac{\\text{hyp}}{\\text{adj}}, \\quad \\csc x = \\frac{\\text{hyp}}{\\text{opp}}$$"
    ),
    "cyclotomic": (
        "Relating to the $n$-th roots of unity. The cyclotomic equation is: "
        "$$z^n - 1 = 0$$ "
        "Its primitive roots are roots of the $n$-th cyclotomic polynomial $\\Phi_n(z)$."
    ),
    "cylinder": (
        "A three-dimensional solid with circular parallel bases of radius $r$ and perpendicular height $h$: "
        "$$\\text{Volume: } V = \\pi r^2 h$$ "
        "$$\\text{Curved Surface Area: } \\text{CSA} = 2\\pi rh$$ "
        "$$\\text{Total Surface Area: } \\text{TSA} = 2\\pi rh + 2\\pi r^2 = 2\\pi r(h + r)$$"
    ),
    "cylindrical polar coodinates": (
        "A 3D coordinate system specifying points by radial distance $r$, azimuth angle $\\theta$, and height $z$: "
        "$$x = r\\cos\\theta, \\quad y = r\\sin\\theta, \\quad z = z$$"
    ),
    "cysteine": (
        "A sulfur-containing proteinogenic amino acid with chemical formula $\\text{C}_3\\text{H}_7\\text{NO}_2\\text{S}$ "
        "and systematic name 2-amino-3-mercaptopropanoic acid ($\\text{HS}-\\text{CH}_2-\\text{CH}(\\text{NH}_2)-\\text{COOH}$), "
        "capable of forming disulfide bridges ($-\\text{S}-\\text{S}-$) in proteins."
    )
}

def apply_enrichment():
    dict_file = 'dictionary.json'
    print(f"Loading {dict_file}...")
    with open(dict_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    updated_count = 0
    c_entries = data.get('C', [])
    word_map = {item.get('word', '').strip().lower(): item for item in c_entries}

    for target_word, new_def in BATCH_C4_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section C: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_C4_DEFINITIONS)} definitions in Section C Batch 4.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    print("Rebuilding core_dictionary.js index...")
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
