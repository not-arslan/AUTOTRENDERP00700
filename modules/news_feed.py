# modules/news_feed.py

import streamlit as st
import requests
from datetime import datetime

@st.cache_data(ttl=180)
def fetch_live_news():
    try:
        url = "https://newsdata.io/api/1/news"
        params = {
            "apikey": st.secrets["newsdata_api_key"],
            "q": "crude oil OR oil prices",
            "language": "en",
            "country": "us,in",
            "category": "business"
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            return res.json().get("results", [])
        else:
            return []
    except:
        return []

def show_news_section():
    st.subheader("📰 Crude Oil Market News")

    news_list = fetch_live_news()

    if not news_list:
        st.warning("No live news found.")
        return

    for news in news_list[:6]:
        st.markdown(f"**🗞️ {news.get('title', 'No title')}**")
        st.markdown(f"Published: {news.get('pubDate', '')[:19].replace('T', ' ')}")
        st.markdown(f"[Read more]({news.get('link', '#')})", unsafe_allow_html=True)
        st.markdown("---")
