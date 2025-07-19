import streamlit as st
from modules.login import login_user
from modules.dashboard import show_dashboard

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_dashboard()
    else:
        login_user()

if __name__ == "__main__":
    main()
