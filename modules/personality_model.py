def spending_personality(df):

    dining=df[df["category"]=="Food"]["amount"].sum()

    savings=df[df["type"]=="income"]["amount"].sum()-df[df["type"]=="expense"]["amount"].sum()

    if dining>4000:
        return "Lifestyle Spender"

    if savings>20000:
        return "Saver"

    return "Balanced"