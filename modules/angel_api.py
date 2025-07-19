import streamlit as st
import pyotp
import requests

client_id = st.secrets["angelone"]["client_id"]
api_key = st.secrets["angelone"]["api_key"]
password = st.secrets["angelone"]["password"]
totp_secret = st.secrets["angelone"]["totp_secret"]

totp = pyotp.TOTP(totp_secret).now()

def get_jwt_token():
    url = "https://smartapi.angelbroking.com/v1.0/user/loginByPassword"
    payload = {
        "clientcode": client_id,
        "password": password,
        "totp": totp
    }
    headers = {
        "Content-Type": "application/json",
        "X-UserType": "USER",
        "X-SourceID": "WEB",
        "X-ClientLocalIP": "127.0.0.1",
        "X-ClientPublicIP": "127.0.0.1",
        "X-MACAddress": "00:00:00:00:00:00",
        "X-PrivateKey": api_key
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()
    return data["data"]["jwtToken"]
