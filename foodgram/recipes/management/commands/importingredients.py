import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient, Dimension, Tag


APP_DIR = settings.BASE_DIR
IMPORT_DIR = os.path.join(APP_DIR, 'import')


class Command(BaseCommand):
    help = 'Import indegredients and dimensions from CSV to DB'

    def handle(self, *args, **kwargs):
        self.stdout.write(import_all())
        self.stdout.write(create_tags())


def import_all():
    Ingredient.objects.all().delete()
    Dimension.objects.all().delete()

    source = os.path.join(IMPORT_DIR, 'ingredients.csv')
    with open(source, encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, quotechar='"')
        for row in reader:
            abbr = row.get('dimension')
            abbr = abbr if (abbr and abbr != ' ') else ''
            dimension, created = Dimension.objects.get_or_create(abbr=abbr)
            ingredient = Ingredient(title=row.get(
                'ingredient'), dimension=dimension)
            ingredient.save()

    return 'Ingredients and Dimensions imported successfully'


def create_tags():
    Tag.objects.all().delete()
    
    items = [('breakfast', 'orange', 'Завтрак'),
             ('lunch', 'green', 'Обед'),
             ('snack', 'orange', 'Перекус'),
             ('dinner', 'purple', 'Ужин'), ]

    tags = [Tag(slug=item[0], color=item[1], name=item[2]) for item in items]
    Tag.objects.bulk_create(tags)

    return 'Tags created'
