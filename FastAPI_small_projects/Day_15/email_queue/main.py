from fastapi import FastAPI, BackgroundTasks

from email_service import send_admin_notification, send_newsletter
from schemas import UserRegister
from email_service import send_welcome_email

app = FastAPI()

@app.post("/register")
async def register_user(
        user: UserRegister,
        background_tasks: BackgroundTasks
):
    print(f"Creating user {user.username}")
    background_tasks.add_task(
        send_welcome_email,
        user.email
    )

    background_tasks.add_task(
        send_admin_notification,
        user.username
    )

    return {
        "message": "User registered successfully"
    }


@app.post("/newsletter")
async def newsletter(
        user: UserRegister,
        background_tasks: BackgroundTasks
):
    print("Newsletter queued")

    background_tasks.add_task(
        send_newsletter,
        user.email
    )

    print("Newsletter sent successfully")

    return {
        "message": "Username added for newsletter successfully"
    }

