import time
import pandas as pd
import joblib
import yfinance as yf
from datetime import datetime

SYMBOLS = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "KOTAKBANK.NS"
]

INITIAL_CAPITAL = 100000
INTERVAL = "5m"
COST = 0.0005

FEATURES = ["SMA_20", "SMA_50", "Return", "Momentum"]

xgb_model = joblib.load("xgb_model.pkl")
xgb_model.set_params(n_jobs=1)

capital_per_symbol = INITIAL_CAPITAL / len(SYMBOLS)

state = {
    s: {"cap": capital_per_symbol, "pos": 0.0}
    for s in SYMBOLS
}

print("Paper trader started...\n")

while True:
    try:
        for ticker in SYMBOLS:
            df = yf.download(
                ticker,
                period="1d",
                interval=INTERVAL,
                auto_adjust=False,
                progress=False,
                threads=False
            )

            if df.empty or len(df) < 55:
                continue

            df["SMA_20"] = df["Close"].rolling(20).mean()
            df["SMA_50"] = df["Close"].rolling(50).mean()
            df["Return"] = df["Close"].pct_change()
            df["Momentum"] = df["Close"] - df["Close"].shift(5)

            row = df.iloc[-2]

            if row[FEATURES].isnull().any():
                continue

            price = float(row["Close"])

            X = pd.DataFrame(
                [[
                    float(row["SMA_20"]),
                    float(row["SMA_50"]),
                    float(row["Return"]),
                    float(row["Momentum"])
                ]],
                columns=FEATURES
            )

            prob = xgb_model.predict_proba(X)[0][1]

            now = datetime.now()
            print(
                f"{now} | {ticker} | "
                f"XGB={prob:.2f} | Price={price:.2f}"
            )

            if prob > 0.6 and state[ticker]["pos"] == 0:
                state[ticker]["pos"] = (state[ticker]["cap"] * (1 - COST)) / price
                state[ticker]["cap"] = 0.0
                print(f"BUY  {ticker}")

            elif prob < 0.4 and state[ticker]["pos"] > 0:
                state[ticker]["cap"] = state[ticker]["pos"] * price * (1 - COST)
                state[ticker]["pos"] = 0.0
                print(f"SELL {ticker}")

        time.sleep(300)

    except KeyboardInterrupt:
        print("Stop.")
        break
