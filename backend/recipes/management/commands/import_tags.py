import csv

from django.core.management.base import BaseCommand

from ...models import Tag


class Command(BaseCommand):
    help = "Импорт тегов"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            dest="path",
            required=True,
            help="Путь к файлу с тегами",
        )

    def handle(self, *args, **options):
        with open(options["path"], encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                _, created = Tag.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )

        self.stdout.write(self.style.SUCCESS("Теги успешно импортированы."))
