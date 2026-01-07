import pandas as pd
import joblib

# ---------------- CONFIG ----------------
INITIAL_CAPITAL = 100000
COST = 0.0005  # 0.05% per trade

# ---------------- LOAD DATA ----------------
df = pd.read_csv("features.csv")

rf = joblib.load("rf_model.pkl")
features = ["SMA_20", "SMA_50", "Return", "Momentum"]

# Generate predictions (based only on past data)
df["Pred"] = rf.predict(df[features])

capital = INITIAL_CAPITAL
position = 0.0

# ---------------- BACKTEST LOOP ----------------
# IMPORTANT: trade on NEXT candle open
for i in range(len(df) - 2):
    signal = df.loc[i, "Pred"]
    trade_price = df.loc[i + 1, "Open"]

    # BUY
    if signal == 1 and position == 0:
        position = (capital * (1 - COST)) / trade_price
        capital = 0.0

    # SELL
    elif signal == 0 and position > 0:
        capital = position * trade_price * (1 - COST)
        position = 0.0

# ---------------- FINAL VALUE ----------------
final_price = df.iloc[-1]["Close"]
final_value = capital if capital > 0 else position * final_price

print("Final Portfolio Value:", round(final_value, 2))
print("Net P/L:", round(final_value - INITIAL_CAPITAL, 2))
