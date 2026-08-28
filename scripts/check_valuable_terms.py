import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    diag_map = json.load(f)

with open("core_dictionary.js", "r", encoding="utf-8") as f:
    core_dict_content = f.read()

dict_words = set(re.findall(r'word:\s*"([^"]+)"', core_dict_content))
dict_words_lower = {w.lower().strip(): w for w in dict_words}

terms = [
    'dna', 'mitosis', 'meiosis', 'chloroplast', 'mitochondria', 'mitochondrion',
    'nephron', 'synapse', 'neuron', 'photosynthesis', 'osmosis',
    'electromagnetic spectrum', 'water cycle', 'hydrologic cycle', 'refraction',
    'reflection', 'electric circuit', 'series circuit', 'parallel circuit',
    'magnetic field', 'atom', 'bohr model', 'periodic table', 'states of matter',
    'covalent bond', 'ionic bond', 'fractional distillation', 'ph scale',
    'solar system', 'layers of the earth', 'solar eclipse', 'lunar eclipse',
    'plate tectonics', 'volcano', 'rock cycle', 'respiration', 'cell membrane',
    'plant cell', 'animal cell', 'digestive system', 'circulatory system',
    'respiratory system', 'nervous system', 'endocrine system', 'skeletal system'
]

print("TERM STATUS REPORT:")
print("-" * 65)
missing_valuable = []
existing_valuable = []

for t in terms:
    in_dict = t in dict_words_lower
    in_diag = t in diag_map
    diag_path = diag_map.get(t, "")
    if in_diag:
        existing_valuable.append(t)
        print(f"✅ {t:<28} | In Dict: {str(in_dict):<5} | Diagram: {diag_path}")
    else:
        missing_valuable.append((t, in_dict))
        print(f"❌ {t:<28} | In Dict: {str(in_dict):<5} | Diagram: MISSING")

print("-" * 65)
print(f"Total checked: {len(terms)} | Existing: {len(existing_valuable)} | Missing: {len(missing_valuable)}")
