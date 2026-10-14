# STEM Dictionary Diagram Mapping & Batch Processing Guide

This document records the exact procedure used to map, crop, verify, and integrate user-captured textbook screenshots into the Osmosis Game engine.

---

## 1. Why This Workflow Outperforms OCR & Generic AI Studio
- **Complete Labels**: Previous automated vector/OCR scripts chopped off labels (e.g. cutting off *Centrum*, *Neural spine* on vertebrae). User screenshots contain full, pristine labels.
- **Zero Hallucination / Drift**: AI Studio web uploads often hallucinate bounding boxes or swap file paths (e.g. assigning a lens aberration diagram to *abomasum*).
- **Direct Dictionary Verification**: Every extracted caption is verified 1:1 against valid entries in `dictionary.json`.

---

## 2. Standard 5-Step Batch Workflow

```mermaid
graph LR
    A[Visual Inspection] --> B[Dictionary Verification]
    B --> C[Clean & Split Cropping]
    C --> D[Save to diagrams/]
    D --> E[Update JSON & JS Maps]
```

1. **Visual Inspection**:
   - Inspect screenshot using high-resolution vision.
   - Read diagram title, subfigure captions (Fig 1, Fig 2), and key labels.
2. **Dictionary Cross-Reference**:
   - Match caption to canonical headwords, raw headwords, and synonyms in `dictionary.json`.
3. **Precision Crop & Multi-Figure Splitting**:
   - Strip textbook horizontal rule lines from top/bottom borders.
   - When a screenshot contains multiple figures (e.g., Astigmatism + Distortion), split them into separate images so each dictionary term gets its own dedicated, focused visual.
4. **Standardized Image Output**:
   - Save high-quality PNGs to `diagrams/dict_<headword>.png`.
5. **Atomic Mapping Updates**:
   - Update `dictionary_diagrams_map.json`.
   - Update `core_dictionary_diagrams.js` (`var DictionaryDiagrams = { ... }`).

---

## 3. Batch Tracking

### Batch 1 (Completed) — Screenshots 1 to 10
Source Folder: `section a-b images/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot 2026-08-03 161441.png` | Axis vertebra of a mammal (Lateral & Anterior) | `dict_axis_vertebra.png` | `axis`, `axis vertebra` |
| 2 | `Screenshot 2026-08-03 161817.png` | Chemical Structure of Azo Dye | `dict_azo_compound.png`, `dict_azo_dye.png` | `azo compound`, `azo dye` |
| 3 | `Screenshot 2026-08-03 161835.png` | Parabola with line of symmetry & equation | `dict_axis_of_symmetry.png` | `axis of symmetry` |
| 4 | `Screenshot 2026-08-03 162009.png` | Fig 1: Astigmatism / Fig II: Distortion | `dict_astigmatism.png`, `dict_distortion.png` | `astigmatism`, `distortion`, `distortion aberration` |
| 5 | `Screenshot 2026-08-03 162107.png` | Fig III: Chromatic / Fig IV & V: Spherical | `dict_chromatic_aberration.png`, `dict_spherical_aberration.png`, `dict_aberration.png` | `aberration`, `chromatic aberration`, `spherical aberration` |
| 6 | `Screenshot 2026-08-03 162120.png` | Fig VI: Blue light focus vs Red light focus | `dict_chromatic_aberration_focus.png` | `chromatic aberration` |
| 7 | `Screenshot 2026-08-03 162141.png` | ABO Blood Group System Table | `dict_abo_blood_group_system.png`, `dict_abo_blood_group.png` | `abo blood group system`, `blood group` |
| 8 | `Screenshot 2026-08-03 162157.png` | Abomasum (true stomach) of a cow | `dict_abomasum.png`, `dict_abomasum_true_stomach.png` | `abomasum`, `abomasum (true stomach)` |
| 9 | `Screenshot 2026-08-03 162218.png` | Line absorption spectrum setup | `dict_absorption_spectrum.png` | `absorption spectrum` |
| 10 | `Screenshot 2026-08-03 162233.png` | Instantaneous Acceleration Graph (v-t curve) | `dict_acceleration_time_graph.png`, `dict_instantaneous_acceleration.png` | `acceleration`, `acceleration-time-graph`, `instantaneous acceleration` |

---

### Batch 2 (Completed) — Screenshots 11 to 20
Source Folder: `section a-b images/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 11 | `Screenshot 2026-08-03 162247.png` | Constant Acceleration-Time Graph | `dict_acceleration_time_graph_constant.png`, `dict_acceleration_time_graph.png` | `acceleration-time graph`, `acceleration time graph` |
| 12 | `Screenshot 2026-08-03 162308.png` | Displacement vs t² graph | `dict_acceleration_due_to_gravity.png` | `acceleration due to gravity` |
| 13 | `Screenshot 2026-08-03 162326.png` | Base Station System (BSS) Architecture | `dict_base_station_system.png`, `dict_bss.png` | `base station system`, `base station system (bss)`, `bss`, `base station controller` |
| 14 | `Screenshot 2026-08-03 162355.png` | Chemical structure of acetanilide | `dict_acetanilide.png`, `dict_acetanilide_n_phenylethanamide.png` | `acetanilide`, `acetanilide (n-phenylethanamide)`, `n-phenylethanamide` |
| 15 | `Screenshot 2026-08-03 162409.png` | 2D molecular structure of acetaldehyde | `dict_acetaldehyde.png` | `acetaldehyde`, `ethanal` |
| 16 | `Screenshot 2026-08-03 162423.png` | Chemical structure of acetamide | `dict_acetamide.png`, `dict_acetamide_ethanamide.png` | `acetamide`, `acetamide (ethanamide)`, `ethanamide` |
| 17 | `Screenshot 2026-08-03 162440.png` | Chemical structure of acetylacetone (tautomers) | `dict_acetylacetone.png` | `acetylacetone`, `pentane-2,4-dione` |
| 18 | `Screenshot 2026-08-03 162453.png` | Chemical structure of acetophenone | `dict_acetophenone.png` | `acetophenone`, `phenylethanone` |
| 19 | `Screenshot 2026-08-03 162508.png` | Acetylation reaction (Pyruvate to Acetyl CoA) | `dict_acetylation.png`, `dict_acetylation_ethanoylation.png` | `acetylation`, `acetylation (ethanoylation)`, `ethanoylation` |
| 20 | `Screenshot 2026-08-03 162521.png` | Structure of acetylcholine (neurotransmitter) | `dict_acetylcholine.png`, `dict_acetylcholine_ach.png` | `acetylcholine`, `acetylcholine (ach)`, `ach` |

---

### Batch 3 & 4 (Completed) — Screenshots 21 to 40
Source Folder: `section a-b images/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 21 | `Screenshot 2026-08-03 162637.png` | Chemical structure of Acetyl-CoA | `dict_acetyl_coa.png`, `dict_acetyl_coenzyme_a_acetyl_coa.png` | `acetyl coenzyme a`, `acetyl-coa`, `acetyl coa` |
| 22 | `Screenshot 2026-08-03 162648.png` | Achromatic Lens | `dict_achromatic_lens.png`, `dict_achromat.png` | `achromatic lens`, `achromat` |
| 23 | `Screenshot 2026-08-03 162714.png` | Chemical Structure of Acid Anhydride | `dict_acid_anhydride.png` | `acid anhydride` |
| 24 | `Screenshot 2026-08-03 162725.png` | Chemical structure of acrylamide | `dict_acrylamide.png` | `acrylamide` |
| 25 | `Screenshot 2026-08-03 162733.png` | Chemical Structure of Acrylonitrile | `dict_acrylonitrile.png`, `dict_acrylonitrile_propenenitrile.png`, `dict_propenenitrile.png` | `acrylonitrile`, `propenenitrile`, `acrylic` |
| 26 | `Screenshot 2026-08-03 162744.png` | Activation energy / SN2 reaction coordinate | `dict_activation_energy.png`, `dict_reaction_coordinate.png`, `dict_transition_state.png` | `activation energy`, `reaction coordinate`, `transition state` |
| 27 | `Screenshot 2026-08-03 162804.png` | Activity Series of Metals in Aqueous Solution | `dict_activity_series.png`, `dict_reactivity_series.png`, `dict_electrochemical_series.png` | `activity series`, `reactivity series`, `electrochemical series` |
| 28 | `Screenshot 2026-08-03 162814.png` | Structure of an acuminate leaf | `dict_acuminate.png`, `dict_acuminate_leaf.png` | `acuminate`, `acuminate leaf` |
| 29 | `Screenshot 2026-08-03 162822.png` | Acute angle (54°) | `dict_acute_angle.png` | `acute angle` |
| 30 | `Screenshot 2026-08-03 162834.png` | Chemical Structure of Acyclovir | `dict_acyclovir.png` | `acyclovir` |
| 31 | `Screenshot 2026-08-03 162845.png` | Collisions from random frequency hopping | `dict_adaptive_frequency_hopping.png`, `dict_frequency_hopping.png` | `adaptive frequency hopping`, `frequency hopping` |
| 32 | `Screenshot 2026-08-03 162858.png` | Adaxial & Abaxial leaf surfaces | `dict_adaxial.png`, `dict_abaxial.png` | `adaxial`, `abaxial` |
| 33 | `Screenshot 2026-08-03 162910.png` | Addition of Vectors (Triangle law) | `dict_addition_of_vectors.png`, `dict_vector_addition.png` | `addition of vectors`, `vector addition` |
| 34 | `Screenshot 2026-08-03 162919.png` | Chemical Structure of Adenosine Triphosphate (ATP) | `dict_adenosine_triphosphate.png`, `dict_atp.png` | `adenosine triphosphate`, `adenosine triphosphate (atp)`, `atp` |
| 35 | `Screenshot 2026-08-03 162927.png` | Chemical Structure of Adipic Acid | `dict_adipic_acid.png`, `dict_hexanedioic_acid.png` | `adipic acid`, `hexanedioic acid` |
| 36 | `Screenshot 2026-08-03 162934.png` | Adipocyte (Fat Cell) anatomical cross-section | `dict_adipocyte.png`, `dict_adipocyte_fat_cell.png`, `dict_fat_cell.png` | `adipocyte`, `adipocyte (fat cell)`, `fat cell` |
| 37 | `Screenshot 2026-08-03 162941.png` | Adjacent angles & Adjacent of right triangle | `dict_adjacent_angles.png`, `dict_adjacent.png`, `dict_adjacent_side.png` | `adjacent`, `adjacent angles`, `adjacent side` |
| 38 | `Screenshot 2026-08-03 162948.png` | Chemical Structure of Adrenaline | `dict_adrenaline.png`, `dict_epinephrine.png` | `adrenaline`, `epinephrine` |
| 39 | `Screenshot 2026-08-03 211010.png` | Chemical structure of Aflatoxin B1 | `dict_aflatoxin.png`, `dict_aflatoxin_b1.png` | `aflatoxin`, `aflatoxin b1` |
| 40 | `Screenshot 2026-08-03 211033.png` | Air layering (marcotting) 4-step process | `dict_air_layering.png`, `dict_air_layering_marcotting.png`, `dict_marcotting.png` | `air layering`, `air layering (marcotting)`, `marcotting` |

---

### Batch 5 (Completed) — Screenshots 41 to 60
Source Folder: `section a-b images/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 41 | `Screenshot 2026-08-03 211050.png` | Chemical structure of Aldosterone | `dict_aldosterone.png` | `aldosterone` |
| 42 | `Screenshot 2026-08-03 211113.png` | Quadratic curve — algebraic curve of order two (a>0 & a<0) | `dict_algebraic_curve.png`, `dict_quadratic_curve.png` | `algebraic curve`, `quadratic curve` |
| 43 | `Screenshot 2026-08-03 211140.png` | Fig I: Alimentary canal of a human / Fig II: Alimentary canal of a rabbit | `dict_alimentary_canal.png`, `dict_alimentary_canal_human.png`, `dict_alimentary_canal_rabbit.png` | `alimentary canal`, `alimentary canal (human)`, `alimentary canal (rabbit)` |
| 44 | `Screenshot 2026-08-03 211200.png` | Fig I: Allotrope of graphite / Fig II: Allotrope of diamond | `dict_allotrope.png`, `dict_allotrope_graphite.png`, `dict_allotrope_diamond.png`, `dict_graphite.png`, `dict_diamond.png` | `allotrope`, `allotrope of graphite`, `allotrope of diamond`, `graphite`, `diamond` |
| 45 | `Screenshot 2026-08-03 211219.png` | Table of Important Alloys, Composition and Uses | `dict_alloy.png` | `alloy` |
| 46 | `Screenshot 2026-08-03 211232.png` | Alternate angles (transversal line diagram) | `dict_alternate_angles.png` | `alternate angles` |
| 47 | `Screenshot 2026-08-03 211240.png` | Alternate leaves (e.g., Rosa) | `dict_alternate_leaves.png`, `dict_alternate_leaf_arrangement.png` | `alternate leaves`, `alternate leaf arrangement` |
| 48 | `Screenshot 2026-08-03 211254.png` | Altitude of a triangle (Triangle ABC) | `dict_altitude.png`, `dict_altitude_of_a_triangle.png` | `altitude`, `altitude of a triangle` |
| 49 | `Screenshot 2026-08-03 211321.png` | Amide structures — Fig I–VI: general, ethanamide, amides, methanamide, N-methyltharcamide, N-methyl-N-ethylethanamide | `dict_amide.png`, `dict_ethanamide.png`, `dict_methanamide.png`, `dict_primary_amide.png`, `dict_tertiary_amide.png` | `amide`, `ethanamide`, `methanamide`, `primary amide`, `tertiary amide` |
| 50 | `Screenshot 2026-08-03 211341.png` | Preparation of NH₃ (ammonia) — lab apparatus | `dict_ammonia.png`, `dict_preparation_of_ammonia.png` | `ammonia`, `preparation of ammonia` |
| 51 | `Screenshot 2026-08-03 211349.png` | Hot-wire ammeter (labelled diagram) | `dict_ammeter.png`, `dict_hot_wire_ammeter.png` | `ammeter`, `hot-wire ammeter` |
| 52 | `Screenshot 2026-08-03 211401.png` | Single stage amplifier (circuit diagram) | `dict_amplifier.png`, `dict_single_stage_amplifier.png` | `amplifier`, `single stage amplifier` |
| 53 | `Screenshot 2026-08-03 211408.png` | Amplexicaul leaf (leaf shape diagram) | `dict_amplexicaul.png`, `dict_amplexicaul_leaf.png` | `amplexicaul`, `amplexicaul leaf` |
| 54 | `Screenshot 2026-08-03 211416.png` | Amplitude of a sinusoid / oscillating system | `dict_amplitude.png` | `amplitude` |
| 55 | `Screenshot 2026-08-03 211426.png` | Block diagram of analogue-to-digital converter (ADC) | `dict_analogue_to_digital_converter.png`, `dict_adc.png` | `analogue-to-digital converter`, `analogue to digital converter`, `adc` |
| 56 | `Screenshot 2026-08-03 211439.png` | AND gate circuit + truth table | `dict_and_gate.png`, `dict_and_gate_truth_table.png` | `and gate` |
| 57 | `Screenshot 2026-08-03 211510.png` | Angle — arc length / radius (radian definition) | `dict_angle.png`, `dict_angle_in_radians.png` | `angle`, `angle in radians` |
| 58 | `Screenshot 2026-08-03 211525.png` | Angle of depression (observer & object) | `dict_angle_of_depression.png` | `angle of depression` |
| 59 | `Screenshot 2026-08-03 211534.png` | Angle of deviation in a prism / angle of minimum deviation | `dict_angle_of_deviation.png`, `dict_angle_of_minimum_deviation.png` | `angle of deviation`, `angle of minimum deviation` |
| 60 | `Screenshot 2026-08-03 211544.png` | Angle between two vectors (Fig 1, 2, 3) | `dict_angle_between_two_vectors.png` | `angle between two vectors` |

---

### Final Batch (Completed) — Screenshots 61 to 138
Source Folder: `section a-b images/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 61 | `Screenshot 2026-08-03 211552.png` | Angle of elevation | `dict_angle_of_elevation.png` | `angle of elevation` |
| 62 | `Screenshot 2026-08-03 211605.png` | Animal husbandry (cow, goat, pig external features) | `dict_animal_husbandry.png`, `dict_cow_external_features.png`, `dict_goat_external_features.png`, `dict_pig_external_features.png` | `animal husbandry`, `cow external features`, `goat external features`, `pig external features` |
| 63 | `Screenshot 2026-08-03 211627.png` | Anomalous expansion of water | `dict_anomalous_expansion_of_water.png` | `anomalous expansion of water` |
| 64 | `Screenshot 2026-08-03 211638.png` | Anomer (alpha and beta glucose) | `dict_anomer.png`, `dict_alpha_glucose.png`, `dict_beta_glucose.png` | `anomer`, `alpha glucose`, `beta glucose` |
| 65 | `Screenshot 2026-08-03 211647.png` | Antheridia of moss / Antheridium | `dict_antheridia_of_moss.png`, `dict_antheridium.png` | `antheridia of moss`, `antheridium` |
| 66 | `Screenshot 2026-08-03 211654.png` | Anthocarp of fruit | `dict_anthocarp.png`, `dict_anthocarp_of_fruit.png` | `anthocarp`, `anthocarp of fruit` |
| 67 | `Screenshot 2026-08-03 211704.png` | Anti-magic square | `dict_anti_magic_square.png` | `anti-magic square` |
| 68 | `Screenshot 2026-08-03 211715.png` | Antinode, node & standing wave | `dict_antinode.png`, `dict_node.png`, `dict_standing_wave.png` | `antinode`, `node`, `standing wave` |
| 69 | `Screenshot 2026-08-03 211725.png` | Antipodal cell | `dict_antipodal_cell.png` | `antipodal cell` |
| 70 | `Screenshot 2026-08-03 211739.png` | Apollonius circle | `dict_apollonius_circle.png` | `apollonius circle` |
| 71 | `Screenshot 2026-08-03 211748.png` | Apothem | `dict_apothem.png` | `apothem` |
| 72 | `Screenshot 2026-08-03 211759.png` | Arc of a circle | `dict_arc.png`, `dict_arc_of_a_circle.png` | `arc`, `arc of a circle` |
| 73 | `Screenshot 2026-08-03 211810.png` | Archimedean spiral | `dict_archimedean_spiral.png` | `archimedean spiral` |
| 74 | `Screenshot 2026-08-03 211822.png` | Argand diagram | `dict_argand_diagram.png` | `argand diagram` |
| 75 | `Screenshot 2026-08-03 211828.png` | Argument of a complex number | `dict_argument_of_a_complex_number.png` | `argument of a complex number` |
| 76 | `Screenshot 2026-08-03 211841.png` | Artery / Structure of an artery | `dict_artery.png`, `dict_structure_of_an_artery.png` | `artery`, `structure of an artery` |
| 77 | `Screenshot 2026-08-03 211854.png` | Chemical structure of Aspirin | `dict_aspirin.png` | `aspirin` |
| 78 | `Screenshot 2026-08-03 211904.png` | Chemical structure of Ascorbic Acid (Vitamin C) | `dict_ascorbic_acid.png`, `dict_vitamin_c.png` | `ascorbic acid`, `vitamin c` |
| 79 | `Screenshot 2026-08-03 211914.png` | Chemical structure of Aspartame | `dict_aspartame.png` | `aspartame` |
| 80 | `Screenshot 2026-08-03 211921.png` | Chemical structure of Aspartic acid | `dict_aspartic_acid.png` | `aspartic acid` |
| 81 | `Screenshot 2026-08-03 211932.png` | Astronomical telescope (near point & infinity) | `dict_astronomical_telescope.png`, `dict_astronomical_telescope_near_point.png`, `dict_astronomical_telescope_infinity.png` | `astronomical telescope`, `astronomical telescope near point`, `astronomical telescope at infinity` |
| 82 | `Screenshot 2026-08-03 212055.png` | Asymptote | `dict_asymptote.png` | `asymptote` |
| 83 | `Screenshot 2026-08-03 212355.png` | Normal curve / Bell curve | `dict_normal_curve.png`, `dict_bell_curve.png` | `normal curve`, `bell curve` |
| 84 | `Screenshot 2026-08-03 212421.png` | Atomic weight / mass table | `dict_atomic_weight_table.png`, `dict_atomic_mass_table.png` | `atomic weight table`, `atomic mass table` |
| 85 | `Screenshot 2026-08-03 212447.png` | Chemical structure of Atropine | `dict_atropine.png` | `atropine` |
| 86 | `Screenshot 2026-08-03 212456.png` | Auricle of a leaf | `dict_auricle_of_a_leaf.png` | `auricle of a leaf` |
| 87 | `Screenshot 2026-08-03 212506.png` | Autotransformer | `dict_autotransformer.png` | `autotransformer` |
| 88 | `Screenshot 2026-08-03 212515.png` | Chemical structure of Auxin (Indole-3-acetic acid) | `dict_auxin.png`, `dict_indole_3_acetic_acid.png` | `auxin`, `indole-3-acetic acid` |
| 89 | `Screenshot 2026-08-03 212523.png` | Awn of a spikelet | `dict_awn_of_a_spikelet.png`, `dict_awn.png` | `awn`, `awn of a spikelet` |
| 90 | `Screenshot 2026-08-03 212536.png` | Parabola line of symmetry | `dict_axis_of_symmetry_parabola.png` | `axis of symmetry of a parabola` |
| 91 | `Screenshot 2026-08-03 212543.png` | Axis vertebra of a mammal | `dict_axis_vertebra.png` | `axis vertebra` |
| 92 | `Screenshot 2026-08-03 212555.png` | Baermann funnel | `dict_baermann_funnel.png` | `baermann funnel` |
| 93 | `Screenshot 2026-08-03 212602.png` | Beam balance | `dict_beam_balance.png` | `beam balance` |
| 94 | `Screenshot 2026-08-03 212642.png` | Vertical & Horizontal bar chart/graph | `dict_bar_chart.png`, `dict_bar_graph.png` | `bar chart`, `bar graph`, `vertical bar chart`, `horizontal bar chart` |
| 95 | `Screenshot 2026-08-03 212657.png` | Chemical structure of Barbiturate | `dict_barbiturate.png` | `barbiturate` |
| 96 | `Screenshot 2026-08-03 212704.png` | Mercury Barometer | `dict_barometer.png`, `dict_mercury_barometer.png` | `barometer`, `mercury barometer` |
| 97 | `Screenshot 2026-08-03 212712.png` | Baryon Number Table | `dict_baryon_number_table.png` | `baryon number table`, `baryon` |
| 98 | `Screenshot 2026-08-03 212726.png` | Basal placentation | `dict_basal_placentation.png` | `basal placentation` |
| 99 | `Screenshot 2026-08-03 212741.png` | Base Station System (BSS) | `dict_base_station_system.png`, `dict_bss.png` | `base station system`, `bss` |
| 100 | `Screenshot 2026-08-03 212749.png` | Base pairing (Thymine-Adenine & Cytosine-Guanine) | `dict_base_pairing.png` | `base pairing`, `base pairing thymine adenine`, `base pairing cytosine guanine` |
| 101 | `Screenshot 2026-08-03 212811.png` | Categories of rays (Parallel, Convergent, Divergent) | `dict_beam_of_rays.png` | `beam of rays`, `parallel rays`, `convergent rays`, `divergent rays` |
| 102 | `Screenshot 2026-08-03 212827.png` | Bell curve / Normal distribution graph | `dict_bell_curve_normal_distribution.png` | `bell curve normal distribution`, `normal distribution` |
| 103 | `Screenshot 2026-08-03 212834.png` | Bell Jar | `dict_bell_jar.png` | `bell jar` |
| 104 | `Screenshot 2026-08-03 213041.png` | Chemical structure of Butene (1-butene, trans-2-butene) | `dict_butene.png` | `butene`, `1-butene`, `trans-2-butene` |
| 105 | `Screenshot 2026-08-03 213048.png` | Chemical structure of Isobutanol (2-methyl-1-propanol) | `dict_isobutanol.png` | `isobutanol`, `2-methyl-1-propanol` |
| 106 | `Screenshot 2026-08-03 213056.png` | Chemical structure of Butane (n-butane, Isobutane) | `dict_butane.png` | `butane`, `n-butane`, `isobutane` |
| 107 | `Screenshot 2026-08-03 213108.png` | Burdisso castrator | `dict_burdizzo_castrator.png` | `burdizzo castrator` |
| 108 | `Screenshot 2026-08-03 213114.png` | Bunsen Burner | `dict_bunsen_burner.png` | `bunsen burner` |
| 109 | `Screenshot 2026-08-03 213126.png` | Bundle scar | `dict_bundle_scar.png` | `bundle scar` |
| 110 | `Screenshot 2026-08-03 213138.png` | Budding processes (flowering plants, yeast, hydra) | `dict_budding.png` | `budding`, `budding in flowering plants`, `budding in yeast`, `budding in hydra` |
| 111 | `Screenshot 2026-08-03 213154.png` | Bulbel | `dict_bulbel.png` | `bulbel` |
| 112 | `Screenshot 2026-08-03 213212.png` | Bud scales | `dict_bud_scales.png` | `bud scales` |
| 113 | `Screenshot 2026-08-03 213223.png` | Bubble chamber | `dict_bubble_chamber.png` | `bubble chamber` |
| 114 | `Screenshot 2026-08-03 213233.png` | Buchner funnel & flask for filtration | `dict_buchner_funnel.png` | `buchner funnel`, `buchner flask` |
| 115 | `Screenshot 2026-08-03 213302.png` | Chemical structure of Bromothymol Blue | `dict_bromothymol_blue.png` | `bromothymol blue` |
| 116 | `Screenshot 2026-08-03 213320.png` | Brewster's Law | `dict_brewsters_law.png` | `brewsters law` |
| 117 | `Screenshot 2026-08-03 213426.png` | Bridge rectifier circuit diagram | `dict_bridge_rectifier.png` | `bridge rectifier` |
| 118 | `Screenshot 2026-08-03 213437.png` | Generation of Bremsstrahlung | `dict_bremsstrahlung.png` | `bremsstrahlung` |
| 119 | `Screenshot 2026-08-03 213451.png` | Box-And-Whisker Plot | `dict_box_and_whisker_plot.png` | `box-and-whisker plot`, `box plot` |
| 120 | `Screenshot 2026-08-03 213502.png` | Born-Haber cycle | `dict_born_haber_cycle.png` | `born-haber cycle` |
| 121 | `Screenshot 2026-08-03 213609.png` | Chemical Structure of Borane | `dict_borane.png` | `borane` |
| 122 | `Screenshot 2026-08-03 213616.png` | Microscopic structure of bone | `dict_bone_microscopic_structure.png` | `bone microscopic structure`, `haversian system` |
| 123 | `Screenshot 2026-08-03 213622.png` | Bomb calorimeter | `dict_bomb_calorimeter.png` | `bomb calorimeter` |
| 124 | `Screenshot 2026-08-03 213630.png` | Boiling Point Composition Diagram | `dict_boiling_point_composition_diagram.png` | `boiling point composition diagram` |
| 125 | `Screenshot 2026-08-03 213641.png` | Block and tackle | `dict_block_and_tackle.png` | `block and tackle` |
| 126 | `Screenshot 2026-08-03 213651.png` | Blastodisc of an egg | `dict_blastodisc.png` | `blastodisc`, `blastodisc of egg` |
| 127 | `Screenshot 2026-08-03 213731.png` | Blast furnace | `dict_blast_furnace.png` | `blast furnace` |
| 128 | `Screenshot 2026-08-03 213759.png` | Biternate leaves | `dict_biternate_leaves.png` | `biternate leaves` |
| 129 | `Screenshot 2026-08-03 213808.png` | Biserrate leaf | `dict_biserrate_leaf.png` | `biserrate leaf` |
| 130 | `Screenshot 2026-08-03 213847.png` | Bipolar integrated circuit | `dict_bipolar_integrated_circuit.png` | `bipolar integrated circuit` |
| 131 | `Screenshot 2026-08-03 213917.png` | Bipinnate leaflets & Bipinnatifid leaf | `dict_bipinnate_leaflets.png` | `bipinnate leaflets`, `bipinnatifid leaf` |
| 132 | `Screenshot 2026-08-03 213926.png` | Bipartite leaf & Complete Bipartite Graph | `dict_bipartite_leaf.png` | `bipartite leaf`, `complete bipartite graph` |
| 133 | `Screenshot 2026-08-03 213932.png` | Chemical Structure of Biotin | `dict_biotin.png` | `biotin` |
| 134 | `Screenshot 2026-08-03 214015.png` | Bimetallic strip & Bimetallic strip thermometer | `dict_bimetallic_strip.png` | `bimetallic strip`, `bimetallic strip thermometer` |
| 135 | `Screenshot 2026-08-03 214026.png` | Bilobed stigma & Bilocular ovary | `dict_bilobed_stigma.png` | `bilobed stigma`, `bilocular ovary` |
| 136 | `Screenshot 2026-08-03 214038.png` | Bimagic square | `dict_bimagic_square.png` | `bimagic square` |
| 137 | `Screenshot 2026-08-03 214049.png` | Bidentate leaf | `dict_bidentate_leaf.png` | `bidentate leaf` |
| 138 | `Screenshot 2026-08-03 214101.png` | Biconcave lens | `dict_biconcave_lens.png` | `biconcave lens` |

---

### F-J Series: Batch 1 (Completed) — Screenshots 1 to 30
Source Folder: `f-j diagrams/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot_11-9-2026_153052_.jpeg` | Galeate helmet-shaped corolla | `dict_galeate.png` | `galeate`, `galeate corolla` |
| 2 | `Screenshot_11-9-2026_15309_.jpeg` | Galactose structure | `dict_galactose.png` | `galactose` |
| 3 | `Screenshot_11-9-2026_153112_.jpeg` | Galilean telescope ray diagram | `dict_galilean_telescope.png` | `galilean telescope` |
| 4 | `Screenshot_11-9-2026_153129_.jpeg` | Moving coil galvanometer | `dict_moving_coil_galvanometer.png` | `moving coil galvanometer`, `galvanometer` |
| 5 | `Screenshot_11-9-2026_15312_.jpeg` | Gallic acid structure | `dict_gallic_acid.png` | `gallic acid`, `3,4,5-trihydroxybenzoic acid` |
| 6 | `Screenshot_11-9-2026_153145_.jpeg` | Gamma-Aminobutyric Acid (GABA) | `dict_gamma_aminobutyric_acid.png` | `gamma-aminobutyric acid`, `gaba` |
| 7 | `Screenshot_11-9-2026_153158_.jpeg` | Gas engine internal cross-section | `dict_gas_engine.png` | `gas engine` |
| 8 | `Screenshot_11-9-2026_153228_.jpeg` | Gas engine (duplicate) | *(merged with #7)* | `gas engine` |
| 9 | `Screenshot_11-9-2026_153243_.jpeg` | Argand diagram / Gaussian plane | `dict_argand_diagram_gaussian.png` | `argand diagram`, `gaussian plane`, `complex plane` |
| 10 | `Screenshot_11-9-2026_153255_.jpeg` | Geiger-Müller radiation counter | `dict_geiger_counter.png` | `geiger counter`, `geiger-muller counter`, `gm counter` |
| 11 | `Screenshot_11-9-2026_15326_.jpeg` | Gas thermometer | `dict_gas_thermometer.png` | `gas thermometer`, `constant volume gas thermometer` |
| 12 | `Screenshot_11-9-2026_153334_.jpeg` | AC Generator / Alternator | `dict_ac_generator.png` | `ac generator`, `alternator`, `dynamo` |
| 13 | `Screenshot_11-9-2026_153348_.jpeg` | Geoboard peg array | `dict_geoboard.png` | `geoboard` |
| 14 | `Screenshot_11-9-2026_15335_.jpeg` | Gem-dimethyl group | `dict_gem_dimethyl_group.png` | `gem-dimethyl group`, `geminal` |
| 15 | `Screenshot_11-9-2026_15340_.jpeg` | Geraniol structure | `dict_geraniol.png` | `geraniol` |
| 16 | `Screenshot_11-9-2026_153411_.jpeg` | Gibbous calyx | `dict_gibbous_calyx.png` | `gibbous calyx`, `gibbous` |
| 17 | `Screenshot_11-9-2026_153420_.jpeg` | Gibberellins plant hormone | `dict_gibberellins.png` | `gibberellins`, `gibberellin`, `gibberellic acid` |
| 18 | `Screenshot_11-9-2026_153436_.jpeg` | Gladiate leaf | `dict_gladiate_leaf.png` | `gladiate leaf`, `gladiate` |
| 19 | `Screenshot_11-9-2026_153452_.jpeg` | Glucuronic acid | `dict_glucuronic_acid.png` | `glucuronic acid` |
| 20 | `Screenshot_11-9-2026_153458_.jpeg` | Glutathione tripeptide | `dict_glutathione.png` | `glutathione` |
| 21 | `Screenshot_11-9-2026_153518_.jpeg` | Glycosidic bonds | `dict_glycosidic_bonds.png` | `glycosidic bonds`, `glycosidic bond`, `glycoside linkage` |
| 22 | `Screenshot_11-9-2026_153527_.jpeg` | Gnomon magic square | `dict_gnomon_magic_square.png` | `gnomon magic square`, `gnomon` |
| 23 | `Screenshot_11-9-2026_153546_.jpeg` | Linear gradient / slope | `dict_gradient.png` | `gradient`, `slope` |
| 24 | `Screenshot_11-9-2026_153554_.jpeg` | Gradate involucre floral bracts | `dict_graduate_involucre.png` | `graduate involucre`, `gradate involucre`, `involucre` |
| 25 | `Screenshot_11-9-2026_15357_.jpeg` | Propane-1,2,3-triol (Glycerol) | `dict_propane_1_2_3_triol.png` | `propane-1,2,3-triol`, `glycerol`, `glycerin` |
| 26 | `Screenshot_11-9-2026_153612_.jpeg` | Graphene 2D honeycomb lattice | `dict_graphene.png` | `graphene` |
| 27 | `Screenshot_11-9-2026_15361_.jpeg` | Grafting (scion & stock) | `dict_grafting.png` | `grafting`, `scion` |
| 28 | `Screenshot_11-9-2026_153624_.jpeg` | Layered structure of graphite | `dict_structure_of_graphite.png` | `graphite`, `structure of graphite` |
| 29 | `Screenshot_11-9-2026_153631_.jpeg` | Lateral view of grasshopper | `dict_grasshopper.png` | `grasshopper`, `lateral view of a grasshopper` |
| 30 | `Screenshot_11-9-2026_153641_.jpeg` | Law of universal gravitation | `dict_gravitation.png` | `gravitation`, `newton's law of gravitation`, `universal gravitation` |

---

### F-J Series: Batch 2 (Completed) — Screenshots 31 to 60
Source Folder: `f-j diagrams/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 31 | `Screenshot_11-9-2026_154155_.jpeg` | Universal gravitation (duplicate) | `dict_gravitation.png` | `gravitation`, `newton's law of gravitation`, `universal gravitation` |
| 32 | `Screenshot_11-9-2026_154217_.jpeg` | Greatest integer function graph | `dict_greatest_integer_function.png` | `greatest integer function`, `floor function`, `step function` |
| 33 | `Screenshot_11-9-2026_154234_.jpeg` | Grouped data frequency distribution table | `dict_grouped_data_frequency_distribution.png` | `grouped data`, `frequency distribution`, `grouped data frequency distribution` |
| 34 | `Screenshot_11-9-2026_154246_.jpeg` | Chemical structure of Guanosine | `dict_guanosine.png` | `guanosine`, `cyclic guanosine monophosphate`, `guanosine triphosphate` |
| 35 | `Screenshot_11-9-2026_154255_.jpeg` | Chemical structure formula of Guanidine | `dict_guanidine.png` | `guanidine` |
| 36 | `Screenshot_11-9-2026_15429_.jpeg` | Great Circle on a sphere | `dict_great_circle.png` | `great circle`, `spherical triangle` |
| 37 | `Screenshot_11-9-2026_15431_.jpeg` | Chemical structure of Guanine | `dict_guanine.png` | `guanine`, `guan ine`, `guanine riboside` |
| 38 | `Screenshot_11-9-2026_154325_.jpeg` | Chemical formula of Haematoxylin | `dict_haematoxylin.png` | `haematoxylin`, `hematoxylin` |
| 39 | `Screenshot_11-9-2026_154335_.jpeg` | Structure of the hair follicle (Longitudinal & Cross) | `dict_hair_follicle.png` | `hair follicle`, `hair`, `structure of the hair follicle` |
| 40 | `Screenshot_11-9-2026_154343_.jpeg` | Half-wave rectification circuit & wave | `dict_half_wave_rectification.png` | `half-wave rectification`, `half-wave rectifier`, `half wave rectification`, `rectification` |
| 41 | `Screenshot_11-9-2026_154412_.jpeg` | Hastate leaf | `dict_hastate_leaf.png` | `hastate`, `hastate leaf` |
| 42 | `Screenshot_11-9-2026_154420_.jpeg` | Host stem transverse section showing haustorium | `dict_haustorium.png` | `haustorium`, `haustorium of dodder`, `dodder` |
| 43 | `Screenshot_11-9-2026_154430_.jpeg` | Head (capitulum) inflorescence | `dict_capitulum_head.png` | `head`, `capitulum`, `head (capitulum)`, `head inflorescence` |
| 44 | `Screenshot_11-9-2026_154455_.jpeg` | Mammalian heart vertical section & Human heart external | `dict_heart.png`, `dict_mammalian_heart_vertical_section.png`, `dict_human_heart_external.png` | `heart`, `mammalian heart`, `human heart`, `vertical section of a heart`, `external appearance of a human heart` |
| 45 | `Screenshot_11-9-2026_154513_.jpeg` | Simplified heat engine | `dict_heat_engine.png` | `heat engine`, `simplified heat engine` |
| 46 | `Screenshot_11-9-2026_154528_.jpeg` | Parallelogram height | `dict_height_parallelogram.png` | `height`, `height of a parallelogram` |
| 47 | `Screenshot_11-9-2026_154549_.jpeg` | Prism height | `dict_height_prism.png` | `prism height`, `height of a prism` |
| 48 | `Screenshot_11-9-2026_154557_.jpeg` | Height of a pyramid/cone | `dict_height_pyramid_cone.png` | `height of a pyramid`, `height of a cone`, `pyramid height` |
| 49 | `Screenshot_11-9-2026_154629_.jpeg` | Height of a triangle (Altitude) | `dict_height_triangle.png` | `height of a triangle`, `altitude of a triangle` |
| 50 | `Screenshot_11-9-2026_154638_.jpeg` | 3D Helix | `dict_helix_3d.png` | `helix`, `helix in a three dimensional plane`, `three dimensional helix` |
| 51 | `Screenshot_11-9-2026_154648_.jpeg` | General formula of a Hemiacetal | `dict_hemiacetal.png` | `hemiacetal`, `general formula of a hemiacetal` |
| 52 | `Screenshot_11-9-2026_154717_.jpeg` | Hesperidium citrus fruit | `dict_hesperidium.png` | `hesperidium`, `hesperidium fruit` |
| 53 | `Screenshot_11-9-2026_154727_.jpeg` | Heterocyclic compounds (Thiophen, Oxazole, Imidazole, Pyridine) | `dict_heterocyclic_compound.png` | `heterocyclic compound`, `heterocyclic`, `thiophene`, `oxazole`, `imidazole`, `pyridine` |
| 54 | `Screenshot_11-9-2026_15472_.jpeg` | Chemical structure of Heroin | `dict_heroin.png` | `heroin`, `diacetylmorphine` |
| 55 | `Screenshot_11-9-2026_154740_.jpeg` | Heterosporous (Microspores & Megaspore) | `dict_heterosporous.png` | `heterosporous`, `heterospory`, `microspore`, `microspores`, `megaspore` |
| 56 | `Screenshot_11-9-2026_154749_.jpeg` | Heterostylic floral forms | `dict_heterostylic.png` | `heterostylic`, `heterostyly`, `style` |
| 57 | `Screenshot_11-9-2026_15478_.jpeg` | Chemical structure of Heroin (duplicate) | *(merged with #54)* | `heroin`, `diacetylmorphine` |
| 58 | `Screenshot_11-9-2026_154811_.jpeg` | Chemical structure of Hexane | `dict_hexane.png` | `hexane`, `structure of hexane` |
| 59 | `Screenshot_11-9-2026_154825_.jpeg` | Hexagonal Prism 3D geometry | `dict_hexagonal_prism.png` | `hexagonal prism`, `prism` |
| 60 | `Screenshot_11-9-2026_154833_.jpeg` | Hexagram (6-pointed star) | `dict_hexagram.png` | `hexagram` |

---

### F-J Series: Batch 3 (Completed) — Screenshots 61 to 70
Source Folder: `f-j diagrams/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 61 | `Screenshot_11-9-2026_15483_.jpeg` | Chemical structure of Hexamine | `dict_hexamine.png` | `hexamine`, `methenamine` |
| 62 | `Screenshot_11-9-2026_154855_.jpeg` | Hilum of seed coat & Hilum of kidney | `dict_hilum.png`, `dict_hilum_seed_coat.png`, `dict_hilum_kidney.png` | `hilum`, `hilum of seed coat`, `hilum of kidney` |
| 63 | `Screenshot_11-9-2026_154923_.jpeg` | A Histogram on the cartesian plane | `dict_histogram.png` | `histogram`, `histogram on cartesian plane` |
| 64 | `Screenshot_11-9-2026_154938_.jpeg` | Hoffmann's Reaction mechanism | `dict_hoffmanns_reaction.png`, `dict_hoffmann_rearrangement.png` | `hoffmann's reaction`, `hoffmann rearrangement`, `hoffmann degradation` |
| 65 | `Screenshot_11-9-2026_154947_.jpeg` | Hoffman voltammeter | `dict_hoffman_voltammeter.png` | `hoffman voltammeter`, `hoffmann voltammeter`, `voltammeter` |
| 66 | `Screenshot_11-9-2026_15499_.jpeg` | Structural formula of Histamine | `dict_histamine.png` | `histamine` |
| 67 | `Screenshot_11-9-2026_155021_.jpeg` | Horizontal line test — y = x³ (one-to-one function) | `dict_horizontal_line_test.png` | `horizontal line test`, `one-to-one function` |
| 68 | `Screenshot_11-9-2026_155029_.jpeg` | Horizontal line test — y = x² (not one-to-one) | `dict_horizontal_line_test_not_one_to_one.png` | `horizontal line test not one-to-one`, `many-to-one function` |
| 69 | `Screenshot_11-9-2026_155057_.jpeg` | Hot-wire ammeter | `dict_hot_wire_ammeter.png` | `hot-wire ammeter`, `hot wire ammeter` |
| 70 | `Screenshot_11-9-2026_155111_.jpeg` | Huygens' eyepiece | `dict_huygens_eyepiece.png` | `huygens' eyepiece`, `huygens eyepiece`, `eyepiece` |
| 71 | `Screenshot_11-9-2026_155124_.jpeg` | Hydraulic machine & press | `dict_hydraulic_machine.png`, `dict_hydraulic_press.png` | `hydraulic machine`, `hydraulic press`, `hydraulics` |
| 72 | `Screenshot_11-9-2026_155138_.jpeg` | Preparation of hydrogen from zinc with dilute acids | `dict_preparation_of_hydrogen.png`, `dict_hydrogen.png` | `hydrogen`, `preparation of hydrogen`, `preparation of hydrogen from zinc with dilute acids` |
| 73 | `Screenshot_11-9-2026_155228_.jpeg` | Intermolecular & Intramolecular hydrogen bonding | `dict_hydrogen_bond.png`, `dict_hydrogen_bonding.png` | `hydrogen bond`, `hydrogen bonding`, `intermolecular hydrogen bonding`, `intramolecular hydrogen bonding` |
| 74 | `Screenshot_11-9-2026_155239_.jpeg` | Standard Hydrogen Electrode (SHE) | `dict_hydrogen_electrode.png`, `dict_standard_hydrogen_electrode.png` | `hydrogen electrode`, `standard hydrogen electrode`, `she`, `normal hydrogen electrode` |
| 75 | `Screenshot_11-9-2026_155249_.jpeg` | Hydrometer | `dict_hydrometer.png` | `hydrometer` |

---

### F-J Series: Batch 4 (Completed) — Screenshots 76 to 111
Source Folder: `f-j diagrams/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 76 | `Screenshot_11-9-2026_155335_.jpeg` | Hyperbola with its various parts on the cartesian plane | `dict_hyperbola.png` | `hyperbola`, `hyperbola on cartesian plane`, `transverse axis`, `conjugate axis` |
| 77 | `Screenshot_11-9-2026_155354_.jpeg` | Hyperopia (Long sightedness) — ray diagram with corrective lens | `dict_hyperopia.png` | `hyperopia`, `long sightedness`, `hyperopia (long sightedness)`, `long-sightedness`, `longsightedness` |
| 78 | `Screenshot_11-9-2026_155414_.jpeg` | Hypocycloid curve on Cartesian plane | `dict_hypocycloid.png` | `hypocycloid` |
| 79 | `Screenshot_11-9-2026_155431_.jpeg` | Hypsometer (thermometer + manometer + boiling water setup) | `dict_hypsometer.png` | `hypsometer` |
| 80 | `Screenshot_11-9-2026_155437_.jpeg` | Hysteresis loop (Magnetic induction B vs Magnetising field H) | `dict_hysteresis_loop.png` | `hysteresis loop`, `hysteresis`, `magnetic hysteresis` |
| 81 | `Screenshot_11-9-2026_155457_.jpeg` | Lower fixed point / Ice point (0°C thermometer calibration) | `dict_ice_point.png` | `ice point`, `lower fixed point`, `ice point thermometer` |
| 82 | `Screenshot_11-9-2026_155515_.jpeg` | Chemical structure of Imine | `dict_imine.png` | `imine`, `chemical structure of imine` |
| 83 | `Screenshot_11-9-2026_155524_.jpeg` | Structure of a linear imide functional group | `dict_imide.png` | `imide`, `linear imide`, `imide functional group` |
| 84 | `Screenshot_11-9-2026_155547_.jpeg` | Incircle of a triangle (inscribed circle with angle bisectors) | `dict_incircle.png` | `incircle`, `incircle of a triangle`, `inscribed circle` |
| 85 | `Screenshot_11-9-2026_155557_.jpeg` | Inclined plane — forces acting on body (normal force, weight, mgSinθ, mgCosθ) | `dict_inclined_plane.png` | `inclined plane`, `forces on an inclined plane` |
| 86 | `Screenshot_11-9-2026_155610_.jpeg` | Truth table of inclusive disjunction (P∨Q) | `dict_inclusive_disjunction.png` | `inclusive disjunction`, `disjunction`, `truth table of inclusive disjunction` |
| 87 | `Screenshot_11-9-2026_155621_.jpeg` | The anvil (incus) of the human ear — full labelled cross-section | `dict_incus.png` | `incus`, `anvil`, `anvil (incus)`, `incus of the ear`, `ossicles` |
| 88 | `Screenshot_11-9-2026_155632_.jpeg` | Indeterminate flowers (racemose inflorescence) | `dict_indeterminate_flowers.png` | `indeterminate`, `indeterminate flowers`, `indeterminate inflorescence` |
| 89 | `Screenshot_11-9-2026_155644_.jpeg` | Structure of Indole (bicyclic heterocycle) | `dict_indole.png` | `indole`, `structure of indole` |
| 90 | `Screenshot_11-9-2026_155716_.jpeg` | Inflated (swollen/bladder-like botanical fruit) | `dict_inflated.png` | `inflated`, `inflated fruit` |
| 91 | `Screenshot_11-9-2026_155736_.jpeg` | Initial Side of an Angle (ray BA as initial side) | `dict_initial_side_of_an_angle.png` | `initial side`, `initial side of an angle` |
| 92 | `Screenshot_11-9-2026_15580_.jpeg` | Innominate bone — Ilium, Ischium, Pubis, Acetabulum, Obturator foramen | `dict_innominate_bone.png` | `innominate bone`, `hip bone`, `ilium`, `ischium`, `pubis`, `acetabulum` |
| 93 | `Screenshot_11-9-2026_155818_.jpeg` | Inscribed circle in a triangle (incircle with angle bisectors) | `dict_inscribed_circle.png` | `inscribed circle`, `inscribed circle in a triangle` |
| 94 | `Screenshot_11-9-2026_155827_.jpeg` | Chemical structure of Inositol (cyclohexane hexol) | `dict_inositol.png` | `inositol`, `chemical structure of inositol` |
| 95 | `Screenshot_11-9-2026_155849_.jpeg` | Insertion Reaction — cyclohexanone → cyclohexanoxime → caprolactam | `dict_insertion_reaction.png` | `insertion reaction`, `beckmann rearrangement`, `caprolactam` |
| 96 | `Screenshot_11-9-2026_15599_.jpeg` | Insulated Gate Field-effect Transistor (IGFET / MOSFET) — cross-section | `dict_igfet.png` | `igfet`, `mosfet`, `insulated gate field-effect transistor`, `insulated gate fet` |
| 97 | `Screenshot_11-9-2026_16034_.jpeg` | Formation of interference fringes (Young's double slit) | `dict_interference_fringes.png` | `interference fringes`, `interference`, `formation of interference fringes` |
| 98 | `Screenshot_11-9-2026_1603_.jpeg` | Integral — area under curve y=f(x) with Riemann sum definition | `dict_integral.png` | `integral`, `integration`, `definite integral`, `area under curve` |
| 99 | `Screenshot_11-9-2026_16052_.jpeg` | Fig I: Interior angle of a polygon (interior + exterior = 180°) | `dict_interior_angle.png` | `interior angle`, `interior angles`, `co-interior angles` |
| 100 | `Screenshot_11-9-2026_16059_.jpeg` | Fig II: Interior angles on a transversal (angles 3,4,5,6) | `dict_interior_angle_transversal.png` | `interior angles transversal`, `alternate interior angles` |
| 101 | `Screenshot_11-9-2026_16119_.jpeg` | Internal division by D and External division by E on a line | `dict_internal_division.png` | `internal division`, `external division`, `section formula` |
| 102 | `Screenshot_11-9-2026_16215_.jpeg` | Introrse anther (facing inward toward pistil) | `dict_introrse.png` | `introrse`, `introrse anther` |
| 103 | `Screenshot_11-9-2026_16227_.jpeg` | Intrinsic semiconductor — energy band diagram (conduction + valence bands) | `dict_intrinsic_semiconductor.png` | `intrinsic semiconductor`, `intrinsic semi conductor`, `semiconductor energy band` |
| 104 | `Screenshot_11-9-2026_16326_.jpeg` | Involute leaf (rolled inward margins) | `dict_involute_leaf.png` | `involute`, `involute leaf` |
| 105 | `Screenshot_11-9-2026_1637_.jpeg` | Involucre (ring of bracts around flower head) | `dict_involucre.png` | `involucre`, `involucral bract` |
| 106 | `Screenshot_11-9-2026_16417_.jpeg` | Isosceles Triangle (two equal sides a, two equal base angles x) | `dict_isosceles_triangle.png` | `isosceles triangle` |
| 107 | `Screenshot_11-9-2026_16442_.jpeg` | Jahn-Teller Effect — Cu(II) d-orbital splitting before and after J-T distortion | `dict_jahn_teller_effect.png` | `jahn-teller effect`, `jahn teller effect`, `jahn-teller distortion` |
| 108 | `Screenshot_11-9-2026_16455_.jpeg` | Jet engine — labelled cross-section (compressor, combustion chamber, turbine, exhaust) | `dict_jet_engine.png` | `jet engine`, `jet propulsion` |
| 109 | `Screenshot_11-9-2026_1648_.jpeg` | Chemical structure of Isoprene (2-methylbuta-1,3-diene) | `dict_isoprene.png` | `isoprene`, `2-methylbuta-1,3-diene`, `chemical structure of isoprene` |
| 110 | `Screenshot_11-9-2026_16524_.jpeg` | Junction Gate Field-Effect Transistor (JGFET) — p⁺ channel in n-substrate | `dict_jgfet.png` | `jgfet`, `junction gate field-effect transistor`, `junction fet`, `jfet` |
| 111 | `Screenshot_11-9-2026_1652_.jpeg` | Fig I: Vertical section through a synovial (movable) joint / Fig II: Section through the shoulder joint | `dict_synovial_joint.png` | `synovial joint`, `synovial membrane`, `synovial fluid`, `movable joint`, `shoulder joint`, `ball and socket joint` |

---

### Section K Series: Batch 1 — Screenshots 1 to 12
Source Folder: `k_diagrams/`

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot_24-9-2026_171045_.jpeg` | Chemical structure of Kainic Acid | `dict_kainic_acid.png` | `kainic acid`, `chemical structure of kainic acid`, `kainate`, `2-carboxy-3-carboxymethyl-4-isopropenylpyrrolidine` |
| 2 | `Screenshot_24-9-2026_171110_.jpeg` | Keepers for bar magnets & Keeper for horse-shoe magnet | `dict_keeper.png` | `keeper`, `magnetic keeper`, `keepers for bar magnets`, `keeper for horse-shoe magnet`, `horseshoe magnet keeper` |
| 3 | `Screenshot_24-9-2026_171123_.jpeg` | Kekulé structure of benzene | `dict_kekule_structure_of_benzene.png` | `kekule structure`, `kekule structure of benzene`, `kekule formula`, `kekulé structure`, `kekulé structure of benzene` |
| 4 | `Screenshot_24-9-2026_171151_.jpeg` | Formation of a ketal (Ketone + R'OH → Hemiketal → Ketal) | `dict_ketal.png` | `ketal`, `formation of a ketal`, `hemiketal` |
| 5 | `Screenshot_24-9-2026_171217_.jpeg` | Types of Ketose (dihydroxy-acetone, D-ribulose, D-xylulose, D-fructose) | `dict_ketose.png` | `ketose`, `types of ketose`, `ketose sugar`, `ketoses` |
| 6 | `Screenshot_24-9-2026_17126_.jpeg` | Chemical structure of Ketamine | `dict_ketamine.png` | `ketamine`, `chemical structure of ketamine` |
| 7 | `Screenshot_24-9-2026_17133_.jpeg` | Anatomy of the kidney (Cortex, Medulla, Pyramid, Pelvis, Calyces, Nephron) | `dict_kidney_anatomy.png` | `anatomy of the kidney`, `kidney anatomy`, `renal cortex`, `renal medulla`, `renal pyramid`, `renal pelvis`, `nephron`, `major calyx`, `minor calyx` |
| 8 | `Screenshot_24-9-2026_171434_.jpeg` | Fig. i) Kirchoff's First Law (Kirchoff's Current Law: I = I1 + I2) | `dict_kirchoffs_first_law.png` | `kirchoff's first law`, `kirchoffs first law`, `kirchoff's current law`, `kirchoffs current law`, `kcl`, `junction rule` |
| 9 | `Screenshot_24-9-2026_171446_.jpeg` | Fig ii.) Kirchoff's Second Law (Kirchoff's voltage law) | `dict_kirchoffs_second_law.png` | `kirchoff's second law`, `kirchoffs second law`, `kirchoff's voltage law`, `kirchoffs voltage law`, `kvl`, `loop rule` |
| 10 | `Screenshot_24-9-2026_171458_.jpeg` | Apparatus for estimating nitrogen by Kjeldahl's method | `dict_kjeldahls_method.png` | `kjeldahl's method`, `kjeldahls method`, `kjeldahl method`, `kjeldahl's flask`, `kjeldahls flask`, `estimating nitrogen by kjeldahl's method` |
| 11 | `Screenshot_24-9-2026_171514_.jpeg` | Kite (a geometric figure) | `dict_kite.png` | `kite`, `kite (a geometric figure)`, `geometric kite` |
| 12 | `Screenshot_24-9-2026_171540_.jpeg` | Knoevenagel Reaction | `dict_knoevenagel_reaction.png` | `knoevenagel reaction`, `knoevenagel condensation` |

---

## 4. Quality Standards
1. **Pristine Author Framing**: High-resolution user captures preserved with complete clarity.
2. **Dual Map Consistency**: `dictionary_diagrams_map.json` and `core_dictionary_diagrams.js` remain synchronized and sorted.






---

### Section N & O Series: Batch 1 (Completed) — Screenshots 1 to 60
Source Folder: `n-o diagrams/` (September 28, 2026 Pristine Author Captures)

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot_28-9-2026_172012_.jpeg` | Chemical Structure of Paracetamol | `dict_paracetamol.png` | `paracetamol`, `acetaminophen`, `4-acetamidophenol` |
| 2 | `Screenshot_28-9-2026_172019_.jpeg` | 1-Naphthol and 2-Naphthol | `dict_naphthol.png` | `naphthol`, `1-naphthol`, `2-naphthol`, `naphthols` |
| 3 | `Screenshot_28-9-2026_172027_.jpeg` | Chemical formula of Naphthalene | `dict_naphthalene.png` | `naphthalene`, `chemical formula of naphthalene` |
| 4 | `Screenshot_28-9-2026_172123_.jpeg` | Nephroid leaf | `dict_nephroid.png` | `nephroid`, `nephroid leaf` |
| 5 | `Screenshot_28-9-2026_172133_.jpeg` | Nephron (labelled anatomy) | `dict_nephron.png` | `nephron`, `renal tubule`, `bowman's capsule`, `glomerulus` |
| 6 | `Screenshot_28-9-2026_172143_.jpeg` | Nephron structure and tubules | `dict_nephron_structure.png` | `nephron structure`, `loop of henle` |
| 7 | `Screenshot_28-9-2026_172155_.jpeg` | Human nervous system | `dict_nervous_system.png` | `nervous system`, `human nervous system`, `central nervous system`, `spinal cord` |
| 8 | `Screenshot_28-9-2026_172226_.jpeg` | Net force of forces acting on an object | `dict_net_force.png` | `net force`, `resultant force` |
| 9 | `Screenshot_28-9-2026_172245_.jpeg` | von Neumann's Computer Architecture | `dict_von_neumann_architecture.png` | `von neumann architecture`, `computer architecture`, `neumann`, `von neumann` |
| 10 | `Screenshot_28-9-2026_172328_.jpeg` | Newton's Law of Cooling (Temperature vs Time) | `dict_newtons_law_of_cooling.png` | `newton's law of cooling`, `newtons law of cooling`, `law of cooling` |
| 11 | `Screenshot_28-9-2026_172349_.jpeg` | Chemical structure of Niacin | `dict_niacin.png` | `niacin`, `nicotinic acid`, `vitamin b3` |
| 12 | `Screenshot_28-9-2026_17236_.jpeg` | Neutral points (magnetic field lines) | `dict_neutral_points.png` | `neutral point`, `neutral points`, `magnetic neutral points` |
| 13 | `Screenshot_28-9-2026_172419_.jpeg` | Chemical Structure of Ninhydrin | `dict_ninhydrin.png` | `ninhydrin`, `2,2-dihydroxyindane-1,3-dione` |
| 14 | `Screenshot_28-9-2026_172445_.jpeg` | The nitrogen cycle | `dict_nitrogen_cycle.png` | `nitrogen cycle`, `nitrogen fixation`, `nitrification` |
| 15 | `Screenshot_28-9-2026_17244_.jpeg` | Chemical Structure of Nicotine | `dict_nicotine.png` | `nicotine` |
| 16 | `Screenshot_28-9-2026_172543_.jpeg` | Chemical Structure of Noradrenaline | `dict_noradrenaline.png` | `noradrenaline`, `norepinephrine` |
| 17 | `Screenshot_28-9-2026_17254_.jpeg` | Decibel scale of sounds (Noise pollution) | `dict_decibel_scale_noise.png` | `noise`, `noise pollution`, `decibel`, `decibel scale` |
| 18 | `Screenshot_28-9-2026_17266_.jpeg` | Normal Curve (Scores vs Frequency) | `dict_normal_curve.png` | `normal curve`, `normal distribution`, `gaussian distribution`, `bell curve` |
| 19 | `Screenshot_28-9-2026_172751_.jpeg` | A truth table describing the operation of NOT | `dict_not_truth_table.png` | `not`, `not operation`, `inverter table` |
| 20 | `Screenshot_28-9-2026_172813_.jpeg` | Nucellus (botanical ovule cross-section) | `dict_nucellus.png` | `nucellus`, `megasporocyte`, `integument`, `micropyle` |
| 21 | `Screenshot_28-9-2026_17282_.jpeg` | Not gate symbol and truth table | `dict_not_gate.png` | `not gate`, `inverter`, `not circuit` |
| 22 | `Screenshot_28-9-2026_172840_.jpeg` | Nuclear reactor (labelled cross-section) | `dict_nuclear_reactor.png` | `nuclear reactor`, `moderator`, `control rods`, `fuel rods` |
| 23 | `Screenshot_28-9-2026_172916_.jpeg` | Chemical Structure of 3-oxobutanoic Acid | `dict_3_oxobutanoic_acid.png` | `3-oxobutanoic acid`, `acetoacetic acid`, `oxoacid` |
| 24 | `Screenshot_28-9-2026_17291_.jpeg` | Number line | `dict_number_line.png` | `number line`, `real line` |
| 25 | `Screenshot_28-9-2026_172940_.jpeg` | Obcordate leaf / Obcordate fruit | `dict_obcordate_leaf.png`, `dict_obcordate_fruit.png` | `obcordate`, `obcordate leaf`, `obcordate fruit` |
| 26 | `Screenshot_28-9-2026_172949_.jpeg` | Obdeltoid leaf | `dict_obdeltoid.png` | `obdeltoid`, `obdeltoid leaf` |
| 27 | `Screenshot_28-9-2026_173055_.jpeg` | Oblique leaf base | `dict_oblique_leaf_base.png` | `oblique leaf base`, `oblique leaf` |
| 28 | `Screenshot_28-9-2026_173134_.jpeg` | Oblanceolate leaf | `dict_oblanceolate.png` | `oblanceolate`, `oblancelate`, `oblanceolate leaf` |
| 29 | `Screenshot_28-9-2026_17313_.jpeg` | Oblique Triangle | `dict_oblique_triangle.png` | `oblique triangle`, `oblique` |
| 30 | `Screenshot_28-9-2026_173215_.jpeg` | Obovate leaf | `dict_obovate.png` | `obovate`, `obovate leaf` |
| 31 | `Screenshot_28-9-2026_173226_.jpeg` | Obtuse leaf | `dict_obtuse_leaf.png` | `obtuse leaf`, `obtuse apex` |
| 32 | `Screenshot_28-9-2026_173239_.jpeg` | Ocreate structure (ocrea / ochrea) | `dict_ocrea.png` | `ocrea`, `ochrea`, `ocreate structure` |
| 33 | `Screenshot_28-9-2026_17323_.jpeg` | Oblong Leaf | `dict_oblong_leaf.png` | `oblong`, `oblong leaf` |
| 34 | `Screenshot_28-9-2026_17330_.jpeg` | Oestrogen structures (Oestradiol, Oestrone, Oestriol) | `dict_oestrogen.png` | `oestrogen`, `estrogen`, `oestradiol`, `estradiol`, `oestrone`, `estrone`, `oestriol` |
| 35 | `Screenshot_28-9-2026_173712_.jpeg` | Ogive (cumulative frequency curve) | `dict_ogive.png` | `ogive`, `cumulative frequency curve`, `cumulative frequency` |
| 36 | `Screenshot_28-9-2026_173812_.jpeg` | Okro pod (cross-section & vertical splits) | `dict_okro.png` | `okro`, `okra`, `lady's finger`, `gumbo` |
| 37 | `Screenshot_28-9-2026_173824_.jpeg` | Olecranon Process (elbow joint anatomy) | `dict_olecranon_process.png` | `olecranon process`, `olecranon`, `ulna` |
| 38 | `Screenshot_28-9-2026_173839_.jpeg` | Omasum of a cow (ruminant digestive tract) | `dict_omasum.png` | `omasum`, `manyplies`, `psalterium`, `ruminant stomach` |
| 39 | `Screenshot_28-9-2026_173926_.jpeg` | Operational amplifiers (inverting & non-inverting) | `dict_operational_amplifier.png` | `operational amplifier`, `op-amp`, `non-inverting amplifier`, `inverting amplifier` |
| 40 | `Screenshot_28-9-2026_17393_.jpeg` | Longitudinal section of onion (tunicated bulb) | `dict_onion.png` | `onion`, `tunicated bulb`, `bulb` |
| 41 | `Screenshot_28-9-2026_173941_.jpeg` | Chemical structure of alpha-Neoendorphin | `dict_neoendorphin.png` | `neoendorphin`, `alpha-neoendorphin`, `endorphin` |
| 42 | `Screenshot_28-9-2026_173959_.jpeg` | Optical fibre (laser light path and cladding) | `dict_optical_fibre.png` | `optical fibre`, `optical fiber`, `total internal reflection`, `core cladding` |
| 43 | `Screenshot_28-9-2026_174012_.jpeg` | Optical Isomerism (non-superimposable mirror images) | `dict_optical_isomerism.png` | `optical isomerism`, `enantiomers`, `chiral`, `chirality` |
| 44 | `Screenshot_28-9-2026_174018_.jpeg` | Optical pyrometer (apparatus diagram) | `dict_optical_pyrometer.png` | `optical pyrometer`, `pyrometer` |
| 45 | `Screenshot_28-9-2026_174032_.jpeg` | The operation of OR illustrated by the truth table | `dict_or_gate.png` | `or`, `or gate`, `or circuit`, `disjunction` |
| 46 | `Screenshot_28-9-2026_174059_.jpeg` | Orange, Citrus spp. (morphology & cross-section) | `dict_orange.png` | `orange`, `citrus`, `hesperidium` |
| 47 | `Screenshot_28-9-2026_174120_.jpeg` | S-orbital and P-orbital electron density shapes | `dict_atomic_orbitals.png` | `orbital`, `atomic orbital`, `s-orbital`, `p-orbital` |
| 48 | `Screenshot_28-9-2026_174137_.jpeg` | Orgel diagrams (D, F and P energy state splitting) | `dict_orgel_diagrams.png` | `orgel diagrams`, `orgel diagram` |
| 49 | `Screenshot_28-9-2026_17418_.jpeg` | Orbicular Leaf | `dict_orbicular_leaf.png` | `orbicular`, `orbicular leaf` |
| 50 | `Screenshot_28-9-2026_17420_.jpeg` | Orthogonal circles | `dict_orthogonal_circles.png` | `orthogonal`, `orthogonal circles` |
| 51 | `Screenshot_28-9-2026_174246_.jpeg` | An experimental set up to show the process of osmosis | `dict_osmosis_experiment.png` | `osmosis`, `osmosis experiment`, `semi-permeable membrane` |
| 52 | `Screenshot_28-9-2026_174320_.jpeg` | Ovate leaf | `dict_ovate_leaf.png` | `ovate`, `ovate leaf` |
| 53 | `Screenshot_28-9-2026_17432_.jpeg` | Otto cycle (P-V indicator diagram) | `dict_otto_cycle.png` | `otto cycle`, `otto engine`, `four-stroke cycle`, `four stroke engine` |
| 54 | `Screenshot_28-9-2026_174338_.jpeg` | Chemical Structure of oxalic acid (ethanedioic acid) | `dict_oxalic_acid.png` | `oxalic acid`, `ethanedioic acid` |
| 55 | `Screenshot_28-9-2026_174410_.jpeg` | Chemical structure of Oxazole | `dict_oxazole.png` | `oxazole`, `1,3-oxazole` |
| 56 | `Screenshot_28-9-2026_174444_.jpeg` | Chemical Structure of oxoanions (sulphate and sulphite) | `dict_oxoanion.png` | `oxoanion`, `oxyanion`, `sulphate`, `sulphite` |
| 57 | `Screenshot_28-9-2026_174456_.jpeg` | Chemical Structure of sulphuric acid (an example of oxoacid) / Chemical structure of Oxycodone | `dict_oxoacid.png`, `dict_oxycodone.png` | `oxoacid`, `oxoacids`, `sulphuric acid`, `oxycodone` |
| 58 | `Screenshot_28-9-2026_174522_.jpeg` | Chemical structure of Ozone (bond length & angle) | `dict_ozone.png` | `ozone`, `trioxygen` |
| 59 | `Screenshot_28-9-2026_174534_.jpeg` | Generalised reaction scheme of Ozonolysis | `dict_ozonolysis.png` | `ozonolysis`, `ozonide` |
| 60 | `Screenshot_28-9-2026_17457_.jpeg` | The production of Oxygen gas (laboratory preparation) | `dict_oxygen_production.png` | `oxygen`, `preparation of oxygen`, `oxygen gas` |


---

### Section L & M Series: Batch 1 (Completed) — Screenshots 1 to 101
Source Folder: `l-m diagrams/` (September 25-26, 2026 Pristine Author Captures)

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot_25-9-2026_172950_.jpeg` | Labiate corolla | `dict_labiate.png` | `labiate`, `labiate corolla`, `bilabiate`, `labiate flower` |
| 2 | `Screenshot_25-9-2026_173027_.jpeg` | Lacerate leaf | `dict_lacerate_leaf.png` | `lacerate`, `lacerate leaf` |
| 3 | `Screenshot_25-9-2026_173038_.jpeg` | Laciniate leaf | `dict_laciniate_leaf.png` | `laciniate`, `laciniate leaf` |
| 4 | `Screenshot_25-9-2026_17307_.jpeg` | Lactic acid (2-Hydroxypropanoic Acid) | `dict_lactic_acid.png` | `lactic acid`, `2-hydroxypropanoic acid`, `2-hydroxypropanoate`, `lactate` |
| 5 | `Screenshot_25-9-2026_173155_.jpeg` | Lactam and lactim tautomerism | `dict_lactam_lactim.png` | `lactam`, `lactim`, `lactam-lactim tautomerism`, `lactams` |
| 6 | `Screenshot_25-9-2026_173249_.jpeg` | Lami's Theorem (3 forces in equilibrium) | `dict_lamis_theorem.png` | `lami's theorem`, `lamis theorem`, `triangle of forces`, `forces in equilibrium` |
| 7 | `Screenshot_25-9-2026_173321_.jpeg` | Lanceolate leaf | `dict_lanceolate_leaf.png` | `lanceolate`, `lanceolate leaf` |
| 8 | `Screenshot_25-9-2026_17335_.jpeg` | Leaf lamina & Petal lamina | `dict_lamina.png` | `lamina`, `leaf lamina`, `petal lamina`, `blade` |
| 9 | `Screenshot_25-9-2026_173437_.jpeg` | Latin square (3 x 3) | `dict_latin_square.png` | `latin square`, `latin square design` |
| 10 | `Screenshot_25-9-2026_17346_.jpeg` | Electrical method for latent heat of evaporation | `dict_latent_heat_evaporation.png` | `latent heat of vaporization`, `latent heat of evaporation`, `specific latent heat of vaporization` |
| 11 | `Screenshot_26-9-2026_142138_.jpeg` | Layering (plant propagation) | `dict_layering.png` | `layering`, `plant layering`, `mound layering` |
| 12 | `Screenshot_26-9-2026_142221_.jpeg` | Leclanche dry cell | `dict_leclanche_cell.png` | `leclanche cell`, `leclanché cell`, `dry cell`, `zinc-carbon cell` |
| 13 | `Screenshot_26-9-2026_142245_.jpeg` | Types of lenses & symbols (converging / diverging) | `dict_lens_types.png` | `lens`, `convex lens`, `concave lens`, `converging lens`, `diverging lens`, `types of lenses` |
| 14 | `Screenshot_26-9-2026_14225_.jpeg` | Parts of a leaf | `dict_leaf_parts.png` | `leaf`, `parts of a leaf`, `leaf structure`, `petiole`, `midrib`, `leaf blade` |
| 15 | `Screenshot_26-9-2026_14232_.jpeg` | Leslie's Cube | `dict_leslies_cube.png` | `leslie's cube`, `leslies cube`, `thermal radiation cube` |
| 16 | `Screenshot_26-9-2026_142343_.jpeg` | Classes of levers (1st, 2nd, 3rd class) | `dict_levers.png` | `lever`, `first class lever`, `second class lever`, `third class lever`, `classes of levers` |
| 17 | `Screenshot_26-9-2026_142429_.jpeg` | Parabola line of symmetry & equation | `dict_parabola_line_of_symmetry.png` | `line of symmetry`, `axis of symmetry`, `parabola symmetry` |
| 18 | `Screenshot_26-9-2026_142442_.jpeg` | Linear Combination of Atomic Orbitals (LCAO) | `dict_lcao.png` | `linear combination of atomic orbitals`, `lcao`, `molecular orbital theory` |
| 19 | `Screenshot_26-9-2026_14248_.jpeg` | Ligulate Corolla | `dict_ligulate_corolla.png` | `ligulate`, `ligulate corolla`, `ray floret` |
| 20 | `Screenshot_26-9-2026_14267_.jpeg` | Linear leaf | `dict_linear_leaf.png` | `linear leaf` |
| 21 | `Screenshot_26-9-2026_142722_.jpeg` | Linear Graph (y = mx + c) | `dict_linear_graph.png` | `linear graph`, `linear equation graph`, `gradient`, `straight line graph` |
| 22 | `Screenshot_26-9-2026_142756_.jpeg` | Measuring linear expansivity of a metal | `dict_linear_expansivity.png` | `linear expansivity`, `thermal expansivity`, `coefficient of linear expansion` |
| 23 | `Screenshot_26-9-2026_142955_.jpeg` | Lipoic Acid | `dict_lipoic_acid.png` | `lipoic acid`, `alpha-lipoic acid`, `thioctic acid` |
| 24 | `Screenshot_26-9-2026_14336_.jpeg` | Lobed leaf | `dict_lobed_leaf.png` | `lobed leaf`, `lobed` |
| 25 | `Screenshot_26-9-2026_143633_.jpeg` | Benzene localized electrons | `dict_localized_electrons.png` | `localized electrons`, `delocalized electrons` |
| 26 | `Screenshot_26-9-2026_143659_.jpeg` | Ammonia lone pair trigonal pyramid | `dict_lone_pair.png` | `lone pair`, `lone pair electrons`, `unshared pair` |
| 27 | `Screenshot_26-9-2026_143734_.jpeg` | Lumbar vertebra of a mammal (anterior & lateral) | `dict_lumbar_vertebra.png` | `lumbar vertebra`, `lumbar vertebrae`, `vertebra` |
| 28 | `Screenshot_26-9-2026_143846_.jpeg` | Lysine | `dict_lysine.png` | `lysine`, `l-lysine` |
| 29 | `Screenshot_26-9-2026_143916_.jpeg` | Mach Angle (Mach cone) | `dict_mach_angle.png` | `mach angle`, `mach cone`, `mach number` |
| 30 | `Screenshot_26-9-2026_143922_.jpeg` | 2-methylpropenoic Acid (Methacrylic acid) | `dict_methacrylic_acid.png` | `2-methylpropenoic acid`, `methacrylic acid` |
| 31 | `Screenshot_26-9-2026_143933_.jpeg` | Ecstasy (MDMA) | `dict_mdma.png` | `mdma`, `ecstasy`, `3,4-methylenedioxymethamphetamine` |
| 32 | `Screenshot_26-9-2026_143946_.jpeg` | Magic-Angle Spinning | `dict_magic_angle_spinning.png` | `magic angle`, `magic-angle spinning` |
| 33 | `Screenshot_26-9-2026_144125_.jpeg` | Right hand grip rule (conductor & solenoid) | `dict_right_hand_grip_rule.png` | `right hand grip rule`, `grip rule`, `magnetic field of conductor` |
| 34 | `Screenshot_26-9-2026_14413_.jpeg` | Lateral view of a maggot | `dict_maggot.png` | `maggot`, `housefly larva` |
| 35 | `Screenshot_26-9-2026_144142_.jpeg` | Magnetic field lines near a bar magnet | `dict_magnetic_field_lines.png` | `magnetic field lines`, `magnetic flux lines`, `bar magnet` |
| 36 | `Screenshot_26-9-2026_14419_.jpeg` | 3 x 3 Magic Square | `dict_magic_square.png` | `magic square` |
| 37 | `Screenshot_26-9-2026_144225_.jpeg` | Magnifying glass | `dict_magnifying_glass.png` | `magnifying glass`, `simple magnifier` |
| 38 | `Screenshot_26-9-2026_144245_.jpeg` | Maize fruit (external & longitudinal section) | `dict_maize_fruit.png` | `maize fruit`, `caryopsis`, `grain of maize`, `maize grain` |
| 39 | `Screenshot_26-9-2026_14426_.jpeg` | Using electricity to magnetise a nail | `dict_electromagnet_nail.png` | `electromagnet`, `magnetisation`, `magnetization` |
| 40 | `Screenshot_26-9-2026_144312_.jpeg` | Major segment & Minor arc | `dict_major_segment.png` | `major segment`, `segment of a circle` |
| 41 | `Screenshot_26-9-2026_144334_.jpeg` | Maleic Anhydride | `dict_maleic_anhydride.png` | `maleic anhydride`, `furan-2,5-dione` |
| 42 | `Screenshot_26-9-2026_144345_.jpeg` | Malfatti Circles | `dict_malfatti_circles.png` | `malfatti circles`, `malfatti's circles` |
| 43 | `Screenshot_26-9-2026_144413_.jpeg` | Malleus (Hammer) of the human ear | `dict_malleus.png` | `malleus`, `hammer bone`, `ear ossicles` |
| 44 | `Screenshot_26-9-2026_14441_.jpeg` | Malpighian Body (Glomerulus + Bowman's capsule) | `dict_malpighian_body.png` | `malpighian body`, `malpighian corpuscle`, `renal corpuscle` |
| 45 | `Screenshot_26-9-2026_144712_.jpeg` | Left breast of a human showing the mammary glands | `dict_mammary_gland.png` | `mammary gland`, `mammary glands`, `lactiferous duct` |
| 46 | `Screenshot_26-9-2026_144721_.jpeg` | Lateral view of a rodent, an example of a mammal | `dict_mammal.png` | `mammal`, `mammalia`, `rodent` |
| 47 | `Screenshot_26-9-2026_144742_.jpeg` | Longitudinal section of a mango | `dict_mango.png` | `mango`, `drupe`, `mango fruit`, `longitudinal section of mango` |
| 48 | `Screenshot_26-9-2026_144813_.jpeg` | The manometer | `dict_manometer.png` | `manometer`, `u-tube manometer`, `gas pressure measurement` |
| 49 | `Screenshot_26-9-2026_144824_.jpeg` | Mechanism of Mannich Reaction | `dict_mannich_reaction.png` | `mannich reaction`, `mannich base` |
| 50 | `Screenshot_26-9-2026_144830_.jpeg` | Chemical structure of Mannitol | `dict_mannitol.png` | `mannitol`, `d-mannitol` |
| 51 | `Screenshot_26-9-2026_144845_.jpeg` | Earth crust showing the layers | `dict_mantle_earth.png` | `mantle`, `earth's mantle`, `upper mantle`, `lower mantle` |
| 52 | `Screenshot_26-9-2026_144850_.jpeg` | Mantle of a snail | `dict_mantle_snail.png` | `mantle (mollusc)`, `snail mantle`, `mollusc mantle` |
| 53 | `Screenshot_26-9-2026_144857_.jpeg` | Earth crust & snail mantle | `dict_mantle.png` | `mantle`, `mantle structure` |
| 54 | `Screenshot_26-9-2026_144914_.jpeg` | Margin of a leaf | `dict_leaf_margin.png` | `margin`, `leaf margin` |
| 55 | `Screenshot_26-9-2026_144920_.jpeg` | Marginal placentation of apocarpous gynoecium | `dict_marginal_placentation.png` | `marginal placentation`, `placentation` |
| 56 | `Screenshot_26-9-2026_144937_.jpeg` | Mass spectrometer | `dict_mass_spectrometer.png` | `mass spectrometer`, `mass spectrometry` |
| 57 | `Screenshot_26-9-2026_144948_.jpeg` | The mass spectrograph | `dict_mass_spectrograph.png` | `mass spectrograph` |
| 58 | `Screenshot_26-9-2026_14497_.jpeg` | Air layering (marcotting) | `dict_marcotting.png` | `marcotting`, `air layering` |
| 59 | `Screenshot_26-9-2026_145039_.jpeg` | Chemical structure of Melamine | `dict_melamine.png` | `melamine`, `1,3,5-triazine-2,4,6-triamine` |
| 60 | `Screenshot_26-9-2026_145049_.jpeg` | Chemical structure of Melatonin | `dict_melatonin.png` | `melatonin`, `n-acetyl-5-methoxytryptamine` |
| 61 | `Screenshot_26-9-2026_145055_.jpeg` | Chemical structure of Mellitic Acid | `dict_mellitic_acid.png` | `mellitic acid`, `benzenehexacarboxylic acid` |
| 62 | `Screenshot_26-9-2026_145120_.jpeg` | Plane of Symmetry of Meso Compound | `dict_meso_compound.png` | `meso compound`, `plane of symmetry`, `meso form` |
| 63 | `Screenshot_26-9-2026_145128_.jpeg` | Chemical structure of Mescaline | `dict_mescaline.png` | `mescaline`, `3,4,5-trimethoxyphenethylamine` |
| 64 | `Screenshot_26-9-2026_145145_.jpeg` | Human hand showing the metacarpal | `dict_metacarpal.png` | `metacarpal`, `metacarpals`, `carpal`, `carpus` |
| 65 | `Screenshot_26-9-2026_145155_.jpeg` | Structure of (Benzene) chromium tricarbonyl, an example of metallocene | `dict_metallocene.png` | `metallocene`, `sandwich compound`, `dibenzenechromium` |
| 66 | `Screenshot_26-9-2026_14516_.jpeg` | Chemical structure of Menthol | `dict_menthol.png` | `menthol`, `2-isopropyl-5-methylcyclohexanol` |
| 67 | `Screenshot_26-9-2026_145218_.jpeg` | Human leg showing the metatarsals | `dict_metatarsals.png` | `metatarsals`, `metatarsal`, `tarsals`, `tarsus` |
| 68 | `Screenshot_26-9-2026_14522_.jpeg` | Chemical structure of Metaldehyde | `dict_metaldehyde.png` | `metaldehyde` |
| 69 | `Screenshot_26-9-2026_145232_.jpeg` | Chemical structure of methanal | `dict_methanal.png` | `methanal`, `formaldehyde` |
| 70 | `Screenshot_26-9-2026_145247_.jpeg` | Chemical structure of Methionine | `dict_methionine.png` | `methionine`, `l-methionine` |
| 71 | `Screenshot_26-9-2026_145258_.jpeg` | Chemical structure of Methyl Orange | `dict_methyl_orange.png` | `methyl orange`, `helianthin` |
| 72 | `Screenshot_26-9-2026_145313_.jpeg` | Chemical structure of Methylbenzene (Toluene) | `dict_methylbenzene.png` | `methylbenzene`, `toluene` |
| 73 | `Screenshot_26-9-2026_145321_.jpeg` | Chemical structure of Methyl Salicylate | `dict_methyl_salicylate.png` | `methyl salicylate`, `oil of wintergreen` |
| 74 | `Screenshot_26-9-2026_145329_.jpeg` | Chemical structure of Methyl Violet | `dict_methyl_violet.png` | `methyl violet`, `gentian violet`, `crystal violet` |
| 75 | `Screenshot_26-9-2026_145339_.jpeg` | Chemical structure of Methylene Blue | `dict_methylene_blue.png` | `methylene blue`, `methylthioninium chloride` |
| 76 | `Screenshot_26-9-2026_145352_.jpeg` | Using a metre bridge to measure an unknown resistance | `dict_metre_bridge.png` | `metre bridge`, `meter bridge`, `slide wire bridge` |
| 77 | `Screenshot_26-9-2026_14535_.jpeg` | Chemical structure of Methyl Red | `dict_methyl_red.png` | `methyl red` |
| 78 | `Screenshot_26-9-2026_145415_.jpeg` | Michelson-Morley Interferometer | `dict_michelson_morley_interferometer.png` | `michelson-morley interferometer`, `interferometer`, `michelson interferometer` |
| 79 | `Screenshot_26-9-2026_145433_.jpeg` | A micrometer screw gauge | `dict_micrometer_screw_gauge.png` | `micrometer screw gauge`, `micrometer`, `screw gauge` |
| 80 | `Screenshot_26-9-2026_145453_.jpeg` | Carbon microphone | `dict_carbon_microphone.png` | `carbon microphone`, `microphone` |
| 81 | `Screenshot_26-9-2026_145512_.jpeg` | Fig. I: A simple light microscope | `dict_light_microscope.png` | `light microscope`, `optical microscope`, `simple light microscope` |
| 82 | `Screenshot_26-9-2026_145524_.jpeg` | Fig. II: A compound microscope | `dict_compound_microscope.png` | `compound microscope` |
| 83 | `Screenshot_26-9-2026_145538_.jpeg` | Simple and compound microscopes | `dict_microscope.png` | `microscope` |
| 84 | `Screenshot_26-9-2026_145554_.jpeg` | Midpoint (M) of a line segment | `dict_midpoint.png` | `midpoint`, `midpoint formula`, `midpoint of a line segment` |
| 85 | `Screenshot_26-9-2026_145625_.jpeg` | Minor Arc | `dict_minor_arc.png` | `minor arc`, `arc of a circle` |
| 86 | `Screenshot_26-9-2026_145640_.jpeg` | Mitochondrion | `dict_mitochondrion.png` | `mitochondrion`, `mitochondria`, `crista`, `cristae` |
| 87 | `Screenshot_26-9-2026_145659_.jpeg` | Mode of a graph | `dict_mode_graph.png` | `mode`, `modal class`, `mode of a graph`, `histogram mode` |
| 88 | `Screenshot_26-9-2026_14569_.jpeg` | Lateral view of a millepede | `dict_millipede.png` | `millipede`, `millepede`, `diplopoda` |
| 89 | `Screenshot_26-9-2026_145714_.jpeg` | Amplitude modulation (AM) | `dict_amplitude_modulation.png` | `amplitude modulation`, `am`, `modulation` |
| 90 | `Screenshot_26-9-2026_145729_.jpeg` | Molar | `dict_molar_tooth.png` | `molar`, `molar tooth`, `teeth` |
| 91 | `Screenshot_26-9-2026_145750_.jpeg` | Monochasium | `dict_monochasium.png` | `monochasium`, `cyme`, `monochasial cyme` |
| 92 | `Screenshot_26-9-2026_145759_.jpeg` | A monochord (sonometer) | `dict_monochord.png` | `monochord`, `sonometer` |
| 93 | `Screenshot_26-9-2026_145812_.jpeg` | The digestive tract of chicken (monogastric) | `dict_monogastric_digestive_tract.png` | `monogastric`, `monogastric digestive system`, `gizzard`, `proventriculus`, `avian digestive system` |
| 94 | `Screenshot_26-9-2026_145830_.jpeg` | Chemical structure of Morphine | `dict_morphine.png` | `morphine` |
| 95 | `Screenshot_26-9-2026_145845_.jpeg` | Mosquito life cycle stages and head / Fig. I: Larva of a mosquito / Fig. II: Pupa of a mosquito / Fig. III: Dorsal view of anopheles mosquito / Fig IV: Lateral view of the head of a mosquito | `dict_mosquito.png`, `dict_mosquito_larva.png`, `dict_mosquito_pupa.png`, `dict_anopheles_mosquito.png`, `dict_mosquito_proboscis.png` | `mosquito`, `life cycle of mosquito`, `mosquito larva`, `larva of a mosquito`, `mosquito pupa`, `pupa of a mosquito`, `anopheles`, `anopheles mosquito` |
| 96 | `Screenshot_26-9-2026_145853_.jpeg` | Moss plant | `dict_moss_plant.png` | `moss`, `moss plant`, `bryophyte`, `rhizoid`, `capsule (moss)` |
| 97 | `Screenshot_26-9-2026_145914_.jpeg` | A motor neurone | `dict_motor_neurone.png` | `motor neurone`, `motor neuron`, `efferent neurone`, `axon`, `dendron`, `myelin sheath` |
| 98 | `Screenshot_26-9-2026_145933_.jpeg` | The permanent-magnet moving-coil instrument | `dict_moving_coil_instrument.png` | `moving-coil instrument`, `moving coil galvanometer`, `galvanometer`, `pmmc` |
| 99 | `Screenshot_26-9-2026_145957_.jpeg` | Multicentre Bond (diboranes (B2H6)) | `dict_multicentre_bond.png` | `multicentre bond`, `multicenter bond`, `diborane`, `banana bond`, `three-centre two-electron bond` |
| 100 | `Screenshot_26-9-2026_15020_.jpeg` | Mushroom | `dict_mushroom.png` | `mushroom`, `agaricus`, `pileus`, `stipe`, `gills (fungi)`, `basidiomycete` |
| 101 | `Screenshot_26-9-2026_15057_.jpeg` | Myopia (Short Sightedness) | `dict_myopia.png` | `myopia`, `short sightedness`, `shortsightedness`, `nearsightedness` |


---

### Section P Series: Batch 1 (Completed) — Screenshots 1 to 50
Source Folder: `p_diagrams/` (September 29, 2026 Pristine Author Captures)

| # | Source Screenshot | Diagram Content / Caption | Generated Diagram File(s) | Mapped Dictionary Term(s) |
|---|---|---|---|---|
| 1 | `Screenshot_29-9-2026_152717_.jpeg` | Chemical Structure of 3-Phosphoglyceraldehyde | `dict_3_phosphoglyceraldehyde.png` | 3-phosphoglyceraldehyde, glyceraldehyde-3-phosphate, g3p, 3-phospho-d-glyceraldehyde |
| 2 | `Screenshot_29-9-2026_152738_.jpeg` | Paleolate (Lodicule) | `dict_paleolate.png` | paleolate, lodicule, paleola, lodicules |
| 3 | `Screenshot_29-9-2026_152747_.jpeg` | Palmately-lobed, simple leaf / Palmate compound leaf | `dict_palmately_lobed_leaf.png`, `dict_palmate_compound_leaf.png` | palmately lobed, palmately-lobed leaf, palmatifid, palmately lobed leaf, palmate, palmate leaf, palmate compound leaf, palmately compound leaf |
| 4 | `Screenshot_29-9-2026_152752_.jpeg` | Palmatisect leaf | `dict_palmatisect.png` | palmatisect, palmatisect leaf, palmatisect venation |
| 5 | `Screenshot_29-9-2026_15279_.jpeg` | Voltage-current characteristic of p-n junction | `dict_pn_junction.png` | p-n junction, pn junction, p-n junction diode, junction diode, semiconductor diode, voltage-current characteristic of p-n junction |
| 6 | `Screenshot_29-9-2026_15280_.jpeg` | Pandurate leaf | `dict_pandurate_leaf.png` | pandurate, pandurate leaf, panduriform, panduriform leaf |
| 7 | `Screenshot_29-9-2026_152816_.jpeg` | Chemical Structure of Pantothenic Acid | `dict_pantothenic_acid.png` | pantothenic acid, vitamin b5, pantothenate, pantothenate (vitamin b5) |
| 8 | `Screenshot_29-9-2026_152825_.jpeg` | Papilionaceous corolla | `dict_papilionaceous.png` | papilionaceous, papilionaceous corolla, butterfly flower, papilionate, papilionaceus |
| 9 | `Screenshot_29-9-2026_152832_.jpeg` | Parabolic reflection | `dict_parabolic_reflection.png` | parabolic reflection, parabolic dish, parabolic reflector, parabola (optics) |
| 10 | `Screenshot_29-9-2026_152843_.jpeg` | Parallax Error | `dict_parallax_error.png` | parallax error, parallax, parallax (measurement) |
| 11 | `Screenshot_29-9-2026_152850_.jpeg` | Chemical Structure of Paraldehyde | `dict_paraldehyde.png` | paraldehyde, 2,4,6-trimethyl-1,3,5-trioxane, para-acetaldehyde |
| 12 | `Screenshot_29-9-2026_152856_.jpeg` | Parallel Circuit | `dict_parallel_circuit.png` | parallel circuit, parallel connection, resistors in parallel, parallel combination |
| 13 | `Screenshot_29-9-2026_15288_.jpeg` | Panicle inflorescence | `dict_panicle.png` | panicle, panicle inflorescence, paniculate, paniculate inflorescence |
| 14 | `Screenshot_29-9-2026_152915_.jpeg` | Parallelodromous leaf | `dict_parallelodromous_leaf.png` | parallelodromous, parallelodromous leaf, parallel venation, parallel-veined leaf, parelleldromous |
| 15 | `Screenshot_29-9-2026_152922_.jpeg` | Parallelogram of vectors | `dict_parallelogram_of_vectors.png` | parallelogram of vectors, parallelogram law of vectors, parallelogram law, parallelogram rule |
| 16 | `Screenshot_29-9-2026_152931_.jpeg` | Parallelogram | `dict_parallelogram.png` | parallelogram, parallelogram (shape), height of a parallelogram |
| 17 | `Screenshot_29-9-2026_152939_.jpeg` | Paramecium | `dict_paramecium.png` | paramecium, paramecia, slipper animalcule, paramecium caudatum, ciliophora |
| 18 | `Screenshot_29-9-2026_152947_.jpeg` | Ectoparasites (louse, tick, tsetsefly) | `dict_ectoparasite.png` | ectoparasite, ectoparasites, louse, tick, tsetse fly, tsetsefly, external parasite |
| 19 | `Screenshot_29-9-2026_152955_.jpeg` | Chemical Structure of Parathion | `dict_parathion.png` | parathion, o,o-diethyl o-(4-nitrophenyl) phosphorothioate, parathion-ethyl |
| 20 | `Screenshot_29-9-2026_15297_.jpeg` | Parallelogram of forces | `dict_parallelogram_of_forces.png` | parallelogram of forces, parallelogram law of forces, resultant force parallelogram |
| 21 | `Screenshot_29-9-2026_153010_.jpeg` | Paripinnate leaves | `dict_paripinnate_leaf.png` | paripinnate, paripinnate leaf, even-pinnate, even pinnate, abruptly pinnate |
| 22 | `Screenshot_29-9-2026_153020_.jpeg` | Parking Orbit | `dict_parking_orbit.png` | parking orbit, geostationary orbit, transfer orbit, low earth orbit, geosynchronous transfer orbit |
| 23 | `Screenshot_29-9-2026_153027_.jpeg` | Parted leaf | `dict_parted_leaf.png` | parted, parted leaf, partite leaf, partite |
| 24 | `Screenshot_29-9-2026_15303_.jpeg` | Parietal structure (placentation) | `dict_parietal_placentation.png` | parietal placentation, parietal, placentation, parietal structure, ovule placentation |
| 25 | `Screenshot_29-9-2026_153052_.jpeg` | Pascal's Triangle | `dict_pascals_triangle.png` | pascal's triangle, pascals triangle, binomial coefficients, pascal triangle |
| 26 | `Screenshot_29-9-2026_153129_.jpeg` | Pectoral girdle | `dict_pectoral_girdle.png` | pectoral girdle, shoulder girdle, pectoral limb girdle, scapula, glenoid cavity, pectoral girdle of a mammal |
| 27 | `Screenshot_29-9-2026_153141_.jpeg` | Peltate leaf | `dict_peltate_leaf.png` | peltate, peltate leaf, shield-shaped leaf |
| 28 | `Screenshot_29-9-2026_153155_.jpeg` | A mammalian pelvic girdle | `dict_pelvic_girdle.png` | pelvic girdle, pelvic limb girdle, ilium, ischium, pubis, acetabulum, hip bone, os coxae |
| 29 | `Screenshot_29-9-2026_15317_.jpeg` | Pedate leaves | `dict_pedate_leaf.png` | pedate, pedate leaf, pedate venation, pedately compound |
| 30 | `Screenshot_29-9-2026_153222_.jpeg` | Chemical Structure of Pentaerythritol | `dict_pentaerythritol.png` | pentaerythritol, 2,2-bis(hydroxymethyl)-1,3-propanediol, tetramethylolmethane |
| 31 | `Screenshot_29-9-2026_153229_.jpeg` | Structural formula of Pentaerythritol Tetranitrate | `dict_pentaerythritol_tetranitrate.png` | pentaerythritol tetranitrate, petn, pentrite |
| 32 | `Screenshot_29-9-2026_153239_.jpeg` | Pentagon | `dict_pentagon.png` | pentagon, regular pentagon, pentagonal, five-sided polygon |
| 33 | `Screenshot_29-9-2026_153256_.jpeg` | Formation of peptide bond | `dict_peptide_bond.png` | peptide bond, peptide linkage, peptide, dipeptide, formation of peptide bond |
| 34 | `Screenshot_29-9-2026_15327_.jpeg` | Structural formula of Penicillin | `dict_penicillin.png` | penicillin, penicillin g, benzylpenicillin, beta-lactam, beta-lactam antibiotic |
| 35 | `Screenshot_29-9-2026_153310_.jpeg` | Perfoliate leaf | `dict_perfoliate_leaf.png` | perfoliate, perfoliate leaf, perfoliatum |
| 36 | `Screenshot_29-9-2026_153325_.jpeg` | Pericyclic Reaction | `dict_pericyclic_reaction.png` | pericyclic reaction, pericyclic reactions, cycloaddition, electrocyclic reaction, sigmatropic reaction |
| 37 | `Screenshot_29-9-2026_153356_.jpeg` | Tangent Periodic Function / Sine and Cosine Periodic Functions | `dict_tangent_periodic_function.png`, `dict_sine_cosine_periodic_function.png` | tangent periodic function, tangent function, sine and cosine periodic functions, sine function, cosine function, periodic functions, periodic function |
| 38 | `Screenshot_29-9-2026_153626_.jpeg` | Periodic Table of the Elements | `dict_periodic_table.png` | periodic table, periodic table of the elements, mendeleev periodic table, elements |
| 39 | `Screenshot_29-9-2026_153645_.jpeg` | Periscope | `dict_periscope.png` | periscope, prism periscope, reflection in periscope |
| 40 | `Screenshot_29-9-2026_15370_.jpeg` | Peristalsis of bolus in the oesophagus | `dict_peristalsis.png` | peristalsis, peristaltic movement, bolus, oesophagus |
| 41 | `Screenshot_29-9-2026_153727_.jpeg` | Examples of permanent magnet moving-coil instrument | `dict_moving_coil_instrument.png` | permanent magnet moving-coil instrument, moving-coil galvanometer, moving coil galvanometer, galvanometer |
| 42 | `Screenshot_29-9-2026_153742_.jpeg` | Chemical Structure of Peroxide Ion | `dict_peroxide_ion.png` | peroxide ion, peroxide, peroxides, o2 2- |
| 43 | `Screenshot_29-9-2026_153750_.jpeg` | Chemical Structure of Peroxymonosulfuric Acid | `dict_peroxymonosulfuric_acid.png` | peroxymonosulfuric acid, caro's acid, persulfuric acid |
| 44 | `Screenshot_29-9-2026_153758_.jpeg` | Perpendicular distance | `dict_perpendicular_distance.png` | perpendicular distance, perpendicular, shortest distance to a line |
| 45 | `Screenshot_29-9-2026_153813_.jpeg` | Personate structure | `dict_personate.png` | personate, personate corolla, personate structure |
| 46 | `Screenshot_29-9-2026_153830_.jpeg` | Petiole | `dict_petiole.png` | petiole, leaf stalk, petiolate |
| 47 | `Screenshot_29-9-2026_153854_.jpeg` | Phase Diagram - Phases of Matter and Phase Transitions | `dict_phase_diagram.png` | phase diagram, phases of matter, phase transitions, triple point, critical point |
| 48 | `Screenshot_29-9-2026_153910_.jpeg` | Phase difference of two waves | `dict_phase_difference.png` | phase difference, phase difference of two waves, phase angle, out of phase |
| 49 | `Screenshot_29-9-2026_153927_.jpeg` | Chemical Structure of phenol or phenolic acid | `dict_phenol.png` | phenol, phenolic acid, carbolic acid, hydroxybenzene |
| 50 | `Screenshot_29-9-2026_153939_.jpeg` | Chemical Structure of Phencyclidine | `dict_phencyclidine.png` | phencyclidine, pcp, phenylcyclohexyl piperidine |
