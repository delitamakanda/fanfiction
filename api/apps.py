from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "API Core"

    def ready(self):
        try:
            from api import signals  # noqa
        except ImportError:
            pass  # noqa
