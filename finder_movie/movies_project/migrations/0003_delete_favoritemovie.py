# Generated by Django 5.1.2 on 2024-12-09 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies_project', '0002_remove_favoritemovie_actors_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FavoriteMovie',
        ),
    ]