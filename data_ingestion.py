import yfinance as yf
import pandas as pd


def fetch_stock_data(ticker, period='6mo', interval='1d'):
    try:
        data = yf.download(ticker, period=period, interval=interval)
        if data.empty:
            print(f"No data fetched for {ticker}.")
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()


def get_current_price(ticker):
    try:
        ticker_data = yf.Ticker(ticker)
        todays_data = ticker_data.history(period='1d', interval='1m')
        if not todays_data.empty:
            return todays_data['Close'][-1]
        else:
            return None
    except Exception as e:
        print(f"Error fetching current price for {ticker}: {e}")
        return None
