import pandas as pd
import os
from datetime import datetime

def build_excel(transactions, output_dir="data/output_excel"):
    """
    Takes final processed transactions and writes them to an Excel file.
    Returns the file path.
    """

    if not transactions:
        raise ValueError("No transactions to export")

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Convert to DataFrame
    df = pd.DataFrame(transactions)

    # Reorder columns (nice for accountants)
    preferred_order = [
        "date",
        "description",
        "amount",
        "type",
        "category",
        "vat_rate"
    ]

    existing_cols = [c for c in preferred_order if c in df.columns]
    df = df[existing_cols + [c for c in df.columns if c not in existing_cols]]

    # File name with timestamp
    filename = f"bank_statement_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    file_path = os.path.join(output_dir, filename)

    # Write Excel
    df.to_excel(file_path, index=False)

    return file_path
