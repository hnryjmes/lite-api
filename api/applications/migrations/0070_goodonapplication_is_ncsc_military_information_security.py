# Generated by Django 3.2.18 on 2023-04-13 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("applications", "0069_auto_20230223_1214"),
    ]

    operations = [
        migrations.AddField(
            model_name="goodonapplication",
            name="is_ncsc_military_information_security",
            field=models.BooleanField(
                blank=True, default=None, help_text="triggers to NCSC for a recommendation", null=True
            ),
        ),
    ]
