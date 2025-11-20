import os
import resend

# Set API key from environment variable
resend.api_key = os.environ.get("re_6AoGYmJw_Kryf1bCHd4qMGwbydCNg5Rvy")


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