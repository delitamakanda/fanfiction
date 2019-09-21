web: gunicorn backend.wsgi:application --preload
worker: celery -A backend worker -l info -B
