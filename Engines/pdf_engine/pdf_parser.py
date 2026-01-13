from .bank_detector import detect_bank
from .hsbc_ocr import extract as hsbc_extract
from .barclays_table import extract as barclays_extract
from .monzo_text import extract as monzo_extract

def extract_transactions(pdf_path):
    bank = detect_bank(pdf_path)

    print("Detected bank:", bank)

    if bank == "HSBC":
        return hsbc_extract(pdf_path)
    elif bank == "BARCLAYS":
        return barclays_extract(pdf_path)
    elif bank == "MONZO":
        return monzo_extract(pdf_path)
    else:
        raise Exception("Unsupported bank format")
