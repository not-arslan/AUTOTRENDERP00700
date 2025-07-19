# modules/login.py

import streamlit as st

def login_user():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.success("Login Successful ✅")
        else:
            st.error("Invalid credentials ❌")
