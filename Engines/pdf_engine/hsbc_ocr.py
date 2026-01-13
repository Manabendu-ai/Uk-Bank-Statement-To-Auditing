from pdf2image import convert_from_path
import pytesseract
import re

def extract(pdf_path):
    images = convert_from_path(pdf_path)
    text = ""

    for img in images:
        text += pytesseract.image_to_string(img)

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    headers = []
    for line in lines:
        match = re.match(r"(\d{2}\s\w{3}\s\d{2})\s+(.*)", line)
        if match and "balance" not in line.lower():
            headers.append(match.groups())

    amounts = []
    for line in lines:
        for m in re.findall(r"\d+[\.,]\d{2}", line):
            amounts.append(float(m.replace(",", ".")))

    txns = []
    for i in range(min(len(headers), len(amounts))):
        date, desc = headers[i]
        txns.append({
            "date": date,
            "description": desc.lower(),
            "amount": amounts[i]
        })

    return txns
