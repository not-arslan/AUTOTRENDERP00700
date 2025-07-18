import requests, pyotp
import streamlit as st
import pandas as pd

client_id = st.secrets["client_id"]
password = st.secrets["client_password"]
api_key = st.secrets["api_key"]
totp_key = st.secrets["totp_secret"]

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
    except:
        return None

def get_option_chain(symbol="NIFTY", exchange="NSE", token=""):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/order/v1/getOptionChain"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json"
    }
    payload = { "symbol": symbol, "exchange": exchange }
    res = requests.post(url, json=payload, headers=headers)
    return pd.DataFrame(res.json()["data"])
