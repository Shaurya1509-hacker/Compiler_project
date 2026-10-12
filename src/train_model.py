import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

def train_model():
    data = pd.read_csv("data/train/dataset.csv")

    features = ["degree", "live_range_length", "use_frequency"]
    X = data[features]
    y = data["label"]

    if data["program"].nunique() < 2:
        raise ValueError("Dataset must contain at least two programs.")

    if y.nunique() < 2:
        raise ValueError("Dataset must contain both spill and non-spill labels.")

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.25,
        random_state=42
    )

    train_idx, test_idx = next(
        splitter.split(X, y, groups=data["program"])
    )

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    if y_train.nunique() < 2:
        raise ValueError(
            "Training data contains only one label. Generate more diverse programs."
        )

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, predictions))
    print("\nClassification Report:")
    print(classification_report(y_test, predictions, zero_division=0))
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/spill_model.pkl")

    print("\nModel saved to models/spill_model.pkl")

if __name__ == "__main__":
    train_model()