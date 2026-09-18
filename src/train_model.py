
import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score
)


# ==========================================
# 1. Load Dataset
# ==========================================

df = pd.read_csv("data/financial_fraud_synthetic_data.csv")
# Convert Date into useful numerical features
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

df["TransactionHour"] = df["Date"].dt.hour
df["TransactionDay"] = df["Date"].dt.day
df["TransactionMonth"] = df["Date"].dt.month
df["TransactionDayOfWeek"] = df["Date"].dt.dayofweek

# Remove original text date
df = df.drop("Date", axis=1)

# ==========================================
# 2. Preprocessing
# ==========================================

df = pd.get_dummies(
    df,
    columns=["TransactionType", "Location"],
    drop_first=True
)


# ==========================================
# 3. Separate Features and Target
# ==========================================

X = df.drop("IsFraud", axis=1)
y = df["IsFraud"]

# Save feature columns for FastAPI
feature_columns = X.columns.tolist()

joblib.dump(
    feature_columns,
    "models/feature_columns.pkl"
)

print("Feature columns saved successfully!")
# ==========================================
# 4. Train-Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# Handle Class Imbalance using SMOTE
# ==========================================

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(
    X_train,
    y_train
)

print("\nBefore SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(y_train_smote.value_counts())
# ==========================================
# 5. Logistic Regression
# ==========================================

logistic_model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced"
)

logistic_model.fit(X_train_smote, y_train_smote)
joblib.dump(logistic_model, "models/fraud_model.pkl")

print("Logistic Regression model saved successfully!")

lr_pred = logistic_model.predict(X_test)
lr_probability = logistic_model.predict_proba(X_test)[:, 1]

print("\n===== Logistic Regression =====")

print("Accuracy :", accuracy_score(y_test, lr_pred))
print(
    "Precision:",
    precision_score(y_test, lr_pred, zero_division=0)
)
print(
    "Recall   :",
    recall_score(y_test, lr_pred, zero_division=0)
)
print(
    "ROC-AUC  :",
    roc_auc_score(y_test, lr_probability)
)


# ==========================================
# 6. Random Forest
# ==========================================

rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight=None
)

rf_model.fit(X_train_smote, y_train_smote)
joblib.dump(rf_model, "models/random_forest_model.pkl")

print("Random Forest model saved successfully!")

rf_pred = rf_model.predict(X_test)
rf_probability = rf_model.predict_proba(X_test)[:, 1]


# ==========================================
# 7. Random Forest Evaluation
# ==========================================

print("\n===== Random Forest =====")

print("Accuracy :", accuracy_score(y_test, rf_pred))
print(
    "Precision:",
    precision_score(y_test, rf_pred, zero_division=0)
)
print(
    "Recall   :",
    recall_score(y_test, rf_pred, zero_division=0)
)
print(
    "ROC-AUC  :",
    roc_auc_score(y_test, rf_probability)
)
print("\n===== Fraud Distribution =====")
print(df["IsFraud"].value_counts())
print(df["IsFraud"].value_counts(normalize=True))

# ==============================
# Gradient Boosting
# ==============================

gb_model = GradientBoostingClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=3,
    random_state=42
)

gb_model.fit(X_train_smote, y_train_smote)

gb_pred = gb_model.predict(X_test)
gb_probability = gb_model.predict_proba(X_test)[:, 1]

joblib.dump(gb_model, "models/gradient_boosting_model.pkl")

print("Gradient Boosting model saved successfully!")

print("\n===== Gradient Boosting =====")
print("Accuracy :", accuracy_score(y_test, gb_pred))
print("Precision:", precision_score(y_test, gb_pred, zero_division=0))
print("Recall   :", recall_score(y_test, gb_pred, zero_division=0))
print("ROC-AUC  :", roc_auc_score(y_test, gb_probability))

