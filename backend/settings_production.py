from backend.settings import *

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = ['*', '.elasticbeanstalk.com',]

# email admin

SERVER_EMAIL = config('ADMIN_EMAIL')

ADMINS = [
  (config('ADMIN_NAME'), config('ADMIN_EMAIL')),
]

ALLOWED_HOSTS = ['*',]

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

# Database RDS AWS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Memcache

CACHES = {
    'default': {
        'BACKEND': 'django_bmemcached.memcached.BMemcached',
        'LOCATION': config('MEMCACHE_SERVERS'),
        'OPTIONS': {
            'username': config('MEMCACHE_USERNAME'),
            'password': config('MEMCACHE_PASSWORD')
        }
    }
}

# SMTP Email servier

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('SENDGRID_SERVER')
EMAIL_PORT = config('SENDGRID_PORT')
EMAIL_HOST_USER = config('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = config('SENDGRID_PASSWORD')
EMAIL_USE_TLS = True

# Disable browsable API

REST_FRAMEWORK = {
  'DEFAULT_RENDERER_CLASSES': (
    'rest_framework.renderers.JSONRenderer',
  )
}
