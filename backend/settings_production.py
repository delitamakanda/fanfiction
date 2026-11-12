"""Deprecated alias kept so existing deployments keep working.

Use ``DJANGO_SETTINGS_MODULE=backend.settings.production`` instead.
"""

from backend.settings.production import *  # noqa: F403
