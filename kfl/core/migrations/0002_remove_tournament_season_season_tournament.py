# Generated by Django 4.2.18 on 2025-02-27 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="tournament",
            name="season",
        ),
        migrations.AddField(
            model_name="season",
            name="tournament",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="season",
                to="core.tournament",
                verbose_name="Турнир",
            ),
            preserve_default=False,
        ),
    ]
