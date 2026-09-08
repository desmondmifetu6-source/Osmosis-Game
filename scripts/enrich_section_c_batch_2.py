"""
=====================================================================
OSMOSIS STEM FORMULA ENRICHMENT PIPELINE - SECTION C (BATCH 2)
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

BATCH_C2_DEFINITIONS = {
    "changing the subject ofa formula": (
        "The transformation or rearrangement of a formula to find the value of a subject of formula. "
        "For example, if $s = ut + \\frac{1}{2}at^2$, then in $a = \\frac{2(s - ut)}{t^2}$, $a$ is made the subject of formula."
    ),
    "clapeyron-clausius equation": (
        "A differential equation that governs the phase transition of a substance. In a two-phase system of the same substance, "
        "if the two phases are denoted by A and B, the Clapeyron-Clausius equation is given by: "
        "$$\\frac{dp}{dT} = \\frac{\\Delta H}{T(V_B - V_A)}$$ "
        "where $p$ is the pressure, $T$ is the thermodynamic temperature, $\\Delta H$ is the change in enthalpy per mole in the change from A to B, "
        "and $V_B$ and $V_A$ are the volumes of B and A respectively."
    ),
    "clausius-mossoti equation": (
        "A relationship between polarisability of a molecule and the dielectric constant of a dielectric substance. It is given by: "
        "$$\\frac{\\varepsilon - 1}{\\varepsilon + 2} = \\frac{d N_A \\alpha}{3 M \\varepsilon_0}$$ "
        "where $\\varepsilon$ is the dielectric constant of a substance, $\\varepsilon_0$ is the permittivity of a vacuum, $M$ is the molar mass, "
        "$d$ is its density, $N_A$ is Avogadro's constant and $\\alpha$ is the molecular polarisability."
    ),
    "coefficient of determination": (
        "The percentage of the variance of the dependent variable that is explained by the independent variables used to fit the data. "
        "Normally the symbol $r^2$ is used to represents the coefficient of determination. This is given by: "
        "$$r^2 = \\frac{\\text{explained variation}}{\\text{total variance}}$$"
    ),
    "coefficient of kinetic friction": (
        "The ratio of the frictional force, parallel to the surface of contact that opposes the motion of a body which is sliding, "
        "to the force, normal to the surface of contact, with which the bodies press against each other: "
        "$$\\mu_k = \\frac{F_k}{N}$$ "
        "where $\\mu_k$ is the coefficient of kinetic friction, $F_k$ is the force of kinetic friction and $N$ is the normal force."
    ),
    "coefficient of linear expansion": (
        "The fractional change in length per degree rise in temperature, represented by the symbol $\\alpha$. "
        "It is expressed as: "
        "$$\\alpha = \\frac{l_2 - l_1}{l_1 \\Delta\\theta}$$ "
        "where $l_1 = \\text{original length}$, $l_2 = \\text{final length}$ and $\\Delta\\theta = \\text{change in temperature}$."
    ),
    "coefficient of restitution": (
        "The ratio of relative speeds after and before an impact along the line of impact. "
        "The coefficient of restitution is given by: "
        "$$C_R = \\frac{V_2 - V_1}{u_1 - u_2}$$ "
        "where $V_1, V_2$ are the final velocities after impact and $u_1, u_2$ are the initial velocities before impact."
    ),
    "coefficient of static friction": (
        "The ratio of the maximum possible frictional force, parallel to the surface of contact that acts to prevent two bodies in contact at rest from sliding, to the normal force: "
        "$$\\mu_s = \\frac{F_s}{F_n}$$ "
        "where $F_s$ is static friction, $\\mu_s$ is the coefficient of static friction and $F_n$ is the normal force."
    ),
    "coefficient of variation": (
        "The coefficient of variation for a list of numbers is equal to the standard deviation for those numbers divided by the mean: "
        "$$C_v = \\frac{\\sigma}{\\mu}$$ "
        "It is used to compare the dispersions of quantitative variables."
    ),
    "combined law of thermodynamics": (
        "The mathematical summation of the first law of thermodynamics ($dU = dQ - PdV$) and the second law of thermodynamics ($dQ \\le TdS$) subsumed into a single mathematical expression: "
        "$$dU - TdS + PdV \\le 0$$ "
        "where $dU$ is a variation in internal energy, $T$ is temperature, $dS$ is variation in entropy, $P$ is pressure and $dV$ is variation in volume."
    ),
    "comfort index": (
        "An index which gives a numerical value of how tolerable conditions are for humans during the warm seasons. "
        "It is expressed as: "
        "$$\\text{Comfort Index} = T + \\frac{RH}{4}$$ "
        "where $T$ is temperature in degrees Fahrenheit and $RH$ is the relative humidity."
    ),
    "complete elliptic integral": (
        "Any elliptic integral expressed in terms of the functions $K$ and $E$, which denote the complete elliptic integral of the first and second kind. "
        "They are related by Legendre's identity for any $0 < k < 1$: "
        "$$K(k)E(1 - k^2) + E(k)K(1 - k^2) - K(k)K(1 - k^2) = \\frac{\\pi}{2}$$"
    ),
    "completing the square": (
        "A way of solving a quadratic equation by adding an expression to make it a perfect square. "
        "For example, $2x^2 - 4x - 3 = 0$ can be expressed as $2[x^2 - 2x] - 3 = 0$. "
        "Completing the square yields $2(x - 1)^2 - 5 = 0$. Solving gives: "
        "$$x = 1 \\pm \\sqrt{\\frac{5}{2}}$$"
    ),
    "complex fraction": (
        "A fraction in which either the numerator or denominator or both contains fractions. "
        "For example, $\\frac{\\frac{1}{3}}{\\frac{2}{7}}$ is a complex fraction. To simplify, multiply by the reciprocal of the denominator: "
        "$$\\frac{\\frac{1}{3}}{\\frac{2}{7}} = \\frac{1}{3} \\times \\frac{7}{2} = \\frac{7}{6}$$"
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

    for target_word, new_def in BATCH_C2_DEFINITIONS.items():
        key = target_word.lower()
        if key in word_map:
            word_map[key]['definition'] = new_def
            updated_count += 1
            print(f"  ✓ Updated: [{target_word}]")
        else:
            print(f"  ⚠️ Not found in Section C: [{target_word}]")

    print(f"\\nEnriched {updated_count} / {len(BATCH_C2_DEFINITIONS)} definitions in Section C Batch 2.")

    print(f"Writing updated {dict_file}...")
    with open(dict_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Rebuild core_dictionary.js
    cleaner.process_dictionary('dictionary.json', 'dictionary.json', 'core_dictionary.js')
    print("\\n✅ Successfully updated dictionary.json and rebuilt core_dictionary.js!")

if __name__ == '__main__':
    apply_enrichment()
