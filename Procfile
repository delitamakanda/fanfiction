web: gunicorn backend.wsgi:application --preload
worker: celery -A backend worker beat -l info --without-gossip --without-mingle --without-heartbeat
