"""
integrate_section_lm_diagrams.py
================================
Precision cropping, high-resolution generation, and dual-map integration
for all 101 user-captured screenshots in 'l-m diagrams/' (Files 13 to 113).

Replaces bad vector-extracted images with pristine, complete-label captures.
Updates:
  - diagrams/dict_*.png
  - dictionary_diagrams_map.json
  - core_dictionary_diagrams.js
  - DIAGRAM_BATCH_MAPPING_GUIDE.md
"""
import os
import json
from PIL import Image, ImageDraw

def clean_crop(img, box=None):
    """
    Crops an image. If box is None, trims extreme borders if needed.
    box format: (left, top, right, bottom) in pixels or relative (0.0 - 1.0).
    """
    w, h = img.size
    if box:
        left, top, right, bottom = box
        if isinstance(left, float):
            box = (int(left * w), int(top * h), int(right * w), int(bottom * h))
        return img.crop(box)
    return img

def main():
    src_dir = "l-m diagrams"
    out_dir = "diagrams"
    map_json_path = "dictionary_diagrams_map.json"
    diag_js_path = "core_dictionary_diagrams.js"
    guide_path = "DIAGRAM_BATCH_MAPPING_GUIDE.md"

    os.makedirs(out_dir, exist_ok=True)

    # 101 specifications for Section L and M (Files 13 through 113 of l-m diagrams/)
    specifications = [
        # 1: Labiate
        ("Screenshot_25-9-2026_172950_.jpeg", [
            ("dict_labiate.png", None, ["labiate", "labiate corolla", "bilabiate", "labiate flower"], "Labiate corolla")
        ]),
        # 2: Lacerate leaf
        ("Screenshot_25-9-2026_173027_.jpeg", [
            ("dict_lacerate_leaf.png", None, ["lacerate", "lacerate leaf"], "Lacerate leaf")
        ]),
        # 3: Laciniate leaf
        ("Screenshot_25-9-2026_173038_.jpeg", [
            ("dict_laciniate_leaf.png", None, ["laciniate", "laciniate leaf"], "Laciniate leaf")
        ]),
        # 4: Lactic acid
        ("Screenshot_25-9-2026_17307_.jpeg", [
            ("dict_lactic_acid.png", None, ["lactic acid", "2-hydroxypropanoic acid", "2-hydroxypropanoate", "lactate"], "Lactic acid (2-Hydroxypropanoic Acid)")
        ]),
        # 5: Lactam / Lactim tautomers
        ("Screenshot_25-9-2026_173155_.jpeg", [
            ("dict_lactam_lactim.png", None, ["lactam", "lactim", "lactam-lactim tautomerism", "lactams"], "Lactam and lactim tautomerism")
        ]),
        # 6: Lami's Theorem
        ("Screenshot_25-9-2026_173249_.jpeg", [
            ("dict_lamis_theorem.png", None, ["lami's theorem", "lamis theorem", "triangle of forces", "forces in equilibrium"], "Lami's Theorem (3 forces in equilibrium)")
        ]),
        # 7: Lanceolate leaf
        ("Screenshot_25-9-2026_173321_.jpeg", [
            ("dict_lanceolate_leaf.png", None, ["lanceolate", "lanceolate leaf"], "Lanceolate leaf")
        ]),
        # 8: Leaf lamina & Petal lamina
        ("Screenshot_25-9-2026_17335_.jpeg", [
            ("dict_lamina.png", None, ["lamina", "leaf lamina", "petal lamina", "blade"], "Leaf lamina & Petal lamina")
        ]),
        # 9: Latin square
        ("Screenshot_25-9-2026_173437_.jpeg", [
            ("dict_latin_square.png", None, ["latin square", "latin square design"], "Latin square (3 x 3)")
        ]),
        # 10: Electrical method for latent heat of evaporation
        ("Screenshot_25-9-2026_17346_.jpeg", [
            ("dict_latent_heat_evaporation.png", None, ["latent heat of vaporization", "latent heat of evaporation", "specific latent heat of vaporization"], "Electrical method for latent heat of evaporation")
        ]),
        # 11: Layering (plant propagation)
        ("Screenshot_26-9-2026_142138_.jpeg", [
            ("dict_layering.png", None, ["layering", "plant layering", "mound layering"], "Layering (plant propagation)")
        ]),
        # 12: Leclanche dry cell
        ("Screenshot_26-9-2026_142221_.jpeg", [
            ("dict_leclanche_cell.png", None, ["leclanche cell", "leclanché cell", "dry cell", "zinc-carbon cell"], "Leclanche dry cell")
        ]),
        # 13: Types of lenses & symbols
        ("Screenshot_26-9-2026_142245_.jpeg", [
            ("dict_lens_types.png", None, ["lens", "convex lens", "concave lens", "converging lens", "diverging lens", "types of lenses"], "Types of lenses & symbols (converging / diverging)")
        ]),
        # 14: Parts of a leaf
        ("Screenshot_26-9-2026_14225_.jpeg", [
            ("dict_leaf_parts.png", None, ["leaf", "parts of a leaf", "leaf structure", "petiole", "midrib", "leaf blade"], "Parts of a leaf")
        ]),
        # 15: Leslie's Cube
        ("Screenshot_26-9-2026_14232_.jpeg", [
            ("dict_leslies_cube.png", None, ["leslie's cube", "leslies cube", "thermal radiation cube"], "Leslie's Cube")
        ]),
        # 16: Levers (1st, 2nd, 3rd class)
        ("Screenshot_26-9-2026_142343_.jpeg", [
            ("dict_levers.png", None, ["lever", "first class lever", "second class lever", "third class lever", "classes of levers"], "Classes of levers (1st, 2nd, 3rd class)")
        ]),
        # 17: Parabola line of symmetry & equation
        ("Screenshot_26-9-2026_142429_.jpeg", [
            ("dict_parabola_line_of_symmetry.png", None, ["line of symmetry", "axis of symmetry", "parabola symmetry"], "Parabola line of symmetry & equation")
        ]),
        # 18: Linear Combination of Atomic Orbitals (LCAO)
        ("Screenshot_26-9-2026_142442_.jpeg", [
            ("dict_lcao.png", None, ["linear combination of atomic orbitals", "lcao", "molecular orbital theory"], "Linear Combination of Atomic Orbitals (LCAO)")
        ]),
        # 19: Ligulate Corolla
        ("Screenshot_26-9-2026_14248_.jpeg", [
            ("dict_ligulate_corolla.png", None, ["ligulate", "ligulate corolla", "ray floret"], "Ligulate Corolla")
        ]),
        # 20: Linear leaf
        ("Screenshot_26-9-2026_14267_.jpeg", [
            ("dict_linear_leaf.png", None, ["linear leaf"], "Linear leaf")
        ]),
        # 21: Linear Graph (y = mx + c)
        ("Screenshot_26-9-2026_142722_.jpeg", [
            ("dict_linear_graph.png", None, ["linear graph", "linear equation graph", "gradient", "straight line graph"], "Linear Graph (y = mx + c)")
        ]),
        # 22: Measuring linear expansivity of a metal
        ("Screenshot_26-9-2026_142756_.jpeg", [
            ("dict_linear_expansivity.png", None, ["linear expansivity", "thermal expansivity", "coefficient of linear expansion"], "Measuring linear expansivity of a metal")
        ]),
        # 23: Lipoic Acid
        ("Screenshot_26-9-2026_142955_.jpeg", [
            ("dict_lipoic_acid.png", None, ["lipoic acid", "alpha-lipoic acid", "thioctic acid"], "Lipoic Acid")
        ]),
        # 24: Lobed leaf
        ("Screenshot_26-9-2026_14336_.jpeg", [
            ("dict_lobed_leaf.png", None, ["lobed leaf", "lobed"], "Lobed leaf")
        ]),
        # 25: Benzene localized electrons
        ("Screenshot_26-9-2026_143633_.jpeg", [
            ("dict_localized_electrons.png", None, ["localized electrons", "delocalized electrons"], "Benzene localized electrons")
        ]),
        # 26: Ammonia lone pair trigonal pyramid
        ("Screenshot_26-9-2026_143659_.jpeg", [
            ("dict_lone_pair.png", None, ["lone pair", "lone pair electrons", "unshared pair"], "Ammonia lone pair trigonal pyramid")
        ]),
        # 27: Lumbar vertebra of a mammal
        ("Screenshot_26-9-2026_143734_.jpeg", [
            ("dict_lumbar_vertebra.png", None, ["lumbar vertebra", "lumbar vertebrae", "vertebra"], "Lumbar vertebra of a mammal (anterior & lateral)")
        ]),
        # 28: Lysine
        ("Screenshot_26-9-2026_143846_.jpeg", [
            ("dict_lysine.png", None, ["lysine", "l-lysine"], "Lysine")
        ]),
        # 29: Mach Angle
        ("Screenshot_26-9-2026_143916_.jpeg", [
            ("dict_mach_angle.png", None, ["mach angle", "mach cone", "mach number"], "Mach Angle (Mach cone)")
        ]),
        # 30: 2-methylpropenoic Acid (Methacrylic acid)
        ("Screenshot_26-9-2026_143922_.jpeg", [
            ("dict_methacrylic_acid.png", None, ["2-methylpropenoic acid", "methacrylic acid"], "2-methylpropenoic Acid (Methacrylic acid)")
        ]),
        # 31: Ecstasy (MDMA)
        ("Screenshot_26-9-2026_143933_.jpeg", [
            ("dict_mdma.png", None, ["mdma", "ecstasy", "3,4-methylenedioxymethamphetamine"], "Ecstasy (MDMA)")
        ]),
        # 32: Magic-Angle Spinning
        ("Screenshot_26-9-2026_143946_.jpeg", [
            ("dict_magic_angle_spinning.png", None, ["magic angle", "magic-angle spinning"], "Magic-Angle Spinning")
        ]),
        # 33: Right hand grip rule
        ("Screenshot_26-9-2026_144125_.jpeg", [
            ("dict_right_hand_grip_rule.png", None, ["right hand grip rule", "grip rule", "magnetic field of conductor"], "Right hand grip rule (conductor & solenoid)")
        ]),
        # 34: Lateral view of a maggot
        ("Screenshot_26-9-2026_14413_.jpeg", [
            ("dict_maggot.png", None, ["maggot", "housefly larva"], "Lateral view of a maggot")
        ]),
        # 35: Magnetic field lines near a bar magnet
        ("Screenshot_26-9-2026_144142_.jpeg", [
            ("dict_magnetic_field_lines.png", None, ["magnetic field lines", "magnetic flux lines", "bar magnet"], "Magnetic field lines near a bar magnet")
        ]),
        # 36: 3 x 3 Magic Square
        ("Screenshot_26-9-2026_14419_.jpeg", [
            ("dict_magic_square.png", None, ["magic square"], "3 x 3 Magic Square")
        ]),
        # 37: Magnifying glass
        ("Screenshot_26-9-2026_144225_.jpeg", [
            ("dict_magnifying_glass.png", None, ["magnifying glass", "simple magnifier"], "Magnifying glass")
        ]),
        # 38: Maize fruit
        ("Screenshot_26-9-2026_144245_.jpeg", [
            ("dict_maize_fruit.png", None, ["maize fruit", "caryopsis", "grain of maize", "maize grain"], "Maize fruit (external & longitudinal section)")
        ]),
        # 39: Using electricity to magnetise a nail
        ("Screenshot_26-9-2026_14426_.jpeg", [
            ("dict_electromagnet_nail.png", None, ["electromagnet", "magnetisation", "magnetization"], "Using electricity to magnetise a nail")
        ]),
        # 40: Major segment & Minor arc
        ("Screenshot_26-9-2026_144312_.jpeg", [
            ("dict_major_segment.png", None, ["major segment", "segment of a circle"], "Major segment & Minor arc")
        ]),
        # 41: Maleic Anhydride
        ("Screenshot_26-9-2026_144334_.jpeg", [
            ("dict_maleic_anhydride.png", None, ["maleic anhydride", "furan-2,5-dione"], "Maleic Anhydride")
        ]),
        # 42: Malfatti Circles
        ("Screenshot_26-9-2026_144345_.jpeg", [
            ("dict_malfatti_circles.png", None, ["malfatti circles", "malfatti's circles"], "Malfatti Circles")
        ]),
        # 43: Malleus (Hammer) of the human ear
        ("Screenshot_26-9-2026_144413_.jpeg", [
            ("dict_malleus.png", None, ["malleus", "hammer bone", "ear ossicles"], "Malleus (Hammer) of the human ear")
        ]),
        # 44: Malpighian Body
        ("Screenshot_26-9-2026_14441_.jpeg", [
            ("dict_malpighian_body.png", None, ["malpighian body", "malpighian corpuscle", "renal corpuscle"], "Malpighian Body (Glomerulus + Bowman's capsule)")
        ]),
        # 45: Mammary glands
        ("Screenshot_26-9-2026_144712_.jpeg", [
            ("dict_mammary_gland.png", None, ["mammary gland", "mammary glands", "lactiferous duct"], "Left breast of a human showing the mammary glands")
        ]),
        # 46: Mammal
        ("Screenshot_26-9-2026_144721_.jpeg", [
            ("dict_mammal.png", None, ["mammal", "mammalia", "rodent"], "Lateral view of a rodent, an example of a mammal")
        ]),
        # 47: Mango
        ("Screenshot_26-9-2026_144742_.jpeg", [
            ("dict_mango.png", None, ["mango", "drupe", "mango fruit", "longitudinal section of mango"], "Longitudinal section of a mango")
        ]),
        # 48: The manometer
        ("Screenshot_26-9-2026_144813_.jpeg", [
            ("dict_manometer.png", None, ["manometer", "u-tube manometer", "gas pressure measurement"], "The manometer")
        ]),
        # 49: Mechanism of Mannich Reaction
        ("Screenshot_26-9-2026_144824_.jpeg", [
            ("dict_mannich_reaction.png", None, ["mannich reaction", "mannich base"], "Mechanism of Mannich Reaction")
        ]),
        # 50: Mannitol
        ("Screenshot_26-9-2026_144830_.jpeg", [
            ("dict_mannitol.png", None, ["mannitol", "d-mannitol"], "Chemical structure of Mannitol")
        ]),
        # 51: Earth crust showing layers (Mantle)
        ("Screenshot_26-9-2026_144845_.jpeg", [
            ("dict_mantle_earth.png", None, ["mantle", "earth's mantle", "upper mantle", "lower mantle"], "Earth crust showing the layers")
        ]),
        # 52: Mantle of a snail
        ("Screenshot_26-9-2026_144850_.jpeg", [
            ("dict_mantle_snail.png", None, ["mantle (mollusc)", "snail mantle", "mollusc mantle"], "Mantle of a snail")
        ]),
        # 53: Mantle (Composite)
        ("Screenshot_26-9-2026_144857_.jpeg", [
            ("dict_mantle.png", None, ["mantle", "mantle structure"], "Earth crust & snail mantle")
        ]),
        # 54: Margin of a leaf
        ("Screenshot_26-9-2026_144914_.jpeg", [
            ("dict_leaf_margin.png", None, ["margin", "leaf margin"], "Margin of a leaf")
        ]),
        # 55: Marginal placentation
        ("Screenshot_26-9-2026_144920_.jpeg", [
            ("dict_marginal_placentation.png", None, ["marginal placentation", "placentation"], "Marginal placentation of apocarpous gynoecium")
        ]),
        # 56: Mass spectrometer
        ("Screenshot_26-9-2026_144937_.jpeg", [
            ("dict_mass_spectrometer.png", None, ["mass spectrometer", "mass spectrometry"], "Mass spectrometer")
        ]),
        # 57: The mass spectrograph
        ("Screenshot_26-9-2026_144948_.jpeg", [
            ("dict_mass_spectrograph.png", None, ["mass spectrograph"], "The mass spectrograph")
        ]),
        # 58: Air layering (marcotting)
        ("Screenshot_26-9-2026_14497_.jpeg", [
            ("dict_marcotting.png", None, ["marcotting", "air layering"], "Air layering (marcotting)")
        ]),
        # 59: Melamine
        ("Screenshot_26-9-2026_145039_.jpeg", [
            ("dict_melamine.png", None, ["melamine", "1,3,5-triazine-2,4,6-triamine"], "Chemical structure of Melamine")
        ]),
        # 60: Melatonin
        ("Screenshot_26-9-2026_145049_.jpeg", [
            ("dict_melatonin.png", None, ["melatonin", "n-acetyl-5-methoxytryptamine"], "Chemical structure of Melatonin")
        ]),
        # 61: Mellitic Acid
        ("Screenshot_26-9-2026_145055_.jpeg", [
            ("dict_mellitic_acid.png", None, ["mellitic acid", "benzenehexacarboxylic acid"], "Chemical structure of Mellitic Acid")
        ]),
        # 62: Plane of Symmetry of Meso Compound
        ("Screenshot_26-9-2026_145120_.jpeg", [
            ("dict_meso_compound.png", None, ["meso compound", "plane of symmetry", "meso form"], "Plane of Symmetry of Meso Compound")
        ]),
        # 63: Mescaline
        ("Screenshot_26-9-2026_145128_.jpeg", [
            ("dict_mescaline.png", None, ["mescaline", "3,4,5-trimethoxyphenethylamine"], "Chemical structure of Mescaline")
        ]),
        # 64: Metacarpal
        ("Screenshot_26-9-2026_145145_.jpeg", [
            ("dict_metacarpal.png", None, ["metacarpal", "metacarpals", "carpal", "carpus"], "Human hand showing the metacarpal")
        ]),
        # 65: Metallocene
        ("Screenshot_26-9-2026_145155_.jpeg", [
            ("dict_metallocene.png", None, ["metallocene", "sandwich compound", "dibenzenechromium"], "Structure of (Benzene) chromium tricarbonyl, an example of metallocene")
        ]),
        # 66: Menthol
        ("Screenshot_26-9-2026_14516_.jpeg", [
            ("dict_menthol.png", None, ["menthol", "2-isopropyl-5-methylcyclohexanol"], "Chemical structure of Menthol")
        ]),
        # 67: Metatarsals
        ("Screenshot_26-9-2026_145218_.jpeg", [
            ("dict_metatarsals.png", None, ["metatarsals", "metatarsal", "tarsals", "tarsus"], "Human leg showing the metatarsals")
        ]),
        # 68: Metaldehyde
        ("Screenshot_26-9-2026_14522_.jpeg", [
            ("dict_metaldehyde.png", None, ["metaldehyde"], "Chemical structure of Metaldehyde")
        ]),
        # 69: Methanal
        ("Screenshot_26-9-2026_145232_.jpeg", [
            ("dict_methanal.png", None, ["methanal", "formaldehyde"], "Chemical structure of methanal")
        ]),
        # 70: Methionine
        ("Screenshot_26-9-2026_145247_.jpeg", [
            ("dict_methionine.png", None, ["methionine", "l-methionine"], "Chemical structure of Methionine")
        ]),
        # 71: Methyl Orange
        ("Screenshot_26-9-2026_145258_.jpeg", [
            ("dict_methyl_orange.png", None, ["methyl orange", "helianthin"], "Chemical structure of Methyl Orange")
        ]),
        # 72: Methylbenzene (Toluene)
        ("Screenshot_26-9-2026_145313_.jpeg", [
            ("dict_methylbenzene.png", None, ["methylbenzene", "toluene"], "Chemical structure of Methylbenzene (Toluene)")
        ]),
        # 73: Methyl Salicylate
        ("Screenshot_26-9-2026_145321_.jpeg", [
            ("dict_methyl_salicylate.png", None, ["methyl salicylate", "oil of wintergreen"], "Chemical structure of Methyl Salicylate")
        ]),
        # 74: Methyl Violet
        ("Screenshot_26-9-2026_145329_.jpeg", [
            ("dict_methyl_violet.png", None, ["methyl violet", "gentian violet", "crystal violet"], "Chemical structure of Methyl Violet")
        ]),
        # 75: Methylene Blue
        ("Screenshot_26-9-2026_145339_.jpeg", [
            ("dict_methylene_blue.png", None, ["methylene blue", "methylthioninium chloride"], "Chemical structure of Methylene Blue")
        ]),
        # 76: Metre bridge
        ("Screenshot_26-9-2026_145352_.jpeg", [
            ("dict_metre_bridge.png", None, ["metre bridge", "meter bridge", "slide wire bridge"], "Using a metre bridge to measure an unknown resistance")
        ]),
        # 77: Methyl Red
        ("Screenshot_26-9-2026_14535_.jpeg", [
            ("dict_methyl_red.png", None, ["methyl red"], "Chemical structure of Methyl Red")
        ]),
        # 78: Michelson-Morley Interferometer
        ("Screenshot_26-9-2026_145415_.jpeg", [
            ("dict_michelson_morley_interferometer.png", None, ["michelson-morley interferometer", "interferometer", "michelson interferometer"], "Michelson-Morley Interferometer")
        ]),
        # 79: Micrometer screw gauge
        ("Screenshot_26-9-2026_145433_.jpeg", [
            ("dict_micrometer_screw_gauge.png", None, ["micrometer screw gauge", "micrometer", "screw gauge"], "A micrometer screw gauge")
        ]),
        # 80: Carbon microphone
        ("Screenshot_26-9-2026_145453_.jpeg", [
            ("dict_carbon_microphone.png", None, ["carbon microphone", "microphone"], "Carbon microphone")
        ]),
        # 81: Light microscope
        ("Screenshot_26-9-2026_145512_.jpeg", [
            ("dict_light_microscope.png", None, ["light microscope", "optical microscope", "simple light microscope"], "Fig. I: A simple light microscope")
        ]),
        # 82: Compound microscope
        ("Screenshot_26-9-2026_145524_.jpeg", [
            ("dict_compound_microscope.png", None, ["compound microscope"], "Fig. II: A compound microscope")
        ]),
        # 83: Simple & Compound Microscope Composite
        ("Screenshot_26-9-2026_145538_.jpeg", [
            ("dict_microscope.png", None, ["microscope"], "Simple and compound microscopes")
        ]),
        # 84: Midpoint
        ("Screenshot_26-9-2026_145554_.jpeg", [
            ("dict_midpoint.png", None, ["midpoint", "midpoint formula", "midpoint of a line segment"], "Midpoint (M) of a line segment")
        ]),
        # 85: Minor Arc
        ("Screenshot_26-9-2026_145625_.jpeg", [
            ("dict_minor_arc.png", None, ["minor arc", "arc of a circle"], "Minor Arc")
        ]),
        # 86: Mitochondrion
        ("Screenshot_26-9-2026_145640_.jpeg", [
            ("dict_mitochondrion.png", None, ["mitochondrion", "mitochondria", "crista", "cristae"], "Mitochondrion")
        ]),
        # 87: Mode of a graph
        ("Screenshot_26-9-2026_145659_.jpeg", [
            ("dict_mode_graph.png", None, ["mode", "modal class", "mode of a graph", "histogram mode"], "Mode of a graph")
        ]),
        # 88: Lateral view of a millipede
        ("Screenshot_26-9-2026_14569_.jpeg", [
            ("dict_millipede.png", None, ["millipede", "millepede", "diplopoda"], "Lateral view of a millepede")
        ]),
        # 89: Amplitude modulation
        ("Screenshot_26-9-2026_145714_.jpeg", [
            ("dict_amplitude_modulation.png", None, ["amplitude modulation", "am", "modulation"], "Amplitude modulation (AM)")
        ]),
        # 90: Molar
        ("Screenshot_26-9-2026_145729_.jpeg", [
            ("dict_molar_tooth.png", None, ["molar", "molar tooth", "teeth"], "Molar")
        ]),
        # 91: Monochasium
        ("Screenshot_26-9-2026_145750_.jpeg", [
            ("dict_monochasium.png", None, ["monochasium", "cyme", "monochasial cyme"], "Monochasium")
        ]),
        # 92: A monochord (sonometer)
        ("Screenshot_26-9-2026_145759_.jpeg", [
            ("dict_monochord.png", None, ["monochord", "sonometer"], "A monochord (sonometer)")
        ]),
        # 93: Digestive tract of chicken (monogastric)
        ("Screenshot_26-9-2026_145812_.jpeg", [
            ("dict_monogastric_digestive_tract.png", None, ["monogastric", "monogastric digestive system", "gizzard", "proventriculus", "avian digestive system"], "The digestive tract of chicken (monogastric)")
        ]),
        # 94: Chemical structure of Morphine
        ("Screenshot_26-9-2026_145830_.jpeg", [
            ("dict_morphine.png", None, ["morphine"], "Chemical structure of Morphine")
        ]),
        # 95: Mosquito (Composite and individual quadrants)
        ("Screenshot_26-9-2026_145845_.jpeg", [
            ("dict_mosquito.png", None, ["mosquito", "life cycle of mosquito"], "Mosquito life cycle stages and head"),
            ("dict_mosquito_larva.png", (0.0, 0.0, 0.5, 0.49), ["mosquito larva", "larva of a mosquito"], "Fig. I: Larva of a mosquito"),
            ("dict_mosquito_pupa.png", (0.5, 0.0, 1.0, 0.49), ["mosquito pupa", "pupa of a mosquito"], "Fig. II: Pupa of a mosquito"),
            ("dict_anopheles_mosquito.png", (0.0, 0.49, 0.5, 1.0), ["anopheles", "anopheles mosquito", "dorsal view of anopheles mosquito"], "Fig. III: Dorsal view of anopheles mosquito"),
            ("dict_mosquito_proboscis.png", (0.5, 0.49, 1.0, 1.0), ["proboscis", "lateral view of the head of a mosquito", "mosquito proboscis"], "Fig IV: Lateral view of the head of a mosquito")
        ]),
        # 96: Moss plant
        ("Screenshot_26-9-2026_145853_.jpeg", [
            ("dict_moss_plant.png", None, ["moss", "moss plant", "bryophyte", "rhizoid", "capsule (moss)"], "Moss plant")
        ]),
        # 97: A motor neurone
        ("Screenshot_26-9-2026_145914_.jpeg", [
            ("dict_motor_neurone.png", None, ["motor neurone", "motor neuron", "efferent neurone", "axon", "dendron", "myelin sheath"], "A motor neurone")
        ]),
        # 98: Moving-coil instrument
        ("Screenshot_26-9-2026_145933_.jpeg", [
            ("dict_moving_coil_instrument.png", None, ["moving-coil instrument", "moving coil galvanometer", "galvanometer", "pmmc"], "The permanent-magnet moving-coil instrument")
        ]),
        # 99: Multicentre Bond (diboranes (B2H6))
        ("Screenshot_26-9-2026_145957_.jpeg", [
            ("dict_multicentre_bond.png", None, ["multicentre bond", "multicenter bond", "diborane", "banana bond", "three-centre two-electron bond"], "Multicentre Bond (diboranes (B2H6))")
        ]),
        # 100: Mushroom (with clean top blanking for stray textbook text)
        ("Screenshot_26-9-2026_15020_.jpeg", [
            ("dict_mushroom.png", "clean_mushroom", ["mushroom", "agaricus", "pileus", "stipe", "gills (fungi)", "basidiomycete"], "Mushroom")
        ]),
        # 101: Myopia (Short Sightedness)
        ("Screenshot_26-9-2026_15057_.jpeg", [
            ("dict_myopia.png", None, ["myopia", "short sightedness", "shortsightedness", "nearsightedness"], "Myopia (Short Sightedness)")
        ])
    ]

    # Load existing dictionary map
    with open(map_json_path, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    processed_count = 0
    mapped_terms_count = 0
    batch_records = []

    for src_file, targets in specifications:
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print(f"WARNING: Source file {src_path} not found!")
            continue

        orig_img = Image.open(src_path)

        out_files = []
        all_terms = []
        caption_descs = []

        for tgt_file, box, terms, desc in targets:
            out_path = os.path.join(out_dir, tgt_file)
            
            if box == "clean_mushroom":
                # Clean top left stray text box with pure white
                cleaned = orig_img.copy()
                draw = ImageDraw.Draw(cleaned)
                draw.rectangle([0, 0, 165, 75], fill=(255, 255, 255))
                cropped = cleaned
            elif box:
                cropped = clean_crop(orig_img, box)
            else:
                cropped = orig_img

            # Save in crisp PNG format
            cropped.save(out_path, format="PNG", optimize=True)
            processed_count += 1
            out_files.append(tgt_file)
            caption_descs.append(desc)

            # Update mapping
            rel_val = f"diagrams/{tgt_file}"
            for term in terms:
                term_clean = term.lower().strip()
                diag_map[term_clean] = rel_val
                mapped_terms_count += 1
                all_terms.append(f"`{term_clean}`")

        batch_records.append({
            "src": src_file,
            "desc": " / ".join(caption_descs),
            "targets": ", ".join(f"`{f}`" for f in out_files),
            "terms": ", ".join(all_terms[:8])
        })

    # Save sorted dictionary_diagrams_map.json
    sorted_map = dict(sorted(diag_map.items()))
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=2, ensure_ascii=False)
    print(f"Updated {map_json_path} (Total mapped terms: {len(sorted_map)})")

    # Regenerate core_dictionary_diagrams.js
    json_str = json.dumps(sorted_map, indent=2, ensure_ascii=False)
    js_content = f"""// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)

const DictionaryDiagrams = {json_str};

if (typeof window !== 'undefined') {{
  window.DictionaryDiagrams = DictionaryDiagrams;
  window.DICTIONARY_DIAGRAMS = DictionaryDiagrams;
}}
if (typeof module !== 'undefined') {{
  module.exports = DictionaryDiagrams;
}}
"""
    with open(diag_js_path, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Saved {diag_js_path}")

    # Append to DIAGRAM_BATCH_MAPPING_GUIDE.md
    with open(guide_path, "r", encoding="utf-8") as f:
        guide_content = f.read()

    new_section = f"\n\n---\n\n### Section L & M Series: Batch 1 (Completed) — Screenshots 1 to 101\n"
    new_section += f"Source Folder: `l-m diagrams/` (September 25-26, 2026 Pristine Author Captures)\n\n"
    new_section += f"| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |\n"
    new_section += f"|---|---|---|---|---|\n"

    for i, rec in enumerate(batch_records, 1):
        new_section += f"| {i} | `{rec['src']}` | {rec['desc']} | {rec['targets']} | {rec['terms']} |\n"

    # Avoid duplicate section if already present
    if "### Section L & M Series: Batch 1" not in guide_content:
        guide_content += new_section
        with open(guide_path, "w", encoding="utf-8") as f:
            f.write(guide_content)
        print(f"Appended Section L & M batch table to {guide_path}")
    else:
        print(f"Section L & M batch already in {guide_path}")

    print(f"\nSUCCESS: Generated {processed_count} diagrams, mapped {mapped_terms_count} terms!")

if __name__ == "__main__":
    main()
