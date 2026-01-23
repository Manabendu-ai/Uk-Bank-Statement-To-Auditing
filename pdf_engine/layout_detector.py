import pdfplumber

def detect_layout(pdf_path):
    """
    Detects structural layout of the statement
    """

    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[0]

            tables = page.extract_tables()
            text = (page.extract_text() or "").lower()

            # Case 1: Table with Money In / Money Out
            for table in tables or []:
                headers = [str(c).lower() for c in table[0] if c]
                if any("money in" in h or "credit" in h for h in headers) and \
                   any("money out" in h or "debit" in h for h in headers):
                    return "TABLE_DEBIT_CREDIT"

            # Case 2: Table with Amount column
            for table in tables or []:
                headers = [str(c).lower() for c in table[0] if c]
                if any("amount" in h for h in headers):
                    return "TABLE_SIGNED_AMOUNT"

            # Case 3: Digital text stream
            if any(k in text for k in ["£", "gbp", "balance"]):
                return "TEXT_STREAM"

    except Exception:
        pass

    return "OCR_FALLBACK"
