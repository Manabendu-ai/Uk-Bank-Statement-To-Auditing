from .layout_detector import detect_layout
from .table_debit_credit import parse_table_debit_credit
from .table_signed_amount import parse_signed_amount
from .text_stream import parse_text_stream
from .ocr_fallback import parse_ocr

def extract_transactions(pdf_path):
    layout = detect_layout(pdf_path)

    if layout == "TABLE_DEBIT_CREDIT":
        txns = parse_table_debit_credit(pdf_path)
        if txns:
            return txns

    if layout == "TABLE_SIGNED_AMOUNT":
        txns = parse_signed_amount(pdf_path)
        if txns:
            return txns

    # 🔥 ALWAYS try text stream
    txns = parse_text_stream(pdf_path)
    if txns:
        return txns

    # 🔥 LAST resort
    return parse_ocr(pdf_path)