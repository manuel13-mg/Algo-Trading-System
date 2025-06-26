def backtest_strategy(data):
    if 'Buy_Signal' not in data.columns or data.empty:
        print("No valid data to backtest.")
        return []

    trades = []
    position = None

    for index, row in data.iterrows():
        if row['Buy_Signal'] is True and position is None:
            position = {'entry_price': row['Close'], 'entry_date': index}
        elif row['Buy_Signal'] is False and position is not None:
            exit_price = row['Close']
            profit = exit_price - position['entry_price']
            trades.append({
                'Entry Date': position['entry_date'],
                'Exit Date': index,
                'Entry Price': position['entry_price'],
                'Exit Price': exit_price,
                'Profit': profit
            })
            position = None

    return trades
