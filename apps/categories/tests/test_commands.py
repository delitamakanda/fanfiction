from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from apps.categories.models import Category, SubCategory


class SeedCommandsTests(TestCase):
    def test_populate_categories_and_subcategories_are_idempotent(self):
        for _ in range(2):
            call_command("populate_categories", stdout=StringIO())
            call_command("populate_subcategories", stdout=StringIO())
        self.assertEqual(Category.objects.count(), 10)
        self.assertTrue(SubCategory.objects.filter(name="Divers Musique").exists())
        self.assertEqual(SubCategory.objects.filter(name="K-POP").count(), 1)
