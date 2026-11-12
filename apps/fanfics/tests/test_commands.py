from io import StringIO

from django.core.management import CommandError, call_command
from django.test import TestCase

from apps.core.testing import make_user
from apps.fanfics.models import Fanfic


class ImportCsvCommandTests(TestCase):
    def test_import_is_idempotent(self):
        make_user("importer")
        call_command("populate_categories", stdout=StringIO())
        call_command(
            "import_from_fanfiction_as_csv",
            "output_op.csv",
            author="importer",
            stdout=StringIO(),
        )
        count = Fanfic.objects.count()
        self.assertGreater(count, 0)
        fanfic = Fanfic.objects.first()
        self.assertTrue(fanfic.fanfic_is_scraped)
        self.assertEqual(fanfic.subcategory.name, "One Piece")
        self.assertTrue(fanfic.link_fanfic.startswith("https://www.fanfiction.net/"))

        call_command(
            "import_from_fanfiction_as_csv",
            "output_op.csv",
            author="importer",
            stdout=StringIO(),
        )
        self.assertEqual(Fanfic.objects.count(), count)

    def test_unknown_author(self):
        with self.assertRaises(CommandError):
            call_command(
                "import_from_fanfiction_as_csv", "output_op.csv", author="nobody"
            )
