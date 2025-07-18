import streamlit as st
from modules.login import login_ui
from modules.dashboard import show_dashboard

# Session-based login system
if "auth" not in st.session_state:
    st.session_state.auth = False

# If authenticated, show dashboard
if st.session_state.auth:
    show_dashboard()
else:
    login_ui()
