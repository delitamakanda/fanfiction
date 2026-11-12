"""Local development settings."""

from decouple import config

from .base import *  # noqa: F403
from .base import INSTALLED_APPS, MIDDLEWARE

DEBUG = config("DEBUG", default=True, cast=bool)

INTERNAL_IPS = ["127.0.0.1", "localhost"]

if DEBUG:
    try:
        import debug_toolbar  # noqa: F401
    except ImportError:  # pragma: no cover - optional dev dependency
        pass
    else:
        INSTALLED_APPS = [*INSTALLED_APPS, "debug_toolbar"]
        MIDDLEWARE = [*MIDDLEWARE, "debug_toolbar.middleware.DebugToolbarMiddleware"]
