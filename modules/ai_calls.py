import pandas as pd

def generate_ai_calls():
    # Dummy AI call generator
    data = {
        "Symbol": ["CRUDEOIL", "BANKNIFTY"],
        "Call": ["BUY", "SELL"],
        "Entry": [5640, 49700],
        "Stop Loss": [5600, 49900],
        "Target": [5700, 49300],
        "Confidence": [0.88, 0.76]
    }
    return pd.DataFrame(data)
