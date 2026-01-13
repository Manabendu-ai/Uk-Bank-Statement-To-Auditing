import json

rules = json.load(open("category_engine/category_rules.json"))

def categorize(txn):
    for category, keywords in rules.items():
        for word in keywords:
            if word in txn["description"]:
                return category, word
    return "Uncategorized", None
