import streamlit as st
import pandas as pd
from datetime import datetime, time
import time as systime
from modules.fyers_api import get_option_chain_fyers

# Auto-refresh every 3 minutes
def _auto_refresh():
    if "last_refresh" not in st.session_state:
        st.session_state.last_refresh = systime.time()
    elif systime.time() - st.session_state.last_refresh > 180:
        st.session_state.last_refresh = systime.time()
        st.experimental_rerun()

_auto_refresh()

@st.cache_data(ttl=180)
def fetch_oi_chain():
    return get_option_chain_fyers()


def show_oi_pcr_section(chain_rows):
    ce_total, pe_total = 0, 0
    rows = []
    for r in chain_rows:
        if "CE" in r and "PE" in r:
            ce = r["CE"]
            pe = r["PE"]
            ce_oi = ce.get("openInterest", 0)
            pe_oi = pe.get("openInterest", 0)
            ce_total += ce_oi
            pe_total += pe_oi
            rows.append({
                "Strike": ce.get("strikePrice"),
                "CE OI": ce_oi,
                "PE OI": pe_oi,
                "PCR": round(pe_oi/ce_oi, 2) if ce_oi else None
            })
    df = pd.DataFrame(rows)
    total_pcr = round(pe_total/ce_total, 2) if ce_total else None
    st.subheader("📈 Option Chain & PCR – NIFTY")
    st.dataframe(df, use_container_width=True)
    st.success(f"🧮 Live PCR: {total_pcr}")


def show_oi_table(chain_rows):
    rows = []
    for r in chain_rows:
        if "CE" in r and "PE" in r:
            ce = r["CE"]
            pe = r["PE"]
            rows.append({
                "Strike": ce.get("strikePrice"),
                "CE OI": ce.get("openInterest", 0),
                "PE OI": pe.get("openInterest", 0),
                "CE Change OI": ce.get("changeinOpenInterest", 0),
                "PE Change OI": pe.get("changeinOpenInterest", 0),
                "PCR": round(pe.get("openInterest", 0) / ce.get("openInterest", 1), 2)
            })
    df = pd.DataFrame(rows)
    st.subheader("📊 OI Table – NIFTY Option Chain")
    st.dataframe(df.sort_values("Strike"), use_container_width=True)
