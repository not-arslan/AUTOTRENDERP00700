import streamlit as st
from modules.angel_api import get_jwt_token, get_option_chain
from modules.ai_calls import generate_ai_calls
from modules.news_feed import fetch_news
from modules.chatbot import miss_trader_chat

def show_dashboard():
    st.title("📊 FS Trader Dashboard")

    token = get_jwt_token()
    if not token:
        st.error("❌ Failed to login to Angel One")
        return

    with st.expander("📈 Live Option Chain"):
        df = get_option_chain("NIFTY", token=token)
        st.dataframe(df)

    with st.expander("📊 AI Buy/Sell Calls"):
        calls = generate_ai_calls()
        st.dataframe(calls)

    with st.expander("📰 Market News & Sentiment"):
        news_df = fetch_news()
        st.dataframe(news_df)

    with st.expander("🤖 Miss.Trader Chatbot"):
        miss_trader_chat()
