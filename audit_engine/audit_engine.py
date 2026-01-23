def build_audit(txn, category, keyword, vat, vat_reason):
    return {
        "date": txn["date"],
        "description": txn["description"],
        "debit": txn["debit"],
        "credit": txn["credit"],
        "category": category,
        "vat": vat,
        "vat_logic": vat_reason,
        "rule_triggered": keyword
    }
