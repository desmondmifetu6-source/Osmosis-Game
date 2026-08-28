import os
import json
import time
import sys
import urllib.request
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8")

WM_API = "https://commons.wikimedia.org/w/api.php"
HEADERS = {"User-Agent": "OsmosisSTEMDictionary/4.0 (educational visual project)"}

FIXES = {
    "meiosis": "Meiosis_Stages.svg",
    "synapse": "Chemical_synapse_schema_cropped.jpg",
    "magnetic field": "VFPt_cylindrical_magnet_thumb.svg",
    "states of matter": "States_of_matter.svg",
    "eye": "Schematic_diagram_of_the_human_eye_en.svg"
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
        print(f"Error {filename}: {e}")
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
        print(f"DL error: {e}")
        return False

with open("dictionary_diagrams_map.json", "r", encoding="utf-8") as f:
    diag_map = json.load(f)

for term, wm_file in FIXES.items():
    slug = term.replace(" ", "_").lower()
    dest_rel = f"diagrams/dict_{slug}.png"
    dest_path = os.path.join(os.getcwd(), dest_rel)
    print(f"Fetching [{term}] -> {wm_file}...")
    thumb_url = api_get_thumb_url(wm_file)
    if thumb_url and download_url(thumb_url, dest_path):
        diag_map[term] = dest_rel
        print(f"  ✅ Saved {term} ({os.path.getsize(dest_path):,} bytes)")
    else:
        print(f"  ❌ Failed {term}")
    time.sleep(0.3)

sorted_map = dict(sorted(diag_map.items()))
with open("dictionary_diagrams_map.json", "w", encoding="utf-8") as f:
    json.dump(sorted_map, f, indent=4, ensure_ascii=False)

with open("core_dictionary_diagrams.js", "w", encoding="utf-8") as f:
    f.write("// core_dictionary_diagrams.js (Audited & Cleaned STEM Diagram Mappings)\n\n")
    f.write("const DictionaryDiagrams = ")
    json.dump(sorted_map, f, indent=4, ensure_ascii=False)
    f.write(";\n\nif (typeof window !== 'undefined') {\n  window.DictionaryDiagrams = DictionaryDiagrams;\n}\n")

print(f"Done! Updated to {len(sorted_map)} diagrams.")
