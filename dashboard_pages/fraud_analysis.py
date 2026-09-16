
# import streamlit as st
# import pandas as pd


# def show(df):

#     st.title(" Fraud Analysis")

#     st.write(
#         "Analysis of fraudulent and normal financial transactions."
#     )

#     # ==========================================
#     # Separate Fraud and Normal Transactions
#     # ==========================================

#     fraud_df = df[df["IsFraud"] == 1]
#     normal_df = df[df["IsFraud"] == 0]

#     total_transactions = len(df)
#     fraud_transactions = len(fraud_df)
#     normal_transactions = len(normal_df)

#     fraud_rate = (
#         fraud_transactions / total_transactions
#     ) * 100

#     fraud_amount = fraud_df["Amount"].sum()

#     # ==========================================
#     # KPI Cards
#     # ==========================================

#     st.subheader(" Fraud Summary")

#     col1, col2, col3, col4 = st.columns(4)

#     with col1:
#         st.metric(
#             "Total Transactions",
#             total_transactions
#         )

#     with col2:
#         st.metric(
#             "Fraud Transactions",
#             fraud_transactions
#         )

#     with col3:
#         st.metric(
#             "Normal Transactions",
#             normal_transactions
#         )

#     with col4:
#         st.metric(
#             "Fraud Rate",
#             f"{fraud_rate:.2f}%"
#         )

#     # ==========================================
#     # Fraud Amount
#     # ==========================================

#     st.subheader(" Total Fraud Amount")

#     st.metric(
#         "Amount Involved in Fraud",
#         f"₹ {fraud_amount:,.2f}"
#     )

#     # ==========================================
#     # Fraud vs Normal Chart
#     # ==========================================

#     st.subheader("Fraud vs Normal Transactions")

#     chart_data = pd.DataFrame({
#         "Transaction Status": [
#             "Normal",
#             "Fraud"
#         ],
#         "Number of Transactions": [
#             normal_transactions,
#             fraud_transactions
#         ]
#     })

#     st.bar_chart(
#         chart_data.set_index(
#             "Transaction Status"
#         )
#     )

#     # ==========================================
#     # Fraudulent Transactions
#     # ==========================================

#     st.subheader(" Fraudulent Transactions")

#     st.dataframe(
#         fraud_df,
#         use_container_width=True
#     )
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def show(df):

    st.title(" Fraud Analysis")

    # -----------------------------------
    # Prepare Date column
    # -----------------------------------

    df["Date"] = pd.to_datetime(df["Date"])

    # -----------------------------------
    # Date Filter
    # -----------------------------------

    st.subheader(" Date Filter")

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    start_date, end_date = st.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    filtered_df = df[
        (df["Date"].dt.date >= start_date) &
        (df["Date"].dt.date <= end_date)
    ]

    st.write(
        f"Showing transactions from **{start_date}** "
        f"to **{end_date}**"
    )

    # -----------------------------------
    # Summary Metrics
    # -----------------------------------

    total_transactions = len(filtered_df)

    total_fraud = filtered_df["IsFraud"].sum()

    normal_transactions = (
        total_transactions - total_fraud
    )

    fraud_rate = (
        total_fraud / total_transactions * 100
        if total_transactions > 0
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Transactions",
        total_transactions
    )

    col2.metric(
        "Fraud Transactions",
        int(total_fraud)
    )

    col3.metric(
        "Normal Transactions",
        normal_transactions
    )

    col4.metric(
        "Fraud Rate",
        f"{fraud_rate:.2f}%"
    )

    # -----------------------------------
    # DAILY TRANSACTION ANALYSIS
    # -----------------------------------

    st.subheader("Daily Transaction Analysis")

    daily_transactions = (
        filtered_df
        .groupby(filtered_df["Date"].dt.date)
        .size()
        .reset_index(name="Transactions")
    )

    fig, ax = plt.subplots()

    ax.plot(
        daily_transactions["Date"],
        daily_transactions["Transactions"],
        marker="o"
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Transactions")
    ax.set_title("Daily Transaction Volume")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)

    # -----------------------------------
    # DAILY FRAUD TREND
    # -----------------------------------

    st.subheader(" Daily Fraud Trend")

    daily_fraud = (
        filtered_df
        .groupby(filtered_df["Date"].dt.date)["IsFraud"]
        .sum()
        .reset_index(name="Fraud Transactions")
    )

    fig2, ax2 = plt.subplots()

    ax2.bar(
        daily_fraud["Date"],
        daily_fraud["Fraud Transactions"]
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Fraud Transactions")
    ax2.set_title("Daily Fraud Transactions")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig2)

    # -----------------------------------
    # HOURLY ANALYSIS
    # -----------------------------------

    st.subheader(" Hourly Transaction Analysis")

    hourly_transactions = (
        filtered_df
        .groupby(filtered_df["Date"].dt.hour)
        .size()
        .reset_index(name="Transactions")
    )

    fig3, ax3 = plt.subplots()

    ax3.plot(
        hourly_transactions["Date"],
        hourly_transactions["Transactions"],
        marker="o"
    )

    ax3.set_xlabel("Hour of Day")
    ax3.set_ylabel("Transactions")
    ax3.set_title("Transactions by Hour")

    ax3.set_xticks(range(0, 24))

    plt.tight_layout()

    st.pyplot(fig3)

    # -----------------------------------
    # MONTHLY FRAUD ANALYSIS
    # -----------------------------------

    st.subheader(" Monthly Fraud Trend")

    monthly_fraud = (
        filtered_df
        .groupby(filtered_df["Date"].dt.to_period("M"))["IsFraud"]
        .sum()
        .reset_index(name="Fraud Transactions")
    )

    monthly_fraud["Date"] = (
        monthly_fraud["Date"].astype(str)
    )

    fig4, ax4 = plt.subplots()

    ax4.bar(
        monthly_fraud["Date"],
        monthly_fraud["Fraud Transactions"]
    )

    ax4.set_xlabel("Month")
    ax4.set_ylabel("Fraud Transactions")
    ax4.set_title("Monthly Fraud Transactions")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig4)

    # -----------------------------------
    # FRAUD BY TRANSACTION TYPE
    # -----------------------------------

    st.subheader(" Fraud by Transaction Type")

    fraud_type = (
        filtered_df[filtered_df["IsFraud"] == 1]
        ["TransactionType"]
        .value_counts()
    )

    st.bar_chart(fraud_type)

    # -----------------------------------
    # FRAUD BY LOCATION
    # -----------------------------------

    st.subheader(" Fraud by Location")

    fraud_location = (
        filtered_df[filtered_df["IsFraud"] == 1]
        ["Location"]
        .value_counts()
    )

    st.bar_chart(fraud_location)


        # -----------------------------------
    # FRAUD LOCATION HEATMAP
    # -----------------------------------

    st.subheader(" Fraud Location Heatmap")

    location_heatmap = (
        filtered_df
        .groupby(["Location", "IsFraud"])
        .size()
        .unstack(fill_value=0)
    )

    # Make sure both Normal and Fraud columns exist
    if 0 not in location_heatmap.columns:
        location_heatmap[0] = 0

    if 1 not in location_heatmap.columns:
        location_heatmap[1] = 0

    location_heatmap = location_heatmap.rename(
        columns={
            0: "Normal",
            1: "Fraud"
        }
    )

    fig5, ax5 = plt.subplots(figsize=(8, 5))

    im = ax5.imshow(
        location_heatmap.values,
        aspect="auto"
    )

    ax5.set_xticks(range(len(location_heatmap.columns)))
    ax5.set_xticklabels(location_heatmap.columns)

    ax5.set_yticks(range(len(location_heatmap.index)))
    ax5.set_yticklabels(location_heatmap.index)

    ax5.set_xlabel("Transaction Status")
    ax5.set_ylabel("Location")
    ax5.set_title("Fraud Distribution by Location")

    # Display values inside heatmap
    for i in range(len(location_heatmap.index)):
        for j in range(len(location_heatmap.columns)):
            ax5.text(
                j,
                i,
                location_heatmap.iloc[i, j],
                ha="center",
                va="center"
            )

    fig5.colorbar(im, ax=ax5)

    plt.tight_layout()

    st.pyplot(fig5)


    # -----------------------------------
    # FRAUD RATE BY LOCATION
    # -----------------------------------

    st.subheader(" Fraud Rate by Location")

    location_rate = (
        filtered_df
        .groupby("Location")["IsFraud"]
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    st.bar_chart(location_rate)


    # -----------------------------------
    # FRAUD VS NORMAL
    # -----------------------------------

    st.subheader(" Fraud vs Normal Transactions")

    status_counts = pd.Series({
        "Normal": (filtered_df["IsFraud"] == 0).sum(),
        "Fraud": (filtered_df["IsFraud"] == 1).sum()
    })

    st.bar_chart(status_counts)


    # -----------------------------------
    # HIGH RISK TRANSACTIONS
    # -----------------------------------

    st.subheader(" Fraudulent Transactions")

    fraud_df = filtered_df[
        filtered_df["IsFraud"] == 1
    ]

    st.dataframe(
        fraud_df,
        use_container_width=True
    )