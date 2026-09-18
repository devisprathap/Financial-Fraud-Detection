# import streamlit as st

# st.set_page_config(
#     page_title="Financial Fraud Detection",
#     page_icon="💳",
#     layout="wide"
# )

# st.title("Financial Fraud Detection System")

# st.write("""
# This application uses Machine Learning to detect
# potentially fraudulent financial transactions.
# """)

# st.subheader("Project Overview")

# st.write("""
# The system analyzes transaction information such as
# amount, merchant, transaction type, and location
# to predict whether a transaction is fraudulent.
# """)

# st.success("Financial Fraud Detection Dashboard is ready!")
import streamlit as st
import pandas as pd
import joblib

# Import dashboard pages
from dashboard_pages import dashboard
from dashboard_pages import transaction_data
from dashboard_pages import fraud_analysis
from dashboard_pages import location_analysis
from dashboard_pages import transaction_analysis
from dashboard_pages import fraud_prediction
from dashboard_pages import about


# ==============================
# Page Configuration
# ==============================

st.set_page_config(
    page_title="Financial Fraud Detection",
    page_icon="",
    layout="wide"
)


# ==============================
# Load Dataset
# ==============================

@st.cache_data
def load_data():
    return pd.read_csv(
        "data/financial_fraud_synthetic_data.csv"
    )



try:
    model = load_model()
except Exception as e:
    st.error(f"Model loading error: {e}")
    st.stop()

# ==============================
# Load Machine Learning Model
# ==============================

@st.cache_resource
def load_model():
    return joblib.load(
        "models/gradient_boosting_model.pkl"
    )


model = load_model()


# ==============================
# Sidebar Navigation
# ==============================

st.sidebar.title(" Navigation")

page = st.sidebar.radio(
    "Select a Page",
    [
        " Dashboard",
        " Transaction Data",
        " Fraud Analysis",
        " Location Analysis",
        " Transaction Analysis",
        " Fraud Prediction",
        " About Project"
    ]
)


# ==============================
# Page Routing
# ==============================

if page == " Dashboard":
    dashboard.show(df)

elif page == " Transaction Data":
    transaction_data.show(df)

elif page == " Fraud Analysis":
    fraud_analysis.show(df)

elif page == " Location Analysis":
    location_analysis.show(df)

elif page == " Transaction Analysis":
    transaction_analysis.show(df)

elif page == " Fraud Prediction":
    fraud_prediction.show(df, model)

elif page == " About Project":
    about.show()
