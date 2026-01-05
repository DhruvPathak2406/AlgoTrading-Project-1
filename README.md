# ForeCastX - Machine Learning–Driven Algorithmic Trading Bot
## Project Overview

This project implements an algorithmic trading system for Indian equity markets using machine learning–based signal generation, technical indicators, and paper trading on live market data.

The goal of the project is to demonstrate a complete trading workflow, starting from raw market data and ending with live (paper) trade execution and portfolio performance tracking.

Due to limited time for final validation and live demonstration, HDFCBANK (NSE) was used as the primary stock for dummy checking, debugging, and live paper trading. However, the overall pipeline is generic and supports multiple stocks. Historical data for several NSE banking stocks has been included in the repository to demonstrate scalability.

---

## Markets & Instruments

Market: Indian Equity Market (NSE)

Primary test stock (used for dummy check and live execution):
- HDFCBANK.NS

Other supported stocks (historical data available):
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

Timeframe: 5-minute candles  
Execution mode: Paper trading

Note: HDFCBANK was used for final testing and live execution due to time constraints. Switching to other stocks only requires changing configuration values.

---

## Tech Stack

Language:
- Python 

Libraries and tools:
- pandas, numpy – data processing and analysis
- yfinance – historical and live market data
- scikit-learn – Random Forest model
- xgboost – Gradient Boosted Trees model
- joblib – model persistence

Machine learning models:
- Random Forest Classifier
- XGBoost Classifier

---

## Repository Structure

project/
│
├── data/
│   ├── historical/        Historical 5-minute OHLCV CSV files
│   └── signals/           Strategy-generated signal files
│
├── models/
│   ├── rf_model.pkl       Trained Random Forest model
│   └── xgb_model.pkl      Trained XGBoost model
│
├── src/
│   ├── get_data.py        Download historical intraday data
│   ├── features.py        Feature engineering
│   ├── train_models.py    Train and evaluate ML models
│   ├── trade_logic.py     Model-based signal generation
│   ├── backtest.py        Historical backtesting
│   ├── paper_trader.py    Live paper trading engine
│   └── strategy_SMA.py    SMA crossover baseline strategy
│
├── .env.example           Example environment variables
├── requirements.txt
└── README.md


---

## Data Collection

File: get_data.py

This script downloads 5-minute intraday OHLCV data from Yahoo Finance for selected NSE stocks. By default, it downloads approximately one month of data per stock and saves each symbol as a CSV file.

---

## Feature Engineering

File: features.py

From the historical OHLC data, the following technical features are computed:

- SMA_20: 20-period Simple Moving Average
- SMA_50: 50-period Simple Moving Average
- Return: Percentage change in closing price
- Momentum: Difference between the current close and the close 5 periods earlier

A target variable is created:
- 1 if the next candle closes higher
- 0 if the next candle closes lower or equal

The processed dataset is saved as features.csv and is used for both model training and backtesting.

---

## Machine Learning Models

File: train_models.py

Two supervised classification models are trained to predict short-term price direction.

Random Forest Classifier:
- Number of trees: 300
- Maximum depth: 6
- Used as a robust baseline model

XGBoost Classifier:
- Number of estimators: 400
- Maximum depth: 5
- Learning rate: 0.05
- Used for higher predictive performance on structured financial data

The dataset is split without shuffling to preserve time-series order.  
Model accuracy on the test set is printed during training.

The trained models are saved as:
- rf_model.pkl
- xgb_model.pkl

---

## Trading Strategy Logic

File: trade_logic.py

For the most recent market candle:
1. Technical features are computed in real time
2. Both ML models independently generate predictions
3. Final trade decision is based on model agreement

Decision rules:
- BUY when both Random Forest and XGBoost predict upward movement
- SELL when both models predict downward movement
- NO TRADE when the models disagree

This ensemble-based decision logic helps reduce false signals and overtrading.

---

## Baseline Strategy

File: strategy_SMA.py

A traditional Simple Moving Average crossover strategy is implemented:

- BUY (CALL) when SMA_20 crosses above SMA_50
- SELL (PUT) when SMA_20 crosses below SMA_50

This strategy serves as a baseline for comparison and as a sanity check against the ML-based strategy.

---

## Backtesting

File: backtest.py

The backtesting module simulates trading on historical feature data using a long-only strategy. Capital is fully allocated to each position, and the final portfolio value is printed at the end of the simulation.

This step ensures the strategy logic works correctly before live deployment.

---

## Live Paper Trading Engine

File: paper_trader.py

This is the main execution engine of the project.

Key characteristics:
- Uses live market prices fetched at 5-minute intervals
- Trades are simulated (paper trading)
- Initial capital is divided across selected symbols
- Portfolio value and ROI are printed after each cycle

Trading rules:
- BUY when both ML models predict bullish movement and no position exists
- SELL when either model turns bearish
- HOLD otherwise

Example output:
[2026-01-07 10:15:00] BUY HDFCBANK.NS @ 1642.50
PORTFOLIO: 101820.40 | ROI: 1.82%

---

## Environment Configuration

File: .env.example

Example configuration:

SYMBOLS=HDFCBANK.NS
INITIAL_CAPITAL=100000
INTERVAL=5m
MODEL_RF=rf_model.pkl
MODEL_XGB=xgb_model.pkl

This allows easy customization of traded stocks, capital, timeframe, and model selection.

---

## How to Run the Project

1. Install dependencies:
   pip install -r requirements.txt

2. Download historical data:
   python src/get_data.py

3. Generate features:
   python src/features.py

4. Train models:
   python src/train_models.py

5. Run backtesting:
   python src/backtest.py

6. Start live paper trading:
   python src/paper_trader.py

---

## Performance Metrics

During backtesting and live paper trading, the following metrics are observed:
- Directional prediction accuracy
- Portfolio return (ROI percentage)
- Number of trades executed
- Real-time portfolio value

Exact metrics are displayed during execution and demonstrated in the recorded project video.

---

## Contribution Guidelines

1. Fork the repository
2. Create a new feature branch
3. Commit changes with clear messages
4. Submit a pull request
