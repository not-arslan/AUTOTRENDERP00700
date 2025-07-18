import pandas as pd
import requests
from textblob import TextBlob
import streamlit as st

def fetch_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=YOUR_NEWSAPI_KEY"
    try:
        res = requests.get(url)
        articles = res.json()["articles"]
        data = []
        for a in articles:
            sentiment = TextBlob(a["title"]).sentiment.polarity
            data.append({
                "Headline": a["title"],
                "URL": a["url"],
                "Sentiment": "🟢 Positive" if sentiment > 0 else "🔴 Negative" if sentiment < 0 else "⚪ Neutral"
            })
        return pd.DataFrame(data)
    except:
        return pd.DataFrame(columns=["Headline", "Sentiment"])
