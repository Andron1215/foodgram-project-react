import csv

from django.core.management.base import BaseCommand

from recipes.models import Tag


class Command(BaseCommand):
    help = "Импорт тегов"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            required=True,
            help="Путь к файлу с тегами",
        )

    def handle(self, *args, **options):
        with open(options["path"], encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                name, color, slug = row
                _, created = Tag.objects.get_or_create(
                    name=name,
                    color=color,
                    slug=slug,
                )

        self.stdout.write(self.style.SUCCESS("Теги успешно импортированы."))
