import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def train_model():
    data = pd.read_csv("data/train/spill_cost_dataset.csv")

    features = [
        "degree",
        "live_range_length",
        "use_frequency"
    ]

    X = data[features]
    y = data["spill_cost"]
    groups = data["program"]

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.2,
        random_state=42
    )

    train_idx, test_idx = next(splitter.split(X, y, groups))

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]
    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        max_depth=10
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Model Evaluation")
    print(f"Mean Absolute Error: {mean_absolute_error(y_test, predictions):.4f}")
    print(f"Mean Squared Error: {mean_squared_error(y_test, predictions):.4f}")
    print(f"R2 Score: {r2_score(y_test, predictions):.4f}")

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/spill_cost_model.pkl")

    print("Model saved to models/spill_cost_model.pkl")


if __name__ == "__main__":
    train_model()