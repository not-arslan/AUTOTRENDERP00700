import streamlit as st

# ✅ Main login function
def login_user():
    if st.session_state.get("logged_in"):
        return True

    st.subheader("🔐 Login to FS Traders Dashboard")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "anis" and password == "anisahmad":
            st.session_state["logged_in"] = True
            st.success("✅ Login Successful")
            st.rerun()  # ⏪ updated from st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

    return False

# ✅ Logout button used in sidebar
def logout_button():
    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.rerun()
