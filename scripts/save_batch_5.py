import os, shutil, json

src_dir = r'c:\Users\Desmond\Desktop\final_osmosis\section a-b images'
out_dir = r'c:\Users\Desmond\Desktop\final_osmosis\diagrams'
map_json_path = r'c:\Users\Desmond\Desktop\final_osmosis\dictionary_diagrams_map.json'
core_js_path = r'c:\Users\Desmond\Desktop\final_osmosis\core_dictionary_diagrams.js'

def process_batch_5():
    batch_copies = [
        ('Screenshot 2026-08-03 211050.png', ['dict_aldosterone.png']),
        ('Screenshot 2026-08-03 211113.png', ['dict_algebraic_curve.png','dict_quadratic_curve.png']),
        ('Screenshot 2026-08-03 211140.png', ['dict_alimentary_canal.png','dict_alimentary_canal_human.png','dict_alimentary_canal_rabbit.png']),
        ('Screenshot 2026-08-03 211200.png', ['dict_allotrope.png','dict_allotrope_graphite.png','dict_allotrope_diamond.png','dict_graphite.png','dict_diamond.png']),
        ('Screenshot 2026-08-03 211219.png', ['dict_alloy.png']),
        ('Screenshot 2026-08-03 211232.png', ['dict_alternate_angles.png']),
        ('Screenshot 2026-08-03 211240.png', ['dict_alternate_leaves.png','dict_alternate_leaf_arrangement.png']),
        ('Screenshot 2026-08-03 211254.png', ['dict_altitude.png','dict_altitude_of_a_triangle.png']),
        ('Screenshot 2026-08-03 211321.png', ['dict_amide.png','dict_ethanamide.png','dict_methanamide.png','dict_primary_amide.png','dict_tertiary_amide.png']),
        ('Screenshot 2026-08-03 211341.png', ['dict_ammonia.png','dict_preparation_of_ammonia.png']),
        ('Screenshot 2026-08-03 211349.png', ['dict_ammeter.png','dict_hot_wire_ammeter.png']),
        ('Screenshot 2026-08-03 211401.png', ['dict_amplifier.png','dict_single_stage_amplifier.png']),
        ('Screenshot 2026-08-03 211408.png', ['dict_amplexicaul.png','dict_amplexicaul_leaf.png']),
        ('Screenshot 2026-08-03 211416.png', ['dict_amplitude.png']),
        ('Screenshot 2026-08-03 211426.png', ['dict_analogue_to_digital_converter.png','dict_adc.png']),
        ('Screenshot 2026-08-03 211439.png', ['dict_and_gate.png','dict_and_gate_truth_table.png']),
        ('Screenshot 2026-08-03 211510.png', ['dict_angle.png','dict_angle_in_radians.png']),
        ('Screenshot 2026-08-03 211525.png', ['dict_angle_of_depression.png']),
        ('Screenshot 2026-08-03 211534.png', ['dict_angle_of_deviation.png','dict_angle_of_minimum_deviation.png']),
        ('Screenshot 2026-08-03 211544.png', ['dict_angle_between_two_vectors.png']),
    ]
    print('=== Batch 5: Copying screenshots 41-60 into diagrams/ ===')
    for src_file, targets in batch_copies:
        src_path = os.path.join(src_dir, src_file)
        if not os.path.exists(src_path):
            print('  WARNING: Source not found: ' + src_path)
            continue
        for tgt in targets:
            tgt_path = os.path.join(out_dir, tgt)
            shutil.copy2(src_path, tgt_path)
            print('  Saved: ' + tgt + '  <-  ' + src_file)

    with open(map_json_path, 'r', encoding='utf-8') as f:
        diag_map = json.load(f)

    new_mappings = {
        'aldosterone': 'diagrams/dict_aldosterone.png',
        'algebraic curve': 'diagrams/dict_algebraic_curve.png',
        'quadratic curve': 'diagrams/dict_quadratic_curve.png',
        'alimentary canal': 'diagrams/dict_alimentary_canal.png',
        'alimentary canal (human)': 'diagrams/dict_alimentary_canal_human.png',
        'alimentary canal (rabbit)': 'diagrams/dict_alimentary_canal_rabbit.png',
        'allotrope': 'diagrams/dict_allotrope.png',
        'allotrope of graphite': 'diagrams/dict_allotrope_graphite.png',
        'allotrope of diamond': 'diagrams/dict_allotrope_diamond.png',
        'graphite': 'diagrams/dict_graphite.png',
        'diamond': 'diagrams/dict_diamond.png',
        'alloy': 'diagrams/dict_alloy.png',
        'alternate angles': 'diagrams/dict_alternate_angles.png',
        'alternate leaves': 'diagrams/dict_alternate_leaves.png',
        'alternate leaf arrangement': 'diagrams/dict_alternate_leaf_arrangement.png',
        'altitude': 'diagrams/dict_altitude.png',
        'altitude of a triangle': 'diagrams/dict_altitude_of_a_triangle.png',
        'amide': 'diagrams/dict_amide.png',
        'ethanamide': 'diagrams/dict_ethanamide.png',
        'methanamide': 'diagrams/dict_methanamide.png',
        'primary amide': 'diagrams/dict_primary_amide.png',
        'tertiary amide': 'diagrams/dict_tertiary_amide.png',
        'ammonia': 'diagrams/dict_ammonia.png',
        'preparation of ammonia': 'diagrams/dict_preparation_of_ammonia.png',
        'ammeter': 'diagrams/dict_ammeter.png',
        'hot-wire ammeter': 'diagrams/dict_hot_wire_ammeter.png',
        'amplifier': 'diagrams/dict_amplifier.png',
        'single stage amplifier': 'diagrams/dict_single_stage_amplifier.png',
        'amplexicaul': 'diagrams/dict_amplexicaul.png',
        'amplexicaul leaf': 'diagrams/dict_amplexicaul_leaf.png',
        'amplitude': 'diagrams/dict_amplitude.png',
        'analogue-to-digital converter': 'diagrams/dict_analogue_to_digital_converter.png',
        'analogue to digital converter': 'diagrams/dict_analogue_to_digital_converter.png',
        'adc': 'diagrams/dict_adc.png',
        'and gate': 'diagrams/dict_and_gate.png',
        'angle': 'diagrams/dict_angle.png',
        'angle in radians': 'diagrams/dict_angle_in_radians.png',
        'angle of depression': 'diagrams/dict_angle_of_depression.png',
        'angle of deviation': 'diagrams/dict_angle_of_deviation.png',
        'angle of minimum deviation': 'diagrams/dict_angle_of_minimum_deviation.png',
        'angle between two vectors': 'diagrams/dict_angle_between_two_vectors.png',
    }
    diag_map.update(new_mappings)
    sorted_map = {k: diag_map[k] for k in sorted(diag_map.keys())}
    with open(map_json_path, 'w', encoding='utf-8') as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    total = len(sorted_map)
    print('Updated dictionary_diagrams_map.json - total entries: ' + str(total))
    js_content = '// core_dictionary_diagrams.js (Audited STEM Diagram Mappings)\n\nvar DictionaryDiagrams = ' + json.dumps(sorted_map, indent=4, ensure_ascii=False) + ';\n'
    with open(core_js_path, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print('Updated core_dictionary_diagrams.js')
    print('=== Batch 5 complete! ===')

if __name__ == '__main__':
    process_batch_5()
