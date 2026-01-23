def build_audit(txn, category, keyword, vat_rate, vat_reason):
    return {
        "description": txn["description"],
        "category": category,
        "rule_triggered": keyword,
        "vat_rate": vat_rate,
        "vat_logic": vat_reason,
        "audit_note": f"Categorized as {category} due to keyword '{keyword}'. VAT applied: {vat_reason}"
    }
