from PIL import Image
import pytesseract

img_path = r"c:\Users\Desmond\Desktop\final_osmosis\section a-b images\Screenshot 2026-08-03 162733.png"
try:
    text = pytesseract.image_to_string(Image.open(img_path))
    print("OCR Output:")
    print(text)
except Exception as e:
    print("OCR Error:", e)
