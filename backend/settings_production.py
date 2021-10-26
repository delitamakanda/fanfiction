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

# Settings REST Framework for production
# Disable browsable API

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'api.custompagination.LimitOffsetPaginationWithUpperBound',
    'PAGE_SIZE': 4,
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'api.customauthentication.CsrfExemptSessionAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '3000/days',
        'user': '1000/days',
        'fanfic': '2000/days',
    },
    'DEFAULT_METADATA_CLASS': 'rest_framework.metadata.SimpleMetadata',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'SEARCH_PARAM': 'q',
    'ORDERING_PARAM': 'ordering',
}

# Python Social Auth

SOCIAL_AUTH_POSTGRES_JSONFIELD = True

# Asynchronous tasks

CELERY_BROKER_URL = config('HEROKU_REDIS_OLIVE_URL')
CELERY_RESULT_BACKEND = config('HEROKU_REDIS_OLIVE_URL')
REDIS_URL = config('HEROKU_REDIS_OLIVE_URL')

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# csrf
CSRF_TRUSTED_ORIGINS = ['fanfiction-fr.netlify.app']
