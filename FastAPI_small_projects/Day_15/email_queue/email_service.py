import time


def send_welcome_email(email:str):
    print(f"Sending email to {email}")
    time.sleep(5)
    print(f"Email sent successfully to {email}")

def send_admin_notification(username: str):
    print(f"Admin notified about {username}")

def send_newsletter(email: str):
    print(f"Newsletter sent to the{email}")
