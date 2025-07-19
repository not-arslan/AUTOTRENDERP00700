# modules/login.py

import streamlit as st

def login_user():
    st.title("🔐 FS Traders Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "anis" and password == "anisahmad":
            st.success("✅ Login Successful")
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

def logout_button():
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
