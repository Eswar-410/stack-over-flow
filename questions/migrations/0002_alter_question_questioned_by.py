# Generated by Django 5.2.4 on 2025-07-14 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="questioned_by",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
