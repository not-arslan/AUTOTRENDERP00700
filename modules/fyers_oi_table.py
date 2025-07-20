import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# ———————————————————————————————————————————————
@st.cache_data(ttl=180)
def get_fyers_option_chain(symbol="NSE:NIFTY50-INDEX", expiry=None):
    if datetime.today().weekday() == 6:
        return None
    headers = {"Authorization": f"Bearer {st.secrets['fyers_access_token']}"}
    payload = {"symbol": symbol}
    if expiry:
        payload["expiry"] = expiry
    url = "https://api.fyers.in/data-rest/v3/options-chain"
    for _ in range(3):
        resp = requests.get(url, headers=headers, params=payload)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 503:
            time.sleep(2)
        else:
            return None
    return None

def extract_expiries(data):
    chains = data.get("data", {}).get("chains", [])
    expiries = sorted({row.get("expiry") for row in chains})
    return [datetime.strptime(e, "%Y-%m-%d").strftime("%d-%b-%Y") for e in expiries if e]

def format_lakh(val):
    try:
        return f"{int(val):,}"
    except:
        return val

def format_percent(val):
    try:
        return f"{val:+.0f} %"
    except:
        return val

def build_full_oi_table(chains, selected_expiry):
    df = pd.DataFrame([c for c in chains if c["expiry"] == selected_expiry])
    if df.empty:
        return pd.DataFrame()

    ce = df[df["type"]=="CE"].set_index("strike")
    pe = df[df["type"]=="PE"].set_index("strike")
    all_strikes = sorted(set(ce.index).union(pe.index))

    rows = []
    for strike in all_strikes:
        ce_row = ce.loc[strike] if strike in ce.index else {}
        pe_row = pe.loc[strike] if strike in pe.index else {}

        row = {
            # Left (CALLS)
            "Chg OI (CE)": format_lakh(ce_row.get("changeInOI", 0)),
            "%Chg (CE)": format_percent(ce_row.get("pChangeInOI", 0)),
            "LTP (CE)": ce_row.get("lastTradedPrice", 0),
            "VWAP (CE)": ce_row.get("vwap", 0),
            "OI (CE)": format_lakh(ce_row.get("openInterest", 0)),
            # Center
            "Strike": strike,
            # Right (PUTS)
            "OI (PE)": format_lakh(pe_row.get("openInterest", 0)),
            "VWAP (PE)": pe_row.get("vwap", 0),
            "LTP (PE)": pe_row.get("lastTradedPrice", 0),
            "%Chg (PE)": format_percent(pe_row.get("pChangeInOI", 0)),
            "Chg OI (PE)": format_lakh(pe_row.get("changeInOI", 0)),
        }
        rows.append(row)

    final = pd.DataFrame(rows)
    final = final[
        ["Chg OI (CE)", "%Chg (CE)", "LTP (CE)", "VWAP (CE)", "OI (CE)",
         "Strike",
         "OI (PE)", "VWAP (PE)", "LTP (PE)", "%Chg (PE)", "Chg OI (PE)"]
    ]
    for col in ["Strike", "LTP (CE)", "VWAP (CE)", "LTP (PE)", "VWAP (PE)"]:
        final[col] = pd.to_numeric(final[col], errors="coerce")
    return final.sort_values("Strike")

# ———————————————————————————————————————————————
def build_intraday_trend_df(session_key="oi_trend_log"):
    if session_key not in st.session_state:
        st.session_state[session_key] = []
    log = st.session_state[session_key]
    if not log:
        return pd.DataFrame()
    return pd.DataFrame(log)

def update_oi_trend_log(total_ce, total_pe, price=0, vwap=0):
    pcr = round(total_pe/total_ce, 2) if total_ce else 0
    signal = "BUY" if pcr > 1.1 else "SELL" if pcr < 0.85 else "NEUTRAL"
    log_entry = {
        "Time": datetime.now().strftime("%H:%M"),
        "Call": int(total_ce),
        "Put": int(total_pe),
        "Diff": int(total_pe) - int(total_ce),
        "PCR": pcr,
        "Option Signal": signal,
        "VWAP": vwap,
        "Price": price,
    }
    if "oi_trend_log" not in st.session_state:
        st.session_state["oi_trend_log"] = []
    log = st.session_state["oi_trend_log"]
    if not log or log[-1]["Time"] != log_entry["Time"]:
        log.append(log_entry)
        st.session_state["oi_trend_log"] = log

def filter_intraday_df_by_interval(df, interval):
    if df.empty:
        return df
    df["_minute"] = pd.to_datetime(df["Time"], format="%H:%M").dt.minute
    filtered = df[df["_minute"] % interval == 0].copy()
    filtered.drop(columns=["_minute"], inplace=True)
    return filtered

def style_oi_table(df):
    if df.empty:
        return df

    def ce_color(val):
        try:
            v = float(str(val).replace(",", ""))
            # Blue gradient
            return f"background-color: rgb({230 - min(int(v/20000),130)}, {230 - min(int(v/8000),110)}, 255); color: black"
        except:
            return ""
    def pe_color(val):
        try:
            v = float(str(val).replace(",", ""))
            # Red gradient
            return f"background-color: rgb(255, {230 - min(int(v/8000),110)}, {230 - min(int(v/8000),110)}); color: black"
        except:
            return ""

    styled = df.style \
        .applymap(ce_color, subset=["OI (CE)", "Chg OI (CE)"]) \
        .applymap(pe_color, subset=["OI (PE)", "Chg OI (PE)"]) \
        .set_properties(**{"background-color": "#181c20", "color": "white"}) \
        .set_table_styles([
            {"selector": "th", "props": [("position", "sticky"), ("top", "0"), ("background-color", "#1a1d1e")]}
        ])
    return styled

def style_intraday_table(df):
    if df.empty:
        return df
    def color_signal(val):
        if val == "BUY":
            return "background-color: #135b1a; color: #fff"
        if val == "SELL":
            return "background-color: #9c1818; color: #fff"
        if val == "NEUTRAL":
            return "background-color: #665a12; color: #fff"
        return ""
    styled = df.style.applymap(color_signal, subset=["Option Signal"])
    return styled

# ———————————————————————————————————————————————
def show_fyers_oi_table():
    st.subheader("📊 Fyers Option Chain – NIFTY (Autotrendr Style)")

    data = get_fyers_option_chain()
    if not data:
        if datetime.today().weekday() == 6:
            st.warning("📅 Today is Sunday. Live Fyers data unavailable.")
        else:
            st.error("⚠️ Failed to fetch Fyers data.")
        return

    expiry_raw = extract_expiries(data)
    if not expiry_raw:
        st.warning("No expiry dates found.")
        return

    # Expiry Tab/Selector (tab style)
    tab_idx = st.selectbox("Select Expiry Date", options=list(range(len(expiry_raw))), format_func=lambda x: expiry_raw[x])
    selected_expiry = datetime.strptime(expiry_raw[tab_idx], "%d-%b-%Y").strftime("%Y-%m-%d")

    # Fetch fresh for expiry
    data_exp = get_fyers_option_chain(expiry=selected_expiry)
    if not data_exp:
        st.error("⚠️ Data missing for selected expiry.")
        return

    # Intraday interval selector
    interval = st.sidebar.selectbox("Intraday Interval", [3, 5, 15], index=1, format_func=lambda x: f"{x} min")

    # ——— Main OI Table ———
    chains = data_exp.get("data", {}).get("chains", [])
    df = build_full_oi_table(chains, selected_expiry)
    st.markdown("### Nifty Option Chain")
    if not df.empty:
        st.dataframe(style_oi_table(df), use_container_width=True, height=560)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download OI Table as CSV", csv, "nifty_oi_table.csv", "text/csv")
        total_ce_oi = df["OI (CE)"].replace({',': ''}, regex=True).astype(int).sum()
        total_pe_oi = df["OI (PE)"].replace({',': ''}, regex=True).astype(int).sum()
        total_pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else 0
        st.info(f"**Total CE OI:** {format_lakh(total_ce_oi)}  **Total PE OI:** {format_lakh(total_pe_oi)}  **PCR:** {total_pcr}")
        update_oi_trend_log(total_ce_oi, total_pe_oi)

    # ——— Intraday OI Trend Table ———
    st.markdown("### Intraday Data")
    df_trend = build_intraday_trend_df()
    filtered_df = filter_intraday_df_by_interval(df_trend, interval)
    if not filtered_df.empty:
        st.dataframe(style_intraday_table(filtered_df), use_container_width=True, height=360)
        st.line_chart(filtered_df.set_index("Time")[["Call", "Put", "PCR"]])
