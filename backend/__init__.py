# import Celery
from __future__ import absolute_import, unicode_literals

from .celery import app as celery_app
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

__all__ = ['celery_app']
