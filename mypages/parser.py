import streamlit as st
import pandas as pd

def expense_parser_page():

    st.title("📥 Add Your Data")

    # ================= CLEAR DATA =================
    if st.button("🗑️ Clear Data"):
        st.session_state.transactions = pd.DataFrame()
        st.success("Data cleared ✅")

    tab1, tab2 = st.tabs(["✍️ Manual Input", "📂 Upload CSV/Excel"])

    # ================= MANUAL INPUT =================
    with tab1:

        text = st.text_area(
            "Enter like:\nFood 200 expense\nSalary 50000 income"
        )

        if st.button("Add Data"):

            rows = []
            for line in text.split("\n"):
                parts = line.split()

                if len(parts) >= 2:
                    rows.append({
                        "category": parts[0],
                        "amount": parts[1],
                        "type": parts[2] if len(parts) > 2 else "expense"
                    })

            df = pd.DataFrame(rows)

            if df.empty:
                st.warning("⚠️ No valid data")
                return

            df.columns = df.columns.str.lower()
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            df = df.dropna()

            # ✅ SAVE (NO DUPLICATION)
            st.session_state.transactions = df.drop_duplicates().copy()

            st.success("✅ Data added successfully")
            st.dataframe(df)

    # ================= FILE UPLOAD =================
    with tab2:

        file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

        # ✅ IMPORTANT: ONLY PROCESS WHEN BUTTON CLICKED
        if file is not None and st.button("Process File"):

            # ---------- READ FILE ----------
            if file.name.endswith(".csv"):
                df = pd.read_csv(file, sep=",", engine="python")

                # 🔥 FIX: if data comes in ONE column
                if len(df.columns) == 1:
                    df = df[df.columns[0]].str.split(",", expand=True)

                    if df.shape[1] >= 4:
                        df.columns = ["date", "category", "amount", "type"]
                    else:
                        st.error("❌ CSV format incorrect")
                        return
            else:
                df = pd.read_excel(file)

            # ---------- CLEAN ----------
            df.columns = df.columns.str.strip().str.lower()

            if "amount" not in df.columns:
                st.error("❌ Amount column missing")
                st.write("Columns found:", df.columns.tolist())
                return

            if "category" not in df.columns:
                df["category"] = "Other"

            if "type" not in df.columns:
                df["type"] = "expense"

            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
            df = df.dropna(subset=["amount"])

            # ✅ FINAL SAVE (NO DUPLICATION EVER)
            df = df.drop_duplicates()

            st.session_state.transactions = df.copy()

            st.success("✅ File processed successfully")
            st.dataframe(df)