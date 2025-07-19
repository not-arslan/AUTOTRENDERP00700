# modules/oi_pcr.py

import streamlit as st
import pandas as pd
import time
import requests
from datetime import datetime

# Only rerun every 3 minutes
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
elif time.time() - st.session_state.last_refresh > 180:
    st.session_state.last_refresh = time.time()
    st.rerun()

@st.cache_data(ttl=180)  # ⏱ Cache for 3 minutes
def fetch_option_chain(symbol="NIFTY", exchange="NSE"):
    try:
        headers = {
            "X-PrivateKey": st.secrets["api_key"]
        }
        url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
        payload = {
            "symbol": symbol,
            "exchange": exchange
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"⚠️ Angel One API error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"❌ Exception while fetching option chain: {str(e)}")
        return None

def calculate_pcr(option_data):
    ce_oi = 0
    pe_oi = 0
    rows = []

    for row in option_data:
        if "CE" in row and "PE" in row:
            ce = row["CE"]
            pe = row["PE"]
            ce_oi_val = ce.get("openInterest", 0)
            pe_oi_val = pe.get("openInterest", 0)
            pcr = round(pe_oi_val / ce_oi_val, 2) if ce_oi_val > 0 else 0

            rows.append({
                "Strike": ce.get("strikePrice", 0),
                "CE OI": ce_oi_val,
                "PE OI": pe_oi_val,
                "PCR": pcr
            })
            ce_oi += ce_oi_val
            pe_oi += pe_oi_val

    total_pcr = round(pe_oi / ce_oi, 2) if ce_oi > 0 else 0
    return pd.DataFrame(rows), total_pcr

def show_oi_pcr_dashboard():
    st.subheader("📈 Live Option Chain – NIFTY (NSE)")
    data = fetch_option_chain()

    if data and "data" in data:
        df, total_pcr = calculate_pcr(data["data"])
        st.dataframe(df, use_container_width=True)
        st.success(f"📊 Live PCR: {total_pcr}")
    else:
        st.error("❌ No data found or failed to fetch.")
