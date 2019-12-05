# Generated by Django 2.2.4 on 2019-12-03 09:10

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("documents", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApplicationDenialReason",
            fields=[
                ("id", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("reason_details", models.TextField(blank=True, default=None, max_length=2200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ApplicationDocument",
            fields=[
                (
                    "document_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="documents.Document",
                    ),
                ),
                ("description", models.TextField(blank=True, default=None, max_length=280, null=True)),
            ],
            bases=("documents.document",),
        ),
    ]
