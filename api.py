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

# Load trained model
model = joblib.load("models/random_forest_model.pkl")

# Load feature columns
feature_columns = joblib.load("models/feature_columns.pkl")


# Input transaction format
class Transaction(BaseModel):
    Amount: float
    MerchantID: int
    TransactionType: str
    Location: str


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Financial Fraud Detection API is running"
    }


# Prediction endpoint
@app.post("/predict")
def predict(transaction: Transaction):

    # Create DataFrame from API input
    data = pd.DataFrame([{
        "Amount": transaction.Amount,
        "MerchantID": transaction.MerchantID,
        "TransactionType": transaction.TransactionType,
        "Location": transaction.Location
    }])

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
