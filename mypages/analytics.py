import streamlit as st
import pandas as pd
import plotly.express as px

def analytics_page():

    st.title("🧠 Financial Insights")

    # ================= CHECK =================
    if "transactions" not in st.session_state or st.session_state.transactions.empty:
        st.warning("⚠️ Please upload data first")
        st.stop()

    df = st.session_state.transactions.copy()

    # ================= CLEAN =================
    df.columns = df.columns.str.strip().str.lower()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    if "type" not in df.columns:
        df["type"] = "expense"

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    expense_df = df[df["type"] == "expense"]

    if expense_df.empty:
        st.warning("No expense data found")
        return

    # ================= 1. CATEGORY FOCUS =================
    st.markdown("## 🎯 Where Your Money Goes")

    cat_summary = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    fig1 = px.bar(
        x=cat_summary.index,
        y=cat_summary.values,
        labels={"x": "Category", "y": "Amount"},
        title="Spending by Category"
    )

    st.plotly_chart(fig1, use_container_width=True)

    top_cat = cat_summary.idxmax()
    percent = (cat_summary.max() / cat_summary.sum()) * 100

    st.info(f"👉 You spend most on **{top_cat}** ({percent:.1f}% of total expenses).")

    st.markdown("---")

    # ================= 2. SPENDING TREND =================
    st.markdown("## 📈 How Your Spending Changes Over Time")

    if "date" in expense_df.columns:

        expense_df = expense_df.copy()
        expense_df["month"] = expense_df["date"].dt.to_period("M").astype(str)

        monthly = expense_df.groupby("month")["amount"].sum()

        fig2 = px.line(
            x=monthly.index,
            y=monthly.values,
            markers=True,
            labels={"x": "Month", "y": "Expense"},
            title="Monthly Spending Trend"
        )

        st.plotly_chart(fig2, use_container_width=True)

        growth = monthly.pct_change().mean()

        if growth > 0:
            st.warning("👉 Your spending is gradually increasing over time.")
        else:
            st.success("👉 Your spending is stable or decreasing.")

    else:
        st.info("Upload data with date to see trend")

    st.markdown("---")

    # ================= 3. BIG SPENDING ALERT =================
    st.markdown("## 🚨 High Spending Alerts")

    avg = expense_df["amount"].mean()

    high_spends = expense_df[expense_df["amount"] > 2 * avg]

    if not high_spends.empty:

        fig3 = px.scatter(
            expense_df,
            x=expense_df.index,
            y="amount",
            color="category",
            title="Unusual High Transactions"
        )

        st.plotly_chart(fig3, use_container_width=True)

        st.warning("👉 Some transactions are much higher than your usual spending.")

    else:
        st.success("👉 No unusually high transactions detected.")

    st.markdown("---")

    # ================= FINAL INSIGHT =================
    st.markdown("## 💡 What This Means")

    if percent > 40:
        st.error(f"👉 A large portion of your money goes to {top_cat}. Consider reducing it.")
    else:
        st.success("👉 Your spending is well balanced across categories.")

    st.write("👉 Track monthly trends to stay in control of your finances.")