import streamlit as st
from modules.angel_api import get_jwt_token, get_option_chain
from modules.ai_calls import generate_ai_calls
from modules.news_feed import fetch_news
from modules.chatbot import miss_trader_chat

def show_dashboard():
    st.title("📊 FS Trader Dashboard")

    # Step 1: Angel One JWT login
    token = get_jwt_token()
    if not token:
        st.error("❌ Failed to login to Angel One")
        return

    # Step 2: NIFTY Option Chain
    with st.expander("📈 Live Option Chain (NIFTY)"):
        try:
            df = get_option_chain("NIFTY", token=token)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error fetching option chain: {e}")

    # Step 3: AI Buy/Sell Calls
    with st.expander("📊 AI Buy/Sell Calls"):
        try:
            calls = generate_ai_calls()
            st.dataframe(calls)
        except Exception as e:
            st.error(f"Error generating AI calls: {e}")

    # Step 4: News & Sentiment
    with st.expander("📰 Market News + Sentiment"):
        try:
            news_df = fetch_news()
            st.dataframe(news_df)
        except Exception as e:
            st.warning(f"Error loading news: {e}")

    # Step 5: Miss.Trader Chat
    with st.expander("🤖 Miss.Trader Chatbot"):
        miss_trader_chat()
