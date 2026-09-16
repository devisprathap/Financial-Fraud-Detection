import pandas as pd

# Load the dataset
df = pd.read_csv("data/financial_fraud_synthetic_data.csv")

# Display first 5 rows
print("First 5 rows:")
print(df.head())

# Display dataset information
print("\nDataset shape:")
print(df.shape)

# Display column names
print("\nColumn names:")
print(df.columns.tolist())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check fraud distribution
print("\nFraud distribution:")
print(df["IsFraud"].value_counts())