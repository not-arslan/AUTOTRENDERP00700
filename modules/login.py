import streamlit as st

def login_user():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.button("Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()  # 🔁 Redirect to dashboard
        else:
            st.error("Invalid credentials ❌")

    if st.session_state.logged_in:
        st.success("Already Logged In ✅")
