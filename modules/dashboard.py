# modules/dashboard.py

import streamlit as st
from modules.angel_api import get_jwt_token, get_option_chain

def show_dashboard():
    st.markdown(
        "<h1 style='font-size: 32px;'>📊 FS Traders Official – Live Dashboard</h1>",
        unsafe_allow_html=True
    )

    token = get_jwt_token()
    if not token:
        st.error("❌ Failed to connect to Angel One API")
        return

    st.success("✅ Connected to Angel One API")

    symbol = st.selectbox("Select Symbol", ["NIFTY", "BANKNIFTY"])
    option_data = get_option_chain(symbol)

    st.subheader(f"🧾 Option Chain for {symbol}")
    st.dataframe(option_data)
