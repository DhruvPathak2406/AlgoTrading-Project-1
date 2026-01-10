import pandas as pd

df = pd.read_csv("HDFCBANK_5m.csv")

df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
df.dropna(inplace=True)
df.reset_index(drop=True, inplace=True)

df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()
df.dropna(inplace=True)

df["Signal"] = "HOLD"

for i in range(1, len(df)):
    if df.loc[i, "SMA_20"] > df.loc[i, "SMA_50"] and df.loc[i-1, "SMA_20"] <= df.loc[i-1, "SMA_50"]:
        df.loc[i, "Signal"] = "CALL"
    elif df.loc[i, "SMA_20"] < df.loc[i, "SMA_50"] and df.loc[i-1, "SMA_20"] >= df.loc[i-1, "SMA_50"]:
        df.loc[i, "Signal"] = "PUT"

signal_map = {"HOLD": 0, "CALL": 1, "PUT": 2}
df["Signal_Label"] = df["Signal"].map(signal_map)

df.to_csv("HDFCBANK_SMA_SIGNALS.csv", index=False)

print("SMA strategy created")
