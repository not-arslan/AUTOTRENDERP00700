# app.py

import streamlit as st
from modules.login import login_user
from modules.dashboard import show_dashboard

def main():
    st.set_page_config(page_title="📊 FS Traders Official", layout="wide")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        login_user()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
