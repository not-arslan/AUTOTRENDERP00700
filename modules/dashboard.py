import streamlit as st
from modules.angel_api import get_jwt_token

def show_dashboard():
    st.title("📊 FS Traders Official – Live Dashboard")
    st.markdown("Welcome to the live market dashboard!")

    try:
        jwt = get_jwt_token()
        st.success("✅ Connected to Angel One")
    except Exception as e:
        st.error("❌ Login to Angel One failed.")
        st.text(str(e))

    # Add other dashboard widgets here later...
