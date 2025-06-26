# Algo Trading System

## 📈 Project Overview
This project is a fully automated **Algorithmic Stock Trading System** built with Python. It fetches stock data, applies technical and machine learning-based analysis, generates buy signals, sends real-time Telegram alerts, and logs trades into Google Sheets.

---

## 🚀 Features
- ✅ Real-time & historical stock data ingestion via **Yahoo Finance API**
- ✅ Calculation of **RSI, 20DMA, 50DMA** for technical analysis
- ✅ Automated **ML model selection per stock** (SVC, RandomForest, LogisticRegression, KNN)
- ✅ **Buy Signal Detection** using combined ML and technical indicators
- ✅ **Telegram Alerts** for live buy signals
- ✅ Automatic trade logging into **Google Sheets**
- ✅ **Cooldown Management** to prevent repeated alerts
- ✅ Monitors **60+ Indian stocks simultaneously**

---

## 🗂️ Folder Structure
```plaintext
data_ingestion.py      # Data fetching and real-time price retrieval
strategy.py            # Signal calculation and Telegram integration
backtest.py            # Backtesting strategy
ml_model.py            # ML training and prediction
google_sheets.py       # Google Sheets API integration
telegram_alerts.py     # Telegram Bot alerts
main.py                # Master pipeline
README.md              # Project documentation
