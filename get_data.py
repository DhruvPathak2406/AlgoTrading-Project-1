import yfinance as yf
import pandas as pd


SYMBOLS = [
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "KOTAKBANK.NS",
    "AXISBANK.NS",
    "INDUSINDBK.NS",
    "FEDERALBNK.NS",
    "BANDHANBNK.NS",
    "PNB.NS",
    "BANKBARODA.NS",
    "IDFCFIRSTB.NS",
    "AUBANK.NS"
]

INTERVAL = "5m"   
PERIOD = "1mo"   

print("Downloading data...")

data_dict = {}

for symbol in SYMBOLS:
    print(f"\nFetching data for: {symbol}")

    data = yf.download(
    tickers=symbol,
    interval=INTERVAL,
    period=PERIOD,
    auto_adjust=False
)


    if data.empty:
        print(f"No data found for {symbol}")
        continue


    filename = f"{symbol.replace('.NS', '')}_{INTERVAL}.csv"
    data.to_csv(filename)
    print(f"Saved -> {filename}")

    data_dict[symbol] = data

print("\nDownload completed")
