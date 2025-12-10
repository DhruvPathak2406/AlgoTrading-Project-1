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

print("Downloading BankNifty company data...")

data_dict = {}

for symbol in SYMBOLS:
    print(f"\nFetching data for: {symbol}")

    data = yf.download(
        tickers=symbol,
        interval=INTERVAL,
        period=PERIOD
    )

    if data.empty:
        print(f"⚠️ WARNING: No data found for {symbol}")
        continue


    filename = f"{symbol.replace('.NS', '')}_{INTERVAL}.csv"
    data.to_csv(filename)
    print(f"Saved -> {filename}")

    data_dict[symbol] = data

print("\nDownload completed for all BankNifty companies.")
