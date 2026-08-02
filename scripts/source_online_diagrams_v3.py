"""
source_online_diagrams_v3.py
============================
Fixes the 13 failed downloads from v2 by using corrected Wikimedia filenames.
Run from final_osmosis/:
    python scripts/source_online_diagrams_v3.py
"""

import os, json, sys, time
import urllib.request, urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

DIAGRAMS_DIR = "diagrams"
MAP_JSON     = "dictionary_diagrams_map.json"
DIAGRAMS_JS  = "core_dictionary_diagrams.js"
WM_API       = "https://commons.wikimedia.org/w/api.php"

HEADERS = {
    "User-Agent": "OsmosisSTEMDictionary/3.0 (educational project)"
}

# Corrected filenames for the 13 failures
FIXES = {
    "bell jar":                             ("diagrams/dict_bell_jar.png",                    "Belljar.svg"),
    "myopia (nearsightedness)":             ("diagrams/dict_myopia_nearsightedness.png",       "Myopia2.svg"),
    "acceleration-time-graph (a-t graph)": ("diagrams/dict_acceleration_time_graph_a_t_graph.png", "Kinematic_graphs_of_a_car.png"),
    "galilean telescope":                   ("diagrams/dict_galilean_telescope.png",            "Galilean_telescope_2.svg"),
    "alloy":                                ("diagrams/dict_alloy.png",                        "Alloy_interstitial.svg"),
    "potometer":                            ("diagrams/dict_potometer.png",                    "Potometer_en.svg"),
    "density":                              ("diagrams/dict_density.png",                      "Relative_density.svg"),
    "demodulation":                         ("diagrams/dict_demodulation.png",                 "Amdemodulation.gif"),
    "atom":                                 ("diagrams/dict_atom.png",                         "Bohr_atom_model.svg"),
    "meiosis":                              ("diagrams/dict_meiosis.png",                      "Meiosis_Stages.svg"),
    "lever":                                ("diagrams/dict_lever.png",                        "Lever.svg"),
    "plant":                                ("diagrams/dict_plant.png",                        "Fleur_delphineum.jpg"),
    "leaf":                                 ("diagrams/dict_leaf.png",                         "Leaf_1_web.jpg"),
}


def api_get_thumb_url(filename, width=600):
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
        print(f"    API error: {e}")
    return None


def download_url(url, dest):
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 500:
            return False
        with open(dest, "wb") as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"    DL error: {e}")
        return False


def main():
    os.makedirs(DIAGRAMS_DIR, exist_ok=True)
    with open(MAP_JSON, encoding="utf-8") as f:
        diag_map = json.load(f)

    success, failed = 0, []

    for term, (rel_path, wm_filename) in FIXES.items():
        print(f"\n[{term}]  File: {wm_filename}")
        thumb_url = api_get_thumb_url(wm_filename, width=600)
        if not thumb_url:
            print(f"  ❌  API resolution failed")
            failed.append((term, wm_filename))
            time.sleep(0.5)
            continue
        print(f"  URL: {thumb_url}")
        ok = download_url(thumb_url, rel_path)
        if ok:
            diag_map[term.lower().strip()] = rel_path
            print(f"  ✅  Saved ({os.path.getsize(rel_path):,} bytes)")
            success += 1
        else:
            failed.append((term, wm_filename))
            print(f"  ❌  Download failed")
        time.sleep(0.4)

    print(f"\n{'='*55}")
    print(f"Fixed: {success} / {len(FIXES)}")
    if failed:
        print("Still failed:", [t for t, _ in failed])

    with open(MAP_JSON, "w", encoding="utf-8") as f:
        json.dump(diag_map, f, indent=4, ensure_ascii=False)

    with open(DIAGRAMS_JS, "w", encoding="utf-8") as f:
        f.write("// core_dictionary_diagrams.js (Auto-extracted + Online-sourced v3)\n\n")
        f.write("const DictionaryDiagrams = ")
        json.dump(diag_map, f, indent=4, ensure_ascii=False)
        f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")

    print(f"Saved {MAP_JSON} and regenerated {DIAGRAMS_JS}")


if __name__ == "__main__":
    main()
