# Generated by Django 4.2.18 on 2025-02-27 09:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_remove_tournament_season_season_tournament"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="season",
            name="tournament",
        ),
    ]
