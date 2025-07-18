# modules/dashboard.py
import streamlit as st
from modules.angel_api import get_jwt_token, get_option_chain

def show_dashboard():
    st.title("📊 FS Trader - Live Option Chain")
    
    try:
        token = get_jwt_token()
        df = get_option_chain("NIFTY", token=token)
        st.success("✅ Live Data Fetched")
        st.dataframe(df)
    except Exception as e:
        st.error(f"❌ Failed to fetch live data: {e}")
