import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Unit


APP_DIR = settings.BASE_DIR
IMPORT_DIR = os.path.join(APP_DIR, 'import')


class Command(BaseCommand):
    help = 'Import indegredients and units from CSV to DB'

    def handle(self, *args, **kwargs):
        self.stdout.write(import_all())


def import_all():
    Ingredient.objects.all().delete()
    Unit.objects.all().delete()
    
    source = os.path.join(IMPORT_DIR, 'ingredients.csv')
    with open(source, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, quotechar='"')
        abbrs = set()
        for row in reader:
            abbrs.add(row.get('unit'))
            ingredient = Ingredient(name=row.get('ingredient'))
            ingredient.save()

        units = [Unit(abbr=abbr) for abbr in abbrs if abbr and abbr != ' ']
        Unit.objects.bulk_create(units)

    return 'Ingredients and Units imported successfully'

