import streamlit as st
import openai

def miss_trader_chat():
    openai.api_key = st.secrets["openai_api_key"]
    user_msg = st.text_input("💬 Ask Miss.Trader (Hindi / English / Hinglish)")
    if st.button("Send") and user_msg:
        with st.spinner("Thinking..."):
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_msg}]
            )
            st.success(res.choices[0].message.content)
