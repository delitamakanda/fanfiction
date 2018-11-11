from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from api.models import Fanfic
from api.models import Category
from api.models import SubCategory
from api.models import Board

class Command(BaseCommand):
    help = 'create dummy data to initialize fanfiction'

    def handle(self, *args, **options):
        user = User.objects.get(id=1)
        category = Category.objects.get(id=1)
        subcategory = SubCategory.objects.get(id=1)

        fanfic = Fanfic.objects.filter(title="dummy fanfic")

        if not fanfic.exists():
            fanfic.objects.create(
                author=user,
                title="dummy fanfic",
                genres="RO",
                category=category,
                subcategory=subcategory
            )

            self.stdout.write(self.style.SUCCESS('Created "%s"' % fanfic))

        """
        Categories
        """

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

        """
        Subcategories
        """

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

            self.stdout.write(self.style.SUCCESS('Created subcategories'))

        """
        Boards
        """

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
