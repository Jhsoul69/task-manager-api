from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

CELERY_BROKER_URL = os.getenv("REDIS_BROKER_URL")

celery_app = Celery("tasks", broker=CELERY_BROKER_URL)
