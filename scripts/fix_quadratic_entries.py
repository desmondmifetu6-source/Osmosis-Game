import json, sys, os

sys.path.insert(0, os.path.dirname(__file__))
import clean_and_enrich_formulas as cleaner

QUADRATIC_FORMULA_DEF = (
    "The quadratic formula states that the solution for $x$ in the standard quadratic equation "
    "$ax^2 + bx + c = 0$ (where $a \\neq 0$) is given by: "
    "$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$ "
    "The term under the square root, $b^2 - 4ac$, is called the discriminant ($\\Delta$). "
    "If $b^2 - 4ac > 0$, there are two distinct real roots; if $b^2 - 4ac = 0$, there is one repeated real root; "
    "and if $b^2 - 4ac < 0$, there are two complex conjugate roots."
)

QUADRATIC_EQUATION_DEF = (
    "An equation containing one or more terms raised to the power two; or a polynomial equation of second degree. "
    "Its highest exponent or power is two and it is of the standard form $ax^2 + bx + c = 0$, where $a, b$ and $c$ "
    "are given real numbers, with $a \\neq 0$. Quadratic equations can be solved by factorisation, completing the squares, "
    "or by using the quadratic formula: "
    "$$x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$$ "
    "The expression $b^2 - 4ac$ is referred to as the discriminant. If $b^2 - 4ac > 0$, the equation has two real roots; "
    "when $b^2 - 4ac < 0$, there are two complex roots; when $b^2 - 4ac = 0$, there are two equal roots; "
    "and for two real roots, $b^2 - 4ac \\ge 0$."
)

QUADRATIC_FUNCTION_DEF = (
    "A function of the form $f(x) = ax^2 + bx + c$, where $a, b$ and $c$ are real numbers and $a \\neq 0$. "
    "The quadratic term is $ax^2$ with $a$ as its coefficient. The term $bx$ is the linear term with $b$ as its coefficient. "
    "The term $c$ is the constant term. The graph of a quadratic function is a parabola, with its axis parallel to the y-axis. "
    "If $a > 0$, the curve opens upwards with the lowest point on it being the vertex, with a point minimum at $x = -\\frac{b}{2a}$. "
    "The y-value at the vertex is the minimum value of y. If $a < 0$, the curve opens downwards with the highest point on it, the vertex, "
    "a maximum point at $x = -\\frac{b}{2a}$. The vertex is a turning point on the parabola. If $|a|$ increases, the parabola becomes "
    "narrower; as $|a|$ decreases, the parabola becomes wider."
)

with open('dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data.get('Q', []):
    w = item.get('word', '').lower()
    if w == 'quadratic formula':
        item['definition'] = QUADRATIC_FORMULA_DEF
    elif w == 'quadratic equation':
        item['definition'] = QUADRATIC_EQUATION_DEF
    elif w == 'quadratic function':
        item['definition'] = QUADRATIC_FUNCTION_DEF

with open('dictionary.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
print("Successfully enriched quadratic formulas and synchronized core_dictionary.js!")
