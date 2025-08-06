from .celery_app import celery_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from .. import database, models

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")

def get_user_email(user_id):
    db: Session = next(database.get_db())
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user.email if user else None

@celery_app.task
def send_task_email(task_title, user_id, action):
    email_to = get_user_email(user_id)
    if not email_to:
        return

    subject = f"Task {action}: {task_title}"
    body = f"Hi,\n\nThe task '{task_title}' has been {action.lower()}.\n\nThanks,\nTask Manager"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_FROM
    msg["To"] = email_to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, email_to, msg.as_string())
        server.quit()
        print(f"Email sent to {email_to}")
    except Exception as e:
        print(f"Email send failed: {str(e)}")
