"""Demo data for local development and for the agentic workflow.

Creates three accounts (password ``demo-password-123``):

- ``demo-admin``: staff + superuser (Django admin);
- ``demo-author``: author of two published fanfics (with chapters) and
  one draft;
- ``demo-reader``: reader who likes, follows and comments a fanfic.

plus a category with two subcategories. The command is idempotent and
refuses to run without ``DEBUG``.

Draft chapters are not created: ``Chapter.clean()`` currently rejects any
``brouillon`` chapter (see CLAUDE.md, "Known issues").
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import FollowStories
from categories.models import Category, SubCategory
from chapters.models import Chapter
from comments.models import Comment
from fanfics.models import Fanfic

DEMO_PASSWORD = "demo-password-123"

# title, subcategory, genre, status, completed, chapters
FANFICS = [
    (
        "Demo — Le voyage de Grand Line",
        "Demo One Piece",
        "AC",
        "publié",
        False,
        ["Le départ", "La tempête"],
    ),
    (
        "Demo — Cartes et cerisiers",
        "Demo Card Captor Sakura",
        "RO",
        "publié",
        True,
        ["Une carte de trop"],
    ),
    ("Demo — Brouillon en cours", "Demo One Piece", "HU", "brouillon", False, []),
]


class Command(BaseCommand):
    help = "Create demo accounts, fanfics, chapters and comments (DEBUG only)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                "seed_demo only runs with DEBUG=True (never on real data)."
            )

        with transaction.atomic():
            self._user("demo-admin", staff=True)
            author = self._user("demo-author")
            reader = self._user("demo-reader")

            category, _ = Category.objects.get_or_create(
                slug="demo-manga",
                defaults={"name": "Demo Manga", "description": "Catégorie de démo"},
            )
            subcategories = {
                name: SubCategory.objects.get_or_create(name=name, category=category)[0]
                for name in {row[1] for row in FANFICS}
            }

            fanfics = []
            for title, sub, genre, status, completed, chapters in FANFICS:
                fanfic, _ = Fanfic.objects.update_or_create(
                    author=author,
                    title=title,
                    defaults={
                        "synopsis": f"Synopsis de démo pour « {title} ».",
                        "genres": [genre],
                        "status": status,
                        "completed": completed,
                        "category": category,
                        "subcategory": subcategories[sub],
                    },
                )
                for chapter_title in chapters:
                    if not fanfic.chapters.filter(title=chapter_title).exists():
                        Chapter.objects.create(
                            author=author,
                            fanfic=fanfic,
                            title=chapter_title,
                            text=f"Texte de démo du chapitre « {chapter_title} ».",
                            status="publié",
                        )
                fanfics.append(fanfic)

            liked = fanfics[0]
            liked.users_like.add(reader)
            liked.total_likes = liked.users_like.count()
            liked.save(update_fields=["total_likes"])
            FollowStories.objects.get_or_create(from_user=reader, to_fanfic=liked)
            Comment.objects.get_or_create(
                author=reader,
                fanfic=liked,
                chapter=liked.chapters.first(),
                defaults={"body": "Super premier chapitre (commentaire de démo) !"},
            )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data ready: demo-admin / demo-author / demo-reader "
                f"(password {DEMO_PASSWORD}), {len(fanfics)} fanfics."
            )
        )

    def _user(self, username, staff=False):
        user, _ = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com"}
        )
        user.is_staff = staff
        user.is_superuser = staff
        user.set_password(DEMO_PASSWORD)
        user.save()
        return user
