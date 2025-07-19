import streamlit as st

def login_user():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    users = {
        "admin": "admin123",
        "anis": "anis123"
    }

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("Login Successful ✅")
            st.session_state.authenticated = True
            st.experimental_rerun()  # 🔥 This is what triggers redirect to dashboard!
        else:
            st.error("Invalid credentials ❌")
