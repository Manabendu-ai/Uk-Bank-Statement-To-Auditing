import json
import json
import os

BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(BASE_DIR, "vat_rules.json")

with open(RULES_PATH, "r") as f:
    vat_rules = json.load(f)


def calculate_vat(txn):
    desc = txn["description"]

    for k in vat_rules["zero_rate"]:
        if k in desc:
            return 0, "Zero Rated (HMRC)"

    for k in vat_rules["reduced_rate"]:
        if k in desc:
            return 5, "Reduced Rate (HMRC)"

    for k in vat_rules["exempt"]:
        if k in desc:
            return 0, "Exempt (HMRC)"

    return 20, "Standard Rate (HMRC)"
