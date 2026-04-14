import streamlit as st
import pandas as pd
import uuid

def init_session():

    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

    if "transactions" not in st.session_state:
        st.session_state.transactions = pd.DataFrame(columns=[
            "description", "amount", "category", "type"
        ])