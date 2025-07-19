import requests
import pyotp
import streamlit as st

client_id = st.secrets["angelone"]["client_id"]
password = st.secrets["angelone"]["password"]
totp_secret = st.secrets["angelone"]["totp_secret"]
api_key = st.secrets["angelone"]["api_key"]

def get_jwt_token():
    totp = pyotp.TOTP(totp_secret).now()
    payload = {
        "clientcode": client_id,
        "password": password,
        "totp": totp
    }

    try:
        response = requests.post(
            "https://apiconnect.angelbroking.com/rest/auth/angelbroking/user/v1/loginByPassword",
            json=payload,
            headers={
                "X-PrivateKey": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        )

        if response.status_code == 200:
            return response.json()["data"]["jwtToken"]
        else:
            st.error("🚫 Login to Angel One failed.")
            st.code(response.text)  # 👈 Show raw response for debugging
            return None

    except Exception as e:
        st.error(f"❌ Login failed: {e}")
        return None
