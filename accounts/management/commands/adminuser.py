from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string

User = get_user_model()

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = "admin@example.com"
        new_password = get_random_string(length=10)
        try:
            if not User.objects.filter(email=email).exists():
                self.stdout.write(self.style.ERROR(f"User with email {email} does not exist."))
                User.objects.create_superuser(
                    username="admin",
                    email=email,
                    password=new_password
                )
                self.stdout.write("============================================")
                self.stdout.write(f"Admin user created with email: {email}")
                self.stdout.write(f"Password: {new_password}")
                self.stdout.write("============================================")
            else:
                self.stdout.write(self.style.ERROR(f"Admin user with email {email} already exists."))
                self.stdout.write("============================================")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
            self.stdout.write("============================================")
