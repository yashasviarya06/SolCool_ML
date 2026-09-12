import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score, accuracy_score


# ==========================================
# Load dataset
# ==========================================

data_path = "data/solcool_data.csv"

df = pd.read_csv(data_path)

print("Dataset loaded successfully")
print(f"Rows: {len(df)}")


# ==========================================
# Create models folder
# ==========================================

os.makedirs(
    "models",
    exist_ok=True
)


# ==========================================
# DEMAND PREDICTION MODEL
# ==========================================

features = [
    "temperature",
    "humidity",
    "harvest_volume_kg",
    "market_price",
    "storage_days",
    "storage_capacity_kg"
]

X = df[features]

y = df["storage_demand_kg"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


demand_model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

demand_model.fit(
    X_train,
    y_train
)

predictions = demand_model.predict(
    X_test
)

r2 = r2_score(
    y_test,
    predictions
)

print()
print("Demand Prediction Model")
print("-----------------------")
print(f"R2 Score: {r2:.3f}")


joblib.dump(
    demand_model,
    "models/demand_model.pkl"
)


# ==========================================
# SPOILAGE RISK MODEL
# ==========================================

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
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

risk_model.fit(
    X_train,
    y_train
)

risk_predictions = risk_model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    risk_predictions
)

print()
print("Spoilage Risk Model")
print("-------------------")
print(f"Accuracy: {accuracy:.3f}")


joblib.dump(
    risk_model,
    "models/spoilage_model.pkl"
)


print()
print("====================================")
print("Models trained successfully!")
print("====================================")
print("Saved:")
print("models/demand_model.pkl")
print("models/spoilage_model.pkl")
