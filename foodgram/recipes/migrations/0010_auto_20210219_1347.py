# Generated by Django 3.1.6 on 2021-02-19 09:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20210219_1135'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['pk']},
        ),
    ]
