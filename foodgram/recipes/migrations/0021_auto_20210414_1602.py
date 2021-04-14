# Generated by Django 3.1.6 on 2021-04-14 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0020_auto_20210409_1023'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dimension',
            options={'verbose_name': 'dimension', 'verbose_name_plural': 'dimensions'},
        ),
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'favorite', 'verbose_name_plural': 'favorites'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'verbose_name': 'follow', 'verbose_name_plural': 'follows'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['title'], 'verbose_name': 'ingredient', 'verbose_name_plural': 'ingredients'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'recipe', 'verbose_name_plural': 'recipes'},
        ),
        migrations.AlterModelOptions(
            name='recipesingredient',
            options={'verbose_name': 'recipe_ingredient', 'verbose_name_plural': 'recipe_ingredients'},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'verbose_name': 'shoppinglist', 'verbose_name_plural': 'shoppinglists'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': 'tag', 'verbose_name_plural': 'tags'},
        ),
        migrations.AlterField(
            model_name='dimension',
            name='abbr',
            field=models.CharField(default='', max_length=25, verbose_name='Единица измерения сокр.'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации'),
        ),
        migrations.AlterField(
            model_name='recipesingredient',
            name='count',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipesingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.ingredient', verbose_name='Ингредиент'),
        ),
        migrations.AlterField(
            model_name='recipesingredient',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='session_key',
            field=models.CharField(max_length=40, verbose_name='Ключ сессии'),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(choices=[('PU', 'purple'), ('GR', 'green'), ('OR', 'orange')], default='GR', max_length=2, verbose_name='Цвет'),
        ),
        migrations.AlterUniqueTogether(
            name='favorite',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='follow',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='recipesingredient',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together=set(),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='recipes_favorite_recipe_and_user_unique'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('author', 'user'), name='recipes_follow_author_and_user_unique'),
        ),
        migrations.AddConstraint(
            model_name='recipesingredient',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredient'), name='recipes_recipesingredient_recipe_and_ingredient_unique'),
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='recipes_shoppinglist_recipe_and_user_unique'),
        ),
    ]
