import os
import json
import shutil
import sys
import time
import urllib.request
import urllib.parse
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")

MAP_JSON = "dictionary_diagrams_map.json"
DIAG_JS = "core_dictionary_diagrams.js"
DIAGRAMS_DIR = "diagrams"
ARTIFACT_DIR = r"C:\Users\Desmond\.gemini\antigravity-ide\brain\4a8d65a9-de51-4a75-a227-bef3146ea89f"

# 1. Map generated images from brain artifact dir
GENERATED_IMAGES = {
    "atom": "atom_diagram_1787932865556.jpg",
    "mitochondrion": "mitochondrion_diagram_1787932910148.jpg",
    "electric circuit": "electric_circuit_diagram_1787932950713.jpg",
    "cell membrane": "cell_membrane_diagram_1787932977810.jpg",
    "solar eclipse": "solar_eclipse_diagram_1787933011282.jpg",
    "covalent bond": "covalent_bond_diagram_1787933053088.jpg",
}

# 2. Wikimedia Commons high quality educational diagrams
WM_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "OsmosisSTEMDictionary/4.0 (educational visual project)"}

WIKIMEDIA_SOURCES = {
    "ionic bond": "Ionic_bonding.svg",
    "meiosis": "Meiosis_diagram.svg",
    "lunar eclipse": "Geometry_of_a_Lunar_Eclipse.svg",
    "synapse": "Synapse_Illustration2_rubric.svg",
    "magnetic field": "Magnetic_field_due_to_bar_magnet.svg",
    "respiratory system": "Respiratory_system_complete_en.svg",
    "skeletal system": "Human_skeleton_front_en.svg",
    "states of matter": "Phase_change_diagram.svg",
    "rock cycle": "Rock_cycle.svg",
    "plate tectonics": "Tectonic_plates_boundaries_detailed-en.svg"
}

def api_get_thumb_url(filename, width=800):
    params = urllib.parse.urlencode({
        "action": "query", "prop": "imageinfo", "iiprop": "url",
        "iiurlwidth": str(width), "titles": f"File:{filename}", "format": "json",
    })
    try:
        req = urllib.request.Request(f"{WM_API}?{params}", headers=HEADERS)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        for page in data.get("query", {}).get("pages", {}).values():
            info = page.get("imageinfo", [{}])[0]
            return info.get("thumburl") or info.get("url")
    except Exception as e:
        print(f"    API error for {filename}: {e}")
    return None

def download_url(url, dest):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 1000:
            return False
        with open(dest, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    DL error: {e}")
        return False

def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    with open(MAP_JSON, "r", encoding="utf-8") as f:
        diag_map = json.load(f)

    # Copy and optimize generated diagrams
    print("--- 1. Processing AI Generated Educational Diagrams ---")
    for term, src_file in GENERATED_IMAGES.items():
        src_path = os.path.join(ARTIFACT_DIR, src_file)
        if not os.path.exists(src_path):
            print(f"  ❌ Source not found: {src_path}")
            continue

        slug = term.replace(" ", "_").lower()
        dest_rel = f"diagrams/dict_{slug}.png"
        dest_path = os.path.join(os.getcwd(), dest_rel)

        # Convert / save as crisp PNG
        try:
            with Image.open(src_path) as img:
                img.save(dest_path, "PNG", optimize=True)
            diag_map[term] = dest_rel
            print(f"  ✅ Integrated [{term}] -> {dest_rel} ({os.path.getsize(dest_path):,} bytes)")
        except Exception as e:
            print(f"  ❌ Error processing {term}: {e}")

    # Sourcing Wikimedia Commons diagrams
    print("\n--- 2. Sourcing Wikimedia Educational Diagrams ---")
    for term, wm_file in WIKIMEDIA_SOURCES.items():
        slug = term.replace(" ", "_").lower()
        dest_rel = f"diagrams/dict_{slug}.png"
        dest_path = os.path.join(os.getcwd(), dest_rel)

        print(f"Fetching [{term}] ({wm_file})...")
        thumb_url = api_get_thumb_url(wm_file, width=800)
        if thumb_url and download_url(thumb_url, dest_path):
            diag_map[term] = dest_rel
            print(f"  ✅ Downloaded & Integrated [{term}] -> {dest_rel} ({os.path.getsize(dest_path):,} bytes)")
        else:
            print(f"  ⚠️ Failed downloading {term}")
        time.sleep(0.3)

    # Re-sort map and save
    sorted_map = dict(sorted(diag_map.items()))
    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)

    with open(DIAG_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(sorted_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")

    print(f"\nSuccessfully updated {MAP_JSON} and regenerated {DIAG_JS} with {len(sorted_map)} total diagrams!")

if __name__ == "__main__":
    main()
