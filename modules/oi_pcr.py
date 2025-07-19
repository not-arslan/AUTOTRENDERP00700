# modules/oi_pcr.py

import streamlit as st
import pandas as pd
from datetime import datetime
import time as systime
import requests

# ⏱ 3-minute auto-refresh
st.experimental_set_query_params(refresh=str(datetime.now().minute // 3))
st.experimental_rerun()

@st.cache_data(ttl=180)  # cache for 3 minutes
def fetch_option_chain(symbol="NIFTY", exchange="NSE"):
    headers = {
        "X-PrivateKey": st.secrets["api_key"]
    }
    url = f"https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
    payload = {
        "symbol": symbol,
        "exchange": exchange
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("⚠️ Failed to fetch data from Angel One.")
        return None

def calculate_pcr(option_data):
    ce_oi = 0
    pe_oi = 0
    rows = []

    for row in option_data:
        if "CE" in row and "PE" in row:
            ce = row["CE"]
            pe = row["PE"]
            rows.append({
                "Strike": ce["strikePrice"],
                "CE OI": ce["openInterest"],
                "PE OI": pe["openInterest"],
                "PCR": round(pe["openInterest"] / ce["openInterest"], 2) if ce["openInterest"] > 0 else 0
            })
            ce_oi += ce["openInterest"]
            pe_oi += pe["openInterest"]

    total_pcr = round(pe_oi / ce_oi, 2) if ce_oi > 0 else 0
    return pd.DataFrame(rows), total_pcr

def show_oi_pcr_dashboard():
    st.subheader("📈 Live Option Chain – NIFTY")
    data = fetch_option_chain()

    if data and "data" in data:
        df, total_pcr = calculate_pcr(data["data"])
        st.dataframe(df, use_container_width=True)
        st.success(f"📊 Live PCR: {total_pcr}")
    else:
        st.error("❌ No data found.")
