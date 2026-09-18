
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Create FastAPI application
app = FastAPI(
    title="Financial Fraud Detection API",
    description="API for financial transaction fraud prediction",
    version="1.0"
)

# Load Gradient Boosting model
model = joblib.load("models/gradient_boosting_model.pkl")

# Load feature columns
feature_columns = joblib.load("models/feature_columns.pkl")


# Input transaction format
class Transaction(BaseModel):
    Amount: float
    MerchantID: int
    TransactionType: str
    Location: str
    Date: str


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Financial Fraud Detection API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict(transaction: Transaction):

    # Create DataFrame
    data = pd.DataFrame([{
        "Amount": transaction.Amount,
        "MerchantID": transaction.MerchantID,
        "TransactionType": transaction.TransactionType,
        "Location": transaction.Location,
        "Date": transaction.Date
    }])

    # Convert Date to datetime
    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    # Create the same date features used during training
    data["TransactionHour"] = data["Date"].dt.hour
    data["TransactionDay"] = data["Date"].dt.day
    data["TransactionMonth"] = data["Date"].dt.month
    data["TransactionDayOfWeek"] = data["Date"].dt.dayofweek

    # Remove original Date column
    data = data.drop("Date", axis=1)

    # One-hot encoding
    data = pd.get_dummies(
        data,
        columns=["TransactionType", "Location"],
        drop_first=True
    )

    # Make columns identical to training columns
    data = data.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # Prediction
    prediction = model.predict(data)[0]

    # Fraud probability
    probability = model.predict_proba(data)[0][1]

    if prediction == 1:
        result = "Fraud"
    else:
        result = "Normal"

    return {
        "prediction": int(prediction),
        "result": result,
        "fraud_probability": round(float(probability), 4)
    }
