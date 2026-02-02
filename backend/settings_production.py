from backend.settings import *

# Helper function to convert empty strings to None
def config_or_none(key, **kwargs):
    """Get config value, treating empty strings as None"""
    value = config(key, **kwargs)
    return None if value == '' else value

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ['*', ]

# email admin

admin_email = config_or_none('ADMIN_EMAIL', default='admin@example.com')
admin_name = config_or_none('ADMIN_NAME', default='Admin')

SERVER_EMAIL = admin_email

ADMINS = [
    (admin_name, admin_email),
]

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media storages

OSS_ACCESS_KEY_ID = config_or_none('OSS_ACCESS_KEY_ID', default='')
OSS_ACCESS_KEY_SECRET = config_or_none('OSS_ACCESS_KEY_SECRET', default='')
OSS_EXPIRE_TIME = config('OSS_EXPIRE_TIME', cast=int, default=3600)
OSS_BUCKET_NAME = config_or_none('OSS_BUCKET_NAME', default='')
OSS_ENDPOINT = config_or_none('OSS_ENDPOINT', default='')

# Only use OSS storage if credentials are provided
if OSS_ACCESS_KEY_ID and OSS_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'

# Database

# Get database configuration, treating empty strings as None
db_name = config_or_none('ALIYUN_BDD_NAME', default=None)
db_user = config_or_none('ALIYUN_BDD_USER', default=None)
db_password = config_or_none('ALIYUN_BDD_PASSWORD', default=None)
db_host = config_or_none('ALIYUN_BDD_HOST', default=None)
db_port = config_or_none('ALIYUN_BDD_PORT', default=None)

# Use PostgreSQL if credentials are provided, otherwise fallback to SQLite
if db_name and db_host:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'HOST': db_host,
            'PORT': db_port,
            'CONN_MAX_AGE': 60,  # Connection pooling: reuse connections for 60 seconds
            'OPTIONS': {
                'connect_timeout': 10,  # Timeout for establishing connections
            }
        }
    }
else:
    # Fallback to SQLite for testing/development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# SMTP Email server

sendgrid_server = config_or_none('SENDGRID_SERVER', default='')
sendgrid_port = config_or_none('SENDGRID_PORT', default='587')
sendgrid_username = config_or_none('SENDGRID_USERNAME', default='')
sendgrid_password = config_or_none('SENDGRID_PASSWORD', default='')

# Only configure SMTP if credentials are provided
if sendgrid_server and sendgrid_username:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = sendgrid_server
    EMAIL_PORT = sendgrid_port
    EMAIL_HOST_USER = sendgrid_username
    EMAIL_HOST_PASSWORD = sendgrid_password
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = SERVER_EMAIL
else:
    # Fallback to console backend for testing
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

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
    "http://localhost:5173",
    "https://fanfics-fr.netlify.app"
]
