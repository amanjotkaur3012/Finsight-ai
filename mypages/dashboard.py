import streamlit as st
import pandas as pd
import plotly.express as px

def dashboard_page():

    st.title("📊 FinSight AI Dashboard")

    if "transactions" not in st.session_state or st.session_state.transactions.empty:
        st.warning("⚠️ Please upload data first")
        return

    df = st.session_state.transactions.copy()

    # ================= CLEAN =================
    df.columns = df.columns.str.strip().str.lower()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    if "type" not in df.columns:
        df["type"] = "expense"

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # ================= SPLIT =================
    expense_df = df[df["type"] == "expense"]
    income_df = df[df["type"] == "income"]

    income = income_df["amount"].sum()
    expense = expense_df["amount"].sum()
    savings = income - expense

    savings_rate = (savings / income * 100) if income > 0 else 0

    # ================= KPI =================
    st.markdown("## 💼 Financial Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Income", f"₹{income:,.0f}")
    col2.metric("💸 Expense", f"₹{expense:,.0f}")
    col3.metric("💼 Savings", f"₹{savings:,.0f}")
    col4.metric("📊 Savings %", f"{savings_rate:.1f}%")

    st.markdown("---")

    # ================= CATEGORY =================
    st.markdown("## 📊 Spending Breakdown")

    cat_summary = expense_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    col1, col2 = st.columns(2)

    fig1 = px.pie(
        cat_summary,
        names=cat_summary.index,
        values=cat_summary.values,
        hole=0.6,
        title="Spending Distribution"
    )
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        cat_summary,
        x=cat_summary.index,
        y=cat_summary.values,
        color=cat_summary.index,
        title="Category Comparison"
    )
    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ================= MONTHLY COMPARISON =================
    st.markdown("## 📅 Monthly Income vs Expense")

    if "date" in df.columns:

        df = df.copy()
        df["month"] = df["date"].dt.strftime("%b %Y")

        monthly_income = df[df["type"] == "income"].groupby("month")["amount"].sum()
        monthly_expense = df[df["type"] == "expense"].groupby("month")["amount"].sum()

        monthly_df = pd.DataFrame({
            "Income": monthly_income,
            "Expense": monthly_expense
        }).fillna(0)

        monthly_df = monthly_df.reset_index()

        fig = px.bar(
            monthly_df,
            x="month",
            y=["Income", "Expense"],
            barmode="group",
            title="Monthly Income vs Expense"
        )

        st.plotly_chart(fig, use_container_width=True)

        if not monthly_df.empty:
            last = monthly_df.iloc[-1]

            if last["Expense"] > last["Income"]:
                st.error("👉 You are spending more than you earn in the latest month.")
            else:
                st.success("👉 Your income is higher than expenses — good financial balance.")

    else:
        st.info("Upload data with date to see monthly comparison")

    st.markdown("---")

    # ================= AI INSIGHTS =================
    st.markdown("## 🤖 AI Insights")

    col1, col2 = st.columns(2)

    if not cat_summary.empty:
        top_cat = cat_summary.idxmax()
        top_val = cat_summary.max()
        col1.error(f"🚨 Highest spending: {top_cat} (₹{top_val:,.0f})")

    if savings_rate < 20:
        col2.error("⚠️ Low savings rate — risky financial behavior")
    elif savings_rate < 40:
        col2.warning("⚡ Moderate savings — can improve")
    else:
        col2.success("✅ Strong financial health")

    st.markdown("---")

    # ================= WASTE DETECTION =================
    st.markdown("## 🚨 Smart Waste Detection")

    waste = cat_summary[cat_summary > 0.25 * expense]

    if not waste.empty:
        for cat, val in waste.items():
            percent = (val / expense) * 100
            st.warning(f"👉 {cat}: ₹{val:,.0f} ({percent:.1f}%) — Too High")
    else:
        st.success("✅ Spending is balanced across categories")

    st.markdown("---")

    # ================= RECOMMENDATIONS =================
    st.markdown("## 💡 Recommendations")

    if savings_rate < 20:
        st.write("• Reduce discretionary spending (shopping, entertainment)")
        st.write("• Set monthly budget limits")
    elif savings_rate < 40:
        st.write("• Optimize 1–2 high expense categories")
        st.write("• Increase savings automation")
    else:
        st.write("• Consider investments (SIP, stocks)")
        st.write("• Maintain current financial discipline")