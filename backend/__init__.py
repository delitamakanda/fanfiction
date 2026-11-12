# Load the Celery app when Django starts so that @shared_task binds to it.
from backend.celery import app as celery_app

__all__ = ("celery_app",)
