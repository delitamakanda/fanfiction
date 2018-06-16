from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'
    verbose_name = "API"

    def ready(self):
        from api.signals import users_like_changed
