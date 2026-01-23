import pdfplumber

def extract(pdf_path):
    txns = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if not table:
                continue

            for row in table[1:]:
                txns.append({
                    "date": row[0],
                    "description": row[1].lower(),
                    "amount": float(row[2] or 0) - float(row[3] or 0)
                })

    return txns
