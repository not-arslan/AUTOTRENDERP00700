import streamlit as st
from datetime import datetime, time
from modules.oi_pcr import show_oi_pcr_section, show_oi_table, fetch_oi_chain
from modules.fyers_api import get_crude_data_fyers
from modules.ai_calls import generate_ai_call
from modules.news_feed import show_news_section
from modules.chatbot import show_chatbot
import pandas as pd

def is_market_open():
    now = datetime.now().time()
    return time(9, 30) <= now <= time(15, 30)

def show_dashboard():
    st.sidebar.title("📊 FS Traders Official")
    
    # ✅ Yeh define karo pehle
    menu = ["📈 OI + PCR", "📊 OI Table", "🛢 CrudeOil", "🤖 AI Calls", "📰 News", "💬 Chatbot"]
    choice = st.sidebar.radio("Go to:", menu)

    if choice == "📈 OI + PCR":
        if is_market_open():
            chain = fetch_oi_chain()
            if chain:
                show_oi_pcr_section(chain)
            else:
                st.warning("⚠️ No option chain data.")
        else:
            st.warning("Market closed – 9:30–15:30 IST")

    elif choice == "📊 OI Table":
        if is_market_open():
            chain = fetch_oi_chain()
            if chain:
                show_oi_table(chain)
            else:
                st.warning("⚠️ No option chain data.")
        else:
            st.warning("Market closed – 9:30–15:30 IST")

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
