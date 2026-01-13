from pdf_engine.pdf_parser import extract_transactions
from normalization_engine.transaction_normalizer import normalize
from category_engine.category_engine import categorize
from vat_engine.vat_engine import calculate_vat
from audit_engine.audit_engine import build_audit


pdf_path = "data/input_pdfs/sample1.pdf"
raw = extract_transactions(pdf_path)
clean = normalize(raw)

final = []

for txn in clean:
    category, keyword = categorize(txn)
    vat_rate, vat_reason = calculate_vat(txn)

    audit = build_audit(txn, category, keyword, vat_rate, vat_reason)

    final.append({
        **txn,
        "category": category,
        "vat_rate": vat_rate,
        "audit": audit
    })

print(final)
