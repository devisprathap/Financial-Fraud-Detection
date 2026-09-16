
import streamlit as st


def show(df):

    st.title(" Transaction Data")

    st.write(
        "This page displays the financial transaction dataset "
        "used for fraud detection."
    )

    # ==========================================
    # Dataset Summary
    # ==========================================

    st.subheader(" Dataset Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Transactions",
            len(df)
        )

    with col2:
        st.metric(
            "Number of Columns",
            len(df.columns)
        )

    with col3:
        st.metric(
            "Fraud Transactions",
            int((df["IsFraud"] == 1).sum())
        )

    # ==========================================
    # Transaction Dataset
    # ==========================================

    st.subheader(" All Transactions")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ==========================================
    # Search / Filter
    # ==========================================

    st.subheader(" Filter Transactions")

    fraud_status = st.selectbox(
        "Select Transaction Status",
        ["All", "Normal", "Fraud"]
    )

    if fraud_status == "Normal":

        filtered_df = df[df["IsFraud"] == 0]

    elif fraud_status == "Fraud":

        filtered_df = df[df["IsFraud"] == 1]

    else:

        filtered_df = df

    st.write(
        f"Showing {len(filtered_df)} transactions"
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )
