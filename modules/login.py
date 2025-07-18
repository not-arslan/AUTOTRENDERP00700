import streamlit as st

def login_ui():
    st.title("🔒 FS Trader Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.auth = True
        else:
            st.error("Invalid credentials")
