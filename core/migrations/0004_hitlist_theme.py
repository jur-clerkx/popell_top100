# Generated by Django 4.1.5 on 2023-01-17 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_hitlistsettings"),
    ]

    operations = [
        migrations.AddField(
            model_name="hitlist",
            name="theme",
            field=models.CharField(
                choices=[("rock", "Rock"), ("carnaval", "Carnaval")],
                default="rock",
                max_length=255,
            ),
        ),
    ]
