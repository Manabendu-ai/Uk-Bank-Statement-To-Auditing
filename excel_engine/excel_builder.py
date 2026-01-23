import pandas as pd


def build_excel(transactions, output_path):
    df = pd.DataFrame(transactions)

    columns = [
        "date",
        "description",
        "debit",
        "credit",
        "balance",
        "vat",
        "category",
        "audit"
    ]

    for col in columns:
        if col not in df.columns:
            df[col] = None

    df = df[columns]

    df.to_excel(output_path, index=False)
