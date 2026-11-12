from django.core.management.base import BaseCommand

from apps.categories.models import Category

# name, logic_value, description
CATEGORIES = [
    (
        "Animes-Mangas",
        "animes-mangas",
        "Fanfictions basées sur des Animes (dessins animés japonais) ou des mangas "
        "(bandes dessinées japonaises)",
    ),
    ("BD-Comics-DA", "bd-comics-da", ""),
    ("Dramas", "dramas", ""),
    ("Fics Originales", "fics-originales", ""),
    ("Films-Séries TV", "films-series-tv", ""),
    ("Historique", "historique", ""),
    ("Jeux Vidéo en ligne", "jeux-video-en-ligne", ""),
    ("Jeux de rôle", "jeux-de-role", ""),
    ("Musique", "musique", ""),
    ("Livres-Romans", "livres", ""),
]


class Command(BaseCommand):
    help = "Create the default categories (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for name, logic_value, description in CATEGORIES:
            _, was_created = Category.objects.get_or_create(
                name=name,
                defaults={"logic_value": logic_value, "description": description},
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} category(ies) created."))
