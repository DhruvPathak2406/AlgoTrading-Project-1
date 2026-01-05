# 📈 Machine Learning–Driven Algorithmic Trading Bot (Indian Equity Markets)

## Project Overview

This project implements an **end-to-end algorithmic trading system** for Indian equity markets using **machine learning–based signal generation**, technical indicators, and **paper trading on live market data**.

The objective of this project is to demonstrate:
- A complete quantitative trading pipeline
- Feature engineering on intraday market data
- Supervised ML model training for price direction prediction
- Ensemble-based trade decision making
- Live paper trading with real-time portfolio tracking

Due to limited time for final validation and demonstration, **HDFCBANK (NSE)** was used as the primary stock for testing and live execution.  
However, the system is **fully designed to support multiple stocks**, and historical data for several NSE banking stocks has been included in the repository.

---

## Markets & Instruments

- **Market**: Indian Equity Market (NSE)
- **Primary Test Instrument**: `HDFCBANK.NS`
- **Other Supported Stocks** (data available):
  - ICICIBANK
  - SBIN
  - AXISBANK
  - KOTAKBANK
  - INDUSINDBK
  - FEDERALBNK
  - BANDHANBNK
  - PNB
  - BANKBARODA
  - IDFCFIRSTB
  - AUBANK

> **Note**: HDFCBANK was used for dummy checking, debugging, and final live paper trading due to time constraints. The pipeline is generalizable and can be extended to other stocks by changing configuration variables.

- **Timeframe**: 5-minute candles
- **Execution Mode**: Paper Trading (Live market prices, simulated capital)

---

## Tech Stack

- **Language**: Python 3
- **Libraries**:
  - `pandas`, `numpy` – data manipulation
  - `yfinance` – historical and live market data
  - `scikit-learn` – Random Forest model
  - `xgboost` – Gradient Boosted Trees
  - `joblib` – model serialization
- **ML Models Used**:
  - Random Forest Classifier
  - XGBoost Classifier

---

## Repository Structure

