from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = 'Accounts API'

    def ready(self):
        import accounts.signals  # noqa
