import pandas as pd
from telegram_alerts import send_telegram_message
from ml_model import predict_with_model
from data_ingestion import get_current_price
from datetime import datetime, timedelta



def calculate_rsi(data, window=14):
    if 'Close' not in data.columns or data.empty:
        print("No valid data to calculate RSI.")
        return data

    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = (100 - (100 / (1 + rs))).squeeze()
    data['RSI'] = rsi
    return data



def calculate_moving_averages(data):
    if 'Close' not in data.columns or data.empty:
        print("No valid data to calculate Moving Averages.")
        return data

    data['20DMA'] = data['Close'].rolling(window=20).mean()
    data['50DMA'] = data['Close'].rolling(window=50).mean()
    return data



last_alert_time = {}

def generate_signals(data, stock, model):
    if 'RSI' not in data.columns or '20DMA' not in data.columns or '50DMA' not in data.columns:
        print("Required columns not found to generate signals.")
        return data

    data['Technical_Signal'] = (data['RSI'] < 30) & (data['20DMA'] > data['50DMA'])
    data['ML_Prediction'] = predict_with_model(model, data)

    data['Buy_Signal'] = data['Technical_Signal'] & (data['ML_Prediction'] == 1)
    data['Signal_Crossover'] = data['Buy_Signal'] & (~data['Buy_Signal'].shift(1).fillna(False))

    signal_indices = data.index[data['Signal_Crossover']].tolist()

    cooldown_period = timedelta(minutes=30)

    for index in signal_indices:
        current_time = datetime.now()
        if stock in last_alert_time and (current_time - last_alert_time[stock]) < cooldown_period:
            continue

        current_price = get_current_price(stock)

        if current_price:
            send_telegram_message(f"Buy Signal: {stock} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} at CURRENT price {current_price:.2f}")
            last_alert_time[stock] = current_time
        else:
            send_telegram_message(f"Buy Signal: {stock} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} but failed to fetch current price.")
            last_alert_time[stock] = current_time

    return data
