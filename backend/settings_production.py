from backend.settings import * # NOQA
import os
import dj_database_url

DATABASES["default"] = dj_database_url.config()  # NOQA
DATABASES["default"]["CONN_MAX_AGE"] = 60  # NOQA
DATABASES["default"]["ATOMIC_REQUESTS"] = True  # NOQA

DEBUG = os.getenv('DEBUG') == "True"

SECRET_KEY = os.getenv('SECRET_KEY')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_REFERRER_POLICY = "strict-origin"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')

# email admin
SERVER_EMAIL = os.getenv('SERVER_EMAIL')

ADMINS = [
	(os.getenv('ADMIN_NAME'), os.getenv('ADMIN_EMAIL')),
]

DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media storages

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

STORAGES["default"] = { # NOQA
	"BACKEND": "backend.storage_backends.MediaStorage"
}

# Cache

CACHES = {
    'default': {
		'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION': '/tmp/fanfiction-recommendations-cache',
        'TIMEOUT': 60 * 5,  # 5 minutes
    }
}

# CSRF
CSRF_TRUSTED_ORIGINS=os.getenv('CSRF_TRUSTED_ORIGINS').split(',')

# Mail support

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv("SENDGRID_SERVER")
EMAIL_HOST_USER = os.getenv("SENDGRID_USERNAME")
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_PASSWORD")
EMAIL_PORT = os.getenv("SENDGRID_PORT")
EMAIL_TIMEOUT = 500
EMAIL_USE_SSL = False
EMAIL_SUBJECT_PREFIX = "[Fanfiction API] "
