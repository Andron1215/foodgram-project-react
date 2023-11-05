import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from ...models import Tags

path_tags_csv = Path(__file__).parents[4] / "data" / "tags.csv"


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(path_tags_csv, encoding="utf8") as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                _, created = Tags.objects.get_or_create(
                    name=row[0],
                    color=row[1],
                    slug=row[2],
                )

        self.stdout.write(self.style.SUCCESS("Теги успешно импортированы."))
