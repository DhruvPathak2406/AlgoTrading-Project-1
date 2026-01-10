import pandas as pd
import joblib

INITIAL_CAPITAL = 100000
COST = 0.0005

FEATURES = ["SMA_20", "SMA_50", "Return", "Momentum"]

df = pd.read_csv("features.csv")
rf = joblib.load("rf_model.pkl")
xgb = joblib.load("xgb_model.pkl")

symbols = df["Symbol"].unique()
capital_per_stock = INITIAL_CAPITAL / len(symbols)

total_final = 0.0

for symbol in symbols:
    data = df[df["Symbol"] == symbol].reset_index(drop=True)

    split = int(len(data) * 0.8)
    data = data.iloc[split:].reset_index(drop=True)

    proba_rf = rf.predict_proba(data[FEATURES])[:, 1]
    proba_xgb = xgb.predict_proba(data[FEATURES])[:, 1]

    data["Signal"] = ((proba_rf + proba_xgb) / 2 > 0.6).astype(int)

    capital = capital_per_stock
    position = 0.0

    for i in range(len(data) - 1):
        signal = data.loc[i, "Signal"]
        price = data.loc[i + 1, "Open"]

        if signal == 1 and position == 0:
            position = (capital * (1 - COST)) / price
            capital = 0.0

        elif signal == 0 and position > 0:
            capital = position * price * (1 - COST)
            position = 0.0

    final_price = data.iloc[-1]["Close"]
    final_value = capital if capital > 0 else position * final_price * (1 - COST)
    total_final += final_value

    print(f"{symbol} Final Value: {final_value:.2f}")

print("\nTotal Portfolio Value:", round(total_final, 2))
print("Net P/L:", round(total_final - INITIAL_CAPITAL, 2))
