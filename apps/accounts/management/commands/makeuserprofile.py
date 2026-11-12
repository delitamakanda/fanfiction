from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.accounts.models import AccountProfile


class Command(BaseCommand):
    help = "Create the missing account profiles."

    def handle(self, *args, **options):
        users = get_user_model().objects.filter(accountprofile__isnull=True)
        profiles = AccountProfile.objects.bulk_create(
            [AccountProfile(user=user) for user in users]
        )
        self.stdout.write(self.style.SUCCESS(f"{len(profiles)} profile(s) created."))
