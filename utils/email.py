import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import get_settings

settings = get_settings()


def send_otp_email(receiver_email: str, otp: str):
    subject = "Your OTP Verification Code"
    body = f"Your OTP code is: {otp}. It is valid for 10 minutes."

    msg = MIMEMultipart()
    msg["From"] = settings.sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.sender_email, settings.sender_password)
        server.sendmail(settings.sender_email, receiver_email, msg.as_string())
        server.quit()
        print(f"OTP sent to {receiver_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
