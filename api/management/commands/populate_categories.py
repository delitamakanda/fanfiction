from django.core.management.base import BaseCommand

from categories.models import Category

class Command(BaseCommand):
    help = 'create dummy data to initialize fanfiction'

    def handle(self, *args, **options):
        if not Category.objects.filter(name="Animes-Mangas").exists():
            Category.objects.create(name='Animes-Mangas', description="Fanfictions basées sur des Animes (dessins animés japonais) ou des mangas (bandes dessinées japonaises)", logic_value='animes-mangas')
        if not Category.objects.filter(name="BD-Comics-DA").exists():
            Category.objects.create(name='BD-Comics-DA', logic_value='bd-comics-da')
        if not Category.objects.filter(name="Dramas").exists():
            Category.objects.create(name='Dramas', logic_value='dramas')
        if not Category.objects.filter(name="Fics Originales").exists():
            Category.objects.create(name='Fics Originales', logic_value='fics-originales')
        if not Category.objects.filter(name="Films-Séries TV").exists():
            Category.objects.create(name='Films-Séries TV', logic_value="films-series-tv")
        if not Category.objects.filter(name="Historique").exists():
            Category.objects.create(name='Historique', logic_value='historique')
        if not Category.objects.filter(name="Jeux Vidéo en ligne").exists():
            Category.objects.create(name='Jeux Vidéo en ligne', logic_value="jeux-video-en-ligne")
        if not Category.objects.filter(name="Jeux de rôle").exists():
            Category.objects.create(name='Jeux de rôle', logic_value='jeux-de-role')
        if not Category.objects.filter(name="Musique").exists():
            Category.objects.create(name='Musique', logic_value='musique')
        if not Category.objects.filter(name="Livres-Romans").exists():
            Category.objects.create(name='Livres-Romans', logic_value='livres')

            self.stdout.write(self.style.SUCCESS('Created categories'))
