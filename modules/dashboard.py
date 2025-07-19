import streamlit as st
from datetime import datetime, time
from modules.angel_api import get_jwt_token, get_option_chain, get_crude_data
from modules.ai_calls import generate_ai_call
from modules.news_feed import show_news_section  # ✅ fixed here
from modules.chatbot import show_chatbot
from modules.login import logout_button
import pandas as pd

def is_market_open():
    now = datetime.now().time()
    return time(9, 30) <= now <= time(15, 30)

def show_oi_pcr_section(data):
    ce_oi, pe_oi, rows = 0, 0, []

    for row in data:
        if "CE" in row and "PE" in row:
            ce = row["CE"]
            pe = row["PE"]
            ce_oi += ce["openInterest"]
            pe_oi += pe["openInterest"]
            rows.append({
                "Strike": ce["strikePrice"],
                "CE OI": ce["openInterest"],
                "PE OI": pe["openInterest"],
                "PCR": round(pe["openInterest"] / ce["openInterest"], 2) if ce["openInterest"] > 0 else 0
            })

    df = pd.DataFrame(rows)
    total_pcr = round(pe_oi / ce_oi, 2) if ce_oi else 0
    st.subheader("📈 Option Chain Data – NIFTY")
    st.dataframe(df, use_container_width=True)
    st.success(f"🧮 Live PCR: {total_pcr}")

def show_dashboard():
    st.sidebar.title("📊 FS Traders")
    logout_button()

    section = st.sidebar.radio("Go to:", ["📈 OI + PCR", "🛢 CrudeOil", "🤖 AI Calls", "📰 News", "💬 Chatbot"])

    try:
        token = get_jwt_token()
    except Exception as e:
        st.error(f"❌ Token Error: {e}")
        return

    if section == "📈 OI + PCR":
        if is_market_open():
            data = get_option_chain(token)
            if data and "data" in data:
                show_oi_pcr_section(data["data"])
            else:
                st.warning("⚠️ No option chain data found.")
        else:
            st.warning("📴 Market is closed. Live updates 9:30 AM – 3:30 PM")

    elif section == "🛢 CrudeOil":
        st.subheader("🛢 MCX CrudeOil – Live Data")
        crude = get_crude_data(token)
        if crude:
            st.dataframe(pd.DataFrame(crude), use_container_width=True)
        else:
            st.error("❌ Could not fetch CrudeOil data.")

    elif section == "🤖 AI Calls":
        st.subheader("🤖 AI-Generated Trade Call")
        ai_call = generate_ai_call()
        if ai_call:
            st.success(f"📢 {ai_call}")
        else:
            st.warning("⚠️ Could not generate call at the moment.")

    elif section == "📰 News":
        show_news_section()  # ✅ fixed here

    elif section == "💬 Chatbot":
        show_chatbot()
