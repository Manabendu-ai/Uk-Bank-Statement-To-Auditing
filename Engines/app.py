import streamlit as st
import os
import pandas as pd

# Import engines
from pdf_engine.pdf_parser import extract_transactions
from normalization_engine.transaction_normalizer import normalize
from category_engine.category_engine import categorize
from vat_engine.vat_engine import calculate_vat
from audit_engine.audit_engine import build_audit
from excel_engine.excel_builder import build_excel

# --------------------------------------------------
# Streamlit page config
# --------------------------------------------------
st.set_page_config(
    page_title="UK Bank Statement AI",
    layout="wide"
)

st.title("🇬🇧 UK Bank Statement Processing System")
st.write(
    "Upload a UK bank statement PDF (scanned or digital) to generate "
    "VAT-classified, audit-ready transaction data."
)

# --------------------------------------------------
# File upload
# --------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload UK Bank Statement PDF",
    type=["pdf"]
)

if uploaded_file:
    # Ensure folders exist
    os.makedirs("data/input_pdfs", exist_ok=True)

    pdf_path = f"data/input_pdfs/{uploaded_file.name}"

    # Save uploaded file
    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF uploaded successfully")

    # --------------------------------------------------
    # Run pipeline
    # --------------------------------------------------
    with st.spinner("Processing bank statement..."):
        try:
            raw = extract_transactions(pdf_path)
            clean = normalize(raw)

            final = []

            for txn in clean:
                category, keyword = categorize(txn)
                vat_rate, vat_reason = calculate_vat(txn)

                audit = build_audit(
                    txn,
                    category,
                    keyword,
                    vat_rate,
                    vat_reason
                )

                final.append({
                    "date": txn["date"],
                    "description": txn["description"],
                    "amount": txn["amount"],
                    "type": txn["type"],
                    "category": category,
                    "vat_rate": vat_rate,
                    "audit_note": audit["audit_note"]
                })

        except Exception as e:
            st.error(f"Error processing PDF: {e}")
            st.stop()

    # --------------------------------------------------
    # Display results
    # --------------------------------------------------
    if not final:
        st.warning("No transactions were extracted from this PDF.")
        st.stop()

    df = pd.DataFrame(final)

    st.success("Processing completed successfully ✅")
    st.subheader("📊 Extracted Transactions")
    st.dataframe(df, use_container_width=True)

    # --------------------------------------------------
    # VAT Summary
    # --------------------------------------------------
    st.subheader("💷 VAT Summary")

    vat_summary = (
        df.groupby("vat_rate")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_amount"})
    )

    st.table(vat_summary)

    # --------------------------------------------------
    # Excel Export
    # --------------------------------------------------
    excel_path = build_excel(final)

    with open(excel_path, "rb") as f:
        st.download_button(
            label="📥 Download Excel",
            data=f,
            file_name=os.path.basename(excel_path),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
