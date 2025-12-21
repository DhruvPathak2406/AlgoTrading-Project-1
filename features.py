import pandas as pd
import numpy as np

df = pd.read_csv("HDFCBANK_5m.csv")

df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df.dropna(inplace=True)

df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()
df["Return"] = df["Close"].pct_change()
df["Momentum"] = df["Close"] - df["Close"].shift(5)

df.dropna(inplace=True)

df["Target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

df.dropna(inplace=True)

df.to_csv("features.csv", index=False)
print("Features created")
