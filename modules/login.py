import streamlit as st

def login_ui():
    st.title("🔒 FS Trader Login")

    # Input fields for username & password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Check login on button press
    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.auth = True
            st.success("✅ Login successful! Welcome Admin.")
        else:
            st.error("❌ Invalid username or password.")
