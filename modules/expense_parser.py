import re

def categorize(desc):

    d = desc.lower()

    if "uber" in d or "ola" in d:
        return "Travel"
    elif "swiggy" in d or "zomato" in d:
        return "Food"
    elif "amazon" in d:
        return "Shopping"
    elif "salary" in d:
        return "Income"
    return "Other"


def parse_expense_text(text):

    lines = text.split("\n")
    data = []

    for line in lines:
        match = re.search(r"(.+?)\s+(\d+)", line)

        if match:
            desc = match.group(1)
            amount = float(match.group(2))

            data.append({
                "description": desc,
                "amount": amount,
                "category": categorize(desc),
                "type": "income" if "salary" in desc.lower() else "expense"
            })

    return data