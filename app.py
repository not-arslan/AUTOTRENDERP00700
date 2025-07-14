import streamlit as st
import pandas as pd

def login_ui():
    st.title("🔐 FS Traders Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        df = pd.read_csv("data/users.csv")
        user = df[(df['email'] == email) & (df['password'] == password)]

        if not user.empty:
            if user.iloc[0]['approved'] == 'yes':
                st.session_state['logged_in'] = True
                st.session_state['email'] = email
                st.session_state['role'] = user.iloc[0]['role']
                st.success("Login successful! Redirecting...")
                st.stop()  # Avoid recursive rerun
            else:
                st.error("Access pending admin approval.")
        else:
            st.error("Invalid email or password.")
