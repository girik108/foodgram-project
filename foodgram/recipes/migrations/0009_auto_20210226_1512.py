# Generated by Django 3.1.6 on 2021-02-26 11:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0008_auto_20210226_1511'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together={('recipe', 'user')},
        ),
    ]
