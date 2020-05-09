web: gunicorn backend.wsgi:application --preload
worker: celery worker --app=backend --loglevel=info -B
