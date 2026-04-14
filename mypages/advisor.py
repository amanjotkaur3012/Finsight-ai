import streamlit as st
from modules.gemini_ai import ask_ai

def advisor_page():

    st.title("🤖 AI Advisor")

    user_input = st.text_input("Ask something")

    if st.button("Ask"):
        response = ask_ai(user_input)
        st.write(response)