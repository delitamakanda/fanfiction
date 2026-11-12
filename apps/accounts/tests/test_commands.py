from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import AccountProfile
from apps.core.testing import make_user


class AccountCommandsTests(TestCase):
    def test_deactivateuser(self):
        old = make_user(last_login=timezone.now() - timedelta(days=100))
        call_command("deactivateuser", "3month", stdout=StringIO())
        old.refresh_from_db()
        self.assertFalse(old.is_active)

    def test_makeuserprofile_and_adminuser(self):
        user = make_user()
        AccountProfile.objects.filter(user=user).delete()
        call_command("makeuserprofile", stdout=StringIO())
        self.assertTrue(AccountProfile.objects.filter(user=user).exists())

        out = StringIO()
        call_command("adminuser", stdout=out)
        call_command("adminuser", stdout=StringIO())
        self.assertTrue(get_user_model().objects.get(username="admin").is_superuser)
        self.assertIn("Password:", out.getvalue())
