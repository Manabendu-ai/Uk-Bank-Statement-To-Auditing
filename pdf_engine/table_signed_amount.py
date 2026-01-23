import pdfplumber

def parse_signed_amount(pdf_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables() or []

            for table in tables:
                headers = [str(c).lower() if c else "" for c in table[0]]

                if "amount" not in " ".join(headers):
                    continue

                date_i = headers.index("date")
                desc_i = headers.index("description")
                amt_i = headers.index("amount")
                bal_i = next((i for i,h in enumerate(headers) if "balance" in h), None)

                for row in table[1:]:
                    try:
                        amt = float(row[amt_i])
                        transactions.append({
                            "date": row[date_i],
                            "description": row[desc_i].lower(),
                            "amount": amt,
                            "balance": float(row[bal_i]) if bal_i and row[bal_i] else None
                        })
                    except Exception:
                        continue

    return transactions
