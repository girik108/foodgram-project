# Generated by Django 3.1.6 on 2021-04-08 05:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20210329_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, verbose_name='Название рецепта'),
        ),
    ]