# Generated by Django 4.2.17 on 2024-12-19 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("plan", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="exerciseplan",
            name="price",
        ),
    ]
