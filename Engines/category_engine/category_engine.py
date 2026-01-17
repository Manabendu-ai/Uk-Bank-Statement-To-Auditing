import json
import os

BASE_DIR = os.path.dirname(__file__)
RULES_PATH = os.path.join(BASE_DIR, "category_rules.json")

with open(RULES_PATH, "r") as f:
    rules = json.load(f)


def categorize(txn):
    for category, keywords in rules.items():
        for word in keywords:
            if word in txn["description"]:
                return category, word
    return "Uncategorized", None
