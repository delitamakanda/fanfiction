"""Small factories shared by the test suites (no extra dependency)."""

from itertools import count

from django.contrib.auth import get_user_model

from apps.categories.models import Category, SubCategory
from apps.chapters.models import Chapter
from apps.core.choices import PublicationStatus
from apps.fanfics.models import Fanfic

PASSWORD = "a-strong-password-42"  # noqa: S105 - test fixture
_sequence = count(1)


def make_user(username=None, **extra):
    n = next(_sequence)
    username = username or f"user{n}"
    extra.setdefault("email", f"{username}@example.com")
    return get_user_model().objects.create_user(
        username=username, password=PASSWORD, **extra
    )


def make_subcategory(name=None):
    n = next(_sequence)
    category = Category.objects.create(name=f"Category {n}")
    return SubCategory.objects.create(
        name=name or f"Subcategory {n}", category=category
    )


def make_fanfic(
    author=None, status=PublicationStatus.PUBLISHED, subcategory=None, **extra
):
    subcategory = subcategory or make_subcategory()
    return Fanfic.objects.create(
        author=author or make_user(),
        title=extra.pop("title", f"Fanfic {next(_sequence)}"),
        genres=extra.pop("genres", ["RO"]),
        status=status,
        category=subcategory.category,
        subcategory=subcategory,
        **extra,
    )


def make_chapter(fanfic, status=PublicationStatus.PUBLISHED, **extra):
    return Chapter.objects.create(
        fanfic=fanfic,
        author=fanfic.author,
        title=extra.pop("title", f"Chapter {next(_sequence)}"),
        text=extra.pop("text", "Il était une fois..."),
        status=status,
        **extra,
    )
