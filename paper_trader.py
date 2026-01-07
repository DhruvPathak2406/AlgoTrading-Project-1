import time
import pandas as pd
import joblib
import yfinance as yf
from datetime import datetime

# -------------------------------------------------
# ENV LOADER
# -------------------------------------------------
def get_env_config():
    config = {
        "SYMBOLS": "HDFCBANK.NS",
        "INITIAL_CAPITAL": "100000",
        "INTERVAL": "5m",
        "MODEL_RF": "rf_model.pkl",
        "MODEL_XGB": "xgb_model.pkl",
        "COST": "0.0005"
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
COST = float(conf["COST"])

# -------------------------------------------------
# LOAD MODELS
# -------------------------------------------------
try:
    rf_model = joblib.load(conf["MODEL_RF"])
    xgb_model = joblib.load(conf["MODEL_XGB"])
except:
    print("ERROR: Models not found")
    raise SystemExit

# -------------------------------------------------
# STATE SETUP
# -------------------------------------------------
ALLOCATION = INITIAL_CAPITAL / len(SYMBOLS)

state = {
    s: {"cap": ALLOCATION, "pos": 0.0}
    for s in SYMBOLS
}

FEATURES = ["SMA_20", "SMA_50", "Return", "Momentum"]

# -------------------------------------------------
# LIVE PAPER TRADING LOOP
# -------------------------------------------------
while True:
    try:
        total_value = 0.0

        for ticker in SYMBOLS:
            df = yf.download(
                ticker,
                period="1d",
                interval=INTERVAL,
                auto_adjust=False,
                progress=False
            )

            if df.empty or len(df) < 55:
                total_value += state[ticker]["cap"]
                continue

            # ---------------- FEATURES (same as training)
            df["SMA_20"] = df["Close"].rolling(20).mean()
            df["SMA_50"] = df["Close"].rolling(50).mean()
            df["Return"] = df["Close"].pct_change()
            df["Momentum"] = df["Close"] - df["Close"].shift(5)

            row = df.iloc[-1]
            if row[FEATURES].isnull().any():
                continue

            price = float(row["Close"])
            X = row[FEATURES].values.reshape(1, -1)

            p_rf = rf_model.predict(X)[0]
            p_xgb = xgb_model.predict(X)[0]

            # ---------------- DEBUG OUTPUT
            print(
                f"{datetime.now()} | {ticker} | "
                f"RF={p_rf} XGB={p_xgb} | Price={price:.2f}"
            )

            # ---------------- BUY (majority vote)
            if (p_rf + p_xgb) >= 1 and state[ticker]["pos"] == 0:
                state[ticker]["pos"] = (state[ticker]["cap"] * (1 - COST)) / price
                state[ticker]["cap"] = 0.0
                print(f"BUY {ticker} @ {price:.2f}")

            # ---------------- SELL
            elif (p_rf + p_xgb) == 0 and state[ticker]["pos"] > 0:
                state[ticker]["cap"] = state[ticker]["pos"] * price * (1 - COST)
                state[ticker]["pos"] = 0.0
                print(f"SELL {ticker} @ {price:.2f}")

            total_value += (
                state[ticker]["cap"] +
                state[ticker]["pos"] * price
            )

        roi = ((total_value - INITIAL_CAPITAL) / INITIAL_CAPITAL) * 100
        print(f"PORTFOLIO VALUE: {total_value:.2f} | ROI: {roi:.2f}%\n")

        time.sleep(300)  # 5 minutes

    except KeyboardInterrupt:
        print("Stopped by user.")
        break

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
