import os
import smtplib
from email.mime.text import MIMEText


def send_welcome_email(to_email, username):
    sender = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")

    msg = MIMEText(
        f"Hello {username},\n\n"
        "Welcome to the To-Do App! Your account has been successfully created.\n\n"
        "Best regards,\nThe To-Do App Team"
    )
    msg["Subject"] = "Welcome to the To-Do App!"
    msg["From"] = sender
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    # For Outlook:
    # server = smtplib.SMTP("smtp.office365.com", 587)

    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, to_email, msg.as_string())
    server.quit()
