import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# -------------------------
# BANK KEYWORDS (EXTENDABLE)
# -------------------------
BANK_KEYWORDS = {
    "HSBC": ["hsbc"],
    "BARCLAYS": ["barclays"],
    "LLOYDS": ["lloyds"],
    "NATWEST": ["natwest"],
    "SANTANDER": ["santander"],
    "MONZO": ["monzo"],
    "STARLING": ["starling"],
    "REVOLUT": ["revolut"],
    "COOPERATIVE": ["co-operative", "coop"],
}

# -------------------------
# FIND BANK NAMES IN TEXT
# -------------------------
def find_banks(text: str):
    found = set()
    text = text.lower()

    for bank, keywords in BANK_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                found.add(bank)

    return found


# -------------------------
# MAIN BANK DETECTOR
# -------------------------
def detect_banks(pdf_path: str):
    banks = set()
    source = "digital"

    # 1️⃣ Try DIGITAL TEXT (pdfplumber)
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:2]:
                text = page.extract_text()
                if text:
                    banks.update(find_banks(text))
    except Exception:
        pass

    # 2️⃣ OCR fallback ONLY if nothing found
    if not banks:
        source = "ocr"
        images = convert_from_path(pdf_path, first_page=1, last_page=2)
        for img in images:
            ocr_text = pytesseract.image_to_string(img)
            banks.update(find_banks(ocr_text))

    # 3️⃣ Final issuer decision
    issuer_bank = list(banks)[0] if banks else "UNKNOWN"

    # ✅ ALWAYS return the same structure
    return {
    "issuer_bank": issuer_bank,
    "all_banks": list(banks),
    "source": source
    }
