import streamlit as st

# --- Login UI Function ---
def login_ui():
    st.title("🔒 FS Trader Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.auth = True
            st.success("✅ Login successful! Welcome Admin.")
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Logout UI Function ---
def logout_ui():
    if st.button("🚪 Logout"):
        st.session_state.auth = False
        st.success("Logged out successfully.")
        st.experimental_rerun()
