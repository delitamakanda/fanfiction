from django.core.management.base import BaseCommand

from api.models import Category
from api.models import SubCategory


class Command(BaseCommand):
    help = 'create dummy data to initialize fanfiction'

    def handle(self, *args, **options):
        category_animes = Category.objects.get(name="Animes-Mangas")
        category_comics = Category.objects.get(name="BD-Comics-DA")
        category_dramas = Category.objects.get(name="Dramas")
        category_originales = Category.objects.get(name="Fics Originales")
        category_series_tv = Category.objects.get(name="Films-Séries TV")
        category_historique = Category.objects.get(name="Historique")
        category_jeux_videos = Category.objects.get(name="Jeux Vidéo en ligne")
        category_jeux_role = Category.objects.get(name="Jeux de rôle")
        category_musique = Category.objects.get(name="Musique")
        category_books = Category.objects.get(name="Livres-Romans")

        if not SubCategory.objects.filter(name="Great Teacher Onizuka").exists():
            SubCategory.objects.create(name="Great Teacher Onizuka", category=category_animes)
        if not SubCategory.objects.filter(name="Love Hina").exists():
            SubCategory.objects.create(name="Love Hina", category=category_animes)
        if not SubCategory.objects.filter(name="K-POP").exists():
            SubCategory.objects.create(name="K-POP", category=category_musique, description="Fanfictions basées sur la musique pop sud-coréenne.")
        if not SubCategory.objects.filter(name="J-POP").exists():
            SubCategory.objects.create(name="J-POP", category=category_musique, description="Fanfictions basées sur la musique pop japonaise.")
        if not SubCategory.objects.filter(name="C-POP").exists():
            SubCategory.objects.create(name="C-POP", category=category_musique, description="Fanfictions basées sur la musique pop chinoise.")

        if not SubCategory.objects.filter(name="Divers %s" % category_animes).exists():
            SubCategory.objects.create(name="Divers %s" % category_animes, category=category_animes)
        if not SubCategory.objects.filter(name="Divers %s" % category_comics).exists():
            SubCategory.objects.create(name="Divers %s" % category_comics, category=category_comics)
        if not SubCategory.objects.filter(name="Divers %s" % category_dramas).exists():
            SubCategory.objects.create(name="Divers %s" % category_dramas, category=category_dramas)
        if not SubCategory.objects.filter(name="Divers %s" % category_originales).exists():
            SubCategory.objects.create(name="Divers %s" % category_originales, category=category_originales)
        if not SubCategory.objects.filter(name="Divers %s" % category_series_tv).exists():
            SubCategory.objects.create(name="Divers %s" % category_series_tv, category=category_series_tv)
        if not SubCategory.objects.filter(name="Divers %s" % category_historique).exists():
            SubCategory.objects.create(name="Divers %s" % category_historique, category=category_historique)
        if not SubCategory.objects.filter(name="Divers %s" % category_jeux_videos).exists():
            SubCategory.objects.create(name="Divers %s" % category_jeux_videos, category=category_jeux_videos)
        if not SubCategory.objects.filter(name="Divers %s" % category_jeux_role).exists():
            SubCategory.objects.create(name="Divers %s" % category_jeux_role, category=category_jeux_role)
        if not SubCategory.objects.filter(name="Divers %s" % category_musique).exists():
            SubCategory.objects.create(name="Divers %s" % category_musique, category=category_musique)
        if not SubCategory.objects.filter(name="Divers %s" % category_books).exists():
            SubCategory.objects.create(name="Divers %s" % category_books, category=category_books)

            self.stdout.write(self.style.SUCCESS('Created subcategories'))
