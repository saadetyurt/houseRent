# Generated by Django 3.0.6 on 2020-05-21 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0017_auto_20200521_0636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
