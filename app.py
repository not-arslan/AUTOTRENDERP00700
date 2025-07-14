
import streamlit as st
from modules.login import login_ui
from modules.auth import is_logged_in, logout_button

st.set_page_config(page_title="FS Traders Official", layout="wide")

if not is_logged_in():
    login_ui()
else:
    st.sidebar.success(f"Logged in as: {st.session_state['email']}")
    logout_button()

    st.title("📊 FS Traders Official Dashboard")
    st.write("Welcome to your secure dashboard!")
