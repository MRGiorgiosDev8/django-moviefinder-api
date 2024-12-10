# Generated by Django 5.1.2 on 2024-12-09 19:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritemovie',
            name='actors',
        ),
        migrations.RemoveField(
            model_name='favoritemovie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='favoritemovie',
            name='imdbRating',
        ),
        migrations.RemoveField(
            model_name='favoritemovie',
            name='plot',
        ),
        migrations.AlterField(
            model_name='favoritemovie',
            name='imdbID',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='favoritemovie',
            name='poster',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='favoritemovie',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]