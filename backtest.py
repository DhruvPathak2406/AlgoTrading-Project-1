import pandas as pd
import joblib

df = pd.read_csv("features.csv")

rf = joblib.load("rf_model.pkl")

features = ["SMA_20", "SMA_50", "Return", "Momentum"]

df["Pred"] = rf.predict(df[features])

capital = 100000
position = 0

for i in range(len(df) - 1):
    pred = df.loc[i, "Pred"]
    price = df.loc[i, "Close"]

    if pred == 1 and position == 0:
        position = capital / price
        capital = 0

    elif pred == 0 and position > 0:
        capital = position * price
        position = 0

final_value = capital if capital > 0 else position * df.iloc[-1]["Close"]
print("Final Portfolio Value:", final_value)
