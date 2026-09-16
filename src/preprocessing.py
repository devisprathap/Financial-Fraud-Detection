import pandas as pd

# Load dataset
df = pd.read_csv("data/financial_fraud_synthetic_data.csv")

print("Original dataset:")
print(df.head())

# Convert categorical columns into numbers
df = pd.get_dummies(
    df,
    columns=["TransactionType", "Location"],
    drop_first=True
)

print("\nAfter preprocessing:")
print(df.head())

print("\nNew columns:")
print(df.columns.tolist())

print("\nDataset shape:")
print(df.shape)