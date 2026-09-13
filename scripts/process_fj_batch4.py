"""
process_fj_batch4.py  —  Processes F-J Diagrams Batch 4 (Screenshots 76-111)
"""
import os, json, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')

SRC_DIR      = 'f-j diagrams'
DIAGRAMS_DIR = 'diagrams'
MAP_JSON     = 'dictionary_diagrams_map.json'
DIAGRAMS_JS  = 'core_dictionary_diagrams.js'

BATCH = [
    ('Screenshot_11-9-2026_155335_.jpeg','dict_hyperbola.png',
     ['hyperbola','hyperbola on cartesian plane','transverse axis','conjugate axis']),
    ('Screenshot_11-9-2026_155354_.jpeg','dict_hyperopia.png',
     ['hyperopia','long sightedness','hyperopia (long sightedness)','long-sightedness','longsightedness']),
    ('Screenshot_11-9-2026_155414_.jpeg','dict_hypocycloid.png',
     ['hypocycloid']),
    ('Screenshot_11-9-2026_155431_.jpeg','dict_hypsometer.png',
     ['hypsometer']),
    ('Screenshot_11-9-2026_155437_.jpeg','dict_hysteresis_loop.png',
     ['hysteresis loop','hysteresis','magnetic hysteresis']),
    ('Screenshot_11-9-2026_155457_.jpeg','dict_ice_point.png',
     ['ice point','lower fixed point','ice point thermometer']),
    ('Screenshot_11-9-2026_155515_.jpeg','dict_imine.png',
     ['imine','chemical structure of imine']),
    ('Screenshot_11-9-2026_155524_.jpeg','dict_imide.png',
     ['imide','linear imide','imide functional group']),
    ('Screenshot_11-9-2026_155547_.jpeg','dict_incircle.png',
     ['incircle','incircle of a triangle','inscribed circle']),
    ('Screenshot_11-9-2026_155557_.jpeg','dict_inclined_plane.png',
     ['inclined plane','forces on an inclined plane']),
    ('Screenshot_11-9-2026_155610_.jpeg','dict_inclusive_disjunction.png',
     ['inclusive disjunction','disjunction','truth table of inclusive disjunction']),
    ('Screenshot_11-9-2026_155621_.jpeg','dict_incus.png',
     ['incus','anvil','anvil (incus)','incus of the ear','ossicles']),
    ('Screenshot_11-9-2026_155632_.jpeg','dict_indeterminate_flowers.png',
     ['indeterminate','indeterminate flowers','indeterminate inflorescence']),
    ('Screenshot_11-9-2026_155644_.jpeg','dict_indole.png',
     ['indole','structure of indole']),
    ('Screenshot_11-9-2026_155716_.jpeg','dict_inflated.png',
     ['inflated','inflated fruit']),
    ('Screenshot_11-9-2026_155736_.jpeg','dict_initial_side_of_an_angle.png',
     ['initial side','initial side of an angle']),
    ('Screenshot_11-9-2026_15580_.jpeg','dict_innominate_bone.png',
     ['innominate bone','hip bone','ilium','ischium','pubis','acetabulum']),
    ('Screenshot_11-9-2026_155818_.jpeg','dict_inscribed_circle.png',
     ['inscribed circle','inscribed circle in a triangle']),
    ('Screenshot_11-9-2026_155827_.jpeg','dict_inositol.png',
     ['inositol','chemical structure of inositol']),
    ('Screenshot_11-9-2026_155849_.jpeg','dict_insertion_reaction.png',
     ['insertion reaction','beckmann rearrangement','caprolactam']),
    ('Screenshot_11-9-2026_15599_.jpeg','dict_igfet.png',
     ['igfet','mosfet','insulated gate field-effect transistor','insulated gate fet']),
    ('Screenshot_11-9-2026_16034_.jpeg','dict_interference_fringes.png',
     ['interference fringes','interference','formation of interference fringes']),
    ('Screenshot_11-9-2026_1603_.jpeg','dict_integral.png',
     ['integral','integration','definite integral','area under curve']),
    ('Screenshot_11-9-2026_16052_.jpeg','dict_interior_angle.png',
     ['interior angle','interior angles','co-interior angles']),
    ('Screenshot_11-9-2026_16059_.jpeg','dict_interior_angle_transversal.png',
     ['interior angles transversal','alternate interior angles']),
    ('Screenshot_11-9-2026_16119_.jpeg','dict_internal_division.png',
     ['internal division','external division','section formula']),
    ('Screenshot_11-9-2026_16215_.jpeg','dict_introrse.png',
     ['introrse','introrse anther']),
    ('Screenshot_11-9-2026_16227_.jpeg','dict_intrinsic_semiconductor.png',
     ['intrinsic semiconductor','intrinsic semi conductor','semiconductor energy band']),
    ('Screenshot_11-9-2026_16326_.jpeg','dict_involute_leaf.png',
     ['involute','involute leaf']),
    ('Screenshot_11-9-2026_1637_.jpeg','dict_involucre.png',
     ['involucre','involucral bract']),
    ('Screenshot_11-9-2026_16417_.jpeg','dict_isosceles_triangle.png',
     ['isosceles triangle']),
    ('Screenshot_11-9-2026_16442_.jpeg','dict_jahn_teller_effect.png',
     ['jahn-teller effect','jahn teller effect','jahn-teller distortion']),
    ('Screenshot_11-9-2026_16455_.jpeg','dict_jet_engine.png',
     ['jet engine','jet propulsion']),
    ('Screenshot_11-9-2026_1648_.jpeg','dict_isoprene.png',
     ['isoprene','2-methylbuta-1,3-diene','chemical structure of isoprene']),
    ('Screenshot_11-9-2026_16524_.jpeg','dict_jgfet.png',
     ['jgfet','junction gate field-effect transistor','junction fet','jfet']),
    ('Screenshot_11-9-2026_1652_.jpeg','dict_synovial_joint.png',
     ['synovial joint','synovial membrane','synovial fluid','movable joint','shoulder joint','ball and socket joint']),
]

os.makedirs(DIAGRAMS_DIR, exist_ok=True)
with open(MAP_JSON, encoding='utf-8') as f:
    diag_map = json.load(f)

copied=0
for src_name, dest_name, terms in BATCH:
    src_path = os.path.join(SRC_DIR, src_name)
    dest_path = os.path.join(DIAGRAMS_DIR, dest_name)
    rel_path = f'diagrams/{dest_name}'
    if not os.path.exists(src_path):
        print(f'  MISSING: {src_path}')
        continue
    shutil.copy2(src_path, dest_path)
    size_kb = os.path.getsize(dest_path)/1024
    print(f'  OK  {dest_name}  ({size_kb:.1f} KB)')
    copied += 1
    for term in terms:
        diag_map[term.lower().strip()] = rel_path

print(f'\nCopied: {copied}/{len(BATCH)}')
diag_map_sorted = dict(sorted(diag_map.items()))
with open(MAP_JSON,'w',encoding='utf-8') as f:
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
print(f'Saved {MAP_JSON} ({len(diag_map_sorted)} entries)')

with open(DIAGRAMS_JS,'w',encoding='utf-8') as f:
    f.write('// core_dictionary_diagrams.js — Auto-generated. DO NOT EDIT MANUALLY.\n')
    f.write('// Last updated: F-J Batch 4 (screenshots 76-111)\n\n')
    f.write('var DictionaryDiagrams = ')
    json.dump(diag_map_sorted, f, indent=2, ensure_ascii=False)
    f.write(';\n\nif (typeof module !== "undefined") { module.exports = DictionaryDiagrams; }\n')
print(f'Regenerated {DIAGRAMS_JS}')
