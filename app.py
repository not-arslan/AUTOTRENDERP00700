# app.py
import streamlit as st
from modules.login import login_user
from modules.dashboard import show_dashboard

def main():
    st.set_page_config(page_title="FS Traders Official – Live Dashboard", layout="wide")
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        show_dashboard()
    else:
        login_user()

if __name__ == "__main__":
    main()

