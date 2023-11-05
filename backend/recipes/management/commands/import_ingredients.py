import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from ...models import Ingredients, Units

path_ingredients_csv = Path(__file__).parents[4] / "data" / "ingredients.csv"


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(path_ingredients_csv, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                measurement_unit, created = Units.objects.get_or_create(
                    name=row[1],
                )
                _, created = Ingredients.objects.get_or_create(
                    name=row[0],
                    measurement_unit=measurement_unit,
                )

        self.stdout.write(
            self.style.SUCCESS("Ингридиенты успешно импортированы.")
        )
