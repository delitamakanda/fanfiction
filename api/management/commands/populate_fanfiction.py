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
            Fanfic.objects.create(
                author=user,
                title="dummy fanfic",
                genres="RO",
                category=category,
                subcategory=subcategory
            )

            self.stdout.write(self.style.SUCCESS('Created "%s"' % fanfic))
