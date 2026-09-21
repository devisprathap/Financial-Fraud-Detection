
import streamlit as st


def show():

    st.title(" About Project")

    # ==========================================
    # Project Overview
    # ==========================================

    st.subheader(" Financial Fraud Detection Model")

    st.write(
        """
        The Financial Fraud Detection Model is a Machine Learning
        based system designed to identify potentially fraudulent
        financial transactions.

        The system analyzes transaction information such as
        transaction amount, merchant, transaction type, and
        location to identify suspicious activities.
        """
    )

    # ==========================================
    # Objective
    # ==========================================

    st.subheader(" Project Objective")

    st.write(
        """
        The main objective of this project is to detect fraudulent
        transactions and provide useful insights through an
        interactive dashboard.

        The system helps users understand fraud patterns and
        identify potentially suspicious transactions.
        """
    )

    # ==========================================
    # Project Workflow
    # ==========================================

    st.subheader(" Project Workflow")

    st.write(
        """
        1.  Collect transaction data
        2.  Clean and preprocess the data
        3.  Convert categorical data into numerical features
        4.  Handle class imbalance using SMOTE
        5.  Train Machine Learning models
        6.  Evaluate model performance
        7.  Predict fraudulent transactions
        8.  Display results through Streamlit dashboard
        """
    )

    # ==========================================
    # Technologies
    # ==========================================

    st.subheader(" Technologies Used")

    technologies = [
        "Python",
        "Pandas",
        "NumPy",
        "Scikit-learn",
        "SMOTE",
        "Logistic Regression",
        "Random Forest",
        "Streamlit",
        "Matplotlib",
        "Joblib"
    ]

    for technology in technologies:
        st.write(f"• {technology}")

    # ==========================================
    # Dataset
    # ==========================================

    st.subheader(" Dataset Information")

    st.write(
        """
        The project uses a synthetic financial transaction dataset
        containing 10,000 transactions.

        Dataset features:

        • Amount - Transaction amount

        • MerchantID -Merchant identifier

        • TransactionType - Type of transaction

        • Location - Transaction location

        • IsFraud -Target variable indicating whether the
          transaction is fraudulent (1) or normal (0)
        """
    )

    # ==========================================
    # Machine Learning
    # ==========================================

    st.subheader(" Machine Learning Models")

    st.write(
        """
        The project experiments with supervised Machine Learning
        algorithms including:

        • Logistic Regression

        • Random Forest
        
        • Gradient boosting
        SMOTE is used to address the class imbalance between
        normal and fraudulent transactions.
        """
    )

    # ==========================================
    # Dashboard Pages
    # ==========================================

    st.subheader(" Dashboard Pages")

    st.write(
        """
         Dashboard - Overall transaction overview

         Transaction Data -View and filter transaction data

         Fraud Analysis - Analyze fraudulent transactions

         Location Analysis - Analyze fraud based on location

        Transaction Analysis -Analyze fraud by transaction type

         Fraud Prediction -Predict whether a transaction is
        potentially fraudulent

        About Project -Project information
        """
    )

    # ==========================================
    # Footer
    # ==========================================

    st.markdown("---")

    st.caption(
        "Financial Fraud Detection Model | "
        "Machine Learning + Streamlit Dashboard"
    )
