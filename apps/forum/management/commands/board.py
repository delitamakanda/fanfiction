from django.core.management.base import BaseCommand

from apps.forum.models import Board

BOARDS = [
    ("Animes-Mangas", "Discussions basées sur les animés et les mangas"),
    ("BD-Comics-DA", "Discussions basées sur les bandes dessinées"),
    ("Dramas", "Discussions basées sur les dramas."),
    ("Films-Séries TV", "Discussions basées sur les séries TV et les films."),
    ("Jeux Vidéo", "Discussions basées sur les jeux vidéos"),
    ("Musique", "Discussions basées sur la musique en général."),
    ("Livres-Romans", "Discussions basées sur les livres et les romans."),
    (
        "Fanfiction le site",
        "Discussions basées sur le site Fanfiction, vos idées, "
        "les fonctionnalités à apporter...",
    ),
]


class Command(BaseCommand):
    help = "Create the default forum boards (idempotent)."

    def handle(self, *args, **options):
        created = 0
        for name, description in BOARDS:
            _, was_created = Board.objects.get_or_create(
                name=name, defaults={"description": description}
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} board(s) created."))
