# Generated by Django 3.0.6 on 2020-05-16 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0009_auto_20200516_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='slug',
            field=models.SlugField(blank=True, max_length=150),
        ),
    ]