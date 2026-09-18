

# def show(df, model):

#     st.title(" Fraud Prediction")

#     st.write(
#         "Enter the transaction details below to predict "
#         "whether the transaction is potentially fraudulent."
#     )

#     # ==========================================
#     # Transaction Details
#     # ==========================================

#     st.subheader(" Transaction Details")

#     col1, col2 = st.columns(2)

#     with col1:

#         amount = st.number_input(
#             "Transaction Amount",
#             min_value=0.0,
#             value=1000.0,
#             step=100.0
#         )

#         merchant_id = st.number_input(
#             "Merchant ID",
#             min_value=0,
#             value=100
#         )

#     with col2:

#         transaction_type = st.selectbox(
#             "Transaction Type",
#             sorted(df["TransactionType"].unique())
#         )

#         location = st.selectbox(
#             "Location",
#             sorted(df["Location"].unique())
#         )

#     # ==========================================
#     # Prediction
#     # ==========================================

#     if st.button(" Predict Transaction"):

#         # Create input dataframe
#         input_data = pd.DataFrame({
#             "Amount": [amount],
#             "MerchantID": [merchant_id],
#             "TransactionType": [transaction_type],
#             "Location": [location]
#         })

#         # Convert categorical columns
#         input_data = pd.get_dummies(
#             input_data,
#             columns=["TransactionType", "Location"],
#             drop_first=True
#         )

#         # Make columns match the model's training columns
#         if hasattr(model, "feature_names_in_"):

#             training_columns = model.feature_names_in_

#             input_data = input_data.reindex(
#                 columns=training_columns,
#                 fill_value=0
#             )

#         # ==========================================
#         # Make Prediction
#         # ==========================================

#         prediction = model.predict(input_data)[0]

#         probability = model.predict_proba(
#             input_data
#         )[0][1]

#         # ==========================================
#         # Display Result
#         # ==========================================

#         st.subheader(" Prediction Result")
        
#         if prediction == 1:

#             st.error(
#                 " FRAUDULENT TRANSACTION DETECTED"
#             )

#             st.metric(
#                 "Fraud Probability",
#                 f"{probability:.2%}"
#             )

#             st.warning(
#                 "This transaction has been classified "
#                 "as potentially fraudulent."
#             )
#             transaction_details = {
#         "sender_email": st.secrets["EMAIL_ADDRESS"],
#         "recipient_email": st.secrets["ALERT_EMAIL"],
#         "password": st.secrets["EMAIL_APP_PASSWORD"],
#         "amount": amount,
#         "merchant_id": merchant_id,
#         "transaction_type": transaction_type,
#         "location": location,
#         "probability": probability
#     }
#             try:
#               send_fraud_email(
#                    st.secrets["EMAIL_ADDRESS"],
#                    st.secrets["EMAIL_APP_PASSWORD"],
#                    st.secrets["ALERT_EMAIL"],
#                    amount,
#                    merchant_id,
#                    transaction_type,
#                    location,
#                    probability
#                 )
               
#               st.success("Fraud alert email sent successfully!")
                
#             except Exception as e:
#                 st.error("Unable to send fraud alert email.")
#                 st.error(str(e))
#         else:

#             st.success(
#                 " TRANSACTION APPEARS NORMAL"
#             )

#             st.metric(
#                 "Fraud Probability",
#                 f"{probability:.2%}"
#             )

#             st.info(
#                 "The transaction has been classified "
#                 "as potentially normal."
#            

import streamlit as st
import pandas as pd
from dashboard_pages.email_alert import send_fraud_email


def show(df, model):

    st.title(" Fraud Prediction")

    st.write(
        "Enter the transaction details below to predict "
        "whether the transaction is potentially fraudulent."
    )

    # ==========================================
    # Transaction Details
    # ==========================================

    st.subheader(" Transaction Details")

    col1, col2 = st.columns(2)

    with col1:

        amount = st.number_input(
            "Transaction Amount",
            min_value=0.0,
            value=1000.0,
            step=100.0
        )

        merchant_id = st.number_input(
            "Merchant ID",
            min_value=0,
            value=100
        )

        transaction_date = st.date_input(
            "Transaction Date"
        )

    with col2:

        transaction_type = st.selectbox(
            "Transaction Type",
            sorted(df["TransactionType"].unique())
        )

        location = st.selectbox(
            "Location",
            sorted(df["Location"].unique())
        )

        transaction_hour = st.number_input(
            "Transaction Hour",
            min_value=0,
            max_value=23,
            value=12
        )

    # ==========================================
    # Prediction
    # ==========================================

    if st.button(" Predict Transaction"):

        # Combine selected date and hour
        transaction_datetime = pd.Timestamp(
            transaction_date
        ) + pd.Timedelta(
            hours=transaction_hour
        )

        # Create input dataframe
        input_data = pd.DataFrame({
            "Amount": [amount],
            "MerchantID": [merchant_id],
            "TransactionType": [transaction_type],
            "Location": [location],

            # Same features used during training
            "TransactionHour": [transaction_datetime.hour],
            "TransactionDay": [transaction_datetime.day],
            "TransactionMonth": [transaction_datetime.month],
            "TransactionDayOfWeek": [transaction_datetime.dayofweek]
        })

        # Convert categorical columns
        input_data = pd.get_dummies(
            input_data,
            columns=["TransactionType", "Location"],
            drop_first=True
        )

        # Make columns match model training columns
        if hasattr(model, "feature_names_in_"):

            training_columns = model.feature_names_in_

            input_data = input_data.reindex(
                columns=training_columns,
                fill_value=0
            )

        # ==========================================
        # Make Prediction
        # ==========================================

        
        probability = model.predict_proba(input_data)[0][1]

        # Fraud decision threshold
        threshold = 0.10

        prediction = 1 if probability >= threshold else 0
        # ==========================================
        # Display Result
        # ==========================================

        st.subheader(" Prediction Result")

        if prediction == 1:

            st.error(
                " FRAUDULENT TRANSACTION DETECTED"
            )

            st.metric(
                "Fraud Probability",
                f"{probability:.2%}"
            )

            st.warning(
                "This transaction has been classified "
                "as potentially fraudulent."
            )

            try:
                send_fraud_email(
                    st.secrets["EMAIL_ADDRESS"],
                    st.secrets["EMAIL_APP_PASSWORD"],
                    st.secrets["ALERT_EMAIL"],
                    amount,
                    merchant_id,
                    transaction_type,
                    location,
                    probability
                )

                st.success(
                    "Fraud alert email sent successfully!"
                )

            except Exception as e:

                st.error(
                    "Unable to send fraud alert email."
                )

                st.error(str(e))

        else:

            st.success(
                " TRANSACTION APPEARS NORMAL"
            )

            st.metric(
                "Fraud Probability",
                f"{probability:.2%}"
            )

            st.info(
                "The transaction has been classified "
                "as potentially normal."
            )