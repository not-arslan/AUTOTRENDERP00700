# app.py

import streamlit as st
from datetime import datetime, time
from modules.oi_pcr import show_oi_pcr_dashboard

def is_market_open():
    now = datetime.now().time()
    market_start = time(9, 30)
    market_end = time(15, 30)
    return market_start <= now <= market_end

def main():
    st.set_page_config(page_title="📊 FS Traders – Live OI & PCR", layout="wide")

    st.title("📊 FS Traders Official – NSE Live OI & PCR Dashboard")

    if is_market_open():
        show_oi_pcr_dashboard()
    else:
        st.warning("📴 Market is currently closed.\n⏰ Live data updates between 9:30 AM – 3:30 PM (IST)")

if __name__ == "__main__":
    main()
