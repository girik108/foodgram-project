from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Unit(models.Model):
    """Класс Единиц измерения ингредиентов"""
    name = models.CharField(max_length=100)
    contraction = models.CharField(max_length=50, default='.')

    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    """Класс Ингредиентов"""
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Справочник тегов"""
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='media/images', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True)
    tag = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}'

class RecipesIngredient(models.Model):
    """Класс Ингредиентов в рецептах"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipes')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE,)
    count = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('recipe', 'ingredient')
    
    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'
