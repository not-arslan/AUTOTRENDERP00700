import streamlit as st
import pandas as pd
import requests

def fetch_fyers_oi_chain(symbol="NSE:NIFTY50-INDEX", expiry=None):
    try:
        headers = {"Authorization": f"Bearer {st.secrets['fyers_access_token']}"}
        payload = {"symbol": symbol}
        if expiry:
            payload["expiry"] = expiry
        url = "https://api.fyers.in/data-rest/v3/options-chain"
        resp = requests.get(url, headers=headers, params=payload, timeout=7)
        if resp.status_code == 200:
            return resp.json(), "Fyers"
        else:
            return None, None
    except Exception as e:
        return None, None

def fetch_angel_oi_chain(symbol="NIFTY", expiry=None):
    try:
        # Replace this with your actual Angel One fetch logic
        # For now, just return None (implement later)
        return None, None
    except Exception as e:
        return None, None

def fetch_kotak_oi_chain(symbol="NIFTY", expiry=None):
    try:
        # Replace this with your actual Kotak fetch logic
        return None, None
    except Exception as e:
        return None, None

def fetch_oi_chain_universal(symbol="NSE:NIFTY50-INDEX", expiry=None):
    # Try Fyers first
    data, source = fetch_fyers_oi_chain(symbol, expiry)
    if data:
        return data, source
    # Try Angel next
    data, source = fetch_angel_oi_chain(symbol, expiry)
    if data:
        return data, source
    # Try Kotak
    data, source = fetch_kotak_oi_chain(symbol, expiry)
    if data:
        return data, source
    # Nothing worked
    return None, None
