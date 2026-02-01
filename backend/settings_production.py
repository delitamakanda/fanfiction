from backend.settings import *

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

DEBUG = config('DEBUG', cast=bool, default=False)

ALLOWED_HOSTS = ['*', ]

# email admin

SERVER_EMAIL = config('ADMIN_EMAIL')

ADMINS = [
    (config('ADMIN_NAME'), config('ADMIN_EMAIL')),
]

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR,'static')]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media storages

OSS_ACCESS_KEY_ID = config('OSS_ACCESS_KEY_ID')
OSS_ACCESS_KEY_SECRET = config('OSS_ACCESS_KEY_SECRET')
OSS_EXPIRE_TIME = config('OSS_EXPIRE_TIME', cast=int, default=3600)
OSS_BUCKET_NAME = config('OSS_BUCKET_NAME')
OSS_ENDPOINT = config('OSS_ENDPOINT')

DEFAULT_FILE_STORAGE = 'backend.storage_backends.MediaStorage'

# Database

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': config('ALIYUN_BDD_NAME', default=None),
		'USER': config('ALIYUN_BDD_USER', default=None),
		'PASSWORD': config('ALIYUN_BDD_PASSWORD', default=None),
		'HOST': config('ALIYUN_BDD_HOST', default=None),
        'PORT': config('ALIYUN_BDD_PORT', default=None),
        'CONN_MAX_AGE': 60,  # Connection pooling: reuse connections for 60 seconds
        'OPTIONS': {
            'connect_timeout': 10,  # Timeout for establishing connections
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
DEFAULT_FROM_EMAIL = SERVER_EMAIL

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
