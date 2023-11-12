import csv

from django.core.management.base import BaseCommand

from ...models import Ingredient, Unit


class Command(BaseCommand):
    help = "Импорт ингридиентов"

    def add_arguments(self, parser):
        parser.add_argument(
            "-p",
            "--path",
            action="store",
            required=True,
            help="Путь к файлу с ингридиентами",
        )

    def handle(self, *args, **options):
        with open(options["path"], encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                measurement_unit, created = Unit.objects.get_or_create(
                    name=row[1],
                )
                _, created = Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=measurement_unit,
                )

        self.stdout.write(
            self.style.SUCCESS("Ингридиенты успешно импортированы.")
        )
