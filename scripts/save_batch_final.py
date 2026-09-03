import os, shutil, json, tempfile

src_dir = r'c:\Users\Desmond\Desktop\final_osmosis\section a-b images'
out_dir = r'c:\Users\Desmond\Desktop\final_osmosis\diagrams'
map_json_path = r'c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json'
core_js_path = r'c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js'
backup_path = map_json_path + '.bak'

batch = [
    ('Screenshot 2026-08-03 211552.png', ['dict_angle_of_elevation.png']),
    ('Screenshot 2026-08-03 211605.png', ['dict_animal_husbandry.png','dict_cow_external_features.png','dict_goat_external_features.png','dict_pig_external_features.png']),
    ('Screenshot 2026-08-03 211627.png', ['dict_anomalous_expansion_of_water.png']),
    ('Screenshot 2026-08-03 211638.png', ['dict_anomer.png','dict_alpha_glucose.png','dict_beta_glucose.png']),
    ('Screenshot 2026-08-03 211647.png', ['dict_antheridia_of_moss.png','dict_antheridium.png']),
    ('Screenshot 2026-08-03 211654.png', ['dict_anthocarp.png','dict_anthocarp_of_fruit.png']),
    ('Screenshot 2026-08-03 211704.png', ['dict_anti_magic_square.png']),
    ('Screenshot 2026-08-03 211715.png', ['dict_antinode.png','dict_node.png','dict_standing_wave.png']),
    ('Screenshot 2026-08-03 211725.png', ['dict_antipodal_cell.png']),
    ('Screenshot 2026-08-03 211739.png', ['dict_apollonius_circle.png']),
    ('Screenshot 2026-08-03 211748.png', ['dict_apothem.png']),
    ('Screenshot 2026-08-03 211759.png', ['dict_arc.png','dict_arc_of_a_circle.png']),
    ('Screenshot 2026-08-03 211810.png', ['dict_archimedean_spiral.png']),
    ('Screenshot 2026-08-03 211822.png', ['dict_argand_diagram.png']),
    ('Screenshot 2026-08-03 211828.png', ['dict_argument_of_a_complex_number.png']),
    ('Screenshot 2026-08-03 211841.png', ['dict_artery.png','dict_structure_of_an_artery.png']),
    ('Screenshot 2026-08-03 211854.png', ['dict_aspirin.png']),
    ('Screenshot 2026-08-03 211904.png', ['dict_ascorbic_acid.png','dict_vitamin_c.png']),
    ('Screenshot 2026-08-03 211914.png', ['dict_aspartame.png']),
    ('Screenshot 2026-08-03 211921.png', ['dict_aspartic_acid.png']),
    ('Screenshot 2026-08-03 211932.png', ['dict_astronomical_telescope.png','dict_astronomical_telescope_near_point.png','dict_astronomical_telescope_infinity.png']),
    ('Screenshot 2026-08-03 212055.png', ['dict_asymptote.png']),
    ('Screenshot 2026-08-03 212355.png', ['dict_normal_curve.png','dict_bell_curve.png']),
    ('Screenshot 2026-08-03 212421.png', ['dict_atomic_weight_table.png','dict_atomic_mass_table.png','dict_periodic_table_weights.png']),
    ('Screenshot 2026-08-03 212447.png', ['dict_atropine.png']),
    ('Screenshot 2026-08-03 212456.png', ['dict_auricle_of_a_leaf.png']),
    ('Screenshot 2026-08-03 212506.png', ['dict_autotransformer.png']),
    ('Screenshot 2026-08-03 212515.png', ['dict_auxin.png','dict_indole_3_acetic_acid.png']),
    ('Screenshot 2026-08-03 212523.png', ['dict_awn_of_a_spikelet.png','dict_awn.png']),
    ('Screenshot 2026-08-03 212536.png', ['dict_axis_of_symmetry_parabola.png','dict_parabola_axis_of_symmetry.png']),
    ('Screenshot 2026-08-03 212543.png', ['dict_axis_vertebra.png']),
    ('Screenshot 2026-08-03 212555.png', ['dict_baermann_funnel.png']),
    ('Screenshot 2026-08-03 212602.png', ['dict_beam_balance.png']),
    ('Screenshot 2026-08-03 212642.png', ['dict_bar_chart.png','dict_bar_graph.png','dict_vertical_bar_chart.png','dict_horizontal_bar_chart.png']),
    ('Screenshot 2026-08-03 212657.png', ['dict_barbiturate.png']),
    ('Screenshot 2026-08-03 212704.png', ['dict_barometer.png','dict_mercury_barometer.png']),
    ('Screenshot 2026-08-03 212712.png', ['dict_baryon_number_table.png','dict_baryon.png']),
    ('Screenshot 2026-08-03 212726.png', ['dict_basal_placentation.png']),
    ('Screenshot 2026-08-03 212741.png', ['dict_base_station_system.png','dict_bss.png']),
    ('Screenshot 2026-08-03 212749.png', ['dict_base_pairing.png','dict_base_pairing_thymine_adenine.png','dict_base_pairing_cytosine_guanine.png']),
    ('Screenshot 2026-08-03 212811.png', ['dict_beam_of_rays.png','dict_parallel_rays.png','dict_convergent_rays.png','dict_divergent_rays.png']),
    ('Screenshot 2026-08-03 212827.png', ['dict_bell_curve_normal_distribution.png','dict_normal_distribution.png']),
    ('Screenshot 2026-08-03 212834.png', ['dict_bell_jar.png']),
    ('Screenshot 2026-08-03 213041.png', ['dict_butene.png','dict_1_butene.png','dict_trans_2_butene.png']),
    ('Screenshot 2026-08-03 213048.png', ['dict_isobutanol.png','dict_2_methyl_1_propanol.png']),
    ('Screenshot 2026-08-03 213056.png', ['dict_butane.png','dict_n_butane.png','dict_isobutane.png']),
    ('Screenshot 2026-08-03 213108.png', ['dict_burdizzo_castrator.png']),
    ('Screenshot 2026-08-03 213114.png', ['dict_bunsen_burner.png']),
    ('Screenshot 2026-08-03 213126.png', ['dict_bundle_scar.png']),
    ('Screenshot 2026-08-03 213138.png', ['dict_budding.png','dict_budding_in_flowering_plants.png','dict_budding_in_yeast.png','dict_budding_in_hydra.png']),
    ('Screenshot 2026-08-03 213154.png', ['dict_bulbel.png']),
    ('Screenshot 2026-08-03 213212.png', ['dict_bud_scales.png']),
    ('Screenshot 2026-08-03 213223.png', ['dict_bubble_chamber.png']),
    ('Screenshot 2026-08-03 213233.png', ['dict_buchner_funnel.png','dict_buchner_flask.png']),
    ('Screenshot 2026-08-03 213302.png', ['dict_bromothymol_blue.png']),
    ('Screenshot 2026-08-03 213320.png', ['dict_brewsters_law.png']),
    ('Screenshot 2026-08-03 213426.png', ['dict_bridge_rectifier.png']),
    ('Screenshot 2026-08-03 213437.png', ['dict_bremsstrahlung.png']),
    ('Screenshot 2026-08-03 213451.png', ['dict_box_and_whisker_plot.png','dict_box_plot.png']),
    ('Screenshot 2026-08-03 213502.png', ['dict_born_haber_cycle.png']),
    ('Screenshot 2026-08-03 213609.png', ['dict_borane.png']),
    ('Screenshot 2026-08-03 213616.png', ['dict_bone_microscopic_structure.png','dict_haversian_system.png']),
    ('Screenshot 2026-08-03 213622.png', ['dict_bomb_calorimeter.png']),
    ('Screenshot 2026-08-03 213630.png', ['dict_boiling_point_composition_diagram.png']),
    ('Screenshot 2026-08-03 213641.png', ['dict_block_and_tackle.png']),
    ('Screenshot 2026-08-03 213651.png', ['dict_blastodisc.png','dict_blastodisc_of_egg.png']),
    ('Screenshot 2026-08-03 213731.png', ['dict_blast_furnace.png']),
    ('Screenshot 2026-08-03 213759.png', ['dict_biternate_leaves.png']),
    ('Screenshot 2026-08-03 213808.png', ['dict_biserrate_leaf.png']),
    ('Screenshot 2026-08-03 213847.png', ['dict_bipolar_integrated_circuit.png']),
    ('Screenshot 2026-08-03 213917.png', ['dict_bipinnate_leaflets.png','dict_bipinnatifid_leaf.png']),
    ('Screenshot 2026-08-03 213926.png', ['dict_bipartite_leaf.png','dict_complete_bipartite_graph.png']),
    ('Screenshot 2026-08-03 213932.png', ['dict_biotin.png']),
    ('Screenshot 2026-08-03 214015.png', ['dict_bimetallic_strip.png','dict_bimetallic_strip_thermometer.png']),
    ('Screenshot 2026-08-03 214026.png', ['dict_bilobed_stigma.png','dict_bilocular_ovary.png']),
    ('Screenshot 2026-08-03 214038.png', ['dict_bimagic_square.png']),
    ('Screenshot 2026-08-03 214049.png', ['dict_bidentate_leaf.png']),
    ('Screenshot 2026-08-03 214101.png', ['dict_biconcave_lens.png']),
]

new_mappings = {
    'angle of elevation': 'diagrams/dict_angle_of_elevation.png',
    'animal husbandry': 'diagrams/dict_animal_husbandry.png',
    'cow external features': 'diagrams/dict_cow_external_features.png',
    'goat external features': 'diagrams/dict_goat_external_features.png',
    'pig external features': 'diagrams/dict_pig_external_features.png',
    'anomalous expansion of water': 'diagrams/dict_anomalous_expansion_of_water.png',
    'anomer': 'diagrams/dict_anomer.png',
    'alpha glucose': 'diagrams/dict_alpha_glucose.png',
    'beta glucose': 'diagrams/dict_beta_glucose.png',
    'antheridia of moss': 'diagrams/dict_antheridia_of_moss.png',
    'antheridium': 'diagrams/dict_antheridium.png',
    'anthocarp': 'diagrams/dict_anthocarp.png',
    'anthocarp of fruit': 'diagrams/dict_anthocarp_of_fruit.png',
    'anti-magic square': 'diagrams/dict_anti_magic_square.png',
    'antinode': 'diagrams/dict_antinode.png',
    'node': 'diagrams/dict_node.png',
    'standing wave': 'diagrams/dict_standing_wave.png',
    'antipodal cell': 'diagrams/dict_antipodal_cell.png',
    'apollonius circle': 'diagrams/dict_apollonius_circle.png',
    'apothem': 'diagrams/dict_apothem.png',
    'arc': 'diagrams/dict_arc.png',
    'arc of a circle': 'diagrams/dict_arc_of_a_circle.png',
    'archimedean spiral': 'diagrams/dict_archimedean_spiral.png',
    'argand diagram': 'diagrams/dict_argand_diagram.png',
    'argument of a complex number': 'diagrams/dict_argument_of_a_complex_number.png',
    'artery': 'diagrams/dict_artery.png',
    'structure of an artery': 'diagrams/dict_structure_of_an_artery.png',
    'aspirin': 'diagrams/dict_aspirin.png',
    'ascorbic acid': 'diagrams/dict_ascorbic_acid.png',
    'vitamin c': 'diagrams/dict_vitamin_c.png',
    'aspartame': 'diagrams/dict_aspartame.png',
    'aspartic acid': 'diagrams/dict_aspartic_acid.png',
    'astronomical telescope': 'diagrams/dict_astronomical_telescope.png',
    'astronomical telescope near point': 'diagrams/dict_astronomical_telescope_near_point.png',
    'astronomical telescope at infinity': 'diagrams/dict_astronomical_telescope_infinity.png',
    'asymptote': 'diagrams/dict_asymptote.png',
    'normal curve': 'diagrams/dict_normal_curve.png',
    'bell curve': 'diagrams/dict_bell_curve.png',
    'atomic weight table': 'diagrams/dict_atomic_weight_table.png',
    'atomic mass table': 'diagrams/dict_atomic_mass_table.png',
    'atropine': 'diagrams/dict_atropine.png',
    'auricle of a leaf': 'diagrams/dict_auricle_of_a_leaf.png',
    'autotransformer': 'diagrams/dict_autotransformer.png',
    'auxin': 'diagrams/dict_auxin.png',
    'indole-3-acetic acid': 'diagrams/dict_indole_3_acetic_acid.png',
    'awn': 'diagrams/dict_awn.png',
    'awn of a spikelet': 'diagrams/dict_awn_of_a_spikelet.png',
    'axis of symmetry of a parabola': 'diagrams/dict_axis_of_symmetry_parabola.png',
    'axis vertebra': 'diagrams/dict_axis_vertebra.png',
    'baermann funnel': 'diagrams/dict_baermann_funnel.png',
    'beam balance': 'diagrams/dict_beam_balance.png',
    'bar chart': 'diagrams/dict_bar_chart.png',
    'bar graph': 'diagrams/dict_bar_graph.png',
    'vertical bar chart': 'diagrams/dict_vertical_bar_chart.png',
    'horizontal bar chart': 'diagrams/dict_horizontal_bar_chart.png',
    'barbiturate': 'diagrams/dict_barbiturate.png',
    'barometer': 'diagrams/dict_barometer.png',
    'mercury barometer': 'diagrams/dict_mercury_barometer.png',
    'baryon number table': 'diagrams/dict_baryon_number_table.png',
    'baryon': 'diagrams/dict_baryon.png',
    'basal placentation': 'diagrams/dict_basal_placentation.png',
    'base station system': 'diagrams/dict_base_station_system.png',
    'bss': 'diagrams/dict_bss.png',
    'base pairing': 'diagrams/dict_base_pairing.png',
    'base pairing thymine adenine': 'diagrams/dict_base_pairing_thymine_adenine.png',
    'base pairing cytosine guanine': 'diagrams/dict_base_pairing_cytosine_guanine.png',
    'beam of rays': 'diagrams/dict_beam_of_rays.png',
    'parallel rays': 'diagrams/dict_parallel_rays.png',
    'convergent rays': 'diagrams/dict_convergent_rays.png',
    'divergent rays': 'diagrams/dict_divergent_rays.png',
    'bell curve normal distribution': 'diagrams/dict_bell_curve_normal_distribution.png',
    'normal distribution': 'diagrams/dict_normal_distribution.png',
    'bell jar': 'diagrams/dict_bell_jar.png',
    'butene': 'diagrams/dict_butene.png',
    '1-butene': 'diagrams/dict_1_butene.png',
    'trans-2-butene': 'diagrams/dict_trans_2_butene.png',
    'isobutanol': 'diagrams/dict_isobutanol.png',
    '2-methyl-1-propanol': 'diagrams/dict_2_methyl_1_propanol.png',
    'butane': 'diagrams/dict_butane.png',
    'n-butane': 'diagrams/dict_n_butane.png',
    'isobutane': 'diagrams/dict_isobutane.png',
    'burdizzo castrator': 'diagrams/dict_burdizzo_castrator.png',
    'bunsen burner': 'diagrams/dict_bunsen_burner.png',
    'bundle scar': 'diagrams/dict_bundle_scar.png',
    'budding': 'diagrams/dict_budding.png',
    'budding in flowering plants': 'diagrams/dict_budding_in_flowering_plants.png',
    'budding in yeast': 'diagrams/dict_budding_in_yeast.png',
    'budding in hydra': 'diagrams/dict_budding_in_hydra.png',
    'bulbel': 'diagrams/dict_bulbel.png',
    'bud scales': 'diagrams/dict_bud_scales.png',
    'bubble chamber': 'diagrams/dict_bubble_chamber.png',
    'buchner funnel': 'diagrams/dict_buchner_funnel.png',
    'buchner flask': 'diagrams/dict_buchner_flask.png',
    'bromothymol blue': 'diagrams/dict_bromothymol_blue.png',
    'brewsters law': 'diagrams/dict_brewsters_law.png',
    'bridge rectifier': 'diagrams/dict_bridge_rectifier.png',
    'bremsstrahlung': 'diagrams/dict_bremsstrahlung.png',
    'box-and-whisker plot': 'diagrams/dict_box_and_whisker_plot.png',
    'box plot': 'diagrams/dict_box_plot.png',
    'born-haber cycle': 'diagrams/dict_born_haber_cycle.png',
    'borane': 'diagrams/dict_borane.png',
    'bone microscopic structure': 'diagrams/dict_bone_microscopic_structure.png',
    'haversian system': 'diagrams/dict_haversian_system.png',
    'bomb calorimeter': 'diagrams/dict_bomb_calorimeter.png',
    'boiling point composition diagram': 'diagrams/dict_boiling_point_composition_diagram.png',
    'block and tackle': 'diagrams/dict_block_and_tackle.png',
    'blastodisc': 'diagrams/dict_blastodisc.png',
    'blastodisc of egg': 'diagrams/dict_blastodisc_of_egg.png',
    'blast furnace': 'diagrams/dict_blast_furnace.png',
    'biternate leaves': 'diagrams/dict_biternate_leaves.png',
    'biserrate leaf': 'diagrams/dict_biserrate_leaf.png',
    'bipolar integrated circuit': 'diagrams/dict_bipolar_integrated_circuit.png',
    'bipinnate leaflets': 'diagrams/dict_bipinnate_leaflets.png',
    'bipinnatifid leaf': 'diagrams/dict_bipinnatifid_leaf.png',
    'bipartite leaf': 'diagrams/dict_bipartite_leaf.png',
    'complete bipartite graph': 'diagrams/dict_complete_bipartite_graph.png',
    'biotin': 'diagrams/dict_biotin.png',
    'bimetallic strip': 'diagrams/dict_bimetallic_strip.png',
    'bimetallic strip thermometer': 'diagrams/dict_bimetallic_strip_thermometer.png',
    'bilobed stigma': 'diagrams/dict_bilobed_stigma.png',
    'bilocular ovary': 'diagrams/dict_bilocular_ovary.png',
    'bimagic square': 'diagrams/dict_bimagic_square.png',
    'bidentate leaf': 'diagrams/dict_bidentate_leaf.png',
    'biconcave lens': 'diagrams/dict_biconcave_lens.png',
}

print('=== Final Batch: Copying screenshots 61-138 into diagrams/ ===')
missing = []
for src_file, targets in batch:
    src_path = os.path.join(src_dir, src_file)
    if not os.path.exists(src_path):
        missing.append(src_file)
        print('  WARNING: Source not found: ' + src_file)
        continue
    for tgt in targets:
        tgt_path = os.path.join(out_dir, tgt)
        shutil.copy2(src_path, tgt_path)
        print('  Saved: ' + tgt)

if missing:
    print('MISSING FILES: ' + str(missing))
    print('Aborting JSON update to protect existing data.')
    exit(1)

# SAFETY: backup existing map
shutil.copy2(map_json_path, backup_path)
print('Backup created: dictionary_diagrams_map.json.bak')

# Load existing
with open(map_json_path, 'r', encoding='utf-8') as f:
    diag_map = json.load(f)

diag_map.update(new_mappings)
sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}

# SAFETY: write to temp file first, verify it loads cleanly
tmp_path = map_json_path + '.tmp'
with open(tmp_path, 'w', encoding='utf-8') as f:
    json.dump(sorted_map, f, indent=4, ensure_ascii=False)

with open(tmp_path, 'r', encoding='utf-8') as f:
    verify = json.load(f)
assert len(verify) == len(sorted_map), 'Verification failed: entry count mismatch!'
print('Verification passed: ' + str(len(verify)) + ' entries')

# Replace real file
os.replace(tmp_path, map_json_path)
print('Updated dictionary_diagrams_map.json - total entries: ' + str(len(sorted_map)))

js_content = '// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = ' + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ';\n'
with open(core_js_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print('Updated core_dictionary_diagrams.js')
print('=== All done! Final batch complete! ===')
