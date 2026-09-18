import smtplib
from email.message import EmailMessage


def send_fraud_email(
    sender_email,
    app_password,
    receiver_email,
    amount,
    merchant_id,
    transaction_type,
    location,
    probability
):
    msg = EmailMessage()

    msg["Subject"] = " Fraud Transaction Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        f"""
Fraud Detection Alert

A potentially fraudulent transaction has been detected.

Transaction Details
-------------------
Amount           : ₹{amount:,.2f}
Merchant ID      : {merchant_id}
Transaction Type : {transaction_type}
Location         : {location}
Fraud Probability: {probability:.2%}

Please review this transaction.
"""
    )

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.send_message(msg)


