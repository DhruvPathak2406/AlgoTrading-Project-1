import time
import pandas as pd
import joblib
import yfinance as yf
from datetime import datetime

def get_env_config():
    config = {
        "SYMBOLS": "HDFCBANK.NS",
        "INITIAL_CAPITAL": 100000.0,
        "INTERVAL": "5m",
        "MODEL_RF": "rf_model.pkl",
        "MODEL_XGB": "xgb_model.pkl"
    }
    try:
        with open(".env", "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    k, v = line.strip().split("=", 1)
                    config[k] = v
    except:
        pass
    return config

conf = get_env_config()
SYMBOLS = conf["SYMBOLS"].split(",")
INITIAL_CAPITAL = float(conf["INITIAL_CAPITAL"])
INTERVAL = conf["INTERVAL"]
ALLOCATION = INITIAL_CAPITAL / len(SYMBOLS)

try:
    rf_model = joblib.load(conf["MODEL_RF"])
    xgb_model = joblib.load(conf["MODEL_XGB"])
except:
    print("Error: Models not found. Check .env file.")
    raise SystemExit

state = {s: {"cap": ALLOCATION, "pos": 0.0} for s in SYMBOLS}

while True:
    try:
        total_val = 0.0
        for ticker in SYMBOLS:
            df = yf.download(ticker, period="1d", interval=INTERVAL, progress=False)
            if df.empty or len(df) < 55:
                total_val += state[ticker]["cap"]
                continue
            
            df["SMA_20"] = df["Close"].rolling(20).mean()
            df["SMA_50"] = df["Close"].rolling(50).mean()
            df["Return"] = df["Close"].pct_change()
            df["Momentum"] = df["Close"] - df["Close"].shift(5)
            
            row = df.iloc[-1]
            if row.isnull().any(): continue
            
            price = float(row["Close"])
            X = row[["SMA_20", "SMA_50", "Return", "Momentum"]].values.reshape(1, -1)
            
            p_rf, p_xgb = rf_model.predict(X)[0], xgb_model.predict(X)[0]
            
            if p_rf == 1 and p_xgb == 1 and state[ticker]["pos"] == 0:
                state[ticker]["pos"] = state[ticker]["cap"] / price
                state[ticker]["cap"] = 0.0
                print(f"[{datetime.now()}] BUY {ticker} @ {price:.2f}")
            elif (p_rf == 0 or p_xgb == 0) and state[ticker]["pos"] > 0:
                state[ticker]["cap"] = state[ticker]["pos"] * price
                state[ticker]["pos"] = 0.0
                print(f"[{datetime.now()}] SELL {ticker} @ {price:.2f}")

            total_val += state[ticker]["cap"] + (state[ticker]["pos"] * price)

        roi = ((total_val - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        print(f"PORTFOLIO: {total_val:.2f} | ROI: {roi:.2f}%")
        time.sleep(300)
    except KeyboardInterrupt:
        break
    except:
        time.sleep(60)