# modules/angel_api.py
import requests, pyotp
from datetime import datetime
import pandas as pd
import streamlit as st

# Read from Streamlit secrets
client_id = st.secrets["client_id"]
password = st.secrets["client_password"]
api_key = st.secrets["api_key"]
totp_key = st.secrets["totp_secret"]

def get_jwt_token():
    """Login and get access token using TOTP"""
    totp = pyotp.TOTP(totp_key).now()
    login_url = "https://smartapi.angelbroking.com/v1.0/user/loginByPassword"

    payload = {
        "clientcode": client_id,
        "password": password,
        "totp": totp
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": "127.0.0.1",
        "X-ClientPublicIP": "127.0.0.1",
        "X-MACAddress": "XX:XX:XX:XX:XX"
    }

    res = requests.post(login_url, json=payload, headers=headers)
    token = res.json()['data']['jwtToken']
    return token

def get_option_chain(symbol="NIFTY", exchange="NSE", token=""):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "symbol": symbol,
        "exchange": exchange
    }
    res = requests.post(url, json=payload, headers=headers)
    return pd.DataFrame(res.json()["data"])

def get_open_interest(token, symbol_token, exchange="NFO"):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/market/v1/getQuote"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "mode": "FULL",
        "exchange": exchange,
        "symboltoken": symbol_token
    }
    res = requests.post(url, json=payload, headers=headers)
    return res.json()["data"]
