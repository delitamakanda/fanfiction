"""Production settings: every secret comes from the environment."""

from decouple import config

from .base import *  # noqa: F403
from .base import DATABASES

DEBUG = config("DEBUG", default=False, cast=bool)
SECRET_KEY = config("SECRET_KEY")
SIMPLE_JWT["SIGNING_KEY"] = SECRET_KEY

DATABASES["default"].update(
    {
        "CONN_MAX_AGE": config("DB_CONN_MAX_AGE", default=60, cast=int),
        "ATOMIC_REQUESTS": True,
    }
)

# --- Security -------------------------------------------------------------- #
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=False, cast=bool)
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# --- Storage: media on S3, static files through WhiteNoise ----------------- #
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

STORAGES = {
    "default": {"BACKEND": "backend.storage_backends.MediaStorage"},
    "staticfiles": {
        "BACKEND": "backend.storage_backends.LenientManifestStaticFilesStorage"
    },
}

# --- Cache ----------------------------------------------------------------- #
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": "/tmp/fanfiction-cache",  # noqa: S108
        "TIMEOUT": 60 * 5,
    }
}

# --- E-mail (SMTP, SendGrid) ----------------------------------------------- #
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("SENDGRID_SERVER", default="localhost")
EMAIL_PORT = config("SENDGRID_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("SENDGRID_USERNAME", default="")
EMAIL_HOST_PASSWORD = config("SENDGRID_PASSWORD", default="")
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 30
EMAIL_SUBJECT_PREFIX = "[Fanfiction API] "
