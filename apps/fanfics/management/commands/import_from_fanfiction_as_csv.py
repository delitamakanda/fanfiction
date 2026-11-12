"""Import fanfictions scraped from https://www.fanfiction.net/ (CSV files).

Usage::

    python manage.py import_from_fanfiction_as_csv output_op.csv --author admin

Files are looked up in ``data/`` next to this command. Each file is bound to a
fandom (category, subcategory, credits) in ``SOURCES``.
"""

import csv
import re
from dataclasses import dataclass
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from apps.categories.models import Category, SubCategory
from apps.fanfics.models import Fanfic

DATA_DIR = Path(__file__).resolve().parent / "data"
BASE_URL = "https://www.fanfiction.net"

RATINGS = {"Rated: K": "g", "Rated: K+": "13", "Rated: T": "r", "Rated: M": "18"}
GENRES = [
    ("Adventure", "AC"),
    ("Romance", "RO"),
    ("Tragedy", "TR"),
    ("Sci", "GE"),
    ("Supernatural", "SU"),
]


@dataclass(frozen=True)
class Source:
    category: str
    subcategory: str
    credits: str


SOURCES = {
    "output_ccs.csv": Source("Animes-Mangas", "Card Captor Sakura", "Clamp"),
    "output_marvel.csv": Source("BD-Comics-DA", "Marvel", "Marvel comics"),
    "output_op.csv": Source("Animes-Mangas", "One Piece", "Eiichirō Oda"),
}


def parse_genres(raw: str) -> list[str]:
    for word, code in GENRES:
        if re.search(rf"\b{word}\b", raw, flags=re.IGNORECASE):
            return [code]
    return ["GE", "DR"]


class Command(BaseCommand):
    help = "Import fanfictions from the CSV files of fanfiction.net."

    def add_arguments(self, parser):
        parser.add_argument("filenames", nargs="+", choices=sorted(SOURCES))
        parser.add_argument(
            "--author",
            default="delitamakanda",
            help="Username that owns the imported fanfics.",
        )

    def handle(self, *args, **options):
        try:
            author = get_user_model().objects.get(username=options["author"])
        except get_user_model().DoesNotExist as exc:
            raise CommandError(f"User {options['author']!r} does not exist") from exc

        for filename in options["filenames"]:
            created = self.import_file(DATA_DIR / filename, SOURCES[filename], author)
            self.stdout.write(
                self.style.SUCCESS(f"{filename}: {created} fanfic(s) imported")
            )

    @transaction.atomic
    def import_file(self, path: Path, source: Source, author) -> int:
        if not path.exists():
            raise CommandError(f"File {path} does not exist")
        try:
            category = Category.objects.get(name=source.category)
        except Category.DoesNotExist as exc:
            raise CommandError(
                f"Category {source.category!r} is missing: run populate_categories"
            ) from exc
        subcategory, _ = SubCategory.objects.get_or_create(
            name=source.subcategory, defaults={"category": category}
        )

        created = 0
        with path.open(newline="", encoding="utf-8") as csv_file:
            for row in csv.DictReader(csv_file):
                row = {key: (value or "").strip() for key, value in row.items()}
                link = BASE_URL + row["link_fanfic"]
                _, was_created = Fanfic.objects.get_or_create(
                    title=row["title"],
                    defaults={
                        "author": author,
                        "genres": parse_genres(row["genre"]),
                        "synopsis": row["synopsis"][:1000],
                        "picture": BASE_URL + row["picture"],
                        "description": link,
                        "link_fanfic": link,
                        "language": "en" if row["language"] == "English" else "fr",
                        "classement": RATINGS.get(row["classement"], "g"),
                        "status": Fanfic.Status.PUBLISHED,
                        "category": category,
                        "subcategory": subcategory,
                        "credits": source.credits,
                        "fanfic_is_scraped": True,
                    },
                )
                created += was_created
        return created
