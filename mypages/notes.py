import streamlit as st
import pandas as pd
import os
from datetime import datetime

def notes_page():

    st.title("📝 Smart Financial Notes")

    file_path = "data/notes.csv"

    # ================= LOAD NOTES =================
    if os.path.exists(file_path):
        notes_df = pd.read_csv(file_path)
    else:
        notes_df = pd.DataFrame(columns=["note", "timestamp"])

    # ================= ADD NOTE =================
    st.markdown("## ✍️ Add New Note")

    note = st.text_area("Write your financial note / insight / reminder")

    if st.button("Save Note"):

        if note.strip() == "":
            st.warning("⚠️ Note cannot be empty")
            return

        new_note = pd.DataFrame([{
            "note": note,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }])

        notes_df = pd.concat([notes_df, new_note], ignore_index=True)

        os.makedirs("data", exist_ok=True)
        notes_df.to_csv(file_path, index=False)

        st.success("✅ Note saved successfully")
        st.rerun()

    st.markdown("---")

    # ================= VIEW NOTES =================
    st.markdown("## 📚 Your Notes")

    if notes_df.empty:
        st.info("No notes yet")
        return

    # Show latest first
    notes_df = notes_df.sort_values(by="timestamp", ascending=False)

    for i, row in notes_df.iterrows():

        with st.expander(f"🗒️ {row['timestamp']}"):

            st.write(row["note"])

            # DELETE BUTTON
            if st.button(f"Delete Note {i}"):

                notes_df = notes_df.drop(i)

                notes_df.to_csv(file_path, index=False)

                st.success("Note deleted")
                st.rerun()

    st.markdown("---")