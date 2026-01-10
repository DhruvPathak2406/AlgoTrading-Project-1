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


for symbol in SYMBOLS:
    print(f"\nFetching data for: {symbol}")

    try:
        data = yf.download(
            tickers=symbol,
            interval=INTERVAL,
            period=PERIOD,
            auto_adjust=False,
            progress=False,
            threads=False
        )

        if data.empty:
            print(f"No data found for {symbol}")
            continue

        filename = f"{symbol.replace('.NS', '')}_{INTERVAL}.csv"
        data.to_csv(filename)
        print(f"Saved -> {filename}")

    except Exception as e:
        print(f"Error fetching {symbol}: {e}")

print("\nDownload completed")
