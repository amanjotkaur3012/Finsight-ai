import streamlit as st
import pandas as pd

from components.sidebar import sidebar

from mypages.dashboard import dashboard_page
from mypages.analytics import analytics_page
from mypages.parser import expense_parser_page
from mypages.advisor import advisor_page
from mypages.goals import goals_page
from mypages.notes import notes_page

st.set_page_config(page_title="FinSight AI", layout="wide")

# ================= SESSION INIT (NO AUTO LOAD) =================
if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame()

# ================= YOUR CUSTOM SIDEBAR =================
page = sidebar()

# ================= ROUTING =================
if page == "Expense Parser":
    expense_parser_page()

elif page == "Dashboard":
    dashboard_page()

elif page == "Analytics":
    analytics_page()

elif page == "AI Advisor":
    advisor_page()

elif page == "Goals Planner":
    goals_page()

elif page == "Notes":
    notes_page()

from utils.pdf_report import generate_pdf

# ================= PDF EXPORT =================
if st.sidebar.button("📄 Download Report"):

    if "transactions" in st.session_state and not st.session_state.transactions.empty:

        df = st.session_state.transactions.copy()
        df.columns = df.columns.str.lower()

        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna()

        if "type" not in df.columns:
            df["type"] = "expense"

        income = df[df["type"] == "income"]["amount"].sum()
        expense = df[df["type"] == "expense"]["amount"].sum()
        savings = income - expense
        savings_rate = (savings / income * 100) if income > 0 else 0

        # CATEGORY
        cat_summary = df[df["type"] == "expense"].groupby("category")["amount"].sum()

        top_cat = cat_summary.idxmax() if not cat_summary.empty else "N/A"

        # INSIGHTS
        insights = [
            f"Highest spending category: {top_cat}",
            f"Savings rate: {savings_rate:.1f}%"
        ]

        # RECOMMENDATIONS
        recommendations = []

        if savings_rate < 20:
            recommendations.append("Increase savings rate")
        else:
            recommendations.append("Maintain good financial discipline")

        if not cat_summary.empty and cat_summary.max() > 0.3 * expense:
            recommendations.append(f"Reduce spending in {top_cat}")

        # DATA PACK
        report_data = {
            "income": income,
            "expense": expense,
            "savings": savings,
            "savings_rate": savings_rate,
            "insights": insights,
            "recommendations": recommendations
        }

        file_path = generate_pdf(report_data)

        with open(file_path, "rb") as f:
            st.sidebar.download_button(
                label="⬇️ Download PDF",
                data=f,
                file_name="financial_report.pdf",
                mime="application/pdf"
            )

    else:
        st.sidebar.warning("⚠️ No data available")