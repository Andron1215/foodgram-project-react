import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Unit


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
            ingredients = []
            for row in reader:
                ingredient_name, unit_name = row
                measurement_unit, created = Unit.objects.get_or_create(
                    name=unit_name,
                )
                ingredients.append(
                    Ingredient(
                        name=ingredient_name, measurement_unit=measurement_unit
                    )
                )
            Ingredient.objects.bulk_create(ingredients, ignore_conflicts=True)

        self.stdout.write(
            self.style.SUCCESS("Ингридиенты успешно импортированы.")
        )
