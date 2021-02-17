from slugify import slugify

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


class Unit(models.Model):
    """Класс Единиц измерения ингредиентов"""
    name = models.CharField(max_length=100)
    contraction = models.CharField(max_length=10, default='.')

    def __str__(self):
        return f'{self.contraction}.'


class Ingredient(models.Model):
    """Класс Ингредиентов"""
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Справочник тегов"""
    name = models.CharField(max_length=50, unique=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    @property
    def translit(self):
        return slugify(self.name, separator='__')


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    tag = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('detail-recipe-pk', kwargs={'pk': self.pk})


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


class ShoppingList(models.Model):
    """Класс список покупок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='purchases')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='+')

    def __str__(self):
        return f'{self.user} -> {self.recipe}'

class Follow(models.Model):
    """Класс подписок"""
    #  ссылка на объект пользователя, который подписывается.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')
    # ссылка на объект пользователя, на которого подписываются.
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')

    def __str__(self):
        return f'{self.user} follow {self.author}'

class Favorite(models.Model):
    """Класс список покупок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='+')

    def __str__(self):
        return f'{self.user} like {self.recipe}'