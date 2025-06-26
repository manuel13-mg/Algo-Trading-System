from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd


def train_ml_model(data, stock_name, accuracy_log):
    if data.empty or 'RSI' not in data.columns or '20DMA' not in data.columns or '50DMA' not in data.columns:
        print("Insufficient data to train ML model.")
        return None, 0.0

    data = data.dropna()
    if data.empty:
        print("No valid data after dropping NaN values.")
        return None, 0.0

    data['Target'] = (data['Close'].shift(-1) > data['Close']).astype(int)

    features = data[['RSI', '20DMA', '50DMA', 'Volume']]
    target = data['Target']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, shuffle=False)

    models = {
        'SVC': SVC(kernel='rbf', probability=True, random_state=42),
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'KNN': KNeighborsClassifier()
    }

    best_model = None
    best_accuracy = 0
    best_model_name = ''

    local_accuracies = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"{name} Accuracy on {stock_name}: {accuracy * 100:.2f}%")
        local_accuracies[name] = accuracy
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = model
            best_model_name = name

    accuracy_log.append(local_accuracies)
    print(f"Selected Model for {stock_name}: {best_model_name} with Accuracy: {best_accuracy * 100:.2f}%")
    return best_model, best_accuracy



def predict_with_model(model, data):
    data = data.dropna()
    if data.empty:
        return pd.Series([0] * len(data), index=data.index)

    features = data[['RSI', '20DMA', '50DMA', 'Volume']]
    predictions = model.predict(features)
    return pd.Series(predictions, index=data.index)