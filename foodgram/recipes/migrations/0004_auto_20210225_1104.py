# Generated by Django 3.1.6 on 2021-02-25 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_auto_20210225_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='contraction',
            field=models.CharField(default='г', max_length=25),
        ),
    ]
