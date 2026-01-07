import pandas as pd
import numpy as np

# Load raw data
df = pd.read_csv("HDFCBANK_5m.csv")

# Ensure numeric columns
df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
df["Close"] = pd.to_numeric(df["Close"], errors="coerce")

# Drop rows where price itself is missing
df.dropna(subset=["Open", "Close"], inplace=True)

# ---------------- FEATURES ----------------
df["SMA_20"] = df["Close"].rolling(20).mean()
df["SMA_50"] = df["Close"].rolling(50).mean()
df["Return"] = df["Close"].pct_change()
df["Momentum"] = df["Close"] - df["Close"].shift(5)

# ---------------- TARGET ----------------
# Predict: will price move +0.2% in next 3 candles?
future_return = (df["Close"].shift(-3) - df["Close"]) / df["Close"]
df["Target"] = (future_return > 0.002).astype(int)

# Final cleanup AFTER all calculations
df.dropna(inplace=True)

# Save
df.to_csv("features.csv", index=False)
print("Features created")
