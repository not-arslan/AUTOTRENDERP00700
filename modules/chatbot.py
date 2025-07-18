import streamlit as st
import openai

def miss_trader_chat():
    st.subheader("🤖 Miss.Trader - AI Chat Assistant")

    openai.api_key = st.secrets["openai_api_key"]

    # User input
    user_msg = st.text_input("💬 Ask Miss.Trader (English / Hindi / Hinglish)")
    
    if st.button("Send") and user_msg:
        try:
            with st.spinner("Miss.Trader is thinking..."):
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_msg}]
                )
                reply = response.choices[0].message.content
                st.success(reply)
        except Exception as e:
            st.error(f"Chatbot error: {e}")
