import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_high_risk_notification(investigation_data: dict) -> bool:
    sender = os.getenv("ALERT_EMAIL_FROM")
    receiver = os.getenv("ALERT_EMAIL_TO")
    password = os.getenv("ALERT_EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))

    if not sender or not receiver or not password:
        return False

    subject = "High Risk Fraud Alert"

    body = f"""
High-risk fraud case detected.

Risk Level: {investigation_data.get("risk_level")}
Fraud Probability: {investigation_data.get("fraud_probability")}
Amount: {investigation_data.get("Amount")}
Recommended Action: {investigation_data.get("recommended_action")}
"""

    message = EmailMessage()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(message)

        return True

    except Exception as e:
        print("Notification failed:", e)
        return False