import sys

try:
    import pytesseract
    print("pytesseract installed")
except ImportError:
    print("pytesseract NOT installed")

try:
    import easyocr
    print("easyocr installed")
except ImportError:
    print("easyocr NOT installed")

try:
    from PIL import Image
    print("PIL installed")
except ImportError:
    print("PIL NOT installed")
