from django.core.management.base import BaseCommand

from apps.accounts.services import send_login_reminders


class Command(BaseCommand):
    help = "E-mail users who have not logged in for two weeks."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=14)

    def handle(self, *args, **options):
        sent = send_login_reminders(days=options["days"])
        self.stdout.write(self.style.SUCCESS(f"{sent} reminder(s) sent."))
