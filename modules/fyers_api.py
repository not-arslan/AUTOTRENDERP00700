# modules/fyers_api.py

import streamlit as st
from fyers_apiv3 import fyersModel

@st.cache_resource(ttl=3600)
def _get_fyers_client():
    """
    Initialize and cache a FyersModel client.
    Requires these keys in your secrets.toml:
      fyers_client_id
      fyers_access_token
    """
    client_id    = st.secrets["fyers_client_id"]
    access_token = st.secrets["fyers_access_token"]
    # log_path can be left blank or point to a folder for logs
    return fyersModel.FyersModel(client_id=client_id, token=access_token, log_path="")

@st.cache_data(ttl=180)
def get_option_chain_fyers(symbol: str = "NSE:NIFTY50-INDEX"):
    """
    Returns a list of option‑chain entries for the given symbol.
    Each entry is a dict with strikePrice, openInterest, etc.
    """
    client = _get_fyers_client()
    payload = {
        "symbol": symbol,
        "strikecount": "",     # leave blank for default range
        "timestamp": ""        # optional timestamp filter
    }
    res = client.optionchain(data=payload)
    return res.get("data", {}).get("optionsChain", [])

@st.cache_data(ttl=180)
def get_crude_data_fyers(symbol: str = "MCX:CRUDEOIL24JULFUT"):
    """
    Returns a list of quote dicts for the given MCX symbol.
    """
    client = _get_fyers_client()
    resp = client.quotes({"symbols": symbol})  # ✅ FIXED LINE
    # Fyers returns quotes under the 'd' key
    return resp.get("d", [])
