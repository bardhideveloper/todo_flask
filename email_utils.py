import os
import resend

resend.api_key = os.environ.get("RESEND_API_KEY")


def send_welcome_email(to_email, username):
    """Send welcome email using Resend API"""
    try:
        resend.Emails.send({
            "from": "ToDo App <onboarding@resend.dev>",
            "to": to_email,
            "subject": "Welcome to the To-Do App!",
            "text": f"Hello {username},\n\nWelcome to the To-Do App! Your account has been created.\n\nBest regards,\nThe To-Do App Team"
        })
    except Exception as e:
        print("EMAIL ERROR:", e)