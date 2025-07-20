# modules/dashboard.py

import streamlit as st
from datetime import datetime, time
from modules.fyers_api import get_option_chain_fyers, get_crude_data_fyers
from modules.ai_calls    import generate_ai_call
from modules.news_feed   import show_news_section
from modules.chatbot     import show_chatbot
from modules.login       import logout_button
from modules.oi_pcr import show_oi_table
import pandas as pd

def is_market_open():
    now = datetime.now().time()
    return time(9, 30) <= now <= time(15, 30)

def show_oi_pcr_section(chain_rows):
    ce_total, pe_total, table = 0, 0, []
    for r in chain_rows:
        if "CE" in r and "PE" in r:
            ce = r["CE"]; pe = r["PE"]
            ce_oi = ce["openInterest"]
            pe_oi = pe["openInterest"]
            ce_total += ce_oi
            pe_total += pe_oi
            table.append({
                "Strike": ce["strikePrice"],
                "CE OI" : ce_oi,
                "PE OI" : pe_oi,
                "PCR"   : round(pe_oi/ce_oi, 2) if ce_oi else None
            })

    df = pd.DataFrame(table)
    total_pcr = round(pe_total/ce_total, 2) if ce_total else None
    st.subheader("📈 Option Chain – NIFTY")
    st.dataframe(df, use_container_width=True)
    st.success(f"🧮 Live PCR: {total_pcr}")

def show_dashboard():
    st.sidebar.title("📊 FS Traders")
    logout_button()

    menu = ["📈 OI + PCR", "🛢 CrudeOil", "🤖 AI Calls", "📰 News", "💬 Chatbot"]
    section = st.sidebar.radio("Go to:", menu)

    # Fetch once
    try:
        if section == "📈 OI + PCR":
            if is_market_open():
                rows = get_option_chain_fyers()
                if rows:
                    show_oi_pcr_section(rows)
                else:
                    st.warning("⚠️ No option chain data found.")
            else:
                st.warning("Market closed. Live 9:30–15:30 IST")
        elif section == "🛢 CrudeOil":
            st.subheader("🛢 MCX CrudeOil – Live")
            data = get_crude_data_fyers()
            if data:
                st.dataframe(pd.DataFrame(data), use_container_width=True)
            else:
                st.error("❌ Could not fetch CrudeOil data.")
        elif section == "🤖 AI Calls":
            st.subheader("🤖 AI Trade Call")
            call = generate_ai_call()
            st.success(call) if call else st.warning("⚠️ No call right now.")
        elif section == "📰 News":
            show_news_section()
        elif section == "💬 Chatbot":
            show_chatbot()
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
