from pdf2image import convert_from_path
import pytesseract
import re

AMOUNT_RE = re.compile(r"-?\£?\d+\.\d{2}")

def parse_ocr(pdf_path):
    transactions = []

    images = convert_from_path(pdf_path, first_page=1, last_page=2)

    for img in images:
        text = pytesseract.image_to_string(img)

        for line in text.split("\n"):
            m = AMOUNT_RE.search(line)
            if not m:
                continue

            amt = float(m.group().replace("£",""))

            transactions.append({
                "date": None,
                "description": line.lower(),
                "amount": amt,
                "balance": None
            })

    return transactions
