from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Shared building blocks: permissions, pagination, fields, monitoring API."""

    name = "apps.core"
    label = "core"
    verbose_name = "Core"
    default_auto_field = "django.db.models.BigAutoField"
