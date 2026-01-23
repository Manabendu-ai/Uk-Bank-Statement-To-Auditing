import pdfplumber
import re

DATE_RE = r"\d{1,2}\s[A-Za-z]{3}\s\d{2,4}"
AMOUNT_RE = r"-?\d+\.\d{2}"

def parse_text_stream(pdf_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")
            for line in lines:
                date_match = re.search(DATE_RE, line)
                amounts = re.findall(AMOUNT_RE, line)

                if date_match and len(amounts) >= 1:
                    amount = float(amounts[-1])
                    balance = float(amounts[-2]) if len(amounts) > 1 else None

                    txn = {
                        "date": date_match.group(),
                        "description": line.replace(date_match.group(), "").strip(),
                        "debit": abs(amount) if amount < 0 else 0.0,
                        "credit": amount if amount > 0 else 0.0,
                        "balance": balance
                    }
                    transactions.append(txn)

    return transactions
