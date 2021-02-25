import csv 
import os.path 
from datetime import datetime 
 
#from django.conf import settings 
#from django.contrib.auth import get_user_model 
#from django.core.management.base import BaseCommand 
#from django.db import IntegrityError 
#from titles.models import Category, Genre, Title 
#from comments.models import Comment 
#from reviews.models import Review 



def import_ingredients(): 
    with open('ingredients.csv', encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile, quotechar='"')
        units = set()
        for row in reader:
            item = row.get('unit')
            if item:
                units.add(item)
        print(units)
    return units 
 
print(import_ingredients())


''' 
BASE_DIR = settings.BASE_DIR 
DATA_DIR = os.path.join(BASE_DIR, 'data') 
 
 
User = get_user_model() 
 
 
class Command(BaseCommand): 
    help = 'Import data from CSV to DB' 
 
    def handle(self, *args, **kwargs): 
        all_imports = [ 
            import_category, 
            import_genre, 
            import_title, 
            import_user, 
            import_review, 
            import_comment, 
        ] 
        for func in all_imports: 
            self.stdout.write(func()) 
 
 
def import_category(): 
    with open(os.path.join(DATA_DIR, 'category.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            category = Category(**row) 
            category.save() 
    return 'Categories imported successfully' 
 
 
def import_genre(): 
    with open(os.path.join(DATA_DIR, 'genre.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            genre = Genre(**row) 
            genre.save() 
    return 'Genres imported successfully' 
 
 
def get_genres(): 
    result = {} 
    with open(os.path.join(DATA_DIR, 'genre_title.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            title = int(row.get('title_id')) 
            genre = Genre.objects.get(id=int(row.get('genre_id'))) 
            if not result.get(title): 
                result[title] = [genre, ] 
            else: 
                result[title].append(genre) 
 
    return result 
 
 
def import_title(): 
 
    genres = get_genres() 
 
    with open(os.path.join(DATA_DIR, 'titles.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            row['year'] = int(row.get('year')) 
            row['category'] = Category.objects.get(id=int(row.get('category'))) 
            title = Title(**row) 
            title.save() 
            title.genre.add(*genres.get(title.id)) 
 
    return 'Titles imported successfully' 
 
 
def import_user(): 
    with open(os.path.join(DATA_DIR, 'users.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            row['bio'] = row.pop('description') 
            user = User(**row) 
            user.set_password('COVID-2019') 
            user.save() 
 
    return 'Users imported successfully' 
 
 
def import_review(): 
    with open(os.path.join(DATA_DIR, 'review.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            row['title_id'] = int(row.get('title_id')) 
            row['author'] = User.objects.get(id=int(row.get('author'))) 
            row['score'] = int(row.get('score')) 
            row['pub_date'] = datetime.fromisoformat( 
                row.get('pub_date').replace('Z', '+00:00')) 
            review = Review(**row) 
            try: 
                review.save() 
            except IntegrityError: 
                pass 
 
    return 'Reviews imported successfully' 
 
 
def import_comment(): 
    with open(os.path.join(DATA_DIR, 'comments.csv'), 
              encoding='utf-8') as csvfile: 
        reader = csv.DictReader(csvfile) 
        for row in reader: 
            row['id'] = int(row.get('id')) 
            row['review_id'] = int(row.get('review_id')) 
            row['author'] = User.objects.get(id=int(row.get('author'))) 
            row['pub_date'] = datetime.fromisoformat( 
                row.get('pub_date').replace('Z', '+00:00')) 
            comment = Comment(**row) 
            comment.save() 
 
    return 'Comments imported successfully' 
'''
