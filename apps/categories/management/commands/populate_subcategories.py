from django.core.management.base import BaseCommand, CommandError

from apps.categories.management.commands.populate_categories import CATEGORIES
from apps.categories.models import Category, SubCategory

# name, category, description
SUBCATEGORIES = [
    ("Great Teacher Onizuka", "Animes-Mangas", ""),
    ("Love Hina", "Animes-Mangas", ""),
    ("K-POP", "Musique", "Fanfictions basées sur la musique pop sud-coréenne."),
    ("J-POP", "Musique", "Fanfictions basées sur la musique pop japonaise."),
    ("C-POP", "Musique", "Fanfictions basées sur la musique pop chinoise."),
] + [(f"Divers {name}", name, "") for name, _, _ in CATEGORIES]


class Command(BaseCommand):
    help = "Create the default subcategories (run populate_categories first)."

    def handle(self, *args, **options):
        categories = {category.name: category for category in Category.objects.all()}
        created = 0
        for name, category_name, description in SUBCATEGORIES:
            if category_name not in categories:
                raise CommandError(
                    f"Category {category_name!r} is missing: run populate_categories"
                )
            _, was_created = SubCategory.objects.get_or_create(
                name=name,
                defaults={
                    "category": categories[category_name],
                    "description": description,
                },
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f"{created} subcategory(ies) created."))
