from django.contrib.auth.models import User

from django.core.management.base import BaseCommand

from accounts.models import AccountProfile

class Command(BaseCommand):
    help = 'create profile for user'

    def handle(self, *args, **options):
        users = User.objects.filter(is_active=True)
        profile = AccountProfile.objects.all()

        for user in users:
            if not profile.filter(user=user).exists():
                AccountProfile.objects.create(user=user)

            self.stdout.write(self.style.SUCCESS('Created "%s"' % profile))
