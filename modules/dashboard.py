# modules/dashboard.py

import streamlit as st
from datetime import datetime, time
from zoneinfo import ZoneInfo
from modules.universal_oi_fetcher import fetch_oi_chain_universal   # <== Universal fetcher import
from modules.fyers_api import get_crude_data_fyers
from modules.ai_calls import generate_ai_call
from modules.news_feed import show_news_section
from modules.chatbot import show_chatbot
from modules.fyers_oi_table import show_fyers_oi_table  # Autotrendr-style OI Table
from modules.oi_pcr import show_oi_pcr_section, show_oi_table
import pandas as pd

def is_market_open():
    now = datetime.now(ZoneInfo("Asia/Kolkata")).time()
    return time(9, 30) <= now <= time(15, 30)

def show_dashboard():
    st.sidebar.title("📊 FS Traders Official")

    menu = [
        "📈 OI + PCR",
        "📊 Angel OI Table",
        "🟣 Fyers OI Table",
        "🛢 CrudeOil",
        "🤖 AI Calls",
        "📰 News",
        "💬 Chatbot"
    ]
    choice = st.sidebar.radio("Go to:", menu)

    if choice == "📈 OI + PCR":
        if is_market_open():
            chain, source = fetch_oi_chain_universal()
            if chain:
                st.success(f"Live OI Chain Source: {source}")
                show_oi_pcr_section(chain)
            else:
                st.error("⚠️ No live OI data from any API.")
        else:
            st.warning("Market closed – 9:30–15:30 IST")

    elif choice == "📊 Angel OI Table":
        if is_market_open():
            chain, source = fetch_oi_chain_universal()
            if chain:
                st.success(f"Live OI Table Source: {source}")
                show_oi_table(chain)
            else:
                st.error("⚠️ No live OI table data from any API.")
        else:
            st.warning("Market closed – 9:30–15:30 IST")

    elif choice == "🟣 Fyers OI Table":
        show_fyers_oi_table()

    elif choice == "🛢 CrudeOil":
        st.subheader("🛢 Live MCX CrudeOil")
        data = get_crude_data_fyers()
        if data:
            st.dataframe(pd.DataFrame(data), use_container_width=True)
        else:
            st.error("❌ Fetch failed.")

    elif choice == "🤖 AI Calls":
        call = generate_ai_call()
        st.subheader("🤖 AI Trade Call")
        st.success(call)

    elif choice == "📰 News":
        show_news_section()

    elif choice == "💬 Chatbot":
        show_chatbot()
