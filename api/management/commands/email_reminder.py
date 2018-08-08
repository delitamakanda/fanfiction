from datetime import timedelta

from django.core.mail import send_mail
from django.core.management.base import BaseCommand 
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.loader import get_template

def email_tardy_users():
    two_weeks_ago = now() - timedelta(days=14)
    tardy_users = User.objects.filter(
      last_login__lt=two_weeks_ago,
      is_active=True
    )

    print("Found " + str(len(tardy_users)) + " tardy users")

    for user in tardy_users:
        template = get_template('mail/login_reminder.txt') 
        context = {
            'username': user.username,
        }

        content = template.render(context)
        send_mail(
            'Il semble que vous n\'êtes pas connecté à votre compte depuis 2 semaines - De l\'aide ?',
            content,
            'Fanfiction <no-reply@fanfiction.com>',
            [user.email],
        )

class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Emailing tardy users")
        email_tardy_users()
