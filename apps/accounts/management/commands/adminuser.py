from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string


class Command(BaseCommand):
    help = "Create the initial superuser (random password) if it does not exist."

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin")
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):
        user_model = get_user_model()
        email = options["email"]
        if user_model.objects.filter(email=email).exists():
            self.stdout.write(f"Admin user with email {email} already exists.")
            return
        password = get_random_string(length=20)
        user_model.objects.create_superuser(
            username=options["username"], email=email, password=password
        )
        self.stdout.write(self.style.SUCCESS(f"Admin user created with email: {email}"))
        self.stdout.write(f"Password: {password}")
