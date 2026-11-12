from django.core.management.base import BaseCommand

from apps.accounts.services import deactivate_inactive_users

DURATIONS = {"month": 30, "3month": 90, "6month": 180, "1year": 365}


class Command(BaseCommand):
    help = "Deactivate users who have not logged in for the given duration."

    def add_arguments(self, parser):
        parser.add_argument("duration", choices=sorted(DURATIONS), default="month")

    def handle(self, *args, **options):
        days = DURATIONS[options["duration"]]
        count = deactivate_inactive_users(days)
        self.stdout.write(
            self.style.SUCCESS(f"{count} user(s) inactive for {days} days deactivated.")
        )
