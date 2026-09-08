"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION C (BATCH 3)
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

BATCH_C3_DEFINITIONS = {
    "chloroform": (
        "An odourless, toxic carcinogenic liquid with the chemical formula $\\text{CHCl}_3$, "
        "melting point $-63.5^\\circ\\text{C}$ ($210\\text{ K}$) and boiling point $61.2^\\circ\\text{C}$ ($334\\text{ K}$). "
        "It has a characteristic pungent, sickly sweet smell and taste. It is produced by reaction of chlorine with ethanol and by the "
        "reduction of carbon tetrachloride with moist iron. When exposed to sunlight and air, it reacts slowly to form phosgene ($\\text{COCl}_2$), "
        "a very poisonous gas."
    ),
    "chloromethane": (
        "A colourless flammable gas with the chemical formula $\\text{CH}_3\\text{Cl}$, relative density $2.22$, "
        "melting point $-97.7^\\circ\\text{C}$ ($176\\text{ K}$) and boiling point $-24.2^\\circ\\text{C}$ ($249\\text{ K}$). "
        "It is a haloalkane made by direct chlorination of methane and was once used as a local anaesthetic and refrigerant."
    ),
    "chol esky deco mpos itio n": (
        "The factorisation of a symmetric positive-definite matrix $A$ as $A = L L^* = R^* R$, where $L$ is lower-triangular, "
        "$R$ is upper-triangular, and $L^*$ and $R^*$ are their respective conjugate transposes. The matrix $R$ is called the "
        "Cholesky factor or 'square root' of $A$ and can be computed directly from element-by-element comparison."
    ),
    "cholecalciferol": (
        "A form of vitamin D (vitamin $\\text{D}_3$) with needle-like crystals and chemical formula $\\text{C}_{27}\\text{H}_{44}\\text{O}$, "
        "with melting point $83^\\circ\\text{C} - 86^\\circ\\text{C}$ ($356.15\\text{ K} - 359\\text{ K}$). "
        "It is found naturally in fish-liver oils and egg yolks, and is synthesized in skin exposed to ultraviolet B radiation."
    ),
    "cholesterol": (
        "A sterol lipid with the chemical formula $\\text{C}_{27}\\text{H}_{45}\\text{OH}$, relative density $1.052$, "
        "melting point $148^\\circ\\text{C} - 150^\\circ\\text{C}$ ($421\\text{ K} - 423\\text{ K}$) and boiling point $360^\\circ\\text{C}$ ($633.15\\text{ K}$) "
        "with decomposition. It is essential for the structural integrity of animal cell membranes and serves as a precursor for steroid hormones, "
        "bile acids, and vitamin D."
    ),
    "chromatic number": (
        "The minimum number of colours needed to colour the vertices of a graph $G$ such that no two adjacent vertices share the same colour, "
        "denoted by $\\chi(G)$. A graph with $\\chi(G) = k$ is said to be $k$-colourable. For example, all bipartite graphs are $2$-colourable, "
        "and all planar graphs are $4$-colourable by the Four Colour Theorem."
    ),
    "chromyl chloride": (
        "A dark red liquid with chemical formula $\\text{CrO}_2\\text{Cl}_2$, boiling point $117^\\circ\\text{C}$ ($390\\text{ K}$) "
        "and melting point $-96.5^\\circ\\text{C}$ ($176.65\\text{ K}$). It is evolved as dark red vapour on addition of concentrated sulfuric acid "
        "to a mixture of potassium dichromate and sodium chloride. It is a powerful oxidising agent."
    ),
    "circle of convergence": (
        "A circle in the complex plane for a power series $\\sum_{n=0}^\\infty c_n (z - a)^n$ centered at $a$ with radius $R$ (radius of convergence). "
        "The series converges absolutely for all $z$ satisfying $|z - a| < R$ and diverges for $|z - a| > R$."
    ),
    "circle of curvature": (
        "The circle that is tangent to a curve $y = f(x)$ at a given point, shares the same principal normal and tangent line, "
        "and has a radius equal to the radius of curvature: "
        "$$r = \\frac{1}{\\kappa} = \\frac{[1 + (f'(x))^2]^{3/2}}{|f''(x)|}$$"
    ),
    "circle theorem": (
        "Fundamental theorems in Euclidean plane geometry: "
        "(i) The angle subtended by an arc at the centre is twice the angle subtended at the circumference: $\\angle\\text{BOC} = 2\\angle\\text{BAC}$. "
        "(ii) Angles in the same segment are equal: $\\angle\\text{EBF} = \\angle\\text{EAF} = \\angle\\text{ECF}$. "
        "(iii) Opposite angles of a cyclic quadrilateral sum to $180^\\circ$: $\\angle\\text{BAD} + \\angle\\text{BCD} = 180^\\circ$. "
        "(iv) The angle in a semicircle is a right angle: $\\angle\\text{ABC} = 90^\\circ$. "
        "(v) The angle between a tangent and radius at the point of contact is $90^\\circ$: $\\angle\\text{OBC} = 90^\\circ$. "
        "(vi) Tangents drawn from an external point are equal in length: $|AB| = |AC|$. "
        "(vii) Alternate segment theorem: the angle between a tangent and chord equals the angle subtended in the alternate segment: $\\angle\\text{CAD} = \\angle\\text{DEA}$."
    ),
    "circular cone": (
        "A cone with a circular base. For a cone of base radius $r$ and perpendicular height $h$, its volume is: "
        "$$V = \\frac{1}{3}\\pi r^2 h$$ "
        "and its total surface area is $A = \\pi r(l + r)$, where $l = \\sqrt{r^2 + h^2}$ is the slant height."
    ),
    "circular permutation": (
        "The number of unique ways of arranging $n$ distinct objects in a circle. Because rotations are considered identical, "
        "the total number of circular permutations is given by: $$(n - 1)!$$"
    ),
    "circulation": (
        "In fluid dynamics and vector calculus, the line integral of the fluid velocity vector $\\mathbf{v}$ around a closed curve $\\Gamma$: "
        "$$\\Gamma = \\oint_\\Gamma \\mathbf{v} \\cdot d\\mathbf{x}$$ "
        "By Stokes' theorem, circulation equals the surface integral of the vorticity $\\nabla \\times \\mathbf{v}$ through any surface bounded by $\\Gamma$."
    ),
    "circumference": (
        "The distance around the boundary of a circle or curved figure. For a circle of radius $r$ or diameter $d$: "
        "$$C = 2\\pi r = \\pi d$$"
    ),
    "cissoid": (
        "A curve generated from a circle of radius $a$. In Cartesian coordinates, the Cissoid of Diocles is given by: "
        "$$y^2(2a - x) = x^3$$ "
        "and in polar coordinates by: "
        "$$r = 2a\\tan\\theta\\sin\\theta$$"
    ),
    "citric acid": (
        "A weak tricarboxylic acid found naturally in citrus fruits, with chemical formula $\\text{C}_6\\text{H}_8\\text{O}_7$ "
        "(or $\\text{C}_3\\text{H}_5\\text{O}(\\text{COOH})_3$) and systematic IUPAC name 2-hydroxypropane-1,2,3-tricarboxylic acid. "
        "It is a key intermediate in the citric acid cycle (Krebs cycle) of cellular respiration."
    ),
    "clairaut's equation": (
        "A first-order non-linear ordinary differential equation of the form: "
        "$$y = x y' + f(y')$$ "
        "or $x y' - y + f(y') = 0$, having general linear solutions $y = C x + f(C)$ and a singular solution representing their envelope."
    ),
    "clairaut's form": (
        "A first-order partial differential equation of the form: "
        "$$z = \\sum_{i=1}^n x_i \\frac{\\partial z}{\\partial x_i} + f\\left(\\frac{\\partial z}{\\partial x_1}, \\dots, \\frac{\\partial z}{\\partial x_n}\\right)$$ "
        "with the complete integral solution $z = \\sum_{i=1}^n a_i x_i + f(a_1, \\dots, a_n)$, where $a_1, \\dots, a_n$ are arbitrary constants."
    ),
    "clarke generalized directional derivative": (
        "For a locally Lipschitz function $f$ on a normed space $X$, defined at $x$ in direction $h$ by: "
        "$$f^\\circ(x; h) = \\limsup_{y \\to x, \\, t \\to 0^+} \\frac{f(y + th) - f(y)}{t}$$ "
        "The Clarke generalized gradient $\\partial f(x)$ is the set of all continuous linear functionals $\\varphi$ satisfying $\\varphi(h) \\le f^\\circ(x; h)$ for all $h \\in X$."
    ),
    "class equation": (
        "In finite group theory, the equation partitioning a group $G$ into its center $Z(G)$ and non-singleton conjugacy classes: "
        "$$|G| = |Z(G)| + \\sum_{i=1}^k [G : C_G(x_i)]$$ "
        "where $C_G(x_i)$ is the centraliser of representative element $x_i$."
    ),
    "class mark": (
        "The midpoint of a class interval in statistics, calculated as the arithmetic mean of the lower and upper class limits: "
        "$$\\text{Class Mark} = \\frac{\\text{Lower Limit} + \\text{Upper Limit}}{2}$$ "
        "For example, for the interval $1 - 5$, the class mark is $\\frac{1 + 5}{2} = 3$, and for $6 - 10$, it is $\\frac{6 + 10}{2} = 8$."
    ),
    "classical eigenvalue problem": (
        "The problem of determining scalars $\\lambda$ (eigenvalues) and non-zero vectors $\\mathbf{x}$ (eigenvectors) satisfying: "
        "$$A\\mathbf{x} = \\lambda\\mathbf{x}$$ "
        "or generalized form $A\\mathbf{x} = \\lambda B\\mathbf{x}$, where $A$ and $B$ are square matrices."
    ),
    "closed form": (
        "An expression for a mathematical function or definite integral evaluated in terms of a finite number of well-known elementary operations and functions. For example, the Gaussian integral: "
        "$$\\int_{-\\infty}^\\infty e^{-x^2} \\, dx = \\sqrt{\\pi}$$"
    ),
    "codomain": (
        "The set containing all possible outputs of a function $f: X \\to Y$, where $Y$ is the codomain. "
        "The range or image $f(X) \\subseteq Y$ consists of the values the function actually takes. "
        "For example, $f(x) = -\\frac{1}{x}$ on integers can have codomain $[-1, 1]$, whereas its image is the discrete set $\\{ -\\frac{1}{x} \\mid x \\in \\mathbb{Z} \\setminus \\{0\\} \\}$."
    ),
    "coefficient": (
        "A constant multiplicative factor assigned to a variable or term in an algebraic expression. "
        "For example, in $4x^2 + 2xy - x$, the coefficient of $x^2$ is $4$, that of $xy$ is $2$, and that of $x$ is $-1$."
    ),
    "coefficient of probability": (
        "A probability density function $P$ such that the probability $dp$ of finding a system in phase space volume element $dv$ is $dp = P \\, dv$, subject to the normalization condition: "
        "$$\\int P \\, dv = 1$$"
    ),
    "coefficient of volume expansion": (
        "The fractional change in volume of a substance per degree rise in temperature, denoted by $\\gamma$: "
        "$$\\gamma = \\frac{\\Delta V}{V_0 \\Delta T}$$ "
        "For isotropic solids, $\\gamma \\approx 3\\alpha$, where $\\alpha$ is the coefficient of linear expansion."
    ),
    "cofunction": (
        "A trigonometric function that yields equal values when evaluated at the complementary angle: "
        "$$\\sin\\theta = \\cos\\left(\\frac{\\pi}{2} - \\theta\\right), \\quad \\tan\\theta = \\cot\\left(\\frac{\\pi}{2} - \\theta\\right), \\quad \\sec\\theta = \\csc\\left(\\frac{\\pi}{2} - \\theta\\right)$$"
    ),
    "column space": (
        "The vector space spanned by the column vectors of a matrix $A$. The column space consists of all linear combinations of the columns: "
        "$$c_1 \\mathbf{v}_1 + c_2 \\mathbf{v}_2 + \\dots + c_n \\mathbf{v}_n$$ "
        "The dimension of the column space equals the rank of the matrix."
    ),
    "column vector": (
        "A matrix consisting of a single column of $n$ elements, representing an $n \\times 1$ matrix: "
        "$$\\mathbf{v} = \\begin{pmatrix} v_1 \\\\ v_2 \\\\ \\vdots \\\\ v_n \\end{pmatrix}$$"
    ),
    "commutative law": (
        "Algebraic laws stating that the order of operations does not alter the result: "
        "Addition: $a + b = b + a$, Multiplication: $a \\cdot b = b \\cdot a$. "
        "Vector dot product is commutative: $\\mathbf{a} \\cdot \\mathbf{b} = \\mathbf{b} \\cdot \\mathbf{a}$, while cross product is anticommutative: $\\mathbf{a} \\times \\mathbf{b} = -(\\mathbf{b} \\times \\mathbf{a})$. "
        "Set union and intersection are commutative: $A \\cup B = B \\cup A$ and $A \\cap B = B \\cap A$."
    ),
    "commutator": (
        "1. In group theory, the element $[x, y] = x^{-1}y^{-1}xy$. Elements $x$ and $y$ commute if and only if $[x, y] = e$. "
        "2. In quantum mechanics and operator algebra, the operator: "
        "$$[P, Q] = PQ - QP$$ "
        "3. In electrical engineering, a mechanical rotary switch on DC motors or generators that periodically reverses current direction between rotor and external circuit."
    ),
    "companion matrix": (
        "For a monic polynomial $p(x) = x^n - b_{n-1}x^{n-1} - \\dots - b_1 x - b_0$, the companion matrix is a square matrix whose characteristic polynomial equals $p(x)$."
    ),
    "comparison test": (
        "A convergence test for infinite series stating that if $0 \\le a_n \\le b_n$ for all $n$, then if $\\sum b_n$ converges, $\\sum a_n$ must also converge. "
        "For example, because $\\frac{1}{k^2} \\le \\frac{1}{k(k-1)}$ for $k \\ge 2$ and $\\sum_{k=2}^\\infty \\frac{1}{k(k-1)}$ converges, $\\sum_{k=1}^\\infty \\frac{1}{k^2}$ converges."
    ),
    "complete residue system": (
        "A set of integers containing exactly one element from every residue class modulo $m$. The standard least non-negative residue system is: "
        "$$\\{0, 1, 2, \\dots, m - 1\\}$$ "
        "where every integer $a_\\nu$ satisfies $a_\\nu \\equiv \\nu \\pmod{m}$."
    ),
    "composite function": (
        "A function formed by applying one function to the result of another: $(f \\circ g)(x) = f(g(x))$. For example, if $f(x) = 2x + 5$ and $g(x) = 6x$, then: "
        "$$f(g(x)) = 2(6x) + 5 = 12x + 5$$"
    ),
    "composition": (
        "The operation combining two functions $f$ and $g$ to form $(f \\circ g)(x) = f(g(x))$. For instance, the composition of $x + 3$ with $x^2$ is $(x + 3)^2$ or $x^2 + 3$. "
        "Repeated $n$-fold composition is denoted $f^{(n)}(x)$."
    ),
    "compound angle formulae": (
        "Fundamental trigonometric identities for angle sums and differences: "
        "$$\\sin(A \\pm B) = \\sin A \\cos B \\pm \\cos A \\sin B$$ "
        "$$\\cos(A \\pm B) = \\cos A \\cos B \\mp \\sin A \\sin B$$ "
        "$$\\tan(A \\pm B) = \\frac{\\tan A \\pm \\tan B}{1 \\mp \\tan A \\tan B}$$"
    ),
    "compound interest": (
        "Interest calculated on both initial principal $P$ and accumulated past interest. The accumulated amount $A$ is given by: "
        "$$A = P\\left(1 + \\frac{r}{n}\\right)^{nt}$$ "
        "and compound interest earned is $\\text{CI} = A - P$, where $r$ is the annual interest rate, $n$ is compounding frequency per year, and $t$ is time in years."
    ),
    "compound microscope": (
        "An optical instrument using two convex lenses (objective and eyepiece) to achieve high magnification. The total angular magnification $M$ is given by: "
        "$$M = m_o \\times m_e = -\\frac{v_o}{u_o}\\left(1 + \\frac{D}{f_e}\\right) \\approx -\\frac{L}{f_o} \\left(\\frac{D}{f_e}\\right)$$ "
        "where $f_o$ and $f_e$ are objective and eyepiece focal lengths, $L$ is tube length, and $D$ is the least distance of distinct vision ($25\\text{ cm}$)."
    ),
    "compressibility": (
        "The measure of fractional volume change per unit change in pressure: "
        "$$\\beta = -\\frac{1}{V}\\frac{\\Delta V}{\\Delta P}$$ "
        "The negative sign ensures $\\beta$ remains positive. Its SI unit is reciprocal pascal ($\\text{Pa}^{-1}$)."
    ),
    "concave down": (
        "A curve where the tangent line lies above the curve on an interval, corresponding to a decreasing first derivative and non-positive second derivative: "
        "$$f''(x) \\le 0$$"
    ),
    "concave up": (
        "A curve where the tangent line lies below the curve on an interval, corresponding to an increasing first derivative and non-negative second derivative: "
        "$$f''(x) \\ge 0$$"
    ),
    "conchoid": (
        "A curve determined from a fixed pole and line. In Cartesian coordinates: "
        "$$(x - a)^2(x^2 + y^2) = b^2 x^2$$ "
        "and in polar coordinates: "
        "$$r = \\frac{a}{\\cos\\theta} \\pm b$$ "
        "where $a$ is the distance to the directrix line and $b$ is the offset parameter."
    ),
    "conditional": (
        "An equation or inequality that holds true only for specific values of its variables. For example, $x^2 - 1 = x + 1$ is a conditional equation valid only for $x = 2$ and $x = -1$."
    ),
    "conditional probability": (
        "The probability of event $A$ occurring given that event $B$ has already occurred: "
        "$$P(A \\mid B) = \\frac{P(A \\cap B)}{P(B)}, \\quad \\text{for } P(B) > 0$$"
    ),
    "conditionally convergent": (
        "A series $\\sum_{n=1}^\\infty a_n$ that converges, but whose series of absolute values $\\sum_{n=1}^\\infty |a_n|$ diverges. For example, the alternating harmonic series: "
        "$$\\sum_{n=1}^\\infty \\frac{(-1)^{n-1}}{n} = 1 - \\frac{1}{2} + \\frac{1}{3} - \\frac{1}{4} + \\dots = \\ln(2)$$ "
        "is conditionally convergent because $\\sum_{n=1}^\\infty \\frac{1}{n}$ diverges."
    ),
    "conductance": (
        "The ability of an electrical component to conduct electric current, denoted by $G$: "
        "$$G = \\frac{1}{R}$$ "
        "In AC circuits, $G = \\frac{R}{R^2 + X^2}$. Measured in siemens ($\\text{S}$), where $1\\text{ S} = 1\\ \\Omega^{-1}$."
    ),
    "conductivity": (
        "A material's intrinsic ability to conduct electric current, denoted by $\\sigma$: "
        "$$\\sigma = \\frac{1}{\\rho}$$ "
        "where $\\rho$ is electrical resistivity. Measured in siemens per metre ($\\text{S}\\cdot\\text{m}^{-1}$ or $(\\Omega\\cdot\\text{m})^{-1}$)."
    ),
    "cone": (
        "A three-dimensional geometric solid tapering smoothly from a flat base to an apex. For a circular cone with base radius $r$ and perpendicular height $h$, the volume is: "
        "$$V = \\frac{1}{3}\\pi r^2 h$$"
    ),
    "confidence limit": (
        "The lower and upper bounds of a confidence interval containing the true population parameter: "
        "$$\\bar{Y} \\pm t_{1 - \\alpha/2, \\, N-1} \\frac{s}{\\sqrt{N}}$$ "
        "where $\\bar{Y}$ is sample mean, $s$ is sample standard deviation, and $N$ is sample size."
    ),
    "congruence": (
        "A relation between integers stating that their difference is divisible by a fixed integer modulus $m$: "
        "$$x \\equiv y \\pmod{m} \\iff m \\mid (x - y)$$ "
        "For example, $8 \\equiv 2 \\pmod{3}$ since $8 - 2 = 6 = 2 \\times 3$."
    ),
    "congruent": (
        "1. In geometry, shapes having identical dimensions and angles. "
        "2. In matrix theory, two matrices $A$ and $B$ are congruent if $B = P A P^T$ for an invertible matrix $P$."
    ),
    "congruent modulo h": (
        "In group theory, elements $x, y \\in G$ are left-congruent modulo subgroup $H$ ($x \\equiv_l y \\pmod{H}$) if $x^{-1}y \\in H$, "
        "and right-congruent ($x \\equiv_r y \\pmod{H}$) if $yx^{-1} \\in H$."
    ),
    "congruent modulo m": (
        "Two integers $b$ and $c$ whose difference $b - c$ is an integral multiple of modulus $m$: "
        "$$b \\equiv c \\pmod{m}$$"
    ),
    "conic": (
        "A plane curve formed by the intersection of a plane with a double right cone. In Cartesian coordinates: "
        "$$A x^2 + B xy + C y^2 + D x + E y + F = 0$$ "
        "In vertex form: $y^2 = 2px - (1 - e^2)x^2$, where $e$ is eccentricity and $p$ is the semi-latus rectum."
    ),
    "conjugacy class": (
        "The set of elements in a group $G$ conjugate to a given element $a$: "
        "$$\\text{cl}(a) = \\{g a g^{-1} \\mid g \\in G\\}$$"
    ),
    "conjugacy problem": (
        "The algorithmic decision problem of determining whether two given elements $x, y \\in G$ are conjugate, "
        "i.e., whether there exists $z \\in G$ such that $y = z x z^{-1}$."
    ),
    "conjugate": (
        "1. Complex conjugate: $\\overline{a + bi} = a - bi$. "
        "2. Conjugate roots: irrational roots of a polynomial with rational coefficients occurring in pairs, such as $3 + \\sqrt{2}$ and $3 - \\sqrt{2}$ for $x^2 - 6x + 7 = 0$."
    ),
    "conjugate exponents": (
        "Any two positive real numbers $p, q > 1$ satisfying Hölder's exponent condition: "
        "$$\\frac{1}{p} + \\frac{1}{q} = 1$$"
    ),
    "conjunctive": (
        "Two complex matrices $A$ and $B$ such that $B = P A P^*$, where $P^*$ is the conjugate transpose (Hermitian adjoint) of an invertible matrix $P$."
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

    for target_word, new_def in BATCH_C3_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section C: [{target_word}]")

    print(f"\nEnriched {updated_count} / {len(BATCH_C3_DEFINITIONS)} definitions in Section C Batch 3.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    print("Rebuilding core_dictionary.js index...")
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
