import streamlit as st
import pandas as pd
import os
import tempfile

from main_pipeline import run_pipeline

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="UK Bank Statement Processor",
    layout="wide"
)

st.title("🇬🇧 UK Bank Statement Processor")
st.caption(
    "Extracts debit & credit transactions, applies HMRC VAT logic, "
    "generates audit-ready Excel output."
)

st.divider()

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload UK Bank Statement PDF",
    type=["pdf"]
)

if uploaded_file:

    # Save uploaded PDF to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    st.success("PDF uploaded successfully")

    # -----------------------------
    # RUN PIPELINE
    # -----------------------------
    with st.spinner("Processing bank statement..."):
        try:
            result = run_pipeline(pdf_path)
        except Exception as e:
            st.error(f"Processing failed: {e}")
            st.stop()

    st.success("Processing completed")

    # -----------------------------
    # BANK INFO
    # -----------------------------
    st.subheader("🏦 Bank Detection")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Issuer Bank", result["issuer_bank"])

    with col2:
        st.write("**All Banks Detected:**")
        st.write(", ".join(result["banks_detected"]) or "None")

    st.divider()

    # -----------------------------
    # TRANSACTIONS TABLE
    # -----------------------------
    st.subheader("📄 Extracted Transactions")

    df = pd.DataFrame(result["transactions"])

    # Reorder columns exactly as required
    df = df[
        [
            "date",
            "description",
            "debit",
            "credit",
            "balance",
            "vat",
            "category",
            "audit",
        ]
    ]

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # VAT SUMMARY
    # -----------------------------
    st.subheader("💷 VAT Summary")

    vat_summary = (
        df.groupby("category")["vat"]
        .sum()
        .reset_index()
        .rename(columns={"vat": "Total VAT"})
    )

    st.table(vat_summary)

    # -----------------------------
    # EXCEL DOWNLOAD
    # -----------------------------
    st.subheader("⬇️ Download Excel")

    with open(result["excel_path"], "rb") as f:
        st.download_button(
            label="Download Accountant-Ready Excel",
            data=f,
            file_name=os.path.basename(result["excel_path"]),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Cleanup temp file
    os.remove(pdf_path)

else:
    st.info("Please upload a UK bank statement PDF to begin.")
