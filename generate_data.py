import pandas as pd
import numpy as np
import os

# Reproducible results
np.random.seed(42)

# Number of records
n = 6000

# -----------------------------
# Basic information
# -----------------------------

dates = pd.date_range(
    start="2025-01-01",
    periods=n,
    freq="h"
)

fpos = [
    "FPO_Ahmedabad",
    "FPO_Nashik",
    "FPO_Jaipur",
    "FPO_Nagpur",
    "FPO_Lucknow",
    "FPO_Indore",
    "FPO_Karnal",
    "FPO_Surat"
]

produce_types = [
    "Tomato",
    "Potato",
    "Onion",
    "Mango",
    "Apple",
    "Cabbage"
]

fpo = np.random.choice(fpos, n)
produce = np.random.choice(produce_types, n)

# -----------------------------
# Environmental conditions
# -----------------------------

temperature = np.clip(
    np.random.normal(28, 6, n),
    15,
    45
)

humidity = np.clip(
    np.random.normal(65, 15, n),
    30,
    95
)

# -----------------------------
# Harvest and storage data
# -----------------------------

harvest_volume = np.random.randint(200, 2000, n)

storage_capacity = np.random.choice(
    [500, 1000, 1500, 2000, 2500],
    n
)

storage_days = np.random.randint(1, 15, n)

# -----------------------------
# Market price
# -----------------------------

base_prices = {
    "Tomato": 28,
    "Potato": 22,
    "Onion": 30,
    "Mango": 60,
    "Apple": 100,
    "Cabbage": 25
}

market_price = np.array([
    base_prices[p] for p in produce
])

market_price = (
    market_price
    + np.random.normal(0, 5, n)
)

market_price = np.maximum(
    market_price,
    5
)

# -----------------------------
# Storage demand
# -----------------------------

storage_demand = (
    harvest_volume * 0.65
    + storage_days * 35
    + humidity * 3
    - temperature * 8
    + np.random.normal(0, 100, n)
)

storage_demand = np.clip(
    storage_demand,
    50,
    storage_capacity
)

# -----------------------------
# Utilization
# -----------------------------

utilization = (
    storage_demand / storage_capacity
) * 100

utilization = np.clip(
    utilization,
    5,
    100
)

# -----------------------------
# Spoilage risk
# -----------------------------

risk_score = (
    temperature * 0.05
    + humidity * 0.025
    + storage_days * 0.08
    + utilization * 0.01
)

# Thresholds are chosen from the generated score distribution
# so the synthetic demo contains meaningful LOW/MEDIUM/HIGH cases.
low_threshold = np.quantile(
    risk_score,
    0.65
)

high_threshold = np.quantile(
    risk_score,
    0.90
)

risk = np.select(
    [
        risk_score < low_threshold,
        risk_score < high_threshold
    ],
    [
        "LOW",
        "MEDIUM"
    ],
    default="HIGH"
)

# -----------------------------
# Future market price
# -----------------------------

future_market_price = (
    market_price
    + np.random.normal(3, 5, n)
)

future_market_price = np.maximum(
    future_market_price,
    5
)

# -----------------------------
# Storage cost
# -----------------------------

storage_cost = np.random.uniform(
    1.5,
    5.0,
    n
)

# -----------------------------
# Economics
# -----------------------------

potential_revenue = (
    harvest_volume * future_market_price
)

storage_expense = (
    storage_demand
    * storage_cost
    * storage_days
)

# -----------------------------
# Decision
# -----------------------------

decision = np.where(
    (
        future_market_price >= market_price * 1.10
    )
    & (risk != "HIGH"),
    "STORE",
    "SELL NOW"
)

# -----------------------------
# Create dataframe
# -----------------------------

df = pd.DataFrame({

    "date": dates,

    "fpo": fpo,

    "produce": produce,

    "temperature": temperature.round(2),

    "humidity": humidity.round(2),

    "harvest_volume_kg": harvest_volume,

    "market_price": market_price.round(2),

    "storage_days": storage_days,

    "storage_capacity_kg": storage_capacity,

    "storage_demand_kg": storage_demand.round(2),

    "utilization_pct": utilization.round(2),

    "spoilage_risk": risk,

    "future_market_price": future_market_price.round(2),

    "storage_cost_per_kg": storage_cost.round(2),

    "potential_revenue": potential_revenue.round(2),

    "decision": decision
})

# -----------------------------
# Save dataset
# -----------------------------

os.makedirs(
    "data",
    exist_ok=True
)

file_path = "data/solcool_data.csv"

df.to_csv(
    file_path,
    index=False
)

print("====================================")
print("SolCool dataset created successfully")
print("====================================")
print(f"Records: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"File saved at: {file_path}")
print()
print("Risk distribution:")
print(df["spoilage_risk"].value_counts())
print()
print(df.head())
