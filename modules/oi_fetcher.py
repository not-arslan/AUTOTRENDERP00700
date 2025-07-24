import requests
import streamlit as st

def fetch_oi_chain(source="auto", symbol="NSE:NIFTY50-INDEX", expiry=None):
    """Auto-select best live OI source."""
    errors = []
    if source in ["auto", "fyers"]:
        try:
            # --- FYERS
            headers = {"Authorization": f"Bearer {st.secrets['fyers_access_token']}"}
            url = "https://api.fyers.in/data-rest/v3/options-chain"
            params = {"symbol": symbol}
            if expiry: params["expiry"] = expiry
            resp = requests.get(url, headers=headers, params=params, timeout=6)
            if resp.status_code == 200:
                return resp.json(), "Fyers"
            else:
                errors.append(("Fyers", resp.status_code))
        except Exception as e:
            errors.append(("Fyers", str(e)))

    if source in ["auto", "angel"]:
        try:
            # --- ANGEL ONE (put your API call here)
            # resp = requests.get(...) # Fill as per Angel API
            # if resp.status_code == 200:
            #     return resp.json(), "Angel"
            pass
        except Exception as e:
            errors.append(("Angel", str(e)))

    if source in ["auto", "kotak"]:
        try:
            # --- KOTAK (put your API call here)
            pass
        except Exception as e:
            errors.append(("Kotak", str(e)))

    # --- Fallback (e.g., manual CSV, NSE site, etc.)
    return None, errors  # Could return ("fallback_data", "Fallback")

