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

## 4. Quality Standards
1. **Pristine Author Framing**: High-resolution user captures preserved with complete clarity.
2. **Dual Map Consistency**: `dictionary_diagrams_map.json` and `core_dictionary_diagrams.js` remain synchronized and sorted.



