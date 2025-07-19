# modules/angel_api.py

import streamlit as st
import requests
import pyotp

@st.cache_data(ttl=600)
def get_jwt_token():
    api_key = st.secrets["api_key"]
    client_id = st.secrets["client_id"]
    password = st.secrets["password"]
    totp_secret = st.secrets["totp_secret"]
    totp = pyotp.TOTP(totp_secret).now()

    login_url = "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    payload = {
        "clientcode": client_id,
        "password": password,
        "totp": totp
    }

    try:
        res = requests.post(login_url, json=payload, headers=headers)
        res_json = res.json()
        return res_json.get("data", {}).get("jwtToken", None)
    except Exception as e:
        st.error(f"Login error: {e}")
        return None

def get_option_chain(symbol="NIFTY"):
    jwt_token = get_jwt_token()
    if not jwt_token:
        return {"error": "No JWT token"}

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "X-PrivateKey": st.secrets["api_key"]
    }

    url = f"https://apiconnect.angelbroking.com/rest/secure/option/getOptionData?symbol={symbol}"

    try:
        res = requests.get(url, headers=headers)
        return res.json()
    except Exception as e:
        st.error(f"Option chain fetch error: {e}")
        return {}
