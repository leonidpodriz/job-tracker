# Generated by Django 5.0.1 on 2024-01-18 20:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("applications", "0003_application_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="notes",
            field=models.TextField(blank=True, null=True),
        ),
    ]
