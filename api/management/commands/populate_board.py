from django.core.management.base import BaseCommand

from api.models import Board

class Command(BaseCommand):
    help = 'create dummy data to initialize fanfiction'

    def handle(self, *args, **options):
        if not Board.objects.filter(name="Animes-Mangas").exists():
            Board.objects.get_or_create(name='Animes-Mangas', description="Discussions basées sur les animés et les mangas")
        if not Board.objects.filter(name="BD-Comics-DA").exists():
            Board.objects.get_or_create(name='BD-Comics-DA', description="Discussions basées sur les bandes dessinées")
        if not Board.objects.filter(name="Dramas").exists():
            Board.objects.get_or_create(name='Dramas', description="Discussions basées sur les dramas.")
        if not Board.objects.filter(name="Films-Séries TV").exists():
            Board.objects.get_or_create(name='Films-Séries TV', description="Discussions basées sur les séries TV et les films.")
        if not Board.objects.filter(name="Jeux Vidéo en ligne").exists():
            Board.objects.get_or_create(name='Jeux Vidéo', description="Discussions basées sur les jeux vidéos")
        if not Board.objects.filter(name="Musique").exists():
            Board.objects.get_or_create(name='Musique', description="Discussions basées sur la musique en général.")
        if not Board.objects.filter(name="Livres-Romans").exists():
            Board.objects.get_or_create(name='Livres-Romans', description="Discussions basées sur les livres et les romans.")
        if not Board.objects.filter(name="Fanfiction le site").exists():
            Board.objects.get_or_create(name='Fanfiction le site', description="Discussions basées sur le site Fanfiction, vos idées, les fonctionnalités à apporter...")

            self.stdout.write(self.style.SUCCESS('Created boards'))
