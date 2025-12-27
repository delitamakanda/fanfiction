from django.apps import AppConfig


class FanficsConfig(AppConfig):
    name = 'fanfics'
    verbose_name = 'Fanfics API'

    def ready(self):
        try:
            import fanfics.signals  # noqa
        except ImportError:
            print("Error: Unable to import fanfics.signals. Please ensure that the 'fanfics' application is correctly installed.")
