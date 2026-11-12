"""Celery application. The beat schedule lives in ``CELERY_BEAT_SCHEDULE``."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.development")

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
