import joblib
import pandas as pd

rf = joblib.load("rf_model.pkl")
xgb = joblib.load("xgb_model.pkl")

df = pd.read_csv("features.csv")

latest = df.iloc[-1][["SMA_20", "SMA_50", "Return", "Momentum"]].values.reshape(1, -1)

rf_pred = rf.predict(latest)[0]
xgb_pred = xgb.predict(latest)[0]

if rf_pred == 1 and xgb_pred == 1:
    signal = "BUY"
elif rf_pred == 0 and xgb_pred == 0:
    signal = "SELL"
else:
    signal = "NO TRADE"

print("Trading Signal:", signal)
