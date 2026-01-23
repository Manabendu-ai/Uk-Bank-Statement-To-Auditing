import json

import os


BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(BASE_DIR, "vat_rules.json")

with open(RULES_PATH, "r") as f:
    VAT_RULES = json.load(f)

def calculate_vat(amount, category):
    """
    amount: positive float (taxable amount)
    category: string
    """
    rule = VAT_RULES.get(category, VAT_RULES["DEFAULT"])
    rate = rule["rate"]
    vat = round(amount * rate / 100, 2)

    return {
        "vat_amount": vat,
        "vat_rate": rate,
        "vat_logic": rule["logic"]
    }