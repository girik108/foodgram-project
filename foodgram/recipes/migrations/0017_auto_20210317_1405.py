# Generated by Django 3.1.6 on 2021-03-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0016_auto_20210315_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='slug',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
