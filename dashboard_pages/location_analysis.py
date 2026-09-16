
import streamlit as st
import pandas as pd


def show(df):

    st.title(" Location Analysis")

    st.write(
        "This page analyzes transactions and fraudulent "
        "activities based on location."
    )

    # ==========================================
    # Location Summary
    # ==========================================

    st.subheader(" Location Summary")

    total_locations = df["Location"].nunique()
    total_fraud = int((df["IsFraud"] == 1).sum())

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Locations",
            total_locations
        )

    with col2:
        st.metric(
            "Total Fraud Transactions",
            total_fraud
        )

    # ==========================================
    # Fraud by Location
    # ==========================================

    st.subheader(" Fraud Transactions by Location")

    fraud_by_location = (
        df[df["IsFraud"] == 1]
        .groupby("Location")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        fraud_by_location
    )

    # ==========================================
    # All Transactions by Location
    # ==========================================

    st.subheader(" Transactions by Location")

    location_transactions = (
        df.groupby("Location")
        .size()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        location_transactions
    )

    # ==========================================
    # Location-wise Fraud Table
    # ==========================================

    st.subheader(" Location-wise Fraud Summary")

    location_summary = (
        df.groupby("Location")
        .agg(
            Total_Transactions=("IsFraud", "count"),
            Fraud_Transactions=("IsFraud", "sum")
        )
        .reset_index()
    )

    location_summary["Fraud_Rate"] = (
        location_summary["Fraud_Transactions"]
        / location_summary["Total_Transactions"]
        * 100
    )

    location_summary["Fraud_Rate"] = (
        location_summary["Fraud_Rate"].round(2)
    )

    st.dataframe(
        location_summary,
        use_container_width=True
    )