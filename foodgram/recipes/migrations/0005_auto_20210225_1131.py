# Generated by Django 3.1.6 on 2021-02-25 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20210225_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='unit',
            old_name='contraction',
            new_name='abbr',
        ),
    ]
