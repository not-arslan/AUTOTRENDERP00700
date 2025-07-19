# modules/login.py

import streamlit as st

def login_user():
    st.title("🔐 Login Page")

    username = st.text_input("anis")
    password = st.text_input("Password", type="anis4545")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.authenticated = True
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
