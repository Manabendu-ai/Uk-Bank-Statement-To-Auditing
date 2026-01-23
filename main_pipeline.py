def run_pipeline(pdf_path):
    # -----------------------------
    # 1. Detect bank(s)
    # -----------------------------
    from pdf_engine.bank_detector import detect_banks

    bank_info = detect_banks(pdf_path)
    issuer_bank = bank_info["issuer_bank"]
    all_banks = bank_info["all_banks"]

    # -----------------------------
    # 2. Extract raw transactions
    # -----------------------------
    from pdf_engine.pdf_parser import extract_transactions

    raw_transactions = extract_transactions(pdf_path)

    if not raw_transactions:
        raise ValueError("No transactions extracted from PDF")

    # -----------------------------
    # 3. Normalize debit / credit
    # -----------------------------
    from normalization_engine.transaction_normalizer import normalize

    normalized = normalize(raw_transactions)

    # -----------------------------
    # 4. Categorize + VAT + Audit
    # -----------------------------
    from category_engine.category_engine import categorize
    from vat_engine.vat_engine import calculate_vat
    from audit_engine.audit_engine import build_audit

    final_transactions = []

    for txn in normalized:
        category, keyword = categorize(txn)

        taxable_amount = txn["debit"] if txn["debit"] > 0 else 0

        vat = calculate_vat(
            amount=taxable_amount,
            category=category
        )

        audit = build_audit(
            txn=txn,
            category=category,
            keyword=keyword,
            vat=vat,
            bank=issuer_bank
        )

        final_transactions.append({
            "date": txn["date"],
            "description": txn["description"],
            "debit": txn["debit"],
            "credit": txn["credit"],
            "balance": txn.get("balance"),
            "category": category,
            "vat": vat,
            "audit": audit
        })

    # -----------------------------
    # 5. FINAL RETURN (THIS WAS THE ISSUE)
    # -----------------------------
    return {
        "issuer_bank": issuer_bank,
        "all_banks": all_banks,
        "transactions": final_transactions
    }
