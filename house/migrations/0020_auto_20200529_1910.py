# Generated by Django 3.0.6 on 2020-05-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0019_house_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]