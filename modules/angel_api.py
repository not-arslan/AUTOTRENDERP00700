import requests
import pyotp
import streamlit as st
import pandas as pd

# Secrets from Streamlit config
client_id = st.secrets["client_id"]
password = st.secrets["client_password"]
api_key = st.secrets["api_key"]
totp_key = st.secrets["totp_secret"]

# 🔐 1. Login and get JWT Token using TOTP
def get_jwt_token():
    try:
        totp = pyotp.TOTP(totp_key).now()
        res = requests.post("https://smartapi.angelbroking.com/v1.0/user/loginByPassword", json={
            "clientcode": client_id,
            "password": password,
            "totp": totp
        }, headers={
            "Content-Type": "application/json",
            "X-UserType": "USER",
            "X-SourceID": "WEB",
            "X-ClientLocalIP": "127.0.0.1",
            "X-ClientPublicIP": "127.0.0.1",
            "X-MACAddress": "XX:XX:XX:XX:XX"
        })

        return res.json()['data']['jwtToken']
    except Exception as e:
        st.error(f"❌ Angel Login Failed: {e}")
        return None

# 📈 2. Fetch Live Option Chain (NIFTY, BANKNIFTY, etc.)
def get_option_chain(symbol="NIFTY", exchange="NSE", token=""):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "symbol": symbol,
        "exchange": exchange
    }
    res = requests.post(url, json=payload, headers=headers)
    return pd.DataFrame(res.json()["data"])

# 🕒 3. Fetch Historical Candles for AI Calls (MCX, NFO, NSE)
def fetch_candles(token, symbol_token, exchange="MCX", interval="FIFTEEN_MINUTE", count=50):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "exchange": exchange,
        "symboltoken": symbol_token,
        "interval": interval,
        "range": f"{count}"
    }

    response = requests.post(url, json=payload, headers=headers)
    candles = response.json()["data"]

    df = pd.DataFrame(candles, columns=["time", "open", "high", "low", "close", "volume"])
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df
