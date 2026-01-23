def normalize(transactions):
    clean = []

    for t in transactions:
        amt = float(t["amount"])

        txn_type = "credit" if amt > 100 else "debit"

        clean.append({
            "date": t["date"],
            "description": t["description"].lower(),
            "amount": amt,
            "type": txn_type
        })

    return clean
