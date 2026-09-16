import streamlit as st
import pandas as pd


def show(df):

    st.title(" Financial Fraud Detection Dashboard")

    st.write(
        "Overview of financial transactions and fraud detection results."
    )

    total = len(df)
    fraud = (df["IsFraud"] == 1).sum()
    normal = (df["IsFraud"] == 0).sum()
    fraud_rate = (fraud / total) * 100

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Transactions", total)
    col2.metric("Fraud Transactions", fraud)
    col3.metric("Normal Transactions", normal)
    col4.metric("Fraud Rate", f"{fraud_rate:.2f}%")

    st.subheader(" Fraud vs Normal Transactions")

    chart_data = pd.DataFrame({
        "Status": ["Normal", "Fraud"],
        "Count": [normal, fraud]
    })

    st.bar_chart(
        chart_data.set_index("Status")
    )