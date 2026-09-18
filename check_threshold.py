import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score


# ==========================================
# Load dataset
# ==========================================

df = pd.read_csv(
    "data/financial_fraud_synthetic_data.csv"
)


# ==========================================
# Create date features
# ==========================================

df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

df["TransactionHour"] = df["Date"].dt.hour
df["TransactionDay"] = df["Date"].dt.day
df["TransactionMonth"] = df["Date"].dt.month
df["TransactionDayOfWeek"] = df["Date"].dt.dayofweek

df = df.drop("Date", axis=1)


# ==========================================
# One-hot encoding
# ==========================================

df = pd.get_dummies(
    df,
    columns=["TransactionType", "Location"],
    drop_first=True
)


# ==========================================
# Separate features and target
# ==========================================

X = df.drop("IsFraud", axis=1)
y = df["IsFraud"]


# ==========================================
# Same train/test split as training
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# Load Gradient Boosting model
# ==========================================

model = joblib.load(
    "models/gradient_boosting_model.pkl"
)


# ==========================================
# Get fraud probabilities
# ==========================================

probabilities = model.predict_proba(X_test)[:, 1]


# ==========================================
# Test different thresholds
# ==========================================

thresholds = [
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50
]


print("\n==========================================")
print(" FRAUD DETECTION THRESHOLD ANALYSIS")
print("==========================================\n")

print(
    f"{'Threshold':<12}"
    f"{'Precision':<12}"
    f"{'Recall':<12}"
    f"{'F1 Score':<12}"
    f"{'Frauds Detected':<18}"
)

print("-" * 66)


for threshold in thresholds:

    predictions = (
        probabilities >= threshold
    ).astype(int)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    frauds_detected = predictions.sum()

    print(
        f"{threshold:<12.2f}"
        f"{precision:<12.3f}"
        f"{recall:<12.3f}"
        f"{f1:<12.3f}"
        f"{frauds_detected:<18}"
    )

print("\nAnalysis completed.")