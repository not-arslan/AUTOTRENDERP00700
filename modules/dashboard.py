import streamlit as st

def show_dashboard():
    st.markdown(
        """
        <h1 style='font-size: 32px;'>📊 FS Traders Official – Live Dashboard</h1>
        <p>Welcome to the live market dashboard!</p>
        """,
        unsafe_allow_html=True
    )

    st.success("✅ Connected to Angel One (Dummy Message)")
    st.markdown("### 🔧 Features coming soon:")
    st.info("Live Option Chain | PCR | AI Calls | News Feed | Sector Heatmap")
