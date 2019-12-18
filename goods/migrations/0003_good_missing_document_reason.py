# Generated by Django 2.2.8 on 2019-12-17 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("goods", "0002_auto_20191209_1209"),
    ]

    operations = [
        migrations.AddField(
            model_name="good",
            name="missing_document_reason",
            field=models.CharField(
                choices=[
                    ("NO_DOCUMENT", "No document available for the good"),
                    ("OFFICIAL_SENSITIVE", "Document is above official-sensitive"),
                    ("COMMERCIALLY_SENSITIVE", "Document is commercially sensitive"),
                ],
                max_length=30,
                null=True,
            ),
        ),
    ]
