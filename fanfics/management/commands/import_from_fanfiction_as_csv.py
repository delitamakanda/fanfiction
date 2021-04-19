import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from fanfics.models import Fanfic


class Command(BaseCommand):
    help = (
        "Import fanfictions from a local csv",
        "from external site : https://www.fanfiction.net/"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = Fanfic

    def import_from_fanfiction_as_csv(self, data):
        try:
            pass
            # self.model_name.objects.get_or_create(
            # title=data["title"],
            # genre=data["genre"],
            # author=data["author"]
            # )
        except Exception as e:
            raise CommandError("Error in inserting {}: {}".format(
                self.model_name, str(e)))

    def get_current_app_path(self):
        return apps.get_app_config('fanfics').path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        file_path = os.path.join(app_path, "management",
                                 "commands", filename)
        return file_path

    def add_arguments(self, parser):
        parser.add_argument('filenames',
                            nargs='+',
                            type=str,
                            help="Inserts Fanfictions from CSV file")

    def handle(self, *args, **options):
        for filename in options['filenames']:
            self.stdout.write(self.style.SUCCESS(
                'Reading:{}'.format(filename)))
            file_path = self.get_csv_file(filename)
            try:
                with open(file_path) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    for row in csv_reader:
                        if row != "":
                            # print(row)
                            words = [word.strip() for word in row]
                            title = words[0]
                            picture = 'https://www.fanfiction.net' + words[1]
                            author = words[2]
                            synopsis = words[3]
                            classement = words[4]
                            language = words[5]
                            genre = words[6]
                            link_fanfic = 'https://www.fanfiction.net' + \
                                words[7]
                            print(words[7])
                            data = {}
                            data["title"] = title
                            data["picture"] = picture
                            data["author"] = author
                            data["genre"] = genre
                            self.import_from_fanfiction_as_csv(data)
                            self.stdout.write(
                                self.style.SUCCESS('{} - {}: {}'.format(
                                    title, author,
                                    genre
                                )
                                )
                            )

            except FileNotFoundError:
                raise CommandError("File {} does not exist".format(
                    file_path))
