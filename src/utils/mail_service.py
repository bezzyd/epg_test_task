from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_HOST_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_HOST_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_FROM"),
    MAIL_PORT=os.getenv("EMAIL_PORT"),
    MAIL_SERVER=os.getenv("EMAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_mail(to_mail: str, from_mail: str, from_name: str) -> None:
    message = MessageSchema(
        subject="You have a new match!",
        recipients=[to_mail],
        body=f"You liked {from_name}! Sender's email: {from_mail}",
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
