from streamlit_option_menu import option_menu
import streamlit as st

def sidebar():
    with st.sidebar:

        st.markdown("## 💰 FinSight AI")
        st.markdown("### Smart Finance Dashboard")

        selected = option_menu(
            "",
            [
                "Expense Parser",   # ✅ FIRST (MOST IMPORTANT)
                "Dashboard",
                "Analytics",
                "AI Advisor",
                "Goals Planner",
                "Notes"
            ],
            icons=[
                "cpu",
                "bar-chart",
                "graph-up",
                "robot",
                "bullseye",
                "journal"
            ],
            default_index=0,  # opens parser first
            styles={
                "container": {"padding": "5px", "background-color": "#020617"},
                "icon": {"color": "#06b6d4", "font-size": "20px"},
                "nav-link": {
                    "color": "white",
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "5px",
                },
                "nav-link-selected": {
                    "background": "linear-gradient(90deg, #06b6d4, #3b82f6)",
                    "color": "white",
                },
            }
        )
    return selected