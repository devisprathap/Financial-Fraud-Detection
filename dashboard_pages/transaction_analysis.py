
import streamlit as st
import pandas as pd


def show(df):

    st.title(" Transaction Analysis")

    st.write(
        "This page analyzes financial transactions based "
        "on transaction type and identifies fraudulent activities."
    )

    # ==========================================
    # Transaction Summary
    # ==========================================

    st.subheader("Transaction Summary")

    total_transactions = len(df)
    total_types = df["TransactionType"].nunique()
    total_fraud = int((df["IsFraud"] == 1).sum())

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Transactions",
            total_transactions
        )

    with col2:
        st.metric(
            "Transaction Types",
            total_types
        )

    with col3:
        st.metric(
            "Fraud Transactions",
            total_fraud
        )

    # ==========================================
    # Transactions by Type
    # ==========================================

    st.subheader(" Transactions by Type")

    transaction_counts = (
        df["TransactionType"]
        .value_counts()
    )

    st.bar_chart(
        transaction_counts
    )

    # ==========================================
    # Fraud by Transaction Type
    # ==========================================

    st.subheader(" Fraud by Transaction Type")

    fraud_by_type = (
        df[df["IsFraud"] == 1]
        .groupby("TransactionType")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        fraud_by_type
    )

    # ==========================================
    # Transaction Type Summary
    # ==========================================

    st.subheader(" Transaction Type Summary")

    type_summary = (
        df.groupby("TransactionType")
        .agg(
            Total_Transactions=("IsFraud", "count"),
            Fraud_Transactions=("IsFraud", "sum"),
            Total_Amount=("Amount", "sum")
        )
        .reset_index()
    )

    type_summary["Fraud_Rate"] = (
        type_summary["Fraud_Transactions"]
        / type_summary["Total_Transactions"]
        * 100
    )

    type_summary["Fraud_Rate"] = (
        type_summary["Fraud_Rate"].round(2)
    )

    type_summary["Total_Amount"] = (
        type_summary["Total_Amount"].round(2)
    )

    st.dataframe(
        type_summary,
        use_container_width=True
    )