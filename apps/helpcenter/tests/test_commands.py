from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.forum.models import Board
from apps.helpcenter.models import FoireAuxQuestions, Lexique


class SeedCommandsTests(TestCase):
    def test_help_and_forum_seeds(self):
        for _ in range(2):
            for command in ("populate_faq", "populate_lexique", "board"):
                call_command(command, stdout=StringIO())
        self.assertEqual(FoireAuxQuestions.objects.count(), 3)
        self.assertTrue(Lexique.objects.filter(title="Drabble").exists())
        self.assertEqual(Board.objects.count(), 8)
