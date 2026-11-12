"""Common settings shared by every environment.

Environment-specific modules (``development``, ``production``, ``test``) import
everything from here and only override what differs. Values that change between
deployments are read from the environment (or a ``.env`` file) with
``python-decouple``.
"""

from datetime import timedelta
from pathlib import Path

import dj_database_url
from celery.schedules import crontab
from decouple import Csv, config
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --------------------------------------------------------------------------- #
# Core
# --------------------------------------------------------------------------- #

SECRET_KEY = config("SECRET_KEY", default="insecure-dev-only-secret-key")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

SITE_ID = 1
SITE_NAME = "Fanfiction API"

ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"

# Existing tables use 32-bit ids: switching would generate migrations for every app.
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# --------------------------------------------------------------------------- #
# Applications
# --------------------------------------------------------------------------- #

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.sites",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.sitemaps",
    "django.contrib.flatpages",
]

THIRD_PARTY_APPS = [
    "multiselectfield",
    "django_filters",
    "storages",
    "markdownx",
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "django_celery_results",
    "django_celery_beat",
]

# App labels are unchanged since the move under ``apps/``: migrations and
# database tables keep their names.
LOCAL_APPS = [
    "apps.core",
    "apps.categories",
    "apps.fanfics",
    "apps.chapters",
    "apps.comments",
    "apps.accounts",
    "apps.posts",
    "apps.helpcenter",
    "apps.forum",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.core.middleware.RequestTimingMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --------------------------------------------------------------------------- #
# Database & cache
# --------------------------------------------------------------------------- #

DATABASES = {
    "default": dj_database_url.parse(
        config("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=config("DB_CONN_MAX_AGE", default=0, cast=int),
    )
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "fanfiction-cache",
    }
}

# --------------------------------------------------------------------------- #
# Authentication
# --------------------------------------------------------------------------- #

# Accepts the username or the e-mail address (case-insensitive).
AUTHENTICATION_BACKENDS = ["apps.accounts.backends.EmailAuthBackend"]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_RESET_TIMEOUT = 60 * 60 * 24  # 1 day
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "admin:login"

# --------------------------------------------------------------------------- #
# Internationalization
# --------------------------------------------------------------------------- #

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LANGUAGES = [
    ("en-us", _("Anglais")),
    ("fr-fr", _("Français")),
]
LOCALE_PATHS = [BASE_DIR / "locale"]

# --------------------------------------------------------------------------- #
# Static & media files
# --------------------------------------------------------------------------- #

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --------------------------------------------------------------------------- #
# E-mail
# --------------------------------------------------------------------------- #

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@localhost")
SERVER_EMAIL = config("SERVER_EMAIL", default="server@localhost")
ADMINS = [
    (
        config("ADMIN_NAME", default="Admin"),
        config("ADMIN_EMAIL", default="admin@localhost"),
    )
]

# --------------------------------------------------------------------------- #
# Django REST framework, JWT & OpenAPI
# --------------------------------------------------------------------------- #

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "apps.core.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # Safe default: anonymous users can read, writes need a token. Views
    # still declare their own permissions explicitly.
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_THROTTLE_CLASSES": ("rest_framework.throttling.AnonRateThrottle",),
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5000/day",
        "user": "10000/day",
        "contact_form": "5/hour",
        "password_reset": "5/hour",
        "share": "10/hour",
        "feedback": "10/hour",
    },
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "SEARCH_PARAM": "q",
    "ORDERING_PARAM": "ordering",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Fanfiction API",
    "DESCRIPTION": "API for managing fanfiction content",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    "CONTACT": {
        "name": "Fanfiction API Team",
        "url": "https://github.com/delitamakanda/fanfiction",
    },
    "LICENSE": {
        "name": "MIT License",
        "url": "https://github.com/delitamakanda/fanfiction/blob/main/LICENSE",
    },
    "PREPROCESSING_HOOKS": ["drf_spectacular.hooks.preprocess_exclude_path_format"],
    "POSTPROCESSING_HOOKS": ["drf_spectacular.hooks.postprocess_schema_enums"],
}

# --------------------------------------------------------------------------- #
# CORS (the Vue front lives on another origin)
# --------------------------------------------------------------------------- #

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:5173,https://fanfics-fr.netlify.app",
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "range",
    "x-csrftoken",
    "x-custom-header",
    "x-requested-with",
)

# --------------------------------------------------------------------------- #
# Celery
# --------------------------------------------------------------------------- #

CELERY_BROKER_URL = config(
    "CELERY_BROKER_URL", default=config("REDIS_URL", default="redis://localhost:6379/0")
)
CELERY_RESULT_BACKEND = "django-db"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_BEAT_SCHEDULE = {
    "user_email_reminder_every_week": {
        "task": "accounts.tasks.send_login_reminders",
        "schedule": crontab(hour=7, minute=30, day_of_week=1),
    },
    "deactivate_inactive_users": {
        "task": "accounts.tasks.deactivate_inactive_users",
        "schedule": crontab(hour=0, minute=0, day_of_month=1, month_of_year=1),
    },
    "refresh_recos_for_all_users": {
        "task": "fanfics.tasks.refresh_recos_for_all_users",
        "schedule": crontab(hour=3, minute=0),
    },
    "purge_recs_from_opted_out_users": {
        "task": "fanfics.tasks.purge_recs_from_opted_out_users",
        "schedule": crontab(hour=3, minute=30),
    },
}

# --------------------------------------------------------------------------- #
# Logging
# --------------------------------------------------------------------------- #

LOG_LEVEL = config("DJANGO_LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "{asctime} {levelname} {name} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "simple"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "apps": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}

# --------------------------------------------------------------------------- #
# Third-party services
# --------------------------------------------------------------------------- #

RECAPTCHA_SECRET_KEY = config("RECAPTCHA_SECRET_KEY", default="")
RECAPTCHA_MIN_SCORE = config("RECAPTCHA_MIN_SCORE", default=0.5, cast=float)
OPENAI_API_KEY = config("OPENAI_API_KEY", default="")
OPENAI_MODEL = config("OPENAI_MODEL", default="gpt-4.1-mini")

# Public URL of the Vue front, used in e-mails (sharing, password reset).
FRONTEND_URL = config("FRONTEND_URL", default="http://localhost:5173")
