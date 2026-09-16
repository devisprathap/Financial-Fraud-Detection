import pandas as pd

file_path = "data/financial_fraud_synthetic_data.csv"

df = pd.read_csv(file_path)

df["Date"] = pd.date_range(
    start="2025-01-01 00:00:00",
    periods=len(df),
    freq="h"
)

df.to_csv(file_path, index=False)

print("Date column added successfully!")