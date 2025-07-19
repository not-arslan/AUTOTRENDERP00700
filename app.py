import streamlit as st
from modules.login import login_user
from modules.dashboard import show_dashboard

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    login_user()
else:
    show_dashboard()
