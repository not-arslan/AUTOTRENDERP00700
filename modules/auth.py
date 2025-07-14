
import streamlit as st

def is_logged_in():
    return st.session_state.get("logged_in", False)

def logout_button():
    if st.button("Logout"):
        st.session_state.clear()
        st.experimental_rerun()
