# modules/fyers_oi_table.py

import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

@st.cache_data(ttl=180)
def get_fyers_option_chain(symbol="NSE:NIFTY50-INDEX", expiry=None):
    """
    Fetch option chain from Fyers API (requires valid access token in st.secrets).
    Includes retry logic and Sunday check.
    """
    # Stop on Sunday
    if datetime.today().weekday() == 6:  # Sunday = 6
        st.warning("📅 Today is Sunday. Live Fyers data is unavailable.")
        return None

    try:
        headers = {
            "Authorization": f"Bearer {st.secrets['fyers_access_token']}"
        }
        payload = {
            "symbol": symbol
        }
        if expiry:
            payload["expiry"] = expiry

        url = "https://api.fyers.in/data-rest/v3/options-chain"

        # Retry logic (max 3 attempts)
        for attempt in range(3):
            response = requests.get(url, headers=headers, params=payload)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 503:
                time.sleep(2)
            else:
                st.error(f"❌ Fyers API Error: {response.status_code}")
                return None

        st.error("❌ Fyers API Error: 503 (after retries)")
        return None

    except Exception as e:
        st.error(f"❌ Exception while calling Fyers API: {e}")
        return None

def extract_expiries(data):
    expiries = set()
    if "data" in data and "chains" in data["data"]:
        for row in data["data"]["chains"]:
            expiries.add(row.get("expiry"))
    return sorted(list(expiries))

def build_oi_pcr_df(data, selected_expiry):
    calls, puts = [], []
    for item in data["data"]["chains"]:
        if item["expiry"] != selected_expiry:
            continue
        if item["type"] == "CE":
            calls.append(item)
        elif item["type"] == "PE":
            puts.append(item)

    df = pd.DataFrame()
    for ce in calls:
        strike = ce["strike"]
        pe = next((p for p in puts if p["strike"] == strike), None)
        if not pe:
            continue
        row = {
            "Strike": strike,
            "CE OI": ce["openInterest"],
            "PE OI": pe["openInterest"],
            "PCR": round(pe["openInterest"] / ce["openInterest"], 2) if ce["openInterest"] else 0
        }
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    return df.sort_values("Strike")

def show_fyers_oi_table():
    st.subheader("📈 Fyers Option Chain – NIFTY (Live)")

    data = get_fyers_option_chain()
    if not data:
        st.error("⚠️ Failed to fetch Fyers data.")
        return

    expiry_list = extract_expiries(data)
    if not expiry_list:
        st.warning("No expiry dates found.")
        return

    selected_expiry = st.selectbox("Select Expiry Date", expiry_list, index=0)

    data = get_fyers_option_chain(expiry=selected_expiry)
    if not data:
        st.error("⚠️ Data missing for selected expiry.")
        return

    df = build_oi_pcr_df(data, selected_expiry)
    st.dataframe(df, use_container_width=True)

    total_ce_oi = df["CE OI"].sum()
    total_pe_oi = df["PE OI"].sum()
    total_pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else 0

    st.success(f"📊 Total PCR: {total_pcr}")
