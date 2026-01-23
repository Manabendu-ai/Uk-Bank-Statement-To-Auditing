import pdfplumber

def parse_table_debit_credit(pdf_path):
    transactions = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables() or []

            for table in tables:
                headers = [str(c).lower() if c else "" for c in table[0]]

                try:
                    date_i = headers.index("date")
                    desc_i = headers.index("description")
                    credit_i = next(i for i,h in enumerate(headers) if "money in" in h or "credit" in h)
                    debit_i = next(i for i,h in enumerate(headers) if "money out" in h or "debit" in h)
                    bal_i = next(i for i,h in enumerate(headers) if "balance" in h)
                except ValueError:
                    continue

                for row in table[1:]:
                    try:
                        debit = float(row[debit_i]) if row[debit_i] else None
                        credit = float(row[credit_i]) if row[credit_i] else None

                        transactions.append({
                            "date": row[date_i],
                            "description": row[desc_i].lower(),
                            "amount": credit if credit else -debit,
                            "balance": float(row[bal_i]) if row[bal_i] else None
                        })
                    except Exception:
                        continue

    return transactions
