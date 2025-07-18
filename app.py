import streamlit as st
from modules.login import login_ui, logout_ui
from modules.dashboard import show_dashboard

# --- Session Setup ---
if "auth" not in st.session_state:
    st.session_state.auth = False

# --- Main App Flow ---
if st.session_state.auth:
    logout_ui()         # 🚪 Show logout button at top
    show_dashboard()    # 📊 Show full dashboard
else:
    login_ui()          # 🔒 Show login form
