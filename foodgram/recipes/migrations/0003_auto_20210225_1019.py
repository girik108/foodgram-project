# Generated by Django 3.1.6 on 2021-02-25 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20210222_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='contraction',
            field=models.CharField(default='.', max_length=25),
        ),
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]