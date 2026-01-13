import pdfplumber
import re

def extract(pdf_path):
    txns = []

    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    for line in text.split("\n"):
        m = re.search(r"(\d{2}/\d{2}/\d{4})\s+(.*)\s+(-?\d+\.\d{2})", line)
        if m:
            date, desc, amt = m.groups()
            txns.append({
                "date": date,
                "description": desc.lower(),
                "amount": float(amt)
            })

    return txns
