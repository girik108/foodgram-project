from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from pytils.translit import slugify


User = get_user_model()


class Dimension(models.Model):
    """Класс Единиц измерения ингредиентов"""
    abbr = models.CharField(max_length=25, default='',
                            verbose_name='Единица измерения сокр.')

    class Meta:
        verbose_name = 'dimension'
        verbose_name_plural = 'dimensions'

    def __str__(self):
        return f'{self.abbr}'


class Ingredient(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    dimension = models.ForeignKey(Dimension,
                                  on_delete=models.CASCADE,
                                  verbose_name='Единица измерения',
                                  related_name='+')

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    PURPLE = 'PU'
    GREEN = 'GR'
    ORANGE = 'OR'
    COLORS = [
        (PURPLE, 'purple'),
        (GREEN, 'green'),
        (ORANGE, 'orange'),
    ]

    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Наименование')
    color = models.CharField(max_length=2, choices=COLORS,
                             default=GREEN, verbose_name='Цвет')
    slug = models.SlugField(max_length=20, verbose_name='Метка')

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    slug_size = 25
    name = models.CharField(max_length=200, unique=True,
                            verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes',
                               verbose_name='Автор')
    image = models.ImageField(upload_to='images/',
                              verbose_name='Загрузить фото')
    tags = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    slug = models.SlugField(
        max_length=slug_size, blank=True,
        verbose_name='Адрес для страницы с рецептом',
        help_text=('Укажите адрес для страницы рецепта. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'recipe'
        verbose_name_plural = 'recipes'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:self.slug_size]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('recipe', kwargs={'pk': self.pk})

    def is_favorite(self, user):
        return self.liked.filter(user=user).exists()

    def is_purch(self, user):
        return self.purchased.filter(user=user).exists()


class RecipesIngredient(models.Model):
    """Класс Ингредиентов в рецептах"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='ingredients',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='ingredients',
                                   verbose_name='Ингредиент')
    count = models.PositiveSmallIntegerField(default=1,
                                             verbose_name='Количество')

    class Meta:
        verbose_name = 'recipe_ingredient'
        verbose_name_plural = 'recipe_ingredients'
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_recipe_and_ingredient_unique',
                fields=('recipe', 'ingredient'),
            ),
        ]

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class ShoppingList(models.Model):
    """Класс список покупок"""
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата добавления')
    user = models.ForeignKey(User, blank=True, null=True,
                             related_name='purchases',
                             verbose_name='Пользователь',
                             on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40,
                                   verbose_name='Ключ сессии')
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               verbose_name='Рецепт',
                               related_name='purchased')

    class Meta:
        verbose_name = 'shoppinglist'
        verbose_name_plural = 'shoppinglists'
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_recipe_and_user_unique',
                fields=('recipe', 'user'),
            ),
        ]

    def __str__(self):
        return f'{self.user} -> {self.recipe}'


class Follow(models.Model):
    """Класс подписок"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower',
                             verbose_name='Пользователь')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following',
                               verbose_name='Автор')

    class Meta:
        verbose_name = 'follow'
        verbose_name_plural = 'follows'
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_author_and_user_unique',
                fields=('author', 'user'),
            ),
        ]

    def __str__(self):
        return f'{self.user} follow {self.author}'


class Favorite(models.Model):
    """Класс Избранного"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='liked',
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'favorite'
        verbose_name_plural = 'favorites'
        constraints = [
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_recipe_and_user_unique',
                fields=('recipe', 'user'),
            ),
        ]

    def __str__(self):
        return f'{self.user} like {self.recipe}'
