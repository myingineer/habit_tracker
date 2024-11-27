from .config import settings
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def send_email(recipient_email, subject, body):
    # Set up the server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection

    try:
        # Log in to the server
        server.login(settings.EMAIL_ADDRESS, settings.EMAIL_APP_PASSWORD)

        # Create the email content
        msg = MIMEMultipart()
        msg["From"] = settings.EMAIL_ADDRESS
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        # Send the email
        server.sendmail(settings.EMAIL_ADDRESS, recipient_email, msg.as_string())
    except Exception as e:
        return {
            "status": "failure",
            "message": "Failed to send email"
        }
    finally:
        # Disconnect from the server
        server.quit()

