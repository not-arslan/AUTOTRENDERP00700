# login.py

import streamlit as st

# Dummy user data – YOU CAN ADD MORE USERS HERE
users = {
    "admin": "admin123",
    "anis": "anis123",
}

def login_user():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login Successful")
        else:
            st.error("❌ Invalid credentials")
