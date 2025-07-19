import streamlit as st

# Dummy user database
users = {
    "admin@gmail.com": "admin123"
}

def login_user():
    st.title("🔐 FS Traders Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    login = st.button("Login")

    if login:
        if email in users and users[email] == password:
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid email or password.")
