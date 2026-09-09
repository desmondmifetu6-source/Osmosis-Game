import os
import urllib.request
import ssl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_DIR = os.path.join(BASE_DIR, 'assets', 'katex')
FONTS_DIR = os.path.join(TARGET_DIR, 'fonts')

os.makedirs(FONTS_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/"

FILES_TO_DOWNLOAD = [
    ("katex.min.css", os.path.join(TARGET_DIR, "katex.min.css")),
    ("katex.min.js", os.path.join(TARGET_DIR, "katex.min.js")),
    ("contrib/auto-render.min.js", os.path.join(TARGET_DIR, "auto-render.min.js")),
]

FONT_FILES = [
    "KaTeX_Main-Regular.woff2",
    "KaTeX_Main-Bold.woff2",
    "KaTeX_Main-Italic.woff2",
    "KaTeX_Math-Italic.woff2",
    "KaTeX_Math-BoldItalic.woff2",
    "KaTeX_Size1-Regular.woff2",
    "KaTeX_Size2-Regular.woff2",
    "KaTeX_Size3-Regular.woff2",
    "KaTeX_Size4-Regular.woff2",
    "KaTeX_AMS-Regular.woff2",
]

print("Downloading local KaTeX bundle...")

for rel_path, dest in FILES_TO_DOWNLOAD:
    url = BASE_URL + rel_path
    print(f"  -> {url} -> {dest}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read()
            with open(dest, 'wb') as out_f:
                out_f.write(content)
        print(f"     Downloaded {len(content):,} bytes")
    except Exception as e:
        print(f"     Error downloading {url}: {e}")

for font in FONT_FILES:
    url = BASE_URL + "fonts/" + font
    dest = os.path.join(FONTS_DIR, font)
    print(f"  -> Font: {font}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            content = resp.read()
            with open(dest, 'wb') as out_f:
                out_f.write(content)
        print(f"     Downloaded font {len(content):,} bytes")
    except Exception as e:
        print(f"     Error downloading font {font}: {e}")

print("KaTeX local bundle ready in assets/katex/")
