# modules/angel_api.py

import streamlit as st
import requests
import pyotp

@st.cache_resource(ttl=3600)
def get_jwt_token():
    api_key = st.secrets["api_key"]
    client_id = st.secrets["client_id"]
    password = st.secrets["password"]
    totp_secret = st.secrets["totp_secret"]

    totp = pyotp.TOTP(totp_secret).now()

    headers = {
        "X-PrivateKey": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "clientcode": client_id,
        "password": password,
        "totp": totp
    }

    url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
    res = requests.post(url, headers=headers, json=payload)

    if res.status_code == 200:
        return res.json()["data"]["jwtToken"]
    else:
        raise Exception("Login failed: " + res.text)

@st.cache_data(ttl=180)
def get_option_chain(token, symbol="NIFTY", exchange="NSE"):
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": st.secrets["api_key"]
    }
    payload = {
        "symbol": symbol,
        "exchange": exchange
    }
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
    res = requests.post(url, headers=headers, json=payload)
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=180)
def get_crude_data(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": st.secrets["api_key"]
    }
    url = "https://apiconnect.angelbroking.com/rest/secure/market/v1/quote"
    payload = {
        "mode": "FULL",
        "exchange": "MCX",
        "symboltoken": "23401",  # Token for CrudeOil Futures
        "tradingsymbol": "CRUDEOIL24JULFUT",
        "symbolname": "CRUDEOIL"
    }
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code == 200:
        return res.json()["data"]["fetched"]
    return None
