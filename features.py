import pandas as pd

FILES = [
    "HDFCBANK_5m.csv",
    "ICICIBANK_5m.csv",
    "KOTAKBANK_5m.csv"
]

all_data = []

for file in FILES:
    symbol = file.replace("_5m.csv", "")
    print(f"Processing {symbol}")

    df = pd.read_csv(file)

    df.reset_index(inplace=True)
    df.rename(columns={"index": "Datetime"}, inplace=True)

    df.sort_values("Datetime", inplace=True)

    df["Open"] = pd.to_numeric(df["Open"], errors="coerce")
    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Open", "Close"], inplace=True)

    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    df["Return"] = df["Close"].pct_change()
    df["Momentum"] = df["Close"] - df["Close"].shift(5)

    future_return = (df["Close"].shift(-3) - df["Close"]) / df["Close"]
    df["Target"] = (future_return > 0.002).astype(int)

    df["Symbol"] = symbol

    df.dropna(inplace=True)
    all_data.append(df)

final_df = pd.concat(all_data, ignore_index=True)
final_df.to_csv("features.csv", index=False)

print("csv created successfully")
