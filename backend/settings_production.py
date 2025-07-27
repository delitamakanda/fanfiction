from backend.settings import *
import dj_database_url

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ['*', ]

# email admin

SERVER_EMAIL = config('ADMIN_EMAIL')

ADMINS = [
    (config('ADMIN_NAME'), config('ADMIN_EMAIL')),
]

STATIC_ROOT = 'static'

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media storages

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'

DATABASES['default'] = dj_database_url.config()

# SMTP Email servier

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('SENDGRID_SERVER')
EMAIL_PORT = config('SENDGRID_PORT')
EMAIL_HOST_USER = config('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = config('SENDGRID_PASSWORD')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = SERVER_EMAIL

# Python Social Auth

SOCIAL_AUTH_JSONFIELD_ENABLED = True

# Asynchronous tasks

CELERY_BROKER_URL = config('HEROKU_REDIS_OLIVE_URL')
CELERY_RESULT_BACKEND = config('HEROKU_REDIS_OLIVE_URL')
REDIS_URL = config('HEROKU_REDIS_OLIVE_URL')

# Cache

CACHES = {
    'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/tmp/fanfiction-recommendations-cache',
        'TIMEOUT': 60 * 5,  # 5 minutes
    }
}

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://fanfiction-fr.netlify.app",
    "https://fanfiction-fr.herokuapp.com",
    "http://localhost:8080"
]
