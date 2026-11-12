from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = "apps.forum"
    label = "forum"
    verbose_name = "Forum"
    default_auto_field = "django.db.models.BigAutoField"
