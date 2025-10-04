# ocr_utils.py
import os
import io
from PIL import Image
import pytesseract

# Optional Windows: set explicit tesseract.exe path via env var
# set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
TESS_CMD = os.getenv("TESSERACT_CMD")
if TESS_CMD and os.path.exists(TESS_CMD):
    pytesseract.pytesseract.tesseract_cmd = TESS_CMD

def read_image_bytes(image_bytes: bytes, lang: str = "eng", config: str = "") -> str:
    img = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(img, lang=lang, config=config)
    return (text or "").strip()
