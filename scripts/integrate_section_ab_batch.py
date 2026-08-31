"""
integrate_section_ab_batch.py
==============================
Batch integrates all 138 section A-B screenshots manually extracted by user
from 'section a-b images/' into 'diagrams/' with proper dict_ names.
Then updates dictionary_diagrams_map.json and core_dictionary_diagrams.js.
"""

import os
import json
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

ASSIGNMENTS = {
    "Screenshot 2026-08-03 161441.png": ("dict_abacus.png", ["abacus"]),
    "Screenshot 2026-08-03 161817.png": ("dict_abaxial.png", ["abaxial"]),
    "Screenshot 2026-08-03 161835.png": ("dict_abbe_refractometer.png", ["abbe refractometer"]),
    "Screenshot 2026-08-03 162009.png": ("dict_abdomen_abdominal_cavity.png", ["abdomen", "abdomen (abdominal cavity)"]),
    "Screenshot 2026-08-03 162107.png": ("dict_abo_blood_group_system.png", ["abo blood group system", "abo blood group"]),
    "Screenshot 2026-08-03 162120.png": ("dict_abomasum.png", ["abomasum"]),
    "Screenshot 2026-08-03 162141.png": ("dict_abruptly_pinnate_even_pinnate.png", ["abruptly pinnate", "abruptly pinnate (even pinnate)"]),
    "Screenshot 2026-08-03 162157.png": ("dict_abscissa.png", ["abscissa"]),
    "Screenshot 2026-08-03 162218.png": ("dict_absorption_spectrum.png", ["absorption spectrum"]),
    "Screenshot 2026-08-03 162233.png": ("dict_acceleration.png", ["acceleration"]),
    "Screenshot 2026-08-03 162247.png": ("dict_acceleration_time_graph.png", ["acceleration-time graph", "acceleration time graph"]),
    "Screenshot 2026-08-03 162308.png": ("dict_acceleration_due_to_gravity.png", ["acceleration due to gravity"]),
    "Screenshot 2026-08-03 162326.png": ("dict_access_point_base_station.png", ["access point (base station)", "access point"]),
    "Screenshot 2026-08-03 162355.png": ("dict_acetanilide_n_phenylethanamide.png", ["acetanilide", "acetanilide (n-phenylethanamide)"]),
    "Screenshot 2026-08-03 162409.png": ("dict_acetaldehyde.png", ["acetaldehyde"]),
    "Screenshot 2026-08-03 162423.png": ("dict_acetamide_ethanamide.png", ["acetamide", "acetamide (ethanamide)"]),
    "Screenshot 2026-08-03 162440.png": ("dict_acetylacetone.png", ["acetylacetone"]),
    "Screenshot 2026-08-03 162453.png": ("dict_acetophenone.png", ["acetophenone"]),
    "Screenshot 2026-08-03 162508.png": ("dict_acetylation_ethanoylation.png", ["acetylation", "acetylation (ethanoylation)"]),
    "Screenshot 2026-08-03 162521.png": ("dict_acetylcholine_ach.png", ["acetylcholine", "acetylcholine (ach)"]),
    "Screenshot 2026-08-03 162637.png": ("dict_acetyl_coenzyme_a_acetyl_coa.png", ["acetyl coenzyme a", "acetyl-coa", "acetyl coenzyme a (acetyl coa)"]),
    "Screenshot 2026-08-03 162648.png": ("dict_achromatic_lens.png", ["achromatic lens"]),
    "Screenshot 2026-08-03 162714.png": ("dict_acid_anhydride.png", ["acid anhydride"]),
    "Screenshot 2026-08-03 162725.png": ("dict_acrylamide.png", ["acrylamide"]),
    "Screenshot 2026-08-03 162733.png": ("dict_acrylonitrile_propenenitrile.png", ["acrylonitrile", "propenenitrile", "propenonitrile"]),
    "Screenshot 2026-08-03 162744.png": ("dict_activation_energy.png", ["activation energy"]),
    "Screenshot 2026-08-03 162804.png": ("dict_activity_series_of_metals.png", ["activity series of metals"]),
    "Screenshot 2026-08-03 162814.png": ("dict_acuminate.png", ["acuminate", "acuminate leaf"]),
    "Screenshot 2026-08-03 162822.png": ("dict_acute_angle.png", ["acute angle"]),
    "Screenshot 2026-08-03 162834.png": ("dict_acyclovir.png", ["acyclovir"]),
    "Screenshot 2026-08-03 162845.png": ("dict_adaptive_frequency_hopping.png", ["adaptive frequency hopping"]),
    "Screenshot 2026-08-03 162858.png": ("dict_adaxial.png", ["adaxial"]),
    "Screenshot 2026-08-03 162910.png": ("dict_addition_of_vectors.png", ["addition of vectors"]),
    "Screenshot 2026-08-03 162919.png": ("dict_adenosine_triphosphate_atp.png", ["adenosine triphosphate", "atp", "adenosine triphosphate (atp)"]),
    "Screenshot 2026-08-03 162927.png": ("dict_adipic_acid.png", ["adipic acid"]),
    "Screenshot 2026-08-03 162934.png": ("dict_adipocyte.png", ["adipocyte", "fat cell"]),
    "Screenshot 2026-08-03 162941.png": ("dict_adjacent_angles.png", ["adjacent angles", "adjacent"]),
    "Screenshot 2026-08-03 162948.png": ("dict_adrenaline_epinephrine.png", ["adrenaline", "epinephrine"]),
    "Screenshot 2026-08-03 211010.png": ("dict_aflatoxin.png", ["aflatoxin", "aflatoxin b1"]),
    "Screenshot 2026-08-03 211033.png": ("dict_air_layering.png", ["air layering", "marcotting"]),
    "Screenshot 2026-08-03 211050.png": ("dict_aldosterone.png", ["aldosterone"]),
    "Screenshot 2026-08-03 211113.png": ("dict_algebraic_curve.png", ["algebraic curve", "quadratic curve"]),
    "Screenshot 2026-08-03 211140.png": ("dict_alimentary_canal.png", ["alimentary canal", "alimentary canal of a human", "alimentary canal of a rabbit"]),
    "Screenshot 2026-08-03 211200.png": ("dict_allotrope.png", ["allotrope", "allotropy", "graphite allotrope", "diamond allotrope"]),
    "Screenshot 2026-08-03 211219.png": ("dict_alloy.png", ["alloy", "alloys"]),
    "Screenshot 2026-08-03 211232.png": ("dict_alternate_angles.png", ["alternate angles"]),
    "Screenshot 2026-08-03 211240.png": ("dict_alternate_leaves.png", ["alternate leaves"]),
    "Screenshot 2026-08-03 211254.png": ("dict_altitude.png", ["altitude", "altitude of a triangle"]),
    "Screenshot 2026-08-03 211321.png": ("dict_amide.png", ["amide", "amides"]),
    "Screenshot 2026-08-03 211341.png": ("dict_ammonia.png", ["ammonia"]),
    "Screenshot 2026-08-03 211349.png": ("dict_ammeter.png", ["ammeter", "hot-wire ammeter"]),
    "Screenshot 2026-08-03 211401.png": ("dict_amplifier.png", ["amplifier", "single stage amplifier"]),
    "Screenshot 2026-08-03 211408.png": ("dict_amplexicaul.png", ["amplexicaul", "amplexicaul leaf"]),
    "Screenshot 2026-08-03 211416.png": ("dict_amplitude.png", ["amplitude"]),
    "Screenshot 2026-08-03 211426.png": ("dict_analogue_to_digital_converter.png", ["analogue-to-digital converter", "adc"]),
    "Screenshot 2026-08-03 211439.png": ("dict_and_gate.png", ["and gate", "truth table"]),
    "Screenshot 2026-08-03 211510.png": ("dict_angle.png", ["angle"]),
    "Screenshot 2026-08-03 211525.png": ("dict_angle_of_depression.png", ["angle of depression"]),
    "Screenshot 2026-08-03 211534.png": ("dict_angle_of_deviation.png", ["angle of deviation"]),
    "Screenshot 2026-08-03 211544.png": ("dict_angle_between_two_vectors.png", ["angle between two vectors"]),
    "Screenshot 2026-08-03 211552.png": ("dict_angle_of_elevation.png", ["angle of elevation"]),
    "Screenshot 2026-08-03 211605.png": ("dict_animal_husbandry.png", ["animal husbandry"]),
    "Screenshot 2026-08-03 211627.png": ("dict_anomalous_expansion_of_water.png", ["anomalous expansion of water"]),
    "Screenshot 2026-08-03 211638.png": ("dict_anomer.png", ["anomer", "anomers"]),
    "Screenshot 2026-08-03 211647.png": ("dict_antheridium.png", ["antheridium", "antheridia"]),
    "Screenshot 2026-08-03 211654.png": ("dict_anthocarp.png", ["anthocarp"]),
    "Screenshot 2026-08-03 211704.png": ("dict_antimagic_square.png", ["antimagic square", "anti magic square"]),
    "Screenshot 2026-08-03 211715.png": ("dict_antinode.png", ["antinode"]),
    "Screenshot 2026-08-03 211725.png": ("dict_antipodal_cell.png", ["antipodal cell", "antipodal"]),
    "Screenshot 2026-08-03 211739.png": ("dict_apollonius_circle.png", ["apollonius circle", "apollonius' circle"]),
    "Screenshot 2026-08-03 211748.png": ("dict_apothem.png", ["apothem"]),
    "Screenshot 2026-08-03 211759.png": ("dict_arc.png", ["arc", "arc of a circle"]),
    "Screenshot 2026-08-03 211810.png": ("dict_archimedean_spiral.png", ["archimedean spiral"]),
    "Screenshot 2026-08-03 211822.png": ("dict_argand_diagram.png", ["argand diagram"]),
    "Screenshot 2026-08-03 211828.png": ("dict_argument.png", ["argument", "argument of a complex number"]),
    "Screenshot 2026-08-03 211841.png": ("dict_artery.png", ["artery"]),
    "Screenshot 2026-08-03 211854.png": ("dict_aspirin.png", ["aspirin"]),
    "Screenshot 2026-08-03 211904.png": ("dict_ascorbic_acid.png", ["ascorbic acid"]),
    "Screenshot 2026-08-03 211914.png": ("dict_aspartame.png", ["aspartame"]),
    "Screenshot 2026-08-03 211921.png": ("dict_aspartic_acid.png", ["aspartic acid"]),
    "Screenshot 2026-08-03 211932.png": ("dict_astronomical_telescope.png", ["astronomical telescope"]),
    "Screenshot 2026-08-03 212055.png": ("dict_asymptote.png", ["asymptote"]),
    "Screenshot 2026-08-03 212355.png": ("dict_normal_curve.png", ["normal curve"]),
    "Screenshot 2026-08-03 212421.png": ("dict_atomic_weight.png", ["atomic weight", "atomic mass"]),
    "Screenshot 2026-08-03 212447.png": ("dict_atropine.png", ["atropine"]),
    "Screenshot 2026-08-03 212456.png": ("dict_auricle.png", ["auricle"]),
    "Screenshot 2026-08-03 212506.png": ("dict_autotransformer.png", ["autotransformer"]),
    "Screenshot 2026-08-03 212515.png": ("dict_auxin.png", ["auxin", "indole-3-acetic acid"]),
    "Screenshot 2026-08-03 212523.png": ("dict_awn.png", ["awn"]),
    "Screenshot 2026-08-03 212536.png": ("dict_axis_of_symmetry.png", ["axis of symmetry"]),
    "Screenshot 2026-08-03 212543.png": ("dict_axis.png", ["axis", "axis vertebra"]),
    "Screenshot 2026-08-03 212555.png": ("dict_baermann_funnel.png", ["baermann funnel"]),
    "Screenshot 2026-08-03 212602.png": ("dict_beam_balance.png", ["beam balance"]),
    "Screenshot 2026-08-03 212642.png": ("dict_bar_chart.png", ["bar chart", "bar graph"]),
    "Screenshot 2026-08-03 212657.png": ("dict_barbiturate.png", ["barbiturate"]),
    "Screenshot 2026-08-03 212704.png": ("dict_barometer.png", ["barometer", "mercury barometer"]),
    "Screenshot 2026-08-03 212712.png": ("dict_baryon_number.png", ["baryon number"]),
    "Screenshot 2026-08-03 212726.png": ("dict_basal_placentation.png", ["basal placentation"]),
    "Screenshot 2026-08-03 212741.png": ("dict_base_station_system.png", ["base station system"]),
    "Screenshot 2026-08-03 212749.png": ("dict_base_pairing.png", ["base pairing", "base pair"]),
    "Screenshot 2026-08-03 212811.png": ("dict_beam_of_light.png", ["beam of light", "categories of rays"]),
    "Screenshot 2026-08-03 212827.png": ("dict_bell_curve.png", ["bell curve"]),
    "Screenshot 2026-08-03 212834.png": ("dict_bell_jar.png", ["bell jar"]),
    "Screenshot 2026-08-03 213041.png": ("dict_butene.png", ["butene", "1-butene"]),
    "Screenshot 2026-08-03 213048.png": ("dict_isobutanol.png", ["isobutanol", "2-methyl-1-propanol"]),
    "Screenshot 2026-08-03 213056.png": ("dict_butane.png", ["butane", "n-butane", "isobutane"]),
    "Screenshot 2026-08-03 213108.png": ("dict_burdizzo_castrator.png", ["burdizzo castrator", "burdizzo"]),
    "Screenshot 2026-08-03 213114.png": ("dict_bunsen_burner.png", ["bunsen burner"]),
    "Screenshot 2026-08-03 213126.png": ("dict_bundle_scar.png", ["bundle scar"]),
    "Screenshot 2026-08-03 213138.png": ("dict_budding.png", ["budding"]),
    "Screenshot 2026-08-03 213154.png": ("dict_bulbel.png", ["bulbel"]),
    "Screenshot 2026-08-03 213212.png": ("dict_bud_scale.png", ["bud scale", "bud scales"]),
    "Screenshot 2026-08-03 213223.png": ("dict_bubble_chamber.png", ["bubble chamber"]),
    "Screenshot 2026-08-03 213233.png": ("dict_buchner_funnel.png", ["buchner funnel", "buchner flask"]),
    "Screenshot 2026-08-03 213302.png": ("dict_bromothymol_blue.png", ["bromothymol blue"]),
    "Screenshot 2026-08-03 213320.png": ("dict_brewsters_law.png", ["brewster's law", "brewsters law"]),
    "Screenshot 2026-08-03 213426.png": ("dict_bridge_rectifier.png", ["bridge rectifier"]),
    "Screenshot 2026-08-03 213437.png": ("dict_bremsstrahlung.png", ["bremsstrahlung"]),
    "Screenshot 2026-08-03 213451.png": ("dict_box_and_whisker_plot.png", ["box and whisker plot", "box-and-whisker-plot", "box plot"]),
    "Screenshot 2026-08-03 213502.png": ("dict_born_haber_cycle.png", ["born-haber cycle", "born haber cycle"]),
    "Screenshot 2026-08-03 213609.png": ("dict_borane.png", ["borane"]),
    "Screenshot 2026-08-03 213616.png": ("dict_bone.png", ["bone", "microscopic structure of bone"]),
    "Screenshot 2026-08-03 213622.png": ("dict_bomb_calorimeter.png", ["bomb calorimeter"]),
    "Screenshot 2026-08-03 213630.png": ("dict_boiling_point_composition_diagram.png", ["boiling point composition diagram"]),
    "Screenshot 2026-08-03 213641.png": ("dict_block_and_tackle.png", ["block and tackle"]),
    "Screenshot 2026-08-03 213651.png": ("dict_blastodisc.png", ["blastodisc"]),
    "Screenshot 2026-08-03 213731.png": ("dict_blast_furnace.png", ["blast furnace"]),
    "Screenshot 2026-08-03 213759.png": ("dict_biternate.png", ["biternate leaves", "biternate"]),
    "Screenshot 2026-08-03 213808.png": ("dict_biserrate.png", ["biserrate leaf", "biserrate"]),
    "Screenshot 2026-08-03 213847.png": ("dict_bipolar_integrated_circuit.png", ["bipolar integrated circuit"]),
    "Screenshot 2026-08-03 213917.png": ("dict_bipinnate.png", ["bipinnate", "bipinnatifid"]),
    "Screenshot 2026-08-03 213926.png": ("dict_bipartite_leaf.png", ["bipartite leaf", "bipartite graph"]),
    "Screenshot 2026-08-03 213932.png": ("dict_biotin.png", ["biotin"]),
    "Screenshot 2026-08-03 214015.png": ("dict_bimetallic_strip.png", ["bimetallic strip"]),
    "Screenshot 2026-08-03 214026.png": ("dict_bilobed_stigma.png", ["bilobed stigma", "bilocular ovary"]),
    "Screenshot 2026-08-03 214038.png": ("dict_bimagic_square.png", ["bimagic square"]),
    "Screenshot 2026-08-03 214049.png": ("dict_bidentate_leaf.png", ["bidentate leaf", "bidentate"]),
    "Screenshot 2026-08-03 214101.png": ("dict_biconcave_lens.png", ["biconcave lens"]),
}

SRC_DIR = "section a-b images"
DEST_DIR = "diagrams"
MAP_JSON = "dictionary_diagrams_map.json"
DIAG_JS = "core_dictionary_diagrams.js"

def run():
    with open(MAP_JSON, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    added = []
    updated = []
    missing_src = []

    for src_name, (dest_name, keys) in ASSIGNMENTS.items():
        src_path = os.path.join(SRC_DIR, src_name)
        dest_path = os.path.join(DEST_DIR, dest_name)

        if not os.path.exists(src_path):
            missing_src.append(src_name)
            continue

        # Copy image file to diagrams directory
        shutil.copy2(src_path, dest_path)

        rel_dest = f"diagrams/{dest_name}"
        for key in keys:
            k = key.lower().strip()
            if k in diag_map:
                diag_map[k] = rel_dest
                updated.append(k)
            else:
                diag_map[k] = rel_dest
                added.append(k)

    # Sort dictionary map
    sorted_map = dict(sorted(diag_map.items()))
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    print(f"Saved {MAP_JSON} ({len(sorted_map)} total entries)")

    # Regenerate JS source of truth for frontend
    with open(DIAG_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")
    print(f"Regenerated {DIAG_JS}")

    print("=" * 60)
    print(f"  New keys added:      {len(added)}")
    print(f"  Existing keys updated: {len(updated)}")
    print(f"  Missing source files: {len(missing_src)}")

if __name__ == "__main__":
    run()
