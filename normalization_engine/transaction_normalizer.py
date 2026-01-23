def normalize(transactions):
    normalized = []

    for txn in transactions:
        debit = float(txn.get("debit", 0))
        credit = float(txn.get("credit", 0))

        normalized.append({
            "date": txn.get("date"),
            "description": txn.get("description", "").lower(),
            "debit": debit,
            "credit": credit,
            "balance": txn.get("balance")
        })

    return normalized