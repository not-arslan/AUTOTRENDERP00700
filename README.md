# FS Trader - Full Setup (Live)

## Setup
1. Create `.streamlit/secrets.toml` with:
```toml
api_key = "YOUR_ANGEL_API_KEY"
client_id = "YOUR_CLIENT_ID"
client_password = "YOUR_PASSWORD"
totp_secret = "YOUR_TOTP_SECRET"
openai_api_key = "YOUR_OPENAI_KEY"
telegram_bot_token = "YOUR_TELEGRAM_TOKEN"
telegram_chat_id = "YOUR_TELEGRAM_CHAT_ID"
email_user = "your_email@gmail.com"
email_pass = "your_email_app_password"
```

2. Install & run:
```bash
pip install -r requirements.txt
streamlit run app.py
```
