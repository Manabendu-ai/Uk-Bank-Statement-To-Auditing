from pdf2image import convert_from_path
import pytesseract
import pdfplumber

def detect_bank(pdf_path):
    # 1️⃣ Try digital text first
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = pdf.pages[0].extract_text()
            if text:
                t = text.lower()
                if "hsbc" in t:
                    return "HSBC"
                if "barclays" in t:
                    return "BARCLAYS"
                if "monzo" in t:
                    return "MONZO"
                if "lloyds" in t:
                    return "LLOYDS"
    except:
        pass

    # 2️⃣ Fallback to OCR for scanned PDFs
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    ocr_text = pytesseract.image_to_string(images[0]).lower()

    if "hsbc" in ocr_text:
        return "HSBC"
    if "barclays" in ocr_text:
        return "BARCLAYS"
    if "monzo" in ocr_text:
        return "MONZO"
    if "lloyds" in ocr_text:
        return "LLOYDS"

    return "UNKNOWN"
