from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from pytils.translit import slugify


User = get_user_model()


class Dimension(models.Model):
    """Класс Единиц измерения ингредиентов"""
    abbr = models.CharField(max_length=25, default='')

    def __str__(self):
        return f'{self.abbr}'


class Ingredient(models.Model):
    """Класс Ингредиентов"""
    title = models.CharField(max_length=100, verbose_name='Наименование')
    dimension = models.ForeignKey(Dimension,
                                  on_delete=models.CASCADE,
                                  verbose_name='Единица измерения',
                                  related_name='+')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f'{self.title}'


class Tag(models.Model):
    """Класс Тегов"""
    CSS_COLORS = ('purple', 'green', 'orange')
    COLORS = [(color, color.title()) for color in CSS_COLORS]
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Наименование')
    color = models.CharField(max_length=10, choices=COLORS,
                             default='green', verbose_name='Цвет')
    slug = models.SlugField(max_length=20, verbose_name='Метка')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    slug_size = 25
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта'
    )
    description = models.TextField(verbose_name='Описание')
    pub_date = models.DateTimeField(
        'date published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes')
    image = models.ImageField(
        upload_to='images/',
        verbose_name='Загрузить фото'
    )
    tags = models.ManyToManyField(Tag)
    time = models.PositiveSmallIntegerField(verbose_name='Время приготовления')
    slug = models.SlugField(
        verbose_name='Адрес для страницы с рецептом',
        max_length=slug_size,
        # unique=True,
        blank=True,
        help_text=('Укажите адрес для страницы рецепта. Используйте только '
                   'латиницу, цифры, дефисы и знаки подчёркивания')
    )

    class Meta:
        ordering = ['-pub_date']

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
                               related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipes')
    count = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class ShoppingList(models.Model):
    """Класс список покупок"""
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, blank=True, null=True,
                             related_name='purchases',
                             on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='purchased')

    class Meta:
        unique_together = ('recipe', 'user')  # , 'session_key')

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

    class Meta:
        unique_together = ('user', 'author')

    def __str__(self):
        return f'{self.user} follow {self.author}'


class Favorite(models.Model):
    """Класс Избранного"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='liked')

    class Meta:
        unique_together = ('recipe', 'user')

    def __str__(self):
        return f'{self.user} like {self.recipe}'
