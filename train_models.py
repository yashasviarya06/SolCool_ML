import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score


# -----------------------------
# Load data
# -----------------------------

data_path = "data/solcool_data.csv"
df = pd.read_csv(data_path)

os.makedirs("models", exist_ok=True)


# -----------------------------
# Demand Prediction Model
# -----------------------------

demand_features = [
    "temperature",
    "humidity",
    "harvest_volume_kg",
    "market_price",
    "storage_days",
    "storage_capacity_kg"
]

X = df[demand_features]
y = df["storage_demand_kg"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

demand_model = RandomForestRegressor(
    n_estimators=50,
    max_depth=12,
    min_samples_leaf=3,
    random_state=42,
    n_jobs=-1
)

demand_model.fit(X_train, y_train)

predictions = demand_model.predict(X_test)

r2 = r2_score(y_test, predictions)

joblib.dump(
    demand_model,
    "models/demand_model.pkl",
    compress=3
)

print("Demand Model R²:", round(r2, 4))
print("Demand model saved.")


# -----------------------------
# Spoilage Risk Model
# -----------------------------

risk_features = [
    "temperature",
    "humidity",
    "storage_days",
    "utilization_pct",
    "storage_capacity_kg"
]

X = df[risk_features]
y = df["spoilage_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

risk_model = RandomForestClassifier(
    n_estimators=50,
    max_depth=10,
    min_samples_leaf=3,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

risk_model.fit(X_train, y_train)

risk_predictions = risk_model.predict(X_test)

accuracy = accuracy_score(y_test, risk_predictions)

joblib.dump(
    risk_model,
    "models/spoilage_model.pkl",
    compress=3
)

print("Spoilage Model Accuracy:", round(accuracy, 4))
print("Spoilage model saved.")

print("\nTraining complete!")
