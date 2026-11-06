from django.contrib.auth.models import User
from django.core.management import CommandError, call_command
from django.test import TestCase, override_settings

from chapters.models import Chapter
from comments.models import Comment
from fanfics.models import Fanfic


class SeedDemoCommandTests(TestCase):
    @override_settings(DEBUG=False)
    def test_refuses_to_run_without_debug(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo")
        self.assertFalse(User.objects.filter(username="demo-admin").exists())

    @override_settings(DEBUG=True)
    def test_creates_demo_data(self):
        call_command("seed_demo")

        admin = User.objects.get(username="demo-admin")
        author = User.objects.get(username="demo-author")
        reader = User.objects.get(username="demo-reader")
        self.assertTrue(admin.is_staff and admin.is_superuser)
        self.assertTrue(author.check_password("demo-password-123"))
        self.assertTrue(hasattr(reader, "accountprofile"))

        self.assertEqual(Fanfic.objects.filter(author=author).count(), 3)
        self.assertEqual(Fanfic.published.filter(author=author).count(), 2)
        self.assertEqual(Chapter.objects.filter(author=author).count(), 3)
        liked = Fanfic.objects.get(users_like=reader)
        self.assertEqual(liked.total_likes, 1)
        self.assertTrue(Comment.objects.filter(author=reader, fanfic=liked).exists())

    @override_settings(DEBUG=True)
    def test_is_idempotent(self):
        call_command("seed_demo")
        call_command("seed_demo")

        self.assertEqual(User.objects.filter(username__startswith="demo-").count(), 3)
        self.assertEqual(
            Fanfic.objects.filter(author__username="demo-author").count(), 3
        )
        self.assertEqual(Chapter.objects.count(), 3)
        self.assertEqual(Comment.objects.count(), 1)
