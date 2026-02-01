#!/bin/bash
set -euo pipefail

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-backend.settings_production}"

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
