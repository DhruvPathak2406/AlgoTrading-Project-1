import pandas as pd
import joblib

INITIAL_CAPITAL = 100000
COST = 0.0005

FEATURES = ["SMA_20", "SMA_50", "Return", "Momentum"]

rf = joblib.load("rf_model.pkl")
xgb = joblib.load("xgb_model.pkl")

df = pd.read_csv("features.csv")

symbols = df["Symbol"].unique()
capital_per_stock = INITIAL_CAPITAL / len(symbols)

portfolio_value = 0.0
trade_log = []

for symbol in symbols:
    data = df[df["Symbol"] == symbol].reset_index(drop=True)

    split = int(len(data) * 0.8)
    data = data.iloc[split:].reset_index(drop=True)

    capital = capital_per_stock
    position = 0.0

    for i in range(len(data) - 1):
        row = data.loc[i]
        next_open = data.loc[i + 1, "Open"]

        X = pd.DataFrame([row[FEATURES]])

        p_rf = rf.predict_proba(X)[0][1]
        p_xgb = xgb.predict_proba(X)[0][1]
        signal = 0.5 * p_rf + 0.5 * p_xgb

        if signal > 0.6 and position == 0:
            position = (capital * (1 - COST)) / next_open
            capital = 0.0
            trade_log.append((symbol, "BUY", next_open, data.loc[i + 1, "Datetime"]))

        elif signal < 0.4 and position > 0:
            capital = position * next_open * (1 - COST)
            position = 0.0
            trade_log.append((symbol, "SELL", next_open, data.loc[i + 1, "Datetime"]))

    final_price = data.iloc[-1]["Close"]
    final_value = capital if capital > 0 else position * final_price * (1 - COST)
    portfolio_value += final_value

    print(f"{symbol} Final Value: {final_value:.2f}")

print("\nTOTAL PORTFOLIO VALUE:", round(portfolio_value, 2))
print("NET P/L:", round(portfolio_value - INITIAL_CAPITAL, 2))

trade_df = pd.DataFrame(trade_log, columns=["Symbol", "Action", "Price", "Time"])
trade_df.to_csv("historical_trades.csv", index=False)

print("\nsaved as historical_trades.csv")
