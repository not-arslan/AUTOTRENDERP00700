# modules/ai_calls.py

import streamlit as st
import requests
import random

OPENAI_KEY = st.secrets.get("openai_api_key", "")
GEMINI_KEY = st.secrets.get("gemini_api_key", "")

def fallback_keyword_analysis(news_text):
    keywords = {
        "bullish": ["inventory draw", "supply cut", "OPEC+", "Middle East tension", "pipeline halt"],
        "bearish": ["inventory build", "slowdown", "recession", "demand fall", "rate hike"]
    }
    score = 0
    for word in keywords["bullish"]:
        if word in news_text.lower():
            score += 1
    for word in keywords["bearish"]:
        if word in news_text.lower():
            score -= 1
    return "Bullish" if score > 0 else "Bearish" if score < 0 else "Neutral"

def call_openai(news_text):
    try:
        res = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": "You're an expert crude oil trader. Analyze sentiment."},
                    {"role": "user", "content": f"Analyze this news for crude oil sentiment: {news_text}"}
                ]
            }
        )
        content = res.json()["choices"][0]["message"]["content"]
        return content.strip()
    except:
        return None

def call_gemini(news_text):
    try:
        res = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_KEY}",
            json={
                "contents": [{
                    "parts": [{
                        "text": f"Analyze this crude oil market news sentiment: {news_text}"
                    }]
                }]
            }
        )
        return res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return None

def generate_ai_call():
    # Replace with live news if available
    sample_news = random.choice([
        "OPEC+ considers extending supply cuts",
        "US crude oil inventories rise sharply last week",
        "Middle East tensions drive oil prices up",
        "Global economic slowdown may reduce oil demand"
    ])

    st.info(f"📰 News Input: {sample_news}")

    openai_result = call_openai(sample_news)
    gemini_result = call_gemini(sample_news)

    final = ""
    if openai_result and gemini_result:
        if "bullish" in openai_result.lower() and "bullish" in gemini_result.lower():
            final = "Bullish"
        elif "bearish" in openai_result.lower() and "bearish" in gemini_result.lower():
            final = "Bearish"
        else:
            final = "Neutral"
    elif openai_result:
        final = openai_result
    elif gemini_result:
        final = gemini_result
    else:
        final = fallback_keyword_analysis(sample_news)

    return f"🧠 Crude Oil Sentiment: {final}"
