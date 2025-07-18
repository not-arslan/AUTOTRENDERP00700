import streamlit as st
import pandas as pd
from textblob import TextBlob
import requests

# 🔍 Function to calculate sentiment polarity
def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "🟢 Positive"
    elif polarity < -0.1:
        return "🔴 Negative"
    else:
        return "🟡 Neutral"

# 📰 Fetch news (sample using Yahoo Finance RSS)
def fetch_news():
    url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=^NSEI&region=IN&lang=en-IN"
    response = requests.get(url)
    
    news_list = []
    if response.status_code == 200:
        from xml.etree import ElementTree as ET
        root = ET.fromstring(response.content)
        for item in root.iter("item"):
            title = item.find("title").text
            link = item.find("link").text
            sentiment = analyze_sentiment(title)
            news_list.append({"Headline": title, "Sentiment": sentiment, "Link": link})

    return pd.DataFrame(news_list)
