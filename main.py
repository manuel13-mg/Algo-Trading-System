from data_ingestion import fetch_stock_data
from strategy import calculate_rsi, calculate_moving_averages, generate_signals
from backtest import backtest_strategy
from google_sheets import update_google_sheet
from ml_model import train_ml_model

stocks = [
    'TCS.NS', 'HDFCBANK.NS', 'RELIANCE.NS', 'INFY.NS', 'ICICIBANK.NS', 'SBIN.NS', 'AXISBANK.NS', 'WIPRO.NS', 'HCLTECH.NS', 'BAJFINANCE.NS',
    'LT.NS', 'MARUTI.NS', 'KOTAKBANK.NS', 'ASIANPAINT.NS', 'ULTRACEMCO.NS', 'ITC.NS', 'TITAN.NS', 'BHARTIARTL.NS', 'ONGC.NS', 'NTPC.NS',
    'POWERGRID.NS', 'GRASIM.NS', 'SUNPHARMA.NS', 'BAJAJ-AUTO.NS', 'TATAMOTORS.NS', 'EICHERMOT.NS', 'BRITANNIA.NS', 'HEROMOTOCO.NS',
    'HINDUNILVR.NS', 'DRREDDY.NS', 'BPCL.NS', 'CIPLA.NS', 'DIVISLAB.NS', 'TATASTEEL.NS', 'JSWSTEEL.NS', 'COALINDIA.NS', 'ADANIENT.NS',
    'ADANIPORTS.NS', 'HINDALCO.NS', 'UPL.NS', 'DABUR.NS', 'GAIL.NS', 'M&M.NS', 'VEDL.NS', 'PEL.NS', 'AMBUJACEM.NS', 'BANKBARODA.NS',
    'BHEL.NS', 'CANBK.NS', 'CHOLAFIN.NS', 'CUMMINSIND.NS', 'DLF.NS', 'GODREJCP.NS', 'INDIGO.NS', 'IOC.NS', 'MANAPPURAM.NS',
    'MOTHERSUMI.NS', 'PIDILITIND.NS', 'PNB.NS', 'SAIL.NS', 'SHREECEM.NS', 'SRF.NS', 'TVSMOTOR.NS', 'UNIONBANK.NS', 'ZEEL.NS'
]

all_accuracies = []

for stock in stocks:
    data = fetch_stock_data(stock)

    if data.empty or 'Close' not in data.columns:
        print(f"Skipping {stock} due to invalid or missing 'Close' data.")
        continue

    data = calculate_rsi(data)
    data = calculate_moving_averages(data)

    model, accuracy = train_ml_model(data, stock, all_accuracies)
    print(f"Best ML Model Accuracy for {stock}: {accuracy * 100:.2f}%")

    if model is not None:
        data = generate_signals(data, stock, model)

        trades = backtest_strategy(data)
        print(f"\nResults for {stock}:")
        for trade in trades:
            print(trade)

        update_google_sheet(trades, f"{stock} Trade Log")

from collections import defaultdict

# Model selection across all stocks
combined_accuracies = defaultdict(list)

for stock_accuracy in all_accuracies:
    for model_name, accuracy in stock_accuracy.items():
        combined_accuracies[model_name].append(accuracy)

average_accuracies = {model: sum(acc) / len(acc) for model, acc in combined_accuracies.items()}
best_model_overall = max(average_accuracies, key=average_accuracies.get)
print(f"\nOverall Best Model Across All Stocks: {best_model_overall} with Average Accuracy: {average_accuracies[best_model_overall] * 100:.2f}%")

print("\nBacktesting, Google Sheet update, and Buy Signal alerts completed.")
