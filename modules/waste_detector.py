def detect_waste(df):

    alerts = []

    for cat in df["category"].unique():

        total = df[df["category"] == cat]["amount"].sum()

        if total > 5000 and cat != "Income":
            alerts.append(f"⚠ High spending in {cat}: ₹{total}")

    return alerts