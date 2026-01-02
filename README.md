# Forecast Quant: Ensemble ML Trading System

Forecast Quant is an end-to-end algorithmic trading engine designed for the Indian Banking Sector (NSE). Unlike traditional systems that rely solely on technical indicators, this project uses an Ensemble Machine Learning approach—combining Random Forest and XGBoost classifiers—to predict 5-minute price movements.

# How It Works?
The system follows a strict data-to-execution pipeline:

Data Acquisition: Fetches real-time and historical 5-minute OHLCV data for major banking tickers (HDFCBANK, SBIN, ICICIBANK, etc.) via the yfinance API.

Feature Engineering: Transforms raw price data into predictive features, including SMA Crossovers, Momentum, and Log Returns.

Ensemble Modeling: Trains two separate ML models (Random Forest and XGBoost) to identify high-probability "Up" moves while ignoring market noise.

Signal Validation: Only executes a "BUY" signal when both models agree (The Ensemble Rule), providing a built-in safety filter.

Live Paper Trading: Runs a continuous loop that monitors the live market, manages virtual capital, and tracks real-time ROI.

# Tech Stack
Language: Python

Data Science: pandas, numpy

Machine Learning: scikit-learn (Random Forest), xgboost (XGBoost)

Financial Data: yfinance

# Project Structure

get_data.py: Multi-ticker historical data downloader.

features.py: Technical indicator generator and target labeling.

train_models.py: Training script for the .pkl model files.

backtest.py: Historical simulation engine to verify strategy ROI before going live.

paper_trader.py: The main execution engine for real-time market monitoring.

.env: Local configuration for tickers and capital.

# Execution Order
To run the project for the first time, execute the files in this specific order:

python get_data.py (Downloads the raw data)

python features.py (Creates the training dataset)

python train_models.py (Generates the .pkl model files)

python backtest.py (Checks historical performance)

python paper_trader.py (Starts live monitoring)

# Backtest Results
On initial testing with HDFC Bank 5-minute data, the Random Forest model achieved a Final Portfolio Value of ₹113,043 from a starting capital of ₹100,000, representing a ~13% return over the test period.
