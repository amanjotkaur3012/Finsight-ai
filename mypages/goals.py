import streamlit as st
import pandas as pd
import os

def goals_page():

    st.title("🎯 Smart Goal Tracking")

    file_path = "data/goals.csv"

    # ================= LOAD GOAL =================
    if os.path.exists(file_path):
        goal_df = pd.read_csv(file_path)
        goal = goal_df.iloc[0]
    else:
        goal = None

    # ================= SET NEW GOAL =================
    st.markdown("## 📝 Set Your Goal")

    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("💰 Target Amount (₹)", min_value=0)

    with col2:
        months = st.number_input("📅 Duration (Months)", min_value=1)

    if st.button("Save Goal"):

        if amount == 0:
            st.warning("Enter valid amount")
            return

        goal_data = pd.DataFrame([{
            "target": amount,
            "months": months
        }])

        os.makedirs("data", exist_ok=True)
        goal_data.to_csv(file_path, index=False)

        st.success("✅ Goal saved successfully")
        st.rerun()

    # ================= TRACKING =================
    if goal is not None:

        st.markdown("---")
        st.markdown("## 📊 Goal Progress")

        target = goal["target"]
        months = goal["months"]

        # ===== GET USER DATA =====
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

        else:
            savings = 0

        # ================= CALCULATIONS =================
        progress = min(1.0, savings / target) if target > 0 else 0
        remaining = max(0, target - savings)
        monthly_required = remaining / months if months > 0 else 0

        # ================= UI =================
        col1, col2, col3 = st.columns(3)

        col1.metric("🎯 Target", f"₹{target:,.0f}")
        col2.metric("💰 Saved", f"₹{savings:,.0f}")
        col3.metric("📉 Remaining", f"₹{remaining:,.0f}")

        st.markdown("### 📈 Progress")
        st.progress(progress)
        st.write(f"{progress*100:.1f}% completed")

        # ================= STATUS =================
        st.markdown("## 🚦 Goal Status")

        if progress >= 1:
            st.success("🎉 Goal Achieved!")
        elif progress > 0.6:
            st.success("✅ On Track")
        elif progress > 0.3:
            st.warning("⚡ Moderate Progress")
        else:
            st.error("🚨 Behind Schedule")

        # ================= SMART INSIGHTS =================
        st.markdown("## 🤖 Smart Insights")

        st.write(f"👉 You need ₹{monthly_required:,.0f}/month to reach goal")

        if monthly_required > savings * 0.5:
            st.warning("⚠️ Required savings too high — extend timeline")

        if savings <= 0:
            st.error("🚨 No savings detected — reduce expenses first")

        # ================= DELETE GOAL =================
        st.markdown("---")

        if st.button("❌ Delete Goal"):
            os.remove(file_path)
            st.success("Goal deleted")
            st.rerun()

    else:
        st.info("No goal set yet")