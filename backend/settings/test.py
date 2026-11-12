"""Settings used by the test runner (``python manage.py test``)."""

from .base import *  # noqa: F403
from .base import MIDDLEWARE

DEBUG = False
SECRET_KEY = "test-secret-key-not-for-production"  # noqa: S105
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

# No collected static files in tests.
MIDDLEWARE = [m for m in MIDDLEWARE if not m.startswith("whitenoise.")]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# External services are always mocked in tests.
OPENAI_API_KEY = ""
RECAPTCHA_SECRET_KEY = "test-recaptcha-secret"  # noqa: S105

LOGGING["root"]["level"] = "WARNING"
LOGGING["loggers"]["django"]["level"] = "ERROR"
LOGGING["loggers"]["apps"]["level"] = "ERROR"
