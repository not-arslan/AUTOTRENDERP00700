import pandas as pd
import requests
import streamlit as st
import pandas_ta as ta
from modules.angel_api import get_jwt_token

def fetch_candles(token, symbol_token, exchange="MCX", interval="FIFTEEN_MINUTE", count=50):
    url = "https://apiconnect.angelbroking.com/rest/secure/angelbroking/historical/v1/getCandleData"
    headers = {
        "Authorization": f"Bearer {token}",
        "X-PrivateKey": st.secrets["api_key"],
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

def generate_ai_calls():
    token = get_jwt_token()
    if not token:
        return pd.DataFrame([{"Error": "Token fetch failed"}])

    # SYMBOL TOKEN FOR CRUDEOIL FUTURES (update it for current contract)
    symbol_token = "46690"  # Example token for CRUDEOIL July FUT (replace with latest)

    try:
        df = fetch_candles(token, symbol_token, exchange="MCX")
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["ema_20"] = ta.ema(df["close"], length=20)
        df["ema_50"] = ta.ema(df["close"], length=50)

        latest = df.iloc[-1]
        signal = "HOLD"
        if latest["ema_20"] > latest["ema_50"] and latest["rsi"] > 55:
            signal = "BUY"
        elif latest["ema_20"] < latest["ema_50"] and latest["rsi"] < 45:
            signal = "SELL"

        return pd.DataFrame([{
            "Symbol": "CRUDEOIL",
            "Call": signal,
            "Entry": latest["close"],
            "Stop Loss": round(latest["close"] * 0.985, 2),
            "Target": round(latest["close"] * 1.015, 2),
            "RSI": round(latest["rsi"], 2),
            "Volume": int(latest["volume"])
        }])

    except Exception as e:
        return pd.DataFrame([{"Error": str(e)}])
